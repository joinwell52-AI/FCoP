"""FCoP v1.0 JSON Schema 校验器。

按 ADR-0016 / TASK-20260509-004 R1 落地。本模块加载 7 份 v1.0 协议
schema（``spec/schemas/*.schema.json`` 在 wheel 内的副本
``src/fcop/_data/schemas/``），把它们组装成一个 ``referencing.Registry``
让跨文件 ``$ref`` 可解析（每个 schema 用自身 ``$id`` 注册），然后对外
暴露两个 opt-in 校验函数：

- :func:`validate_envelope_frontmatter` —— 拿一个 IPC envelope 的
  frontmatter dict + envelope 类型，按 ``ipc-envelope.schema.json`` 校验
- :func:`validate_record` —— 拿任意 record + schema 文件名，按对应
  schema 校验

返回值都是 :class:`ValidationIssue` 列表（空 list ≡ 合法）；本模块
**不 raise** —— 把决策权留给 caller（``Project.write_review`` 等）。

设计要点：

- **opt-in**：现有 ``write_task`` / ``write_report`` / ``write_issue``
  路径不被自动接进来。只有 v1.0 新增的 REVIEW（TASK-004 R2）以及未来
  的 boundary / failure / event API 才会主动走这层。
- **schema = single source of truth**：包内 schema 副本与
  ``spec/schemas/`` 必须字节一致；测试 ``test_bundled_schemas_in_sync``
  在 CI 上守门。
- **跨文件 $ref 用绝对 $id**（``https://fcop.dev/schemas/.../v1.0.json``），
  这是 ``referencing.Registry`` 唯一可移植的解析方式。``fcop.dev`` 是
  protocol identifier 不是 fetch URL —— 不会发起任何网络请求。

参见 ``adr/ADR-0016-json-schema-for-7-abstractions.md`` 与 TASK-004
charter §决议 2。
"""

from __future__ import annotations

import datetime as _dt
import json
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]
from referencing import Registry, Resource

from fcop.models import ValidationIssue

__all__ = [
    "BUNDLED_SCHEMA_DIR",
    "SCHEMA_NAMES",
    "SCHEMA_REGISTRY",
    "ENVELOPE_TYPES",
    "load_bundled_schema",
    "normalize_for_json",
    "validate_envelope_frontmatter",
    "validate_record",
]


# ── 常量 ────────────────────────────────────────────────────────────


def _resolve_bundled_schema_dir() -> Path:
    """定位包内 schema 副本目录。

    使用 ``importlib.resources`` 让 wheel 安装与 editable 安装都能找到。
    返回的是文件系统路径（``as_file`` 解出），便于直接 ``read_bytes()``。
    """
    pkg_root = resources.files("fcop").joinpath("_data").joinpath("schemas")
    return Path(str(pkg_root))


BUNDLED_SCHEMA_DIR: Path = _resolve_bundled_schema_dir()
"""包内权威 schema 目录。CI 测试断言它与 ``spec/schemas/`` 字节一致。"""

SCHEMA_NAMES: tuple[str, ...] = (
    "agent.schema.json",
    "boundary.schema.json",
    "encoding.schema.json",
    "event.schema.json",
    "failure.schema.json",
    "ipc-envelope.schema.json",
    "review.schema.json",
)
"""v1.0 7 份 schema 文件名（按字母序）。新增 schema 必须 bump MINOR。"""

ENVELOPE_TYPES: frozenset[str] = frozenset({"TASK", "REPORT", "ISSUE", "REVIEW"})
"""IPC envelope 4 类型。来自 ADR-0021 §IPC Surface，frozen for v1.x。"""


# ── 加载 ────────────────────────────────────────────────────────────


def load_bundled_schema(name: str) -> dict[str, Any]:
    """加载包内 schema 文件并返回 dict。

    Args:
        name: schema 文件名，e.g. ``"review.schema.json"``。必须是
            :data:`SCHEMA_NAMES` 中的成员。

    Raises:
        ValueError: ``name`` 不在已知 schema 集中。
        FileNotFoundError: schema 文件物理缺失（wheel 打包错误）。
    """
    if name not in SCHEMA_NAMES:
        raise ValueError(
            f"unknown schema {name!r}; must be one of {sorted(SCHEMA_NAMES)}"
        )
    path = BUNDLED_SCHEMA_DIR / name
    if not path.is_file():
        raise FileNotFoundError(
            f"bundled schema missing: {path} (wheel packaging error?)"
        )
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def _build_registry() -> tuple[Registry, dict[str, dict[str, Any]]]:
    """import 时一次性把 7 份 schema 加进 registry。

    用每个 schema 自身的 ``$id``（绝对 URI）注册，跨文件 ``$ref`` 才能
    被 ``referencing.Registry.lookup`` 命中。返回 (registry, schemas)
    元组，schemas 以 filename 为 key 让别处查方便。
    """
    schemas: dict[str, dict[str, Any]] = {}
    registry = Registry()
    for fname in SCHEMA_NAMES:
        s = load_bundled_schema(fname)
        schemas[fname] = s
        registry = registry.with_resource(
            uri=s["$id"], resource=Resource.from_contents(s)
        )
    return registry, schemas


