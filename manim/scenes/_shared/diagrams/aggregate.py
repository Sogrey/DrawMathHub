"""
归总问题线段图 — 第23讲及同类题型。

上下两条等长线段表示同一总量；上按原单一量分段，下按新单一量分段。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class AggregateDiagramMixin:
    """归总问题：总量不变，先求总量再求新份数/新单一量。"""

    def _agg_hline(
        self,
        left_x: float,
        right_x: float,
        y: float,
        parts: int,
        *,
        stroke_width: float = 4.0,
        tick_h: float = 0.11,
        color=WHITE,
    ) -> tuple[VGroup, float]:
        main = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=color, stroke_width=stroke_width,
        )
        ticks = VGroup()
        seg_w = (right_x - left_x) / parts
        for i in range(parts + 1):
            x = left_x + i * seg_w
            ticks.add(Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=color, stroke_width=stroke_width * 0.85,
            ))
        return VGroup(main, ticks), seg_w

    def make_aggregate_line_diagram(
        self,
        draw_y: float,
        *,
        old_unit: int = 12,
        old_parts: int = 4,
        new_unit: int = 8,
        old_unit_label: str = "12人",
        new_unit_label: str = "8人",
        ask_label: str = "?行",
        answer_label: str = "6行",
        total_w: float = 4.8,
        row_gap: float = 1.15,
        line_stroke: float = 4.0,
        tick_h: float = 0.11,
        show_hint: bool = True,
        x_shift: float = 0.15,
    ) -> dict[str, Any]:
        if old_unit <= 0 or old_parts <= 0 or new_unit <= 0:
            raise ValueError("单一量与份数须为正")

        total = old_unit * old_parts
        if total % new_unit != 0:
            raise ValueError("总量须能被新的单一量整除")
        new_parts = total // new_unit

        left_x = -total_w / 2
        right_x = left_x + total_w
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        top_line, top_seg_w = self._agg_hline(
            left_x, right_x, top_y, old_parts,
            stroke_width=line_stroke, tick_h=tick_h, color=TEAL_D,
        )
        bot_line, bot_seg_w = self._agg_hline(
            left_x, right_x, bot_y, new_parts,
            stroke_width=line_stroke, tick_h=tick_h, color=PURPLE_A,
        )

        # 上：第一份 = 原单一量
        top_span = Line(
            np.array([left_x, top_y + tick_h + 0.04, 0]),
            np.array([left_x + top_seg_w, top_y + tick_h + 0.04, 0]),
        )
        top_unit_brace = Brace(top_span, direction=UP, buff=0.10)
        top_unit_brace.set_color(TEAL_D)
        top_unit_lab = self.safe_text(old_unit_label, font_size=18, color=TEAL_D)
        top_unit_lab.next_to(top_unit_brace, UP, buff=0.08)
        top_unit_block = VGroup(top_unit_brace, top_unit_lab)

        top_parts_lab = self.safe_text(
            f"{old_parts}行",
            font_size=16, color=GREY_B,
        )
        top_parts_lab.next_to(top_line, RIGHT, buff=0.18)

        # 下：第一份 = 新单一量
        bot_span = Line(
            np.array([left_x, bot_y + tick_h + 0.04, 0]),
            np.array([left_x + bot_seg_w, bot_y + tick_h + 0.04, 0]),
        )
        bot_unit_brace = Brace(bot_span, direction=UP, buff=0.08)
        bot_unit_brace.set_color(PURPLE_A)
        bot_unit_lab = self.safe_text(new_unit_label, font_size=18, color=PURPLE_A)
        bot_unit_lab.next_to(bot_unit_brace, UP, buff=0.06)
        bot_unit_block = VGroup(bot_unit_brace, bot_unit_lab)

        # 整段下括号：求新份数（答案标签必须同组，防整体平移后错位）
        ask_span = Line(
            np.array([left_x, bot_y - tick_h - 0.04, 0]),
            np.array([right_x, bot_y - tick_h - 0.04, 0]),
        )
        ask_brace = Brace(ask_span, direction=DOWN, buff=0.12)
        ask_brace.set_color(YELLOW)
        ask_lab_q = self.safe_text(ask_label, font_size=20, color=YELLOW)
        ask_lab_q.next_to(ask_brace, DOWN, buff=0.12)
        ask_lab_ans = self.safe_text(answer_label, font_size=20, color=YELLOW)
        ask_lab_ans.next_to(ask_brace, DOWN, buff=0.12)
        ask_lab_ans.set_opacity(0)
        ask_block = VGroup(ask_brace, ask_lab_q, ask_lab_ans)

        total_note = self.safe_text(
            f"总量不变：{old_unit}×{old_parts}={total}（人）",
            font_size=16, color=ORANGE,
        )
        total_note.next_to(ask_block, DOWN, buff=0.22)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "两条线段一样长，表示总人数相同",
                font_size=17, color=GREY_B,
            )

        top_block = VGroup(top_line, top_unit_block, top_parts_lab)
        bot_block = VGroup(bot_line, bot_unit_block)
        annotated = VGroup(top_block, bot_block, ask_block, total_note)
        layout_row = VGroup(annotated)
        if show_hint:
            hint.next_to(annotated, DOWN, buff=0.16)
            layout_row = VGroup(annotated, hint)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "top_block": top_block,
            "top_line": top_line,
            "top_unit_block": top_unit_block,
            "top_parts_lab": top_parts_lab,
            "bot_block": bot_block,
            "bot_line": bot_line,
            "bot_unit_block": bot_unit_block,
            "ask_block": ask_block,
            "ask_brace": ask_brace,
            "ask_lab_q": ask_lab_q,
            "ask_lab_ans": ask_lab_ans,
            "total_note": total_note,
            "hint": hint,
            "old_unit": old_unit,
            "old_parts": old_parts,
            "new_unit": new_unit,
            "new_parts": new_parts,
            "total": total,
        }
