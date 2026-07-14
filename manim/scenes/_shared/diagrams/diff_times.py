"""
差倍问题线段图 — 第17讲及同类题型。

上行 1 倍量、下行多倍量，多出的部分标「差」。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class DiffTimesDiagramMixin:
    """差倍问题：1 倍 + n 倍，多出的（n-1）倍标差。"""

    def _diff_hline(
        self,
        left_x: float,
        right_x: float,
        y: float,
        *,
        stroke_width: float = 4.0,
        tick_h: float = 0.12,
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

    def _diff_vtick(self, x: float, y: float, *, tick_h: float = 0.12, color=GREY_B) -> Line:
        return Line(
            np.array([x, y + tick_h, 0]),
            np.array([x, y - tick_h, 0]),
            color=color, stroke_width=1.8,
        )

    def make_diff_times_diagram(
        self,
        draw_y: float,
        *,
        difference: int = 24,
        multiple: int = 3,
        top_name: str = "鸡",
        bottom_name: str = "鸭",
        unit_w: float = 0.78,
        row_gap: float = 1.20,
        line_stroke: float = 4.0,
        tick_h: float = 0.12,
        show_hint: bool = True,
        hint_text: str = "",
        x_shift: float = 0.40,
        unit_label: str = "只",
    ) -> dict[str, Any]:
        if multiple < 2:
            raise ValueError("差倍问题 multiple 必须 ≥ 2")

        diff_parts = multiple - 1
        unit_value = difference // diff_parts
        bottom_value = unit_value * multiple

        left_x = 0.0
        top_right = left_x + unit_w
        bot_right = left_x + multiple * unit_w
        diff_left = top_right
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        align_l = DashedLine(
            np.array([left_x, top_y + 0.35, 0]),
            np.array([left_x, bot_y - 0.35, 0]),
            color=GREY_B, stroke_width=1.5, dash_length=0.08,
        )
        # 1 倍右端对齐虚线，便于看出「多出的」从这里开始
        align_mid = DashedLine(
            np.array([top_right, top_y + 0.20, 0]),
            np.array([top_right, bot_y - 0.20, 0]),
            color=GREY_B, stroke_width=1.5, dash_length=0.08,
        )
        align = VGroup(align_l, align_mid)

        top_line = self._diff_hline(
            left_x, top_right, top_y,
            stroke_width=line_stroke, tick_h=tick_h, color=TEAL_D,
        )
        top_name_m = self.safe_text(top_name, font_size=20, color=WHITE)
        top_name_m.next_to(top_line, LEFT, buff=0.22)

        top_span = Line(
            np.array([left_x, top_y + tick_h + 0.02, 0]),
            np.array([top_right, top_y + tick_h + 0.02, 0]),
        )
        top_brace = Brace(top_span, direction=UP, buff=0.08)
        top_brace.set_color(TEAL_D)
        top_mult = self.safe_text("1 倍", font_size=16, color=TEAL_D)
        top_mult.next_to(top_brace, UP, buff=0.05)
        top_block = VGroup(top_name_m, top_line, top_brace, top_mult)

        bot_line = self._diff_hline(
            left_x, bot_right, bot_y,
            stroke_width=line_stroke, tick_h=tick_h, color=PURPLE_A,
        )
        bot_ticks = VGroup()
        for i in range(1, multiple):
            bot_ticks.add(self._diff_vtick(left_x + i * unit_w, bot_y, tick_h=tick_h))
        bot_name_m = self.safe_text(bottom_name, font_size=20, color=WHITE)
        bot_name_m.next_to(bot_line, LEFT, buff=0.22)

        bot_span = Line(
            np.array([left_x, bot_y - tick_h - 0.02, 0]),
            np.array([bot_right, bot_y - tick_h - 0.02, 0]),
        )
        bot_brace = Brace(bot_span, direction=DOWN, buff=0.08)
        bot_brace.set_color(PURPLE_A)
        bot_mult = self.safe_text(f"{multiple} 倍", font_size=16, color=PURPLE_A)
        bot_mult.next_to(bot_brace, DOWN, buff=0.05)
        bot_block = VGroup(bot_name_m, bot_line, bot_ticks, bot_brace, bot_mult)

        # 「差」：下行多出的 (倍数-1) 段
        diff_span = Line(
            np.array([diff_left, bot_y + tick_h + 0.08, 0]),
            np.array([bot_right, bot_y + tick_h + 0.08, 0]),
        )
        diff_brace = Brace(diff_span, direction=UP, buff=0.08)
        diff_brace.set_color(YELLOW)
        diff_label = self.safe_text(
            f"{difference} {unit_label}",
            font_size=18, color=YELLOW,
        )
        diff_label.next_to(diff_brace, UP, buff=0.06)
        diff_block = VGroup(diff_brace, diff_label)

        parts_note = self.safe_text(
            f"差相当于 {diff_parts} 个「1 倍」",
            font_size=16, color=ORANGE,
        )
        parts_note.next_to(bot_mult, DOWN, buff=0.22)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                hint_text or "把较小数当作 1 倍，差 =（倍数−1）个 1 倍量",
                font_size=17, color=GREY_B,
            )

        core = VGroup(align, top_block, bot_block)
        annotated = VGroup(core, diff_block, parts_note)
        layout_row = VGroup(annotated)
        if show_hint:
            hint.next_to(annotated, DOWN, buff=0.20)
            layout_row = VGroup(annotated, hint)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "annotated": annotated,
            "core": core,
            "align": align,
            "align_l": align_l,
            "align_mid": align_mid,
            "top_block": top_block,
            "top_line": top_line,
            "top_brace": top_brace,
            "top_mult": top_mult,
            "top_name": top_name_m,
            "bot_block": bot_block,
            "bot_line": bot_line,
            "bot_ticks": bot_ticks,
            "bot_brace": bot_brace,
            "bot_mult": bot_mult,
            "bot_name": bot_name_m,
            "diff_block": diff_block,
            "diff_brace": diff_brace,
            "diff_label": diff_label,
            "parts_note": parts_note,
            "hint": hint,
            "difference": difference,
            "multiple": multiple,
            "diff_parts": diff_parts,
            "unit_value": unit_value,
            "bottom_value": bottom_value,
            "unit_label": unit_label,
        }
