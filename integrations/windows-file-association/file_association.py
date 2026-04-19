"""Windows .fcop 文件关联注册

首次运行时：
1. 从打包资源提取 fcop.ico 到 %APPDATA%\\CodeFlow\\fcop.ico （持久化路径）
2. 写入 HKCU\\Software\\Classes 注册表，实现 .fcop 扩展关联
3. 双击 .fcop 文件自动启动 CodeFlow-Desktop.exe 并传入文件路径

设计原则：
- 幂等：已注册则跳过，不重复写
- 无权限要求：只写 HKCU（当前用户），不需要管理员
- 非 Windows 平台：静默跳过，不报错
- 失败静默：注册失败不影响主程序启动
- 可逆：提供 unregister() 用于卸载清理

注册表结构（HKCU\\Software\\Classes）：
    .fcop                              → (Default) = "CodeFlow.FcopFile"
                                        Content Type = "text/x-fcop"
    CodeFlow.FcopFile                  → (Default) = 描述
    CodeFlow.FcopFile\\DefaultIcon      → (Default) = "...\\fcop.ico"
    CodeFlow.FcopFile\\shell\\open
        \\command                       → (Default) = '"CodeFlow-Desktop.exe" "%1"'
"""
from __future__ import annotations

import logging
import os
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PROGID = "CodeFlow.FcopFile"
EXTENSION = ".fcop"
DESCRIPTION = "FCoP File (File-based Coordination Protocol)"
CONTENT_TYPE = "text/x-fcop"


def _is_windows() -> bool:
    return sys.platform == "win32"


def _appdata_dir() -> Path:
    base = os.environ.get("APPDATA")
    if base:
        d = Path(base) / "CodeFlow"
    else:
        d = Path.home() / ".codeflow"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _persistent_icon_path() -> Path:
    """图标的持久路径。注册表里写的是这个路径，不能指向 _MEIPASS（打包后每次启动位置都变）。"""
    return _appdata_dir() / "fcop.ico"


def _bundled_icon_source() -> Path | None:
    """查找 fcop.ico 源文件。打包后从 _MEIPASS/panel/，开发模式从 docs/images/ 或 panel/。"""
    if getattr(sys, "frozen", False):
        meipass = Path(getattr(sys, "_MEIPASS", ""))
        candidates = [
            meipass / "panel" / "fcop.ico",
            meipass / "fcop.ico",
        ]
    else:
        here = Path(__file__).resolve().parent
        repo_root = here.parent
        candidates = [
            here / "panel" / "fcop.ico",
            repo_root / "docs" / "images" / "fcop.ico",
        ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _current_exe_path() -> str | None:
    """只在打包后（frozen）返回可执行文件路径；开发模式返回 None 表示不注册。"""
    if getattr(sys, "frozen", False):
        return str(Path(sys.executable).resolve())
    return None


def _deploy_persistent_icon() -> Path | None:
    src = _bundled_icon_source()
    if not src:
        logger.debug("[fcop-assoc] 找不到 fcop.ico 源文件，跳过")
        return None
    dst = _persistent_icon_path()
    try:
        if (
            not dst.exists()
            or dst.stat().st_size != src.stat().st_size
        ):
            shutil.copyfile(src, dst)
            logger.info("[fcop-assoc] 图标部署到 %s", dst)
        return dst
    except Exception as e:
        logger.warning("[fcop-assoc] 图标部署失败: %s", e)
        return None


def is_registered() -> bool:
    """扩展名关联是否已存在"""
    if not _is_windows():
        return False
    try:
        import winreg
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, fr"Software\Classes\{EXTENSION}"
        ):
            return True
    except OSError:
        return False


def register() -> bool:
    """注册 .fcop 文件关联。幂等，失败静默返回 False。"""
    if not _is_windows():
        logger.debug("[fcop-assoc] 非 Windows 平台，跳过")
        return False

    exe = _current_exe_path()
    if not exe:
        logger.debug("[fcop-assoc] 开发模式（非 frozen），跳过文件关联注册")
        return False

    icon = _deploy_persistent_icon()
    if not icon:
        return False

    try:
        import winreg

        classes = r"Software\Classes"

        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, fr"{classes}\{EXTENSION}"
        ) as k:
            winreg.SetValue(k, "", winreg.REG_SZ, PROGID)
            winreg.SetValueEx(
                k, "Content Type", 0, winreg.REG_SZ, CONTENT_TYPE
            )
            winreg.SetValueEx(
                k, "PerceivedType", 0, winreg.REG_SZ, "text"
            )

        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, fr"{classes}\{PROGID}"
        ) as k:
            winreg.SetValue(k, "", winreg.REG_SZ, DESCRIPTION)

        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, fr"{classes}\{PROGID}\DefaultIcon"
        ) as k:
            winreg.SetValue(k, "", winreg.REG_SZ, f'"{icon}"')

        with winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, fr"{classes}\{PROGID}\shell\open\command"
        ) as k:
            winreg.SetValue(k, "", winreg.REG_SZ, f'"{exe}" "%1"')

        _notify_shell_refresh()

        logger.info(
            "[fcop-assoc] .fcop 关联注册成功 (exe=%s, icon=%s)", exe, icon
        )
        return True
    except Exception as e:
        logger.warning("[fcop-assoc] 注册失败: %s", e)
        return False


def unregister() -> bool:
    """卸载 .fcop 文件关联"""
    if not _is_windows():
        return False
    try:
        import winreg

        classes = r"Software\Classes"
        paths = [
            fr"{classes}\{PROGID}\shell\open\command",
            fr"{classes}\{PROGID}\shell\open",
            fr"{classes}\{PROGID}\shell",
            fr"{classes}\{PROGID}\DefaultIcon",
            fr"{classes}\{PROGID}",
            fr"{classes}\{EXTENSION}",
        ]
        for path in paths:
            try:
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, path)
            except OSError:
                pass
        _notify_shell_refresh()
        logger.info("[fcop-assoc] .fcop 关联已卸载")
        return True
    except Exception as e:
        logger.warning("[fcop-assoc] 卸载失败: %s", e)
        return False


def _notify_shell_refresh():
    """通知 Windows Shell 刷新图标缓存，让新关联立即生效。"""
    try:
        import ctypes
        SHCNE_ASSOCCHANGED = 0x08000000
        SHCNF_IDLIST = 0x0000
        ctypes.windll.shell32.SHChangeNotify(
            SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None
        )
    except Exception:
        pass


def ensure_registered_once() -> bool:
    """启动时调用：首次运行注册，之后跳过。
    返回 True 表示本次触发了注册动作，False 表示已注册或跳过。
    """
    if not _is_windows():
        return False
    if not getattr(sys, "frozen", False):
        return False
    if is_registered():
        logger.debug("[fcop-assoc] 已注册，跳过")
        return False
    return register()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    import argparse
    ap = argparse.ArgumentParser(description="FCoP 文件关联管理")
    ap.add_argument(
        "action",
        choices=["register", "unregister", "status"],
        help="register=注册；unregister=卸载；status=查看当前状态",
    )
    args = ap.parse_args()

    if args.action == "register":
        ok = register()
        sys.exit(0 if ok else 1)
    elif args.action == "unregister":
        ok = unregister()
        sys.exit(0 if ok else 1)
    else:
        reg = is_registered()
        print(f"已注册: {reg}")
        print(f"图标路径: {_persistent_icon_path()}")
        print(f"当前 EXE: {_current_exe_path() or '(开发模式)'}")
        sys.exit(0)
