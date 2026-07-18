"""
储蓄问题 — 第51讲：本金 + 按年分段的利息线段图。

左段为本金；右段为存期利息，均分成「年数」小格，每格为本金×年利率。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class SavingsInterestDiagramMixin:
    """利息＝本金×利率×存期。"""

    def make_savings_interest_diagram(
        self,
        draw_y: float,
        *,
        principal: int = 20000,
        years: int = 5,
        rate: float = 0.0265,
        total_w: float = 7.4,
        principal_frac: float = 0.55,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if principal <= 0 or years <= 0 or rate <= 0:
            raise ValueError("本金、存期、利率须为正")

        # 20000×2.65%×5 = 2650
        interest = int(round(principal * rate * years))
        yearly = principal * rate
        rate_pct = rate * 100
        # 显示用：2.65
        rate_str = f"{rate_pct:g}"

        prin_w = total_w * principal_frac
        int_w = total_w - prin_w
        unit_w = int_w / years
        left_x = -total_w / 2
        mid_x = left_x + prin_w
        right_x = left_x + total_w
        y = 0.30

        prin_color = TEAL_D
        int_color = ORANGE

        main = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        ticks = VGroup()
        for i in range(years + 1):
            x = mid_x + i * unit_w
            ticks.add(Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=WHITE if i in (0, years) else GREY_B,
                stroke_width=line_stroke * (0.85 if i in (0, years) else 0.55),
            ))
        ticks.add(Line(
            np.array([left_x, y + tick_h, 0]),
            np.array([left_x, y - tick_h, 0]),
            color=WHITE, stroke_width=line_stroke * 0.85,
        ))

        prin_bar = RoundedRectangle(
            width=prin_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        prin_bar.set_fill(prin_color, opacity=0.30)
        prin_bar.move_to(np.array([left_x + prin_w / 2, y, 0]))

        int_bar = RoundedRectangle(
            width=int_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        int_bar.set_fill(int_color, opacity=0.30)
        int_bar.move_to(np.array([mid_x + int_w / 2, y, 0]))

        # 年段浅色分隔线（已在 ticks 里）
        year_ticks = VGroup(*[
            Line(
                np.array([mid_x + i * unit_w, y + tick_h * 0.7, 0]),
                np.array([mid_x + i * unit_w, y - tick_h * 0.7, 0]),
                color=int_color, stroke_width=2.0,
            )
            for i in range(1, years)
        ])

        prin_lab = self.safe_text(f"本金 {principal} 元", font_size=18, color=prin_color)
        prin_lab.next_to(prin_bar, UP, buff=0.16)

        int_lab = self.safe_text(f"{years} 年利息", font_size=18, color=int_color)
        int_lab.next_to(int_bar, UP, buff=0.16)

        year_labs = VGroup()
        for i in range(years):
            lab = self.safe_text(f"第{i + 1}年", font_size=12, color=GREY_B)
            lab.move_to(np.array([mid_x + (i + 0.5) * unit_w, y - 0.42, 0]))
            year_labs.add(lab)

        rate_note = self.safe_text(
            f"每年利息为本金的 {rate_str}%",
            font_size=15, color=GREY_B,
        )
        rate_note.next_to(VGroup(prin_bar, int_bar), DOWN, buff=0.55)

        for m in (
            prin_bar, int_bar, year_ticks, prin_lab, int_lab, year_labs, rate_note,
        ):
            m.set_opacity(0)

        note_formula = self.safe_text(
            "利息＝本金×利率×存期",
            font_size=18, color=WHITE,
        )
        note_calc_q = self.safe_text(
            f"{principal}×{rate_str}%×{years}=？",
            font_size=20, color=WHITE,
        )
        note_calc_ans = self.safe_text(
            f"{principal}×{rate_str}%×{years}={interest}（元）",
            font_size=20, color=YELLOW,
        )
        for m in (note_formula, note_calc_q, note_calc_ans):
            m.set_opacity(0)

        notes = VGroup(note_formula, note_calc_q, note_calc_ans).arrange(
            DOWN, buff=0.16, aligned_edge=LEFT,
        )
        notes.next_to(rate_note, DOWN, buff=0.28)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "利息＝本金×利率×存期",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.12)

        diagram = VGroup(
            main, ticks, prin_bar, int_bar, year_ticks,
            prin_lab, int_lab, year_labs, rate_note, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "main": main,
            "ticks": ticks,
            "prin_bar": prin_bar,
            "int_bar": int_bar,
            "year_ticks": year_ticks,
            "prin_lab": prin_lab,
            "int_lab": int_lab,
            "year_labs": year_labs,
            "rate_note": rate_note,
            "notes": notes,
            "note_formula": note_formula,
            "note_calc_q": note_calc_q,
            "note_calc_ans": note_calc_ans,
            "hint": hint,
            "principal": principal,
            "years": years,
            "rate": rate,
            "rate_str": rate_str,
            "interest": interest,
            "yearly": yearly,
            "answer": f"到期利息{interest}元",
        }
