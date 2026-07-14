"""
排队问题图解 — 第2讲及同类题型。

约定：仅本模块维护排队（求总人数）相关逻辑。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class QueueDiagramMixin:
    def make_queue_total_diagram(
        self,
        front_count: int,
        back_count: int,
        draw_y: float,
        *,
        circle_r: float = 0.18,
        gap: float = 0.42,
        zone_show_max: int = 5,
        zone_head: int = 2,
        zone_tail: int = 2,
    ) -> dict[str, Any]:
        """
        排队问题（求全队总人数）示意图：
        前区圈/省略号 + 中间关键人 + 后区圈/省略号。人数再大也不画满。
        front_count / back_count 均不含中间关键人。
        """
        parts: list[Mobject] = []
        draw_order: list[Mobject] = []
        front_ellipsis: VGroup | None = None
        back_ellipsis: VGroup | None = None
        front_zone_circles = VGroup()
        back_zone_circles = VGroup()
        front_brace_start: Mobject | None = None
        front_brace_end: Mobject | None = None
        back_brace_start: Mobject | None = None
        back_brace_end: Mobject | None = None

        if front_count > 0:
            if front_count <= zone_show_max:
                front_zone = VGroup(*[
                    self._person_circle(circle_r) for _ in range(front_count)
                ]).arrange(RIGHT, buff=gap)
                front_zone_circles = front_zone
                parts.append(front_zone)
                draw_order.append(front_zone)
                front_brace_start = front_zone[0]
                front_brace_end = front_zone[-1]
            else:
                front_head = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_head)
                ]).arrange(RIGHT, buff=gap)
                front_ellipsis = self._horizontal_ellipsis()
                front_tail = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_tail)
                ]).arrange(RIGHT, buff=gap)
                front_zone = VGroup(front_head, front_ellipsis, front_tail)
                front_zone_circles.add(*front_head, *front_tail)
                parts.extend([front_head, front_ellipsis, front_tail])
                draw_order.extend([front_head, front_ellipsis, front_tail])
                front_brace_start = front_head[0]
                front_brace_end = front_tail[-1]
        else:
            front_zone = VGroup()

        center_person = self._person_circle(circle_r)
        parts.append(center_person)
        draw_order.append(center_person)

        if back_count > 0:
            if back_count <= zone_show_max:
                back_zone = VGroup(*[
                    self._person_circle(circle_r) for _ in range(back_count)
                ]).arrange(RIGHT, buff=gap)
                back_zone_circles = back_zone
                parts.append(back_zone)
                draw_order.append(back_zone)
                back_brace_start = back_zone[0]
                back_brace_end = back_zone[-1]
            else:
                back_head = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_head)
                ]).arrange(RIGHT, buff=gap)
                back_ellipsis = self._horizontal_ellipsis()
                back_tail = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_tail)
                ]).arrange(RIGHT, buff=gap)
                back_zone = VGroup(back_head, back_ellipsis, back_tail)
                back_zone_circles.add(*back_head, *back_tail)
                parts.extend([back_head, back_ellipsis, back_tail])
                draw_order.extend([back_head, back_ellipsis, back_tail])
                back_brace_start = back_head[0]
                back_brace_end = back_tail[-1]
        else:
            back_zone = VGroup()

        row = VGroup(*parts).arrange(RIGHT, buff=gap)
        row.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(row)

        if front_brace_start is None:
            front_brace_start = center_person
            front_brace_end = center_person
        if back_brace_start is None:
            back_brace_start = center_person
            back_brace_end = center_person

        total_brace_start = front_brace_start
        total_brace_end = back_brace_end

        return {
            "row": row,
            "draw_order": draw_order,
            "front_zone": front_zone,
            "front_ellipsis": front_ellipsis,
            "front_zone_circles": front_zone_circles,
            "center_person": center_person,
            "back_zone": back_zone,
            "back_ellipsis": back_ellipsis,
            "back_zone_circles": back_zone_circles,
            "front_brace_start": front_brace_start,
            "front_brace_end": front_brace_end,
            "back_brace_start": back_brace_start,
            "back_brace_end": back_brace_end,
            "total_brace_start": total_brace_start,
            "total_brace_end": total_brace_end,
            "circle_r": circle_r,
        }
