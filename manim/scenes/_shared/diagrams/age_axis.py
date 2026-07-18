"""
年龄问题（二）— 第30讲：年龄轴法。

年龄差不变；以年龄差为单位，在轴上标出「过去 / 今年」的份数关系。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class AgeAxisDiagramMixin:
    """年龄轴：两人以年龄差为单位的份数关系。"""

    def make_age_axis_diagram(
        self,
        draw_y: float,
        *,
        age_sum: int = 100,
        young_units: int = 2,
        old_units: int = 3,
        young_name: str = "爸爸",
        old_name: str = "爷爷",
        unit_w: float = 1.35,
        line_stroke: float = 4.0,
        tick_h: float = 0.18,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "岁",
    ) -> dict[str, Any]:
        if young_units <= 0 or old_units <= young_units:
            raise ValueError("需满足 old_units > young_units > 0")
        total_units = young_units + old_units
        if age_sum % total_units != 0:
            raise ValueError("年龄和须能被份数和整除")
        diff = age_sum // total_units
        young_age = diff * young_units
        old_age = diff * old_units

        # 过去：爷爷 = 爸爸今年 = young_units 份；当时爸爸 = 1 份（= 年龄差）
        past_old_units = young_units
        past_young_units = past_old_units - (old_units - young_units)  # = 1 when 3&2
        # 更稳：差 always old-young
        age_gap_units = old_units - young_units
        past_young_units = past_old_units - age_gap_units

        n_ticks = old_units  # 0..old_units
        total_w = n_ticks * unit_w
        left_x = -total_w / 2
        y = 0.0

        main = Line(
            np.array([left_x, y, 0]),
            np.array([left_x + total_w, y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        # 右端箭头表示年龄轴方向
        axis_tip = Arrow(
            np.array([left_x + total_w - 0.15, y, 0]),
            np.array([left_x + total_w + 0.35, y, 0]),
            buff=0, stroke_width=line_stroke,
            color=WHITE, max_tip_length_to_length_ratio=0.45, tip_length=0.2,
        )

        ticks = VGroup()
        tick_labels = VGroup()
        for i in range(n_ticks + 1):
            x = left_x + i * unit_w
            ticks.add(Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.85,
            ))
            if i == 0:
                lab = self.safe_text("0", font_size=16, color=GREY_B)
                lab.next_to(np.array([x, y, 0]), DOWN, buff=0.22)
                tick_labels.add(lab)

        # 第一个年龄差单位段
        u0, u1 = left_x, left_x + unit_w
        diff_span = Line(np.array([u0, y + tick_h + 0.02, 0]), np.array([u1, y + tick_h + 0.02, 0]))
        diff_brace = Brace(diff_span, direction=UP, buff=0.10)
        diff_brace.set_color(ORANGE)
        diff_lab = self.safe_text("1个年龄差", font_size=15, color=ORANGE)
        diff_lab.next_to(diff_brace, UP, buff=0.06)
        diff_block = VGroup(diff_brace, diff_lab)

        # 爸爸今年：0 → young_units
        y_end = left_x + young_units * unit_w
        young_span = Line(
            np.array([left_x, y - tick_h - 0.02, 0]),
            np.array([y_end, y - tick_h - 0.02, 0]),
        )
        young_brace = Brace(young_span, direction=DOWN, buff=0.14)
        young_brace.set_color(TEAL_D)
        young_lab_q = self.safe_text(
            f"{young_name}今年？",
            font_size=16, color=TEAL_D,
        )
        young_lab_ans = self.safe_text(
            f"{young_name}今年 {young_age}{unit_label}（{young_units}个差）",
            font_size=15, color=TEAL_D,
        )
        young_lab_q.next_to(young_brace, DOWN, buff=0.08)
        young_lab_ans.next_to(young_brace, DOWN, buff=0.08)
        young_lab_ans.set_opacity(0)
        young_block = VGroup(young_brace, young_lab_q, young_lab_ans)

        # 爷爷今年：0 → old_units
        o_end = left_x + old_units * unit_w
        old_span = Line(
            np.array([left_x, y + tick_h + 0.02, 0]),
            np.array([o_end, y + tick_h + 0.02, 0]),
        )
        old_brace = Brace(old_span, direction=UP, buff=0.48)
        old_brace.set_color(YELLOW)
        old_lab_q = self.safe_text(
            f"{old_name}今年？",
            font_size=16, color=YELLOW,
        )
        old_lab_ans = self.safe_text(
            f"{old_name}今年 {old_age}{unit_label}（{old_units}个差）",
            font_size=15, color=YELLOW,
        )
        old_lab_q.next_to(old_brace, UP, buff=0.06)
        old_lab_ans.next_to(old_brace, UP, buff=0.06)
        old_lab_ans.set_opacity(0)
        old_block = VGroup(old_brace, old_lab_q, old_lab_ans)

        # 过去关系说明（当时爸爸 = 1 个差 = 爷爷当时的一半）
        past_note = self.safe_text(
            f"当年：{old_name}={young_name}今年={young_units}个差，"
            f"{young_name}={past_young_units}个差（正好一半）",
            font_size=14, color=GREY_A,
        )
        past_note.set_opacity(0)

        sum_note = self.safe_text(
            f"年龄和 = {young_units}+{old_units}={total_units} 个年龄差 = {age_sum}{unit_label}",
            font_size=15, color=ORANGE,
        )
        sum_note.set_opacity(0)

        calc_note = self.safe_text(
            f"{age_sum}÷{total_units}={diff}，{old_name}={diff}×{old_units}={old_age}{unit_label}",
            font_size=15, color=YELLOW,
        )
        calc_note.set_opacity(0)

        notes = VGroup(past_note, sum_note, calc_note).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT,
        )

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "年龄差永远不变，用「年龄差」作单位看份数",
                font_size=16, color=GREY_B,
            )

        axis = VGroup(main, axis_tip, ticks, tick_labels)
        annotated = VGroup(
            axis, diff_block, young_block, old_block, notes,
        )
        layout_row = VGroup(annotated)
        if show_hint:
            notes.next_to(young_block, DOWN, buff=0.28)
            hint.next_to(notes, DOWN, buff=0.14)
            layout_row = VGroup(annotated, hint)
        else:
            notes.next_to(young_block, DOWN, buff=0.28)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "axis": axis,
            "main": main,
            "axis_tip": axis_tip,
            "ticks": ticks,
            "tick_labels": tick_labels,
            "diff_block": diff_block,
            "young_block": young_block,
            "old_block": old_block,
            "young_lab_q": young_lab_q,
            "young_lab_ans": young_lab_ans,
            "old_lab_q": old_lab_q,
            "old_lab_ans": old_lab_ans,
            "notes": notes,
            "past_note": past_note,
            "sum_note": sum_note,
            "calc_note": calc_note,
            "hint": hint,
            "age_sum": age_sum,
            "young_units": young_units,
            "old_units": old_units,
            "total_units": total_units,
            "diff": diff,
            "young_age": young_age,
            "old_age": old_age,
            "young_name": young_name,
            "old_name": old_name,
            "unit_label": unit_label,
        }
