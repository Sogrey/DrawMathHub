"""
方程问题 — 第39讲：用线段图表述追及等量关系并列方程。

同地同向：甲先走 head 小时，再共同走 x 小时后乙追上；
甲总路程 = 乙总路程 → 列出方程。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class EquationCatchupDiagramMixin:
    """方程追及：甲（先行+共同）与乙（共同）等长线段图。"""

    def _eq_hline(
        self,
        left_x: float,
        right_x: float,
        y: float,
        *,
        stroke_width: float = 4.0,
        tick_h: float = 0.11,
        color=WHITE,
    ) -> VGroup:
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
        return VGroup(cap_l, main, cap_r)

    def make_equation_catchup_diagram(
        self,
        draw_y: float,
        *,
        ahead_speed: int = 48,
        chaser_speed: int = 72,
        head_start: int = 2,
        ahead_name: str = "甲车",
        chaser_name: str = "乙车",
        row_gap: float = 1.05,
        total_w: float = 7.0,
        line_stroke: float = 4.0,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "千米",
        time_unit: str = "小时",
    ) -> dict[str, Any]:
        if chaser_speed <= ahead_speed or head_start <= 0:
            raise ValueError("追赶者须更快，且先行时间为正")

        lead_dist = ahead_speed * head_start
        speed_diff = chaser_speed - ahead_speed
        if lead_dist % speed_diff != 0:
            raise ValueError("先行路程须能被速度差整除")
        x_ans = lead_dist // speed_diff

        # 追上时总路程（两边相等）
        total_dist = chaser_speed * x_ans
        # 甲：先行段 + 共同段
        jointly_ahead = ahead_speed * x_ans
        # 宽度比例
        lead_w = total_w * lead_dist / total_dist
        rest_w = total_w - lead_w

        left_x = -total_w / 2
        mid_x = left_x + lead_w
        right_x = left_x + total_w
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        # 竖导引：起点 / 乙出发 / 追上
        dash_start = DashedLine(
            np.array([left_x, top_y + 0.40, 0]),
            np.array([left_x, bot_y - 0.40, 0]),
            color=GREY_B, stroke_width=1.6, dash_length=0.08,
        )
        dash_mid = DashedLine(
            np.array([mid_x, top_y + 0.28, 0]),
            np.array([mid_x, bot_y - 0.28, 0]),
            color=GREY_B, stroke_width=1.4, dash_length=0.08,
        )
        dash_end = DashedLine(
            np.array([right_x, top_y + 0.45, 0]),
            np.array([right_x, bot_y - 0.45, 0]),
            color=YELLOW, stroke_width=2.0, dash_length=0.08,
        )
        catch_lab = self.safe_text("追上", font_size=15, color=YELLOW)
        catch_lab.next_to(dash_end, UP, buff=0.10)
        guides = VGroup(dash_start, dash_mid, dash_end, catch_lab)

        # 甲：两段
        line_lead = self._eq_hline(
            left_x, mid_x, top_y, stroke_width=line_stroke, color=TEAL_D,
        )
        line_ax = self._eq_hline(
            mid_x, right_x, top_y, stroke_width=line_stroke, color=TEAL_D,
        )
        brace_lead = Brace(
            Line(np.array([left_x, top_y, 0]), np.array([mid_x, top_y, 0])),
            direction=UP, buff=0.12,
        )
        brace_lead.set_color(TEAL_D)
        lab_lead = self.safe_text(
            f"{ahead_name}{head_start}{time_unit}路程",
            font_size=13, color=TEAL_D,
        )
        lab_lead.next_to(brace_lead, UP, buff=0.05)

        brace_ax = Brace(
            Line(np.array([mid_x, top_y, 0]), np.array([right_x, top_y, 0])),
            direction=UP, buff=0.12,
        )
        brace_ax.set_color(TEAL_D)
        lab_ax = self.safe_text(
            f"{ahead_name} x {time_unit}路程",
            font_size=13, color=TEAL_D,
        )
        lab_ax.next_to(brace_ax, UP, buff=0.05)

        name_a = self.safe_text(ahead_name, font_size=16, color=TEAL_D)
        name_a.next_to(np.array([left_x, top_y, 0]), LEFT, buff=0.20)

        top_row = VGroup(
            line_lead, line_ax, brace_lead, lab_lead, brace_ax, lab_ax, name_a,
        )

        # 乙：一段等长
        line_b = self._eq_hline(
            left_x, right_x, bot_y, stroke_width=line_stroke, color=ORANGE,
        )
        brace_b = Brace(
            Line(np.array([left_x, bot_y, 0]), np.array([right_x, bot_y, 0])),
            direction=DOWN, buff=0.12,
        )
        brace_b.set_color(ORANGE)
        lab_b = self.safe_text(
            f"{chaser_name} x {time_unit}路程",
            font_size=14, color=ORANGE,
        )
        lab_b.next_to(brace_b, DOWN, buff=0.05)

        name_b = self.safe_text(chaser_name, font_size=16, color=ORANGE)
        name_b.next_to(np.array([left_x, bot_y, 0]), LEFT, buff=0.20)

        bot_row = VGroup(line_b, brace_b, lab_b, name_b)

        # 等量关系与方程批注
        note_eq = self.safe_text(
            f"等量关系：{ahead_name}路程＝{chaser_name}路程",
            font_size=15, color=YELLOW,
        )
        note_form_q = self.safe_text(
            f"{ahead_speed}×{head_start}+{ahead_speed}x={chaser_speed}x",
            font_size=16, color=WHITE,
        )
        note_form_ans = self.safe_text(
            f"x={x_ans}",
            font_size=18, color=ORANGE,
        )
        for m in (note_eq, note_form_q, note_form_ans):
            m.set_opacity(0)

        notes = VGroup(note_eq, note_form_q, note_form_ans)
        note_eq.next_to(bot_row, DOWN, buff=0.42)
        note_form_q.next_to(note_eq, DOWN, buff=0.12)
        note_form_ans.next_to(note_form_q, DOWN, buff=0.12)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "追上时两车路程相等，据此列方程",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(guides, top_row, bot_row, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "guides": guides,
            "top_row": top_row,
            "bot_row": bot_row,
            "line_lead": line_lead,
            "line_ax": line_ax,
            "brace_lead": VGroup(brace_lead, lab_lead),
            "brace_ax": VGroup(brace_ax, lab_ax),
            "name_a": name_a,
            "line_b": line_b,
            "brace_b": VGroup(brace_b, lab_b),
            "name_b": name_b,
            "catch_lab": catch_lab,
            "notes": notes,
            "note_eq": note_eq,
            "note_form_q": note_form_q,
            "note_form_ans": note_form_ans,
            "hint": hint,
            "ahead_speed": ahead_speed,
            "chaser_speed": chaser_speed,
            "head_start": head_start,
            "x_ans": x_ans,
            "lead_dist": lead_dist,
            "total_dist": total_dist,
            "unit_label": unit_label,
            "time_unit": time_unit,
        }
