"""Manim 图解图标资源路径（iconfont PNG/SVG）。"""

from __future__ import annotations

from pathlib import Path

from manim import ImageMobject  # noqa: E402
from video_export import PROJECT_ROOT  # noqa: E402

ICONS_ROOT = PROJECT_ROOT / "manim" / "assets" / "icons"


def resolve_icon_path(relative: str) -> Path:
    """相对路径如 dishes/pizza.png → 绝对路径。"""
    return ICONS_ROOT / relative


def load_icon_png(relative: str, height: float = 0.48) -> ImageMobject:
    """加载 PNG 图标并统一高度。"""
    path = resolve_icon_path(relative)
    if not path.is_file():
        raise FileNotFoundError(f"图标不存在: {path}")
    icon = ImageMobject(str(path))
    icon.set_height(height)
    return icon
