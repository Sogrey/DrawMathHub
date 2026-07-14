"""
租船问题（进一法）线段图 — 第9讲及同类题型。

水平线段按每船容量切分，满员段 + 余段，大括号标总人数与船数。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class BoatRentalDiagramMixin:
    """租船进一法：total ÷ capacity，有余数则 boats = quotient + 1。"""

    def _segment_tick(
        self,
        x: float,
        y: float,
        *,
        tick_h: float = 0.14,
        color=WHITE,
        stroke_width: float = 2.0,
    ) -> Line:
        return Line(
            np.array([x, y + tick_h, 0]),
            np.array([x, y - tick_h, 0]),
            color=color, stroke_width=stroke_width,
        )

    def _brace_over_segment(
        self,
        left_x: float,
        right_x: float,
        y: float,
        label_text: str,
        *,
        direction=UP,
        buff: float = 0.10,
        brace_color=TEAL_D,
        label_color=TEAL_D,
        font_size: int = 16,
    ) -> tuple[Brace, Mobject]:
        span = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
        )
        brace = Brace(span, direction=direction, buff=buff)
        brace.set_color(brace_color)
        label = self.safe_text(label_text, font_size=font_size, color=label_color)
        label.next_to(brace, direction, buff=0.06)
        return brace, label

    def make_boat_rental_diagram(
        self,
        total: int,
        capacity: int,
        draw_y: float,
        *,
        full_seg_width: float = 0.50,
        line_stroke: float = 4.5,
        tick_h: float = 0.14,
    ) -> dict[str, Any]:
        if capacity <= 0:
            raise ValueError("capacity 必须大于 0")
        quotient = total // capacity
        remainder = total % capacity
        boats = quotient + (1 if remainder > 0 else 0)

        rem_width = (
            full_seg_width * remainder / capacity if remainder > 0 else 0.0
        )
        total_width = quotient * full_seg_width + rem_width
        left_x = -total_width / 2
        right_x = total_width / 2
        base_y = 0.0

        main_line = Line(
            np.array([left_x, base_y, 0]),
            np.array([right_x, base_y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        cap_l = Line(
            np.array([left_x, base_y + tick_h, 0]),
            np.array([left_x, base_y - tick_h, 0]),
            color=WHITE, stroke_width=line_stroke * 0.75,
        )
        cap_r = Line(
            np.array([right_x, base_y + tick_h, 0]),
            np.array([right_x, base_y - tick_h, 0]),
            color=WHITE, stroke_width=line_stroke * 0.75,
        )
        line_block = VGroup(cap_l, main_line, cap_r)

        full_segments: list[dict[str, Any]] = []
        full_parts: list[Mobject] = []
        for i in range(quotient):
            seg_left = left_x + i * full_seg_width
            seg_right = seg_left + full_seg_width
            seg_center = (seg_left + seg_right) / 2
            tick_r = self._segment_tick(
                seg_right, base_y, tick_h=tick_h, color=GREY_B, stroke_width=1.8,
            )
            brace, label = self._brace_over_segment(
                seg_left, seg_right, base_y + tick_h + 0.02,
                f"{capacity}人",
                brace_color=TEAL_D, label_color=TEAL_D, font_size=15,
            )
            parts = VGroup(tick_r, brace, label)
            full_segments.append({
                "index": i + 1,
                "left": seg_left,
                "right": seg_right,
                "center": seg_center,
                "tick": tick_r,
                "brace": brace,
                "label": label,
                "parts": parts,
            })
            full_parts.append(parts)

        remainder_segment: dict[str, Any] | None = None
        rem_parts: Mobject | None = None
        if remainder > 0:
            rem_left = left_x + quotient * full_seg_width
            rem_right = rem_left + rem_width
            rem_center = (rem_left + rem_right) / 2
            tick_r = self._segment_tick(
                rem_right, base_y, tick_h=tick_h, color=RED, stroke_width=2.0,
            )
            brace, label = self._brace_over_segment(
                rem_left, rem_right, base_y + tick_h + 0.02,
                f"余{remainder}人",
                brace_color=RED, label_color=RED, font_size=15,
            )
            rem_parts = VGroup(tick_r, brace, label)
            remainder_segment = {
                "left": rem_left,
                "right": rem_right,
                "center": rem_center,
                "remainder": remainder,
                "tick": tick_r,
                "brace": brace,
                "label": label,
                "parts": rem_parts,
            }

        # 上方大括号：总人数（抬高，避免与分段「4人」标注重叠）
        people_span_y = base_y + tick_h + 0.50
        people_span = Line(
            np.array([left_x, people_span_y, 0]),
            np.array([right_x, people_span_y, 0]),
        )
        people_brace = Brace(people_span, direction=UP, buff=0.10)
        people_brace.set_color(YELLOW)
        people_label = self.safe_text(f"共{total}人", font_size=20, color=YELLOW)
        people_label.next_to(people_brace, UP, buff=0.08)
        people_block = VGroup(people_brace, people_label)

        # 下方大括号：船数
        boats_brace = Brace(main_line, direction=DOWN, buff=0.18)
        boats_brace.set_color(BLUE_B)
        boats_label = self.safe_text("? 条船", font_size=20, color=BLUE_B)
        boats_label.next_to(boats_brace, DOWN, buff=0.08)
        boats_block = VGroup(boats_brace, boats_label)

        extra_boat_note = self.safe_text(
            f"剩余{remainder}人还要再租1条船", font_size=18, color=RED,
        )
        final_boats_note = self.safe_text(
            f"{quotient}+1={boats}（条）", font_size=20, color=YELLOW,
        )
        rule_note = self.safe_text(
            "所有人都要有船坐 → 进一法", font_size=17, color=GREY_B,
        )
        extra_block = VGroup(extra_boat_note, final_boats_note, rule_note).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT,
        )
        extra_block.next_to(boats_block, DOWN, buff=0.28)

        hint = self.safe_text(
            "线段图：每段代表一条满员船", font_size=18, color=GREY_B,
        )

        full_block = VGroup(line_block, *full_parts)
        if rem_parts is not None:
            full_block.add(rem_parts)
        diagram_core = VGroup(full_block, people_block, boats_block, extra_block)
        hint.next_to(diagram_core, DOWN, buff=0.16)
        full = VGroup(diagram_core, hint)
        full.move_to(np.array([0.0, draw_y, 0.0]))
        self.clamp_content(full)

        return {
            "diagram": full,
            "layout_row": full,
            "hint": hint,
            "main_line": main_line,
            "line_block": line_block,
            "full_segments": full_segments,
            "full_parts": full_parts,
            "full_block": VGroup(*full_parts) if full_parts else VGroup(),
            "remainder_segment": remainder_segment,
            "rem_parts": rem_parts,
            "people_brace": people_brace,
            "people_label": people_label,
            "people_block": people_block,
            "boats_brace": boats_brace,
            "boats_label": boats_label,
            "boats_block": boats_block,
            # 兼容旧键名
            "total_brace": people_brace,
            "total_label": people_label,
            "total_block": people_block,
            "extra_boat_note": extra_boat_note,
            "final_boats_note": final_boats_note,
            "rule_note": rule_note,
            "extra_block": extra_block,
            "total": total,
            "capacity": capacity,
            "quotient": quotient,
            "remainder": remainder,
            "boats": boats,
        }
