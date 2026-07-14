"""
移多补少问题图解 — 第3讲及同类题型。

约定：仅本模块维护移多补少相关逻辑。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class TransferDiagramMixin:
    def _received_circle(
        self, radius: float, *, color=ORANGE, stroke_width: int = 3, fill_opacity: float = 0.45,
    ) -> Circle:
        """较少方补上的物品（与原有圆圈区分颜色）。"""
        c = Circle(radius=radius, color=color, stroke_width=stroke_width)
        c.set_fill(color, opacity=fill_opacity)
        return c

    def make_transfer_balance_diagram(
        self,
        more_count: int,
        less_count: int,
        draw_y: float,
        more_name: str = "芳芳",
        less_name: str = "晶晶",
        *,
        circle_r: float = 0.16,
        gap: float = 0.36,
        row_buff: float = 0.75,
        zone_show_max: int = 6,
        zone_head: int = 3,
        zone_tail: int = 2,
        extra_gap: float = 0.55,
        ellipsis_buff: float = 0.48,
    ) -> dict[str, Any]:
        """
        移多补少示意图：上下两行左对齐，上行=较多方，下行=较少方。
        上行 = 相同部分 + 多出部分；相同部分与下行等宽对齐。
        """
        if more_count < less_count:
            more_count, less_count = less_count, more_count
            more_name, less_name = less_name, more_name

        diff = more_count - less_count
        transfer_half = diff // 2

        def _zone(count: int) -> tuple[VGroup, VGroup, list[Mobject], VGroup | None]:
            if count <= 0:
                return VGroup(), VGroup(), [], None
            if count <= zone_show_max:
                zone = VGroup(*[
                    self._person_circle(circle_r) for _ in range(count)
                ]).arrange(RIGHT, buff=gap)
                return zone, zone, [zone], None
            head = VGroup(*[
                self._person_circle(circle_r) for _ in range(zone_head)
            ]).arrange(RIGHT, buff=gap)
            ellipsis = self._horizontal_ellipsis()
            tail = VGroup(*[
                self._person_circle(circle_r) for _ in range(zone_tail)
            ]).arrange(RIGHT, buff=gap)
            zone = VGroup(head, ellipsis, tail).arrange(
                RIGHT, buff=ellipsis_buff, aligned_edge=ORIGIN,
            )
            ellipsis.align_to(head[0], ORIGIN)
            circles = VGroup(*head, *tail)
            return zone, circles, [head, ellipsis, tail], ellipsis

        same_zone, same_circles, same_draw, same_ellipsis = _zone(less_count)
        extra_zone, extra_circles, extra_draw, extra_ellipsis = _zone(diff)
        less_zone, less_circles, less_draw, less_ellipsis = _zone(less_count)

        more_row_parts: list[Mobject] = [same_zone]
        more_draw: list[Mobject] = list(same_draw)
        if len(extra_zone) > 0:
            more_row_parts.append(extra_zone)
            more_draw.extend(extra_draw)
        more_bars = VGroup(*more_row_parts).arrange(RIGHT, buff=extra_gap)
        less_bars = less_zone

        label_more = self.safe_text(more_name, font_size=24, color=YELLOW)
        label_less = self.safe_text(less_name, font_size=24, color=PURPLE_A)
        bars_x = self.safe_left + 1.75

        more_bars.move_to(np.array([bars_x + more_bars.width / 2, draw_y + row_buff / 2, 0]))
        more_bars.align_to(np.array([bars_x, 0, 0]), LEFT)
        less_bars.move_to(np.array([bars_x + less_bars.width / 2, draw_y - row_buff / 2, 0]))
        less_bars.align_to(np.array([bars_x, 0, 0]), LEFT)

        label_more.next_to(more_bars, LEFT, buff=0.25)
        label_less.next_to(less_bars, LEFT, buff=0.25)

        diagram = VGroup(label_more, label_less, more_bars, less_bars)
        self.clamp_content(diagram)

        give_circles = (
            VGroup(*extra_circles[-transfer_half:])
            if transfer_half > 0 and len(extra_circles) > 0 else VGroup()
        )
        keep_circles = (
            VGroup(*extra_circles[:-transfer_half])
            if transfer_half > 0 and len(extra_circles) > transfer_half else extra_circles
        )
        received_circles = VGroup(*[
            self._received_circle(circle_r) for _ in range(transfer_half)
        ]) if transfer_half > 0 else VGroup()
        if len(received_circles) > 0:
            received_circles.arrange(RIGHT, buff=gap)
            received_circles.next_to(less_bars, RIGHT, buff=extra_gap)
            received_circles.align_to(less_bars, ORIGIN)
            self.clamp_content(received_circles)
        extra_brace_span = extra_zone if len(extra_zone) > 0 else None

        draw_order: list[Mobject] = [label_more, *more_draw, label_less, *less_draw]

        return {
            "diagram": diagram,
            "draw_order": draw_order,
            "more_bars": more_bars,
            "less_bars": less_bars,
            "same_circles_more": same_circles,
            "same_circles_less": less_circles,
            "same_ellipsis_more": same_ellipsis,
            "same_ellipsis_less": less_ellipsis,
            "extra_circles": extra_circles,
            "extra_ellipsis": extra_ellipsis,
            "give_circles": give_circles,
            "keep_circles": keep_circles,
            "received_circles": received_circles,
            "more_brace_span": more_bars,
            "less_brace_span": less_bars,
            "same_brace_span": same_zone,
            "extra_brace_span": extra_brace_span,
            "diff": diff,
            "transfer_half": transfer_half,
            "circle_r": circle_r,
            "more_name": more_name,
            "less_name": less_name,
        }
