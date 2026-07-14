"""
错中求解（减法看错数字）— 第14讲及同类题型。

以「被减数 − 减数 = 差」结构对照正确/错误数位；
未看错的数位用 □ 占位。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class WrongSubtractDiagramMixin:
    """错中求解：被减数/减数看错数字，倒推正确结果。"""

    PLACEHOLDER = "□"

    def _wrong_sub_cell(
        self,
        text: str,
        *,
        width: float = 0.62,
        height: float = 0.46,
        fill=TEAL_D,
        fill_opacity: float = 0.28,
        font_size: int = 26,
        color=WHITE,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.08,
            color=fill, stroke_width=2,
        )
        box.set_fill(fill, opacity=fill_opacity)
        label = Text(text, font_size=font_size, color=color, font=self.DEFAULT_FONT)
        label.move_to(box.get_center())
        return VGroup(box, label)

    def _wrong_sub_number(
        self,
        digits: list[str],
        highlight_idx: int,
        *,
        role: str = "minuend",
        wrong: bool = False,
        cell_w: float = 0.40,
        cell_h: float = 0.42,
        cell_buff: float = 0.05,
    ) -> tuple[VGroup, VGroup]:
        """多位数字：□ 表未看错数位，高亮看错/已知数位。"""
        if role == "minuend":
            known_fill = TEAL_D
        else:
            known_fill = PURPLE_A

        cells: list[VGroup] = []
        for i, digit in enumerate(digits):
            is_ph = digit == self.PLACEHOLDER
            is_hi = i == highlight_idx
            if is_ph:
                cell = self._wrong_sub_cell(
                    digit, width=cell_w, height=cell_h,
                    fill=GREY, fill_opacity=0.10, font_size=18, color=GREY_B,
                )
            elif is_hi and wrong:
                cell = self._wrong_sub_cell(
                    digit, width=cell_w, height=cell_h,
                    fill=RED, fill_opacity=0.24, font_size=22, color=WHITE,
                )
            elif is_hi:
                cell = self._wrong_sub_cell(
                    digit, width=cell_w, height=cell_h,
                    fill=known_fill, fill_opacity=0.30, font_size=22, color=WHITE,
                )
            else:
                cell = self._wrong_sub_cell(
                    digit, width=cell_w, height=cell_h,
                    fill=GREY, fill_opacity=0.10, font_size=22, color=WHITE,
                )
            cells.append(cell)

        group = VGroup(*cells).arrange(RIGHT, buff=cell_buff)
        return group, cells[highlight_idx]

    def _wrong_sub_col_header(
        self,
        title: str,
        subtitle: str,
        *,
        title_color=YELLOW,
        subtitle_color=GREY_B,
    ) -> VGroup:
        top = self.safe_text(title, font_size=18, color=title_color)
        sub = self.safe_text(subtitle, font_size=15, color=subtitle_color)
        return VGroup(top, sub).arrange(DOWN, buff=0.08)

    def make_wrong_subtract_diagram(
        self,
        draw_y: float,
        *,
        minuend_tens_correct: int,
        minuend_tens_wrong: int,
        subtrahend_units_correct: int,
        subtrahend_units_wrong: int,
        wrong_result: int,
        row_gap: float = 1.08,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        ph = self.PLACEHOLDER
        minuend_delta = (minuend_tens_wrong - minuend_tens_correct) * 10
        subtrahend_delta = subtrahend_units_correct - subtrahend_units_wrong
        correct_result = wrong_result - minuend_delta - subtrahend_delta

        top_y = row_gap / 2
        bot_y = -row_gap / 2
        header_y = top_y + 0.78

        x_minus = 1.18
        x_sub = 2.28
        x_equals = 3.05
        x_diff = 3.75

        hdr_minuend = self._wrong_sub_col_header(
            "被减数", "十位看错", subtitle_color=ORANGE,
        )
        hdr_minus = self.safe_text("−", font_size=28, color=WHITE)
        hdr_sub = self._wrong_sub_col_header(
            "减数", "个位看错", subtitle_color=BLUE_B,
        )
        hdr_equals = self.safe_text("=", font_size=28, color=WHITE)
        hdr_diff = self.safe_text("差", font_size=18, color=YELLOW)

        correct_tag = self.safe_text("正确", font_size=20, color=TEAL_D)
        wrong_tag = self.safe_text("错误", font_size=20, color=RED)

        c_minuend, c_min_hi = self._wrong_sub_number(
            [ph, str(minuend_tens_correct), ph],
            highlight_idx=1, role="minuend", wrong=False,
        )
        c_sub, c_sub_hi = self._wrong_sub_number(
            [ph, ph, str(subtrahend_units_correct)],
            highlight_idx=2, role="subtrahend", wrong=False,
        )
        c_minus = self.safe_text("−", font_size=32, color=WHITE)
        c_equals = self.safe_text("=", font_size=32, color=WHITE)
        c_diff = self._wrong_sub_cell("?", fill=GREY, fill_opacity=0.15, color=YELLOW)

        w_minuend, w_min_hi = self._wrong_sub_number(
            [ph, str(minuend_tens_wrong), ph],
            highlight_idx=1, role="minuend", wrong=True,
        )
        w_sub, w_sub_hi = self._wrong_sub_number(
            [ph, ph, str(subtrahend_units_wrong)],
            highlight_idx=2, role="subtrahend", wrong=True,
        )
        w_minus = self.safe_text("−", font_size=32, color=WHITE)
        w_equals = self.safe_text("=", font_size=32, color=WHITE)
        w_diff = self._wrong_sub_cell(str(wrong_result), fill=RED, fill_opacity=0.22)

        x_minuend = 0.0
        row_xs = [x_minuend, x_minus, x_sub, x_equals, x_diff]
        for mob, x in zip([c_minuend, c_minus, c_sub, c_equals, c_diff], row_xs):
            mob.move_to(np.array([x, top_y, 0]))
        for mob, x in zip([w_minuend, w_minus, w_sub, w_equals, w_diff], row_xs):
            mob.move_to(np.array([x, bot_y, 0]))

        headers = VGroup(hdr_minuend, hdr_minus, hdr_sub, hdr_equals, hdr_diff)
        hdr_minuend.move_to(np.array([x_minuend, header_y, 0]))
        hdr_minus.move_to(np.array([x_minus, header_y - 0.04, 0]))
        hdr_sub.move_to(np.array([x_sub, header_y, 0]))
        hdr_equals.move_to(np.array([x_equals, header_y - 0.04, 0]))
        hdr_diff.move_to(np.array([x_diff, header_y - 0.04, 0]))

        correct_tag.next_to(c_minuend, LEFT, buff=0.22)
        wrong_tag.next_to(w_minuend, LEFT, buff=0.22)

        correct_row = VGroup(correct_tag, c_minuend, c_minus, c_sub, c_equals, c_diff)
        wrong_row = VGroup(wrong_tag, w_minuend, w_minus, w_sub, w_equals, w_diff)

        arrow_minuend = Arrow(
            c_min_hi.get_bottom(), w_min_hi.get_top(),
            buff=0.10, stroke_width=2.5, color=ORANGE,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow_sub = Arrow(
            c_sub_hi.get_bottom(), w_sub_hi.get_top(),
            buff=0.10, stroke_width=2.5, color=BLUE_B,
            max_tip_length_to_length_ratio=0.18,
        )
        digit_arrows = VGroup(arrow_minuend, arrow_sub)

        delta_minuend = self.safe_text(f"+{minuend_delta}", font_size=16, color=ORANGE)
        delta_minuend.next_to(arrow_minuend, LEFT, buff=0.06)
        delta_sub = self.safe_text(f"−{subtrahend_delta}", font_size=16, color=BLUE_B)
        delta_sub.next_to(arrow_sub, LEFT, buff=0.06)
        digit_deltas = VGroup(delta_minuend, delta_sub)

        result_arrow = Arrow(
            c_diff.get_bottom(), w_diff.get_top(),
            buff=0.10, stroke_width=2.5, color=YELLOW,
            max_tip_length_to_length_ratio=0.15,
        )

        res_note1 = self.safe_text(f"差多了{minuend_delta}", font_size=14, color=ORANGE)
        res_note2 = self.safe_text(f"差多了{subtrahend_delta}", font_size=14, color=BLUE_B)
        res_notes = VGroup(res_note1, res_note2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        res_notes.next_to(w_diff, RIGHT, buff=0.22)

        fix_note = self.safe_text(
            f"倒推：{wrong_result}−{minuend_delta}−{subtrahend_delta}={correct_result}",
            font_size=17, color=TEAL_D,
        )

        table_core = VGroup(headers, correct_row, wrong_row)
        overlays = VGroup(digit_arrows, digit_deltas, result_arrow, res_notes)
        annotated_table = VGroup(table_core, overlays)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "□ 表示其他数位没看错的数字；标出看错位置再倒推",
                font_size=18, color=GREY_B,
            )

        core = VGroup(annotated_table)
        layout_row = VGroup(core)

        if show_hint:
            hint.next_to(annotated_table, DOWN, buff=0.22)
            layout_row = VGroup(core, hint)

        fix_note.next_to(layout_row, DOWN, buff=0.18)

        diagram = VGroup(layout_row, fix_note)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "core": core,
            "annotated_table": annotated_table,
            "table_core": table_core,
            "overlays": overlays,
            "hint": hint,
            "headers": headers,
            "correct_row": correct_row,
            "wrong_row": wrong_row,
            "digit_deltas": digit_deltas,
            "digit_arrows": digit_arrows,
            "result_arrow": result_arrow,
            "result_notes": res_notes,
            "fix_note": fix_note,
            "minuend_delta": minuend_delta,
            "subtrahend_delta": subtrahend_delta,
            "wrong_result": wrong_result,
            "correct_result": correct_result,
        }
