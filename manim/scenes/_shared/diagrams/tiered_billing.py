"""
分段计费问题 — 第41讲：线段图法。

按阶梯把用量画成一段线段；先算前几阶满额费用，与总费用比较，判断落在哪一阶。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class TieredBillingDiagramMixin:
    """阶梯水费：三段用量线段 + 前两阶费用对比。"""

    def make_tiered_billing_diagram(
        self,
        draw_y: float,
        *,
        t1_cap: float = 10,
        t1_price: float = 2.5,
        t2_cap: float = 15,
        t2_price: float = 3.75,
        t3_price: float = 7.5,
        total_fee: float = 88.75,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_vol: str = "立方米",
        unit_fee: str = "元",
    ) -> dict[str, Any]:
        t2_span = t2_cap - t1_cap
        fee1 = t1_cap * t1_price
        fee2 = t2_span * t2_price
        fee12 = fee1 + fee2
        if total_fee <= fee12:
            raise ValueError("本母题总费用应超过前两阶满额费用")
        t3_vol = (total_fee - fee12) / t3_price
        total_vol = t2_cap + t3_vol

        # 线段宽度：前两阶按实际水量，第三段略短表示未知（视觉）
        w1, w2, w3 = 2.4, 1.5, 1.8
        total_w = w1 + w2 + w3
        left_x = -total_w / 2
        x0, x1, x2, x3 = left_x, left_x + w1, left_x + w1 + w2, left_x + total_w
        y = 0.25
        stroke = 4.0
        tick_h = 0.12

        def seg(xa, xb, color=WHITE):
            main = Line(
                np.array([xa, y, 0]), np.array([xb, y, 0]),
                color=color, stroke_width=stroke,
            )
            caps = VGroup(
                Line(
                    np.array([xa, y + tick_h, 0]), np.array([xa, y - tick_h, 0]),
                    color=color, stroke_width=stroke * 0.85,
                ),
                Line(
                    np.array([xb, y + tick_h, 0]), np.array([xb, y - tick_h, 0]),
                    color=color, stroke_width=stroke * 0.85,
                ),
            )
            return VGroup(main, caps)

        s1 = seg(x0, x1, TEAL_D)
        s2 = seg(x1, x2, ORANGE)
        s3 = seg(x2, x3, YELLOW)

        # 上方：各段水量标注
        b1 = Brace(Line(np.array([x0, y, 0]), np.array([x1, y, 0])), UP, buff=0.14)
        b1.set_color(TEAL_D)
        l1 = self.safe_text(f"{t1_cap:g} {unit_vol}", font_size=14, color=TEAL_D)
        l1.next_to(b1, UP, buff=0.06)

        b2 = Brace(Line(np.array([x1, y, 0]), np.array([x2, y, 0])), UP, buff=0.14)
        b2.set_color(ORANGE)
        l2 = self.safe_text(f"{t2_cap:g} {unit_vol}", font_size=14, color=ORANGE)
        l2.next_to(b2, UP, buff=0.06)

        b3 = Brace(Line(np.array([x2, y, 0]), np.array([x3, y, 0])), UP, buff=0.14)
        b3.set_color(YELLOW)
        l3_q = self.safe_text(f"? {unit_vol}", font_size=14, color=YELLOW)
        l3_ans = self.safe_text(f"{t3_vol:g} {unit_vol}", font_size=14, color=YELLOW)
        l3_q.next_to(b3, UP, buff=0.06)
        l3_ans.next_to(b3, UP, buff=0.06)
        l3_ans.set_opacity(0)

        # 费用小注（在段上方稍远）
        fee1_lab = self.safe_text(
            f"{t1_price:g}×{t1_cap:g}={fee1:g}",
            font_size=13, color=GREY_B,
        )
        fee1_lab.next_to(l1, UP, buff=0.10)
        fee2_lab = self.safe_text(
            f"{t2_price:g}×{t2_span:g}={fee2:g}",
            font_size=13, color=GREY_B,
        )
        fee2_lab.next_to(l2, UP, buff=0.10)
        fee1_lab.set_opacity(0)
        fee2_lab.set_opacity(0)

        # 下方：前两阶合计 < 总费用
        b12 = Brace(Line(np.array([x0, y, 0]), np.array([x2, y, 0])), DOWN, buff=0.16)
        b12.set_color(WHITE)
        cmp_lab = self.safe_text(
            f"{fee1:g}+{fee2:g}={fee12:g} ＜ {total_fee:g} {unit_fee}",
            font_size=15, color=YELLOW,
        )
        cmp_lab.next_to(b12, DOWN, buff=0.08)
        cmp_g = VGroup(b12, cmp_lab)
        cmp_g.set_opacity(0)

        # 推理批注
        note_over = self.safe_text(
            f"故用水量超过 {t2_cap:g} {unit_vol}",
            font_size=15, color=ORANGE,
        )
        note_calc_q = self.safe_text(
            f"总量：({total_fee:g}－{fee12:g})÷{t3_price:g}+{t2_cap:g}=?",
            font_size=15, color=YELLOW,
        )
        note_calc_ans = self.safe_text(
            f"总量：({total_fee:g}－{fee12:g})÷{t3_price:g}+{t2_cap:g}={total_vol:g}",
            font_size=15, color=YELLOW,
        )
        for m in (note_over, note_calc_q, note_calc_ans):
            m.set_opacity(0)

        notes = VGroup(note_over, note_calc_q, note_calc_ans)
        note_over.next_to(cmp_g, DOWN, buff=0.28)
        note_calc_q.next_to(note_over, DOWN, buff=0.12)
        note_calc_ans.move_to(note_calc_q)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "先算满阶费用，再与总费用比较，判断落在哪一阶",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        line_g = VGroup(s1, s2, s3)
        braces_top = VGroup(b1, l1, b2, l2, b3, l3_q, l3_ans, fee1_lab, fee2_lab)
        diagram = VGroup(line_g, braces_top, cmp_g, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "line_g": line_g,
            "s1": s1,
            "s2": s2,
            "s3": s3,
            "brace1": VGroup(b1, l1),
            "brace2": VGroup(b2, l2),
            "brace3": VGroup(b3, l3_q, l3_ans),
            "l3_q": l3_q,
            "l3_ans": l3_ans,
            "fee1_lab": fee1_lab,
            "fee2_lab": fee2_lab,
            "cmp_g": cmp_g,
            "notes": notes,
            "note_over": note_over,
            "note_calc_q": note_calc_q,
            "note_calc_ans": note_calc_ans,
            "hint": hint,
            "fee1": fee1,
            "fee2": fee2,
            "fee12": fee12,
            "t3_vol": t3_vol,
            "total_vol": total_vol,
            "total_fee": total_fee,
            "t1_cap": t1_cap,
            "t2_cap": t2_cap,
            "t1_price": t1_price,
            "t2_price": t2_price,
            "t3_price": t3_price,
            "t2_span": t2_span,
        }
