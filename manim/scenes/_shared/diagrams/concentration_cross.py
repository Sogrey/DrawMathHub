"""
浓度问题 — 第52讲：十字交叉法图解。

左上/左下为两种溶液浓度，中心为混合浓度；
交叉得右上/右下浓度差，即两种溶液质量比。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class ConcentrationCrossDiagramMixin:
    """十字交叉法：两种浓度混合求用量比。"""

    def make_concentration_cross_diagram(
        self,
        draw_y: float,
        *,
        high: float = 0.20,
        low: float = 0.05,
        mix: float = 0.15,
        total: float = 600,
        arm: float = 1.55,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if not (high > mix > low > 0) or total <= 0:
            raise ValueError("须满足 高浓度 > 混合浓度 > 低浓度 > 0，且总量为正")

        high_pct = int(round(high * 100))
        low_pct = int(round(low * 100))
        mix_pct = int(round(mix * 100))
        # 高浓度份数 = 混合 − 低；低浓度份数 = 高 − 混合
        high_parts_pct = mix_pct - low_pct  # 10
        low_parts_pct = high_pct - mix_pct  # 5
        # 化简比
        g = int(np.gcd(high_parts_pct, low_parts_pct))
        high_ratio = high_parts_pct // g
        low_ratio = low_parts_pct // g
        high_amt = int(round(total * high_ratio / (high_ratio + low_ratio)))
        low_amt = int(round(total * low_ratio / (high_ratio + low_ratio)))

        # 局部坐标（随后整体移到 draw_y）
        tl = np.array([-arm, arm * 0.72, 0])
        bl = np.array([-arm, -arm * 0.72, 0])
        tr = np.array([arm, arm * 0.72, 0])
        br = np.array([arm, -arm * 0.72, 0])
        c = np.array([0.0, 0.0, 0])

        high_color = TEAL_D
        low_color = ORANGE
        mix_color = YELLOW

        # 交叉线：左上→右下，左下→右上
        line_high = Line(tl, br, color=WHITE, stroke_width=3.5)
        line_low = Line(bl, tr, color=WHITE, stroke_width=3.5)

        mix_dot = Dot(c, radius=0.08, color=mix_color)
        mix_lab = self.safe_text(f"{mix_pct}%", font_size=26, color=mix_color)
        mix_lab.next_to(mix_dot, UP, buff=0.18)

        high_lab = self.safe_text(f"{high_pct}%", font_size=28, color=high_color)
        high_lab.move_to(tl + LEFT * 0.55)

        low_lab = self.safe_text(f"{low_pct}%", font_size=28, color=low_color)
        low_lab.move_to(bl + LEFT * 0.55)

        # 右上：混合−低 = 高浓度对应份数
        diff_high = self.safe_text(
            f"{mix_pct}%-{low_pct}%={high_parts_pct}%",
            font_size=20, color=high_color,
        )
        diff_high.move_to(tr + RIGHT * 0.95)

        # 右下：高−混合 = 低浓度对应份数
        diff_low = self.safe_text(
            f"{high_pct}%-{mix_pct}%={low_parts_pct}%",
            font_size=20, color=low_color,
        )
        diff_low.move_to(br + RIGHT * 0.95)

        for m in (
            line_high, line_low, mix_dot, mix_lab,
            high_lab, low_lab, diff_high, diff_low,
        ):
            m.set_opacity(0)

        note_ratio_q = self.safe_text(
            f"{high_pct}%盐水∶{low_pct}%盐水＝{high_parts_pct}%∶{low_parts_pct}%",
            font_size=18, color=WHITE,
        )
        note_ratio_ans = self.safe_text(
            f"化简得 {high_ratio}∶{low_ratio}",
            font_size=20, color=YELLOW,
        )
        note_calc_high = self.safe_text(
            f"{int(total)}×{high_ratio}/({high_ratio}+{low_ratio})={high_amt}（克）",
            font_size=18, color=high_color,
        )
        note_calc_low = self.safe_text(
            f"{int(total)}×{low_ratio}/({high_ratio}+{low_ratio})={low_amt}（克）",
            font_size=18, color=low_color,
        )
        for m in (note_ratio_q, note_ratio_ans, note_calc_high, note_calc_low):
            m.set_opacity(0)

        notes = VGroup(
            note_ratio_q, note_ratio_ans, note_calc_high, note_calc_low,
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        notes.next_to(VGroup(line_high, line_low), DOWN, buff=0.55)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "交叉差之比＝两种溶液质量比",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.12)

        diagram = VGroup(
            line_high, line_low, mix_dot, mix_lab,
            high_lab, low_lab, diff_high, diff_low, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "line_high": line_high,
            "line_low": line_low,
            "mix_dot": mix_dot,
            "mix_lab": mix_lab,
            "high_lab": high_lab,
            "low_lab": low_lab,
            "diff_high": diff_high,
            "diff_low": diff_low,
            "notes": notes,
            "note_ratio_q": note_ratio_q,
            "note_ratio_ans": note_ratio_ans,
            "note_calc_high": note_calc_high,
            "note_calc_low": note_calc_low,
            "hint": hint,
            "high_pct": high_pct,
            "low_pct": low_pct,
            "mix_pct": mix_pct,
            "high_parts_pct": high_parts_pct,
            "low_parts_pct": low_parts_pct,
            "high_ratio": high_ratio,
            "low_ratio": low_ratio,
            "high_amt": high_amt,
            "low_amt": low_amt,
            "total": int(total),
            "answer": f"{high_pct}%需{high_amt}克，{low_pct}%需{low_amt}克",
        }
