"""
因数与倍数问题 — 第40讲：短除法分析最大公因数与最小公倍数。

已知 GCD、LCM，短除后商互质，利用 GCD×a×b＝LCM 求两数。
短除号形态：左竖线 + 右下横线组成的「└」角括号（横线在被除数下）。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class GcdLcmShortDiagramMixin:
    """短除法：公因数短除 → 互质商 → 还原两数。"""

    def make_gcd_lcm_short_diagram(
        self,
        draw_y: float,
        *,
        gcd: int = 9,
        lcm: int = 90,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if gcd <= 0 or lcm <= 0 or lcm % gcd != 0:
            raise ValueError("LCM 须能被 GCD 整除")
        product = lcm // gcd  # ab
        pairs = [(1, 10), (2, 5)] if product == 10 else [(1, product)]

        # ── 短除角括号 └ ──
        #    9 |  A     B
        #      |_________
        #         a     b   ← 互质
        # 横线在被除数下方（教材短除），不是除法「屋檐」
        stroke = 3.2
        bracket_h = 0.72
        bracket_w = 2.9

        # 角点：竖线下端 = 横线左端
        corner = np.array([0.0, 0.0, 0])
        vert = Line(
            corner,
            corner + UP * bracket_h,
            color=WHITE, stroke_width=stroke,
        )
        horiz = Line(
            corner,
            corner + RIGHT * bracket_w,
            color=WHITE, stroke_width=stroke,
        )
        bracket = VGroup(vert, horiz)

        gcd_lab = self.safe_text(str(gcd), font_size=30, color=YELLOW)
        gcd_lab.next_to(vert, LEFT, buff=0.16)
        gcd_lab.move_to(np.array([
            gcd_lab.get_center()[0],
            corner[1] + bracket_h * 0.45,
            0,
        ]))

        a_lab = self.safe_text("A", font_size=30, color=TEAL_D)
        b_lab = self.safe_text("B", font_size=30, color=ORANGE)
        top_nums = VGroup(a_lab, b_lab).arrange(RIGHT, buff=0.95)
        # A、B 在横线上方、竖线右侧
        top_nums.move_to(
            np.array([
                corner[0] + bracket_w * 0.52,
                corner[1] + bracket_h * 0.48,
                0,
            ])
        )

        quot_a = self.safe_text("a", font_size=30, color=TEAL_D)
        quot_b = self.safe_text("b", font_size=30, color=ORANGE)
        bottom = VGroup(quot_a, quot_b).arrange(RIGHT, buff=0.95)
        # a、b 在横线下方
        bottom.move_to(
            np.array([
                top_nums.get_center()[0],
                corner[1] - 0.48,
                0,
            ])
        )

        short_div = VGroup(bracket, gcd_lab, top_nums, bottom)

        # 互质：虚线圆角框 + 箭头指向「互质」
        pad = 0.28
        oval = DashedVMobject(
            RoundedRectangle(
                width=bottom.width + pad * 2,
                height=bottom.height + pad,
                corner_radius=0.18,
                color=GREY_A,
                stroke_width=2.0,
            ),
            num_dashes=22,
        )
        oval.move_to(bottom.get_center())

        coprime_lab = self.safe_text("互质", font_size=18, color=TEAL_D)
        coprime_lab.next_to(oval, RIGHT, buff=0.55)
        arrow = DashedLine(
            oval.get_right() + RIGHT * 0.06,
            coprime_lab.get_left() + LEFT * 0.06,
            color=TEAL_D, stroke_width=2.0, dash_length=0.08,
        )
        # 箭头尖
        tip = Triangle(fill_opacity=1, stroke_width=0, color=TEAL_D)
        tip.scale(0.08)
        tip.rotate(-PI / 2)
        tip.next_to(coprime_lab, LEFT, buff=0.02)
        coprime_g = VGroup(oval, arrow, tip, coprime_lab)

        # 批注
        note_rel = self.safe_text(
            f"{gcd}×a×b＝{lcm}  →  a×b＝{product}",
            font_size=18, color=YELLOW,
        )
        note_pairs = self.safe_text(
            f"{product}＝1×10＝2×5（互质）",
            font_size=17, color=WHITE,
        )
        note_case1 = self.safe_text(
            "① 1×9＝9，10×9＝90",
            font_size=17, color=TEAL_D,
        )
        note_case2 = self.safe_text(
            "② 2×9＝18，5×9＝45",
            font_size=17, color=ORANGE,
        )
        for m in (note_rel, note_pairs, note_case1, note_case2):
            m.set_opacity(0)

        notes = VGroup(note_rel, note_pairs, note_case1, note_case2)
        note_rel.next_to(short_div, DOWN, buff=0.70)
        note_pairs.next_to(note_rel, DOWN, buff=0.14)
        note_case1.next_to(note_pairs, DOWN, buff=0.14)
        note_case2.next_to(note_case1, DOWN, buff=0.12)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "短除后商互质，GCD×a×b＝LCM",
                font_size=15, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(short_div, coprime_g, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "short_div": short_div,
            "bracket": bracket,
            "gcd_lab": gcd_lab,
            "top_nums": top_nums,
            "bottom": bottom,
            "coprime_g": coprime_g,
            "notes": notes,
            "note_rel": note_rel,
            "note_pairs": note_pairs,
            "note_case1": note_case1,
            "note_case2": note_case2,
            "hint": hint,
            "gcd": gcd,
            "lcm": lcm,
            "product": product,
            "pairs": pairs,
        }
