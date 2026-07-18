"""
纳税问题 — 第50讲：工资线段分「免征额 + 应纳税所得额」。

整段表示工资；左段免征，右段为应纳税所得额并标注税率，税额＝所得额×税率。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class TaxIncomeDiagramMixin:
    """个税：工资 − 免征额 = 应纳税所得额，再×税率。"""

    def make_tax_income_diagram(
        self,
        draw_y: float,
        *,
        salary: int = 7200,
        exemption: int = 5000,
        rate: float = 0.03,
        total_w: float = 7.2,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if salary <= exemption or exemption <= 0 or rate <= 0:
            raise ValueError("工资须大于免征额，且免征额、税率为正")

        taxable = salary - exemption
        tax = int(round(taxable * rate))
        rate_pct = int(round(rate * 100))

        exempt_w = total_w * exemption / salary
        tax_w = total_w - exempt_w
        left_x = -total_w / 2
        mid_x = left_x + exempt_w
        right_x = left_x + total_w
        y = 0.25

        exempt_color = TEAL_D
        tax_color = ORANGE

        main = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        ticks = VGroup(*[
            Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.85,
            )
            for x in (left_x, mid_x, right_x)
        ])

        exempt_bar = RoundedRectangle(
            width=exempt_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        exempt_bar.set_fill(exempt_color, opacity=0.30)
        exempt_bar.move_to(np.array([left_x + exempt_w / 2, y, 0]))

        tax_bar = RoundedRectangle(
            width=tax_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        tax_bar.set_fill(tax_color, opacity=0.30)
        tax_bar.move_to(np.array([mid_x + tax_w / 2, y, 0]))

        salary_lab = self.safe_text(f"工资 {salary} 元", font_size=18, color=GREY_B)
        salary_lab.next_to(main, UP, buff=0.48)

        exempt_lab = self.safe_text(f"{exemption} 元", font_size=18, color=exempt_color)
        exempt_lab.next_to(exempt_bar, UP, buff=0.14)
        exempt_tag = self.safe_text("免征额", font_size=15, color=exempt_color)
        exempt_tag.next_to(exempt_bar, DOWN, buff=0.14)

        tax_lab_q = self.safe_text(f"({salary}−{exemption}) 元", font_size=16, color=tax_color)
        tax_lab_q.next_to(tax_bar, UP, buff=0.14)
        tax_lab_ans = self.safe_text(f"{taxable} 元", font_size=18, color=YELLOW)
        tax_lab_ans.move_to(tax_lab_q.get_center())

        rate_brace = Brace(tax_bar, direction=DOWN, buff=0.32)
        rate_brace.set_color(tax_color)
        rate_note = self.safe_text(f"按 {rate_pct}% 的税率缴纳", font_size=15, color=tax_color)
        rate_note.next_to(rate_brace, DOWN, buff=0.08)

        for m in (
            exempt_bar, tax_bar, salary_lab, exempt_lab, exempt_tag,
            tax_lab_q, tax_lab_ans, rate_brace, rate_note,
        ):
            m.set_opacity(0)
        tax_lab_ans.set_opacity(0)

        note_taxable = self.safe_text(
            f"应纳税所得额：{salary}−{exemption}={taxable}（元）",
            font_size=18, color=WHITE,
        )
        note_tax_q = self.safe_text(
            f"应纳税额：{taxable}×{rate_pct}%=？",
            font_size=18, color=WHITE,
        )
        note_tax_ans = self.safe_text(
            f"应纳税额：{taxable}×{rate_pct}%={tax}（元）",
            font_size=18, color=YELLOW,
        )

        for m in (note_taxable, note_tax_q, note_tax_ans):
            m.set_opacity(0)

        notes = VGroup(note_taxable, note_tax_q, note_tax_ans).arrange(
            DOWN, buff=0.16, aligned_edge=LEFT,
        )
        notes.next_to(VGroup(main, rate_note), DOWN, buff=0.40)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "应纳税额＝应纳税所得额×税率",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.12)

        diagram = VGroup(
            main, ticks, exempt_bar, tax_bar,
            salary_lab, exempt_lab, exempt_tag,
            tax_lab_q, tax_lab_ans, rate_brace, rate_note,
            notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "main": main,
            "ticks": ticks,
            "exempt_bar": exempt_bar,
            "tax_bar": tax_bar,
            "salary_lab": salary_lab,
            "exempt_lab": exempt_lab,
            "exempt_tag": exempt_tag,
            "tax_lab_q": tax_lab_q,
            "tax_lab_ans": tax_lab_ans,
            "rate_brace": rate_brace,
            "rate_note": rate_note,
            "notes": notes,
            "note_taxable": note_taxable,
            "note_tax_q": note_tax_q,
            "note_tax_ans": note_tax_ans,
            "hint": hint,
            "salary": salary,
            "exemption": exemption,
            "taxable": taxable,
            "rate": rate,
            "rate_pct": rate_pct,
            "tax": tax,
            "answer": f"应缴纳个人所得税{tax}元",
        }
