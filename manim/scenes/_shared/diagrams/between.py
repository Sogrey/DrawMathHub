"""
之间问题图解 — 第1讲及同类题型。

约定：仅本模块维护之间问题相关逻辑。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class BetweenDiagramMixin:
    def make_between_diagram(
        self,
        left_rank: int,
        right_rank: int,
        draw_y: float,
        *,
        circle_r: float = 0.18,
        gap: float = 0.42,
        prefix_show_max: int = 5,
        prefix_tail: int = 2,
        between_edge: int = 1,
        suffix_extra: int = 2,
    ) -> dict[str, Any]:
        """
        之间问题示意图：前缀圈/省略号 + 左关键人 + 之间(边圈+横省略号+边圈)
        + 右关键人 + 后缀冗余圈。人数再大也不画满，仅示意起止。
        """
        parts: list[Mobject] = []
        draw_order: list[Mobject] = []

        prefix_circles = VGroup()
        prefix_ellipsis = None
        before_count = left_rank - 1
        if before_count > 0:
            if before_count <= prefix_show_max:
                prefix_circles = VGroup(*[
                    self._person_circle(circle_r) for _ in range(before_count)
                ]).arrange(RIGHT, buff=gap)
                parts.append(prefix_circles)
                draw_order.append(prefix_circles)
            else:
                prefix_ellipsis = self._horizontal_ellipsis()
                prefix_circles = VGroup(*[
                    self._person_circle(circle_r) for _ in range(prefix_tail)
                ]).arrange(RIGHT, buff=gap)
                parts.extend([prefix_ellipsis, prefix_circles])
                draw_order.extend([prefix_ellipsis, prefix_circles])

        left_person = self._person_circle(circle_r)
        parts.append(left_person)
        draw_order.append(left_person)

        between_count = right_rank - left_rank - 1
        between_start = VGroup()
        between_ellipsis = None
        between_end = VGroup()
        between_all = VGroup()

        if between_count > 0:
            if between_count <= between_edge * 2:
                between_all = VGroup(*[
                    self._person_circle(circle_r) for _ in range(between_count)
                ]).arrange(RIGHT, buff=gap)
                parts.append(between_all)
                draw_order.append(between_all)
            else:
                between_start = VGroup(*[
                    self._person_circle(circle_r) for _ in range(between_edge)
                ]).arrange(RIGHT, buff=gap)
                between_ellipsis = self._horizontal_ellipsis()
                between_end = VGroup(*[
                    self._person_circle(circle_r) for _ in range(between_edge)
                ]).arrange(RIGHT, buff=gap)
                parts.extend([between_start, between_ellipsis, between_end])
                draw_order.extend([between_start, between_ellipsis, between_end])

        right_person = self._person_circle(circle_r)
        parts.append(right_person)
        draw_order.append(right_person)

        suffix_circles = VGroup()
        if suffix_extra > 0:
            suffix_circles = VGroup(*[
                self._person_circle(circle_r) for _ in range(suffix_extra)
            ]).arrange(RIGHT, buff=gap)
            parts.append(suffix_circles)
            draw_order.append(suffix_circles)

        row = VGroup(*parts).arrange(RIGHT, buff=gap)
        row.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(row)

        rank_left_anchor = (
            prefix_circles[0] if len(prefix_circles) > 0 else left_person
        )
        if between_ellipsis is not None:
            between_region = VGroup(between_start, between_ellipsis, between_end)
            between_brace_start = between_start[0]
            between_brace_end = between_end[-1]
        elif len(between_all) > 0:
            between_region = between_all
            between_brace_start = between_all[0]
            between_brace_end = between_all[-1]
        else:
            between_region = VGroup()
            between_brace_start = left_person
            between_brace_end = right_person

        between_zone_circles = VGroup()
        if between_ellipsis is not None:
            if len(between_start) > 0:
                between_zone_circles.add(*between_start)
            if len(between_end) > 0:
                between_zone_circles.add(*between_end)
        elif len(between_all) > 0:
            between_zone_circles.add(*between_all)

        return {
            "row": row,
            "draw_order": draw_order,
            "prefix_circles": prefix_circles,
            "prefix_ellipsis": prefix_ellipsis,
            "left_person": left_person,
            "between_start": between_start,
            "between_ellipsis": between_ellipsis,
            "between_end": between_end,
            "between_all": between_all,
            "between_region": between_region,
            "between_zone_circles": between_zone_circles,
            "right_person": right_person,
            "suffix_circles": suffix_circles,
            "rank_left_anchor": rank_left_anchor,
            "between_brace_start": between_brace_start,
            "between_brace_end": between_brace_end,
            "circle_r": circle_r,
        }
