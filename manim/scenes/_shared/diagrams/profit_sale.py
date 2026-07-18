"""
利润问题 — 第49讲：分两段售价的销量线段图。

全程按销量分成「正价段 + 促销段」，标出各段单价；总利润＝两段售出额－总成本。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class ProfitSaleDiagramMixin:
    """进价定利润率定价，分段售出求总利润。"""

    def make_profit_sale_diagram(
        self,
        draw_y: float,
        *,
        total_n: int = 200,
        sold_n: int = 160,
        cost: int = 5,
        profit_rate: float = 0.40,
        discount: float = 0.60,
        total_w: float = 7.0,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if not (0 < sold_n < total_n):
            raise ValueError("正价销量须在 0 与总量之间")
        if cost <= 0 or profit_rate < 0 or not (0 < discount <= 1):
            raise ValueError("进价、利润率、折扣参数不合法")

        remain_n = total_n - sold_n
        # 定价 = 进价 × (1+利润率)；本讲 5×1.4=7
        price = int(round(cost * (1 + profit_rate)))
        sale_price = price * discount  # 7×0.6=4.2
        total_cost = total_n * cost
        revenue = sold_n * price + remain_n * sale_price
        profit = int(round(revenue - total_cost))  # 288

        sold_w = total_w * sold_n / total_n
        remain_w = total_w - sold_w
        left_x = -total_w / 2
        mid_x = left_x + sold_w
        right_x = left_x + total_w
        y = 0.15

        sold_color = TEAL_D
        remain_color = ORANGE

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

        sold_bar = RoundedRectangle(
            width=sold_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        sold_bar.set_fill(sold_color, opacity=0.30)
        sold_bar.move_to(np.array([left_x + sold_w / 2, y, 0]))

        remain_bar = RoundedRectangle(
            width=remain_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        remain_bar.set_fill(remain_color, opacity=0.30)
        remain_bar.move_to(np.array([mid_x + remain_w / 2, y, 0]))

        # 上标销量
        sold_n_lab = self.safe_text(f"{sold_n}个", font_size=18, color=sold_color)
        sold_n_lab.next_to(sold_bar, UP, buff=0.18)
        remain_n_lab = self.safe_text(f"{remain_n}个", font_size=18, color=remain_color)
        remain_n_lab.next_to(remain_bar, UP, buff=0.18)
        total_n_lab = self.safe_text(f"共{total_n}个", font_size=16, color=GREY_B)
        total_n_lab.next_to(main, UP, buff=0.55)

        # 下标单价
        sold_p_lab = self.safe_text(f"{price}元/个", font_size=16, color=sold_color)
        sold_p_lab.next_to(sold_bar, DOWN, buff=0.18)
        remain_p_q = self.safe_mathtex(
            rf"({price}\times {int(discount * 100)}\%)",
            font_size=20, color=remain_color,
        )
        remain_p_unit = self.safe_text("元/个", font_size=15, color=remain_color)
        remain_p_lab = VGroup(remain_p_q, remain_p_unit).arrange(RIGHT, buff=0.06)
        remain_p_lab.next_to(remain_bar, DOWN, buff=0.16)

        # 初始：分段填色与标价可分步显现
        for m in (sold_bar, remain_bar, sold_n_lab, remain_n_lab,
                  sold_p_lab, remain_p_lab, total_n_lab):
            m.set_opacity(0)

        # 底部算式
        note_price = VGroup(
            self.safe_text("定价：", font_size=18, color=WHITE),
            self.safe_mathtex(
                rf"{cost}\times(1+{int(profit_rate * 100)}\%)={price}",
                font_size=24, color=WHITE,
            ),
            self.safe_text("（元）", font_size=16, color=WHITE),
        ).arrange(RIGHT, buff=0.08)

        note_profit_q = VGroup(
            self.safe_mathtex(
                rf"{sold_n}\times{price}+({total_n}-{sold_n})"
                rf"\times({price}\times{int(discount * 100)}\%)"
                rf"-{total_n}\times{cost}=?",
                font_size=20, color=WHITE,
            ),
        )

        note_profit_ans = VGroup(
            self.safe_mathtex(
                rf"{sold_n}\times{price}+({total_n}-{sold_n})"
                rf"\times({price}\times{int(discount * 100)}\%)"
                rf"-{total_n}\times{cost}={profit}",
                font_size=20, color=YELLOW,
            ),
            self.safe_text("（元）", font_size=16, color=YELLOW),
        ).arrange(RIGHT, buff=0.08)

        for m in (note_price, note_profit_q, note_profit_ans):
            m.set_opacity(0)

        notes = VGroup(note_price, note_profit_q, note_profit_ans).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT,
        )
        notes.next_to(VGroup(main, sold_p_lab, remain_p_lab), DOWN, buff=0.45)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "两段售出额相加，再减去总成本",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.12)

        diagram = VGroup(
            main, ticks, sold_bar, remain_bar,
            sold_n_lab, remain_n_lab, total_n_lab,
            sold_p_lab, remain_p_lab, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "main": main,
            "ticks": ticks,
            "sold_bar": sold_bar,
            "remain_bar": remain_bar,
            "sold_n_lab": sold_n_lab,
            "remain_n_lab": remain_n_lab,
            "total_n_lab": total_n_lab,
            "sold_p_lab": sold_p_lab,
            "remain_p_lab": remain_p_lab,
            "notes": notes,
            "note_price": note_price,
            "note_profit_q": note_profit_q,
            "note_profit_ans": note_profit_ans,
            "hint": hint,
            "total_n": total_n,
            "sold_n": sold_n,
            "remain_n": remain_n,
            "cost": cost,
            "price": price,
            "sale_price": sale_price,
            "profit": profit,
            "profit_rate": profit_rate,
            "discount": discount,
            "answer": f"利润{profit}元",
        }
