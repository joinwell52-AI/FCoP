"""tests/test_schemas/ —— v1.0 7 份 JSON Schema 的回归测试套件。

按 TASK-20260509-004 R1 + ADR-0016 §tests-checklist 落地。每份 schema
至少 3 用例：合法 / 缺必填 / 非法枚举。另外两份横切测试：

- ``test_bundled_schemas_in_sync.py`` 断言 ``src/fcop/_data/schemas/`` 与
  ``spec/schemas/`` 字节一致（防漂移）
- ``test_legacy_files_validate.py`` 断言 ``docs/agents/log/`` 下所有真实
  0.7.x envelope 文件 100% 通过新 schema（I5 见证 / backward compat）
"""
