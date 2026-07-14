"""
和差问题线段图 — 第18讲及同类题型。

方法一：给较小数补差（虚线加长），和变为（和+差）。
方法二：给较大数去差（多出段改虚线），和变为（和−差）。
可各建一份图，上下分栏同时保留。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class SumDiffDiagramMixin:
    """和差问题：已知和与差，线段图求两量（补差 / 去差）。"""

    def _sd_hline(
        self,
        left_x: float,
        right_x: float,
        y: float,
        *,
        stroke_width: float = 4.0,
        tick_h: float = 0.12,
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

    def make_sum_diff_diagram(
        self,
        draw_y: float,
        *,
        total: int = 12,
        difference: int = 6,
        large_name: str = "女",
        small_name: str = "男",
        small_w: float = 0.72,
        row_gap: float = 0.92,
        line_stroke: float = 3.5,
        tick_h: float = 0.10,
        show_hint: bool = False,
        x_shift: float = 0.25,
        unit_label: str = "人",
        scale: float = 1.0,
        method_tag: str = "",
    ) -> dict[str, Any]:
        if difference <= 0 or total <= difference:
            raise ValueError("需满足 total > difference > 0")

        large = (total + difference) // 2
        small = (total - difference) // 2
        large_w = small_w * (large / small) if small else small_w * 2

        left_x = 0.0
        small_right = left_x + small_w
        large_right = left_x + large_w
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        align_l = DashedLine(
            np.array([left_x, top_y + 0.28, 0]),
            np.array([left_x, bot_y - 0.28, 0]),
            color=GREY_B, stroke_width=1.4, dash_length=0.08,
        )
        align_mid = DashedLine(
            np.array([small_right, top_y + 0.14, 0]),
            np.array([small_right, bot_y - 0.14, 0]),
            color=GREY_B, stroke_width=1.4, dash_length=0.08,
        )
        align = VGroup(align_l, align_mid)

        large_base = self._sd_hline(
            left_x, small_right, top_y,
            stroke_width=line_stroke, tick_h=tick_h, color=PURPLE_A,
        )
        large_extra_solid = VGroup(
            Line(
                np.array([small_right, top_y, 0]),
                np.array([large_right, top_y, 0]),
                color=PURPLE_A, stroke_width=line_stroke,
            ),
            Line(
                np.array([large_right, top_y + tick_h, 0]),
                np.array([large_right, top_y - tick_h, 0]),
                color=PURPLE_A, stroke_width=line_stroke * 0.85,
            ),
        )
        large_extra_dashed = self._sd_hline(
            small_right, large_right, top_y,
            stroke_width=line_stroke * 0.9, tick_h=tick_h,
            color=PURPLE_A, dashed=True,
        )
        large_name_m = self.safe_text(large_name, font_size=18, color=WHITE)
        large_name_m.next_to(large_base, LEFT, buff=0.18)
        large_line = VGroup(large_base, large_extra_solid)
        large_block = VGroup(large_name_m, large_line)

        small_line = self._sd_hline(
            left_x, small_right, bot_y,
            stroke_width=line_stroke, tick_h=tick_h, color=TEAL_D,
        )
        small_name_m = self.safe_text(small_name, font_size=18, color=WHITE)
        small_name_m.next_to(small_line, LEFT, buff=0.18)
        small_block = VGroup(small_name_m, small_line)

        diff_span = Line(
            np.array([small_right, top_y + tick_h + 0.04, 0]),
            np.array([large_right, top_y + tick_h + 0.04, 0]),
        )
        diff_brace = Brace(diff_span, direction=UP, buff=0.06)
        diff_brace.set_color(ORANGE)
        diff_label = self.safe_text(
            f"差：{difference}{unit_label}",
            font_size=15, color=ORANGE,
        )
        diff_label.next_to(diff_brace, UP, buff=0.04)
        diff_block = VGroup(diff_brace, diff_label)

        sum_span = Line(
            np.array([large_right + 0.12, top_y + 0.14, 0]),
            np.array([large_right + 0.12, bot_y - 0.14, 0]),
        )
        sum_brace = Brace(sum_span, direction=RIGHT, buff=0.05)
        sum_brace.set_color(YELLOW)
        sum_label = self.safe_text(
            f"和：{total}{unit_label}",
            font_size=16, color=YELLOW,
        )
        sum_label.next_to(sum_brace, RIGHT, buff=0.08)
        sum_block = VGroup(sum_brace, sum_label)

        add_main = DashedLine(
            np.array([small_right, bot_y, 0]),
            np.array([large_right, bot_y, 0]),
            color=TEAL_D, stroke_width=line_stroke * 0.9, dash_length=0.10,
        )
        add_cap = Line(
            np.array([large_right, bot_y + tick_h, 0]),
            np.array([large_right, bot_y - tick_h, 0]),
            color=TEAL_D, stroke_width=line_stroke * 0.75,
        )
        add_seg = VGroup(add_main, add_cap)
        add_note = self.safe_text(f"{difference}{unit_label}", font_size=14, color=TEAL_D)
        add_note.next_to(add_main, DOWN, buff=0.06)
        add_block = VGroup(add_seg, add_note)

        m1_sum_label = self.safe_text(
            f"和：({total}+{difference}){unit_label}",
            font_size=15, color=YELLOW,
        )
        m1_sum_label.next_to(sum_brace, RIGHT, buff=0.08)

        rem_span = Line(
            np.array([small_right + 0.12, top_y + 0.14, 0]),
            np.array([small_right + 0.12, bot_y - 0.14, 0]),
        )
        rem_sum_brace = Brace(rem_span, direction=RIGHT, buff=0.05)
        rem_sum_brace.set_color(YELLOW)
        rem_sum_label = self.safe_text(
            f"和：({total}−{difference}){unit_label}",
            font_size=15, color=YELLOW,
        )
        rem_sum_label.next_to(rem_sum_brace, RIGHT, buff=0.08)
        rem_sum_block = VGroup(rem_sum_brace, rem_sum_label)

        rem_extra_note = self.safe_text(
            f"{difference}{unit_label}",
            font_size=14, color=PURPLE_A,
        )
        rem_extra_note.move_to(np.array([
            (small_right + large_right) / 2,
            (top_y + bot_y) / 2,
            0,
        ]))

        tag_text = method_tag or "方法"
        m1_tag = self.safe_text("方法一：补差", font_size=16, color=ORANGE)
        m2_tag = self.safe_text("方法二：去差", font_size=16, color=TEAL_D)
        # 标签放在左上，不压差括号
        m1_tag.next_to(large_name_m, UP, buff=0.20)
        m1_tag.align_to(large_name_m, LEFT)
        m2_tag.move_to(m1_tag.get_center())
        if method_tag:
            # 外部只展示一个方法标签时覆盖文案
            pass

        equal_note = self.safe_text("此时两量相等", font_size=14, color=ORANGE)
        equal_note.next_to(small_line, DOWN, buff=0.28)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "补差→两份较大数；去差→两份较小数",
                font_size=15, color=GREY_B,
            )

        core = VGroup(align, large_block, small_block)
        method1_bits = VGroup(add_block, m1_sum_label, m1_tag)
        method2_bits = VGroup(
            large_extra_dashed, rem_sum_block, rem_extra_note, m2_tag,
        )
        annotated = VGroup(
            core, diff_block, sum_block,
            method1_bits, method2_bits, equal_note,
        )
        layout_row = VGroup(annotated)
        if show_hint:
            hint.next_to(annotated, DOWN, buff=0.14)
            layout_row = VGroup(annotated, hint)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        if scale != 1.0:
            diagram.scale(scale)
        diagram.move_to(np.array([0.15, draw_y, 0]))
        self.clamp_content(diagram)

        panel_base = VGroup(
            align, large_name_m, large_base, large_extra_solid,
            small_block, diff_block, sum_block,
        )
        panel_m1 = VGroup(
            align, large_name_m, large_base, large_extra_solid,
            small_block, diff_block, sum_brace, m1_sum_label,
            add_block, m1_tag, equal_note,
        )
        panel_m2 = VGroup(
            align, large_name_m, large_base, large_extra_dashed,
            small_block, diff_block, rem_sum_block,
            rem_extra_note, m2_tag, equal_note,
        )

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "annotated": annotated,
            "panel_base": panel_base,
            "panel_m1": panel_m1,
            "panel_m2": panel_m2,
            "core": core,
            "align": align,
            "align_l": align_l,
            "align_mid": align_mid,
            "large_block": large_block,
            "large_line": large_line,
            "large_base": large_base,
            "large_extra_solid": large_extra_solid,
            "large_extra_dashed": large_extra_dashed,
            "large_name": large_name_m,
            "small_block": small_block,
            "small_line": small_line,
            "small_name": small_name_m,
            "diff_block": diff_block,
            "sum_block": sum_block,
            "sum_brace": sum_brace,
            "sum_label": sum_label,
            "add_block": add_block,
            "add_seg": add_seg,
            "add_note": add_note,
            "m1_sum_label": m1_sum_label,
            "m1_tag": m1_tag,
            "rem_sum_block": rem_sum_block,
            "rem_sum_brace": rem_sum_brace,
            "rem_sum_label": rem_sum_label,
            "rem_extra_note": rem_extra_note,
            "m2_tag": m2_tag,
            "equal_note": equal_note,
            "hint": hint,
            "total": total,
            "difference": difference,
            "large": large,
            "small": small,
            "unit_label": unit_label,
        }
