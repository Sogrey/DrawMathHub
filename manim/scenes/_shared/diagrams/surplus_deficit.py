"""
盈亏问题 — 第36讲：线段图法。

两种分法：一种有余（盈）、一种不足（亏）；用双线对比求出份数与总量。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class SurplusDeficitDiagramMixin:
    """盈亏问题：每人分得量不同时的盈／亏线段对比。"""

    def _sd_seg(
        self,
        left_x: float,
        right_x: float,
        y: float,
        *,
        stroke_width: float = 4.0,
        tick_h: float = 0.10,
        color=WHITE,
        dashed: bool = False,
    ) -> VGroup:
        if dashed:
            main = DashedLine(
                np.array([left_x, y, 0]),
                np.array([right_x, y, 0]),
                color=color, stroke_width=stroke_width, dash_length=0.10,
            )
        else:
            main = Line(
                np.array([left_x, y, 0]),
                np.array([right_x, y, 0]),
                color=color, stroke_width=stroke_width,
            )
        cap_l = Line(
            np.array([left_x, y + tick_h, 0]),
            np.array([left_x, y - tick_h, 0]),
            color=color, stroke_width=stroke_width * 0.85,
        )
        cap_r = Line(
            np.array([right_x, y + tick_h, 0]),
            np.array([right_x, y - tick_h, 0]),
            color=color, stroke_width=stroke_width * 0.85,
        )
        if dashed:
            return VGroup(main, cap_r)
        return VGroup(cap_l, main, cap_r)

    def make_surplus_deficit_diagram(
        self,
        draw_y: float,
        *,
        rate_a: int = 12,
        surplus: int = 5,
        rate_b: int = 14,
        deficit: int = 5,
        row_gap: float = 1.05,
        base_w: float = 4.2,
        line_stroke: float = 4.0,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "个",
        name_a: str = "第一种",
        name_b: str = "第二种",
    ) -> dict[str, Any]:
        if rate_b <= rate_a:
            raise ValueError("需 rate_b > rate_a")
        rate_diff = rate_b - rate_a
        gap_total = surplus + deficit
        if gap_total % rate_diff != 0:
            raise ValueError("（盈+亏）须能被分配差整除")
        people = gap_total // rate_diff
        apples = rate_a * people + surplus
        # 校验另一公式
        if rate_b * people - deficit != apples:
            raise ValueError("盈亏数据不一致")

        # 宽度：按「每人分量」比例；盈／亏段按数量相对 rate_a
        w_a = base_w
        w_b = base_w * (rate_b / rate_a)
        w_sur = base_w * (surplus / rate_a)
        w_def = base_w * (deficit / rate_a)

        left_x = - (w_b) / 2  # 以较长的第二种左端对齐视觉中心
        # 实际上两种从同一左端开始
        left_x = -w_b / 2
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        # 第一种：每人 rate_a + 盈
        a_end = left_x + w_a
        sur_end = a_end + w_sur
        line_a = self._sd_seg(left_x, a_end, top_y, stroke_width=line_stroke, color=TEAL_D)
        line_sur = self._sd_seg(
            a_end, sur_end, top_y, stroke_width=line_stroke, color=YELLOW,
        )

        brace_a = Brace(
            Line(np.array([left_x, top_y, 0]), np.array([a_end, top_y, 0])),
            direction=UP, buff=0.12,
        )
        brace_a.set_color(TEAL_D)
        lab_a = self.safe_text(f"每人分 {rate_a} {unit_label}", font_size=14, color=TEAL_D)
        lab_a.next_to(brace_a, UP, buff=0.05)

        brace_sur = Brace(
            Line(np.array([a_end, top_y, 0]), np.array([sur_end, top_y, 0])),
            direction=UP, buff=0.12,
        )
        brace_sur.set_color(YELLOW)
        lab_sur = self.safe_text(f"盈 {surplus}", font_size=14, color=YELLOW)
        lab_sur.next_to(brace_sur, UP, buff=0.05)

        name_lab_a = self.safe_text(name_a, font_size=15, color=GREY_B)
        name_lab_a.next_to(np.array([left_x, top_y, 0]), LEFT, buff=0.22)

        top_row = VGroup(
            line_a, line_sur, brace_a, lab_a, brace_sur, lab_sur, name_lab_a,
        )

        # 第二种：每人 rate_b，末段虚线表示亏（尚未有的苹果）
        b_solid_end = left_x + w_b - w_def  # = 实际苹果右端 = sur_end
        b_end = left_x + w_b
        # 对齐：实际总量右端应对齐
        # sur_end 应对应 b_solid_end；若比例正确，w_a+w_sur = w_b-w_def
        # 校验并微移：强制 b_solid 终点 = sur_end
        align_apples_x = sur_end
        b_end = align_apples_x + w_def
        line_b_solid = self._sd_seg(
            left_x, align_apples_x, bot_y, stroke_width=line_stroke, color=ORANGE,
        )
        line_b_def = self._sd_seg(
            align_apples_x, b_end, bot_y,
            stroke_width=line_stroke, color=ORANGE, dashed=True,
        )

        brace_b = Brace(
            Line(np.array([left_x, bot_y, 0]), np.array([b_end, bot_y, 0])),
            direction=DOWN, buff=0.12,
        )
        brace_b.set_color(ORANGE)
        lab_b = self.safe_text(f"每人分 {rate_b} {unit_label}", font_size=14, color=ORANGE)
        lab_b.next_to(brace_b, DOWN, buff=0.05)

        brace_def = Brace(
            Line(np.array([align_apples_x, bot_y, 0]), np.array([b_end, bot_y, 0])),
            direction=UP, buff=0.08,
        )
        brace_def.set_color(RED_B)
        lab_def = self.safe_text(f"亏 {deficit}", font_size=14, color=RED_B)
        lab_def.next_to(brace_def, UP, buff=0.04)

        name_lab_b = self.safe_text(name_b, font_size=15, color=GREY_B)
        name_lab_b.next_to(np.array([left_x, bot_y, 0]), LEFT, buff=0.22)

        bot_row = VGroup(
            line_b_solid, line_b_def, brace_b, lab_b, brace_def, lab_def, name_lab_b,
        )

        # 对齐虚线：左端、苹果总量右端
        align_l = DashedLine(
            np.array([left_x, top_y + 0.35, 0]),
            np.array([left_x, bot_y - 0.35, 0]),
            color=GREY_B, stroke_width=1.3, dash_length=0.08,
        )
        align_apples = DashedLine(
            np.array([align_apples_x, top_y + 0.20, 0]),
            np.array([align_apples_x, bot_y - 0.20, 0]),
            color=GREY_B, stroke_width=1.3, dash_length=0.08,
        )
        align = VGroup(align_l, align_apples)

        apples_tag = self.safe_text("苹果总量", font_size=13, color=GREY_B)
        apples_tag.next_to(align_apples, DOWN, buff=0.06)
        apples_tag.shift(RIGHT * 0.35)

        # 批注
        note_gap = self.safe_text(
            f"相差：{surplus}+{deficit}={gap_total}（{unit_label}）",
            font_size=15, color=YELLOW,
        )
        note_diff = self.safe_text(
            f"每人多分：{rate_b}－{rate_a}={rate_diff}（{unit_label}）",
            font_size=15, color=GREY_B,
        )
        note_people_q = self.safe_text(
            f"人数：{gap_total}÷{rate_diff}=?",
            font_size=15, color=TEAL_D,
        )
        note_people_ans = self.safe_text(
            f"人数：{gap_total}÷{rate_diff}={people}（人）",
            font_size=15, color=TEAL_D,
        )
        note_apples = self.safe_text(
            f"苹果：{rate_a}×{people}+{surplus}={apples}（{unit_label}）",
            font_size=15, color=ORANGE,
        )
        for m in (note_gap, note_diff, note_people_q, note_people_ans, note_apples):
            m.set_opacity(0)

        notes = VGroup(note_gap, note_diff, note_people_q, note_people_ans, note_apples)
        note_gap.next_to(bot_row, DOWN, buff=0.55)
        note_diff.next_to(note_gap, DOWN, buff=0.10)
        note_people_q.next_to(note_diff, DOWN, buff=0.10)
        note_people_ans.move_to(note_people_q)
        note_apples.next_to(note_people_ans, DOWN, buff=0.10)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "（盈＋亏）÷分配差＝份数",
                font_size=15, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(
            align, top_row, bot_row, apples_tag, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "align": align,
            "top_row": top_row,
            "bot_row": bot_row,
            "line_a": line_a,
            "line_sur": line_sur,
            "brace_a": VGroup(brace_a, lab_a),
            "brace_sur": VGroup(brace_sur, lab_sur),
            "line_b_solid": line_b_solid,
            "line_b_def": line_b_def,
            "brace_b": VGroup(brace_b, lab_b),
            "brace_def": VGroup(brace_def, lab_def),
            "name_a": name_lab_a,
            "name_b": name_lab_b,
            "apples_tag": apples_tag,
            "notes": notes,
            "note_gap": note_gap,
            "note_diff": note_diff,
            "note_people_q": note_people_q,
            "note_people_ans": note_people_ans,
            "note_apples": note_apples,
            "hint": hint,
            "rate_a": rate_a,
            "rate_b": rate_b,
            "surplus": surplus,
            "deficit": deficit,
            "rate_diff": rate_diff,
            "gap_total": gap_total,
            "people": people,
            "apples": apples,
            "unit_label": unit_label,
        }