SCHEMA_REGISTRY, _SCHEMAS_BY_FILENAME = _build_registry()
"""模块级 registry。共享给所有校验调用，import 时构建一次。"""


# ── normalize ───────────────────────────────────────────────────────


def normalize_for_json(value: Any) -> Any:
    """递归把 YAML-parsed Python 对象转成 JSON-Schema 友好形式。

    YAML 解析器（PyYAML safe_load）会把 ISO date / datetime 字符串自动
    解析为 ``datetime.date`` / ``datetime.datetime`` 对象。JSON Schema
    没有 date 类型，所有时间字段都用 ``"type": "string"`` + pattern
    描述，所以校验前需要把这些对象转回 ISO 字符串。

    其他 Python 类型（int / float / str / bool / None / list / dict）
    原样返回。

    本函数纯，不改原对象（list / dict 走 deep copy 风格）。
    """
    if isinstance(value, dict):
        return {k: normalize_for_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize_for_json(v) for v in value]
    if isinstance(value, _dt.datetime):
        # 保留时区信息；naive datetime 也直接 isoformat 即可（pattern 容错）
        return value.isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    return value


# ── 公开 API ────────────────────────────────────────────────────────


def _wrap_errors(
    validator: Draft202012Validator, instance: Any, *, field_prefix: str = ""
) -> list[ValidationIssue]:
    """把 jsonschema 错误转成 :class:`ValidationIssue` 列表。"""
    issues: list[ValidationIssue] = []
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        path_parts = [str(p) for p in err.path]
        field = ".".join(path_parts) if path_parts else "<root>"
        if field_prefix:
            field = f"{field_prefix}.{field}" if path_parts else field_prefix
        issues.append(
            ValidationIssue(
                severity="error",
                field=field,
                message=err.message,
            )
        )
    return issues


def validate_envelope_frontmatter(
    frontmatter: dict[str, Any],
    envelope_type: str,
) -> list[ValidationIssue]:
    """按 ``ipc-envelope.schema.json`` 校验一条 envelope frontmatter。

    Args:
        frontmatter: 已经解析为 dict 的 YAML frontmatter。如果没有
            ``type`` 字段，本函数会按 ``envelope_type`` 注入一个
            （legacy 0.7.x 文件 type 隐含在文件名 PREFIX，frontmatter
            没写）。这一步不修改原 dict——内部 deep-copy。
        envelope_type: ``"TASK"`` / ``"REPORT"`` / ``"ISSUE"`` /
            ``"REVIEW"``，必须在 :data:`ENVELOPE_TYPES` 内。

    Returns:
        :class:`ValidationIssue` 列表。空 list ≡ frontmatter 合规。

    Raises:
        ValueError: ``envelope_type`` 不是 4 类之一。
    """
    if envelope_type not in ENVELOPE_TYPES:
        raise ValueError(
            f"envelope_type must be one of {sorted(ENVELOPE_TYPES)}, "
            f"got {envelope_type!r}"
        )

    fm = normalize_for_json(frontmatter)
    if isinstance(fm, dict):
        fm.setdefault("type", envelope_type)
    # 0.7.x 文件 sender / recipient 历史上有 from / to 别名；这里不做
    # 自动 mapping —— caller（test_legacy_files_validate）显式做了。
    # 这里保持纯净，仅按 schema 验。

    schema = _SCHEMAS_BY_FILENAME["ipc-envelope.schema.json"]
    validator = Draft202012Validator(schema, registry=SCHEMA_REGISTRY)
    return _wrap_errors(validator, fm)


def validate_record(
    record: dict[str, Any] | list[Any],
    schema_name: str,
) -> list[ValidationIssue]:
    """按指定 schema 校验任意 record。

    用于 v1.0 新引入的非 envelope record（Failure / Recovery / Event /
    Boundary 配置等）。Envelope frontmatter 请用
    :func:`validate_envelope_frontmatter`。

    Args:
        record: 任意 JSON-able 结构。
        schema_name: schema 文件名，e.g. ``"failure.schema.json"``。
            必须是 :data:`SCHEMA_NAMES` 之一。

    Returns:
        :class:`ValidationIssue` 列表。空 list ≡ 合规。

    Raises:
        ValueError: ``schema_name`` 不在已知 schema 集中。
    """
    if schema_name not in SCHEMA_NAMES:
        raise ValueError(
            f"unknown schema {schema_name!r}; must be one of "
            f"{sorted(SCHEMA_NAMES)}"
        )
    schema = _SCHEMAS_BY_FILENAME[schema_name]
    validator = Draft202012Validator(schema, registry=SCHEMA_REGISTRY)
    return _wrap_errors(validator, normalize_for_json(record))
