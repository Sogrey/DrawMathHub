"""
归一问题线段图 — 第22讲及同类题型。

一条线段均分成 n 份；上括号标已知份数与总量，下括号标新份数与待求。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class UnitaryDiagramMixin:
    """归一问题：先求单一量，再求新总量/新份数。"""

    def make_unitary_line_diagram(
        self,
        draw_y: float,
        *,
        known_parts: int = 3,
        known_total: int = 15,
        new_parts: int = 7,
        known_label: str = "3盆花 15元",
        new_label: str = "7盆花 ?元",
        answer_label: str = "7盆花 35元",
        unit_w: float = 0.62,
        line_stroke: float = 4.0,
        tick_h: float = 0.12,
        show_hint: bool = True,
        x_shift: float = 0.20,
    ) -> dict[str, Any]:
        if known_parts <= 0 or new_parts <= 0:
            raise ValueError("份数必须为正")
        if new_parts < known_parts:
            # 仍可画图，仅常见情形是 new ≥ known
            pass

        unit_value = known_total // known_parts
        new_total = unit_value * new_parts

        total_w = new_parts * unit_w
        left_x = -total_w / 2
        right_x = left_x + total_w
        known_right = left_x + known_parts * unit_w
        y = 0.0

        main = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        ticks = VGroup()
        for i in range(new_parts + 1):
            x = left_x + i * unit_w
            ticks.add(Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.85,
            ))

        # 已知份段浅色填充条
        known_bar = RoundedRectangle(
            width=known_parts * unit_w,
            height=0.22,
            corner_radius=0.04,
            color=TEAL_D,
            stroke_width=0,
        )
        known_bar.set_fill(TEAL_D, opacity=0.30)
        known_bar.move_to(np.array([
            left_x + known_parts * unit_w / 2,
            y, 0,
        ]))

        known_span = Line(
            np.array([left_x, y + tick_h + 0.04, 0]),
            np.array([known_right, y + tick_h + 0.04, 0]),
        )
        known_brace = Brace(known_span, direction=UP, buff=0.10)
        known_brace.set_color(TEAL_D)
        known_lab = self.safe_text(known_label, font_size=18, color=TEAL_D)
        known_lab.next_to(known_brace, UP, buff=0.06)
        known_block = VGroup(known_brace, known_lab)

        new_span = Line(
            np.array([left_x, y - tick_h - 0.04, 0]),
            np.array([right_x, y - tick_h - 0.04, 0]),
        )
        new_brace = Brace(new_span, direction=DOWN, buff=0.14)
        new_brace.set_color(YELLOW)
        new_lab_q = self.safe_text(new_label, font_size=18, color=YELLOW)
        new_lab_q.next_to(new_brace, DOWN, buff=0.14)
        # 必须先加入 new_block 再整体 move_to，否则答案标签会停在旧坐标、与线段重叠
        new_lab_ans = self.safe_text(answer_label, font_size=18, color=YELLOW)
        new_lab_ans.next_to(new_brace, DOWN, buff=0.14)
        new_lab_ans.set_opacity(0)
        new_block = VGroup(new_brace, new_lab_q, new_lab_ans)

        unit_note = self.safe_text(
            f"单一量：{known_total}÷{known_parts}={unit_value}",
            font_size=16, color=ORANGE,
        )
        unit_note.next_to(new_block, DOWN, buff=0.24)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "单一量不变：先求一份，再求新的总量",
                font_size=17, color=GREY_B,
            )

        line_core = VGroup(main, ticks, known_bar)
        annotated = VGroup(line_core, known_block, new_block, unit_note)
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
            "line_core": line_core,
            "main": main,
            "ticks": ticks,
            "known_bar": known_bar,
            "known_block": known_block,
            "known_brace": known_brace,
            "known_lab": known_lab,
            "new_block": new_block,
            "new_brace": new_brace,
            "new_lab_q": new_lab_q,
            "new_lab_ans": new_lab_ans,
            "unit_note": unit_note,
            "hint": hint,
            "known_parts": known_parts,
            "known_total": known_total,
            "new_parts": new_parts,
            "unit_value": unit_value,
            "new_total": new_total,
        }
