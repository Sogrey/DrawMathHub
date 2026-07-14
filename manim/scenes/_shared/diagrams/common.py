"""图解公共图元（圆圈、省略号等），供各题型 Mixin 复用。"""

from __future__ import annotations

from manim import *  # noqa: F403


class DiagramCommonMixin:
    def _person_circle(self, radius: float = 0.18, *, color=WHITE, stroke_width: int = 2) -> Circle:
        return Circle(radius=radius, color=color, stroke_width=stroke_width)

    def _horizontal_ellipsis(
        self, *, color=GREY_B, dot_r: float = 0.08, count: int = 4, buff: float = 0.1,
    ) -> VGroup:
        """横向省略号，与圆圈同行垂直居中。"""
        return VGroup(*[
            Dot(radius=dot_r, color=color, fill_opacity=1) for _ in range(count)
        ]).arrange(RIGHT, buff=buff)
