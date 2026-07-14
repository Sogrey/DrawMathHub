"""
倍数问题线段图 — 第13讲及同类题型。

上行 1 倍量，下行多倍量；支持「几倍少几 / 几倍多几」。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class MultipleTimesDiagramMixin:
    """倍数问题：双行线段图（1 倍量 + 多倍量）。"""

    def _hline_with_caps(
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

    def _v_tick(self, x: float, y: float, *, tick_h: float = 0.12, color=GREY_B) -> Line:
        return Line(
            np.array([x, y + tick_h, 0]),
            np.array([x, y - tick_h, 0]),
            color=color, stroke_width=1.8,
        )

    def make_multiple_times_diagram(
        self,
        unit_value: int,
        multiple: int,
        draw_y: float,
        *,
        less_by: int = 0,
        more_by: int = 0,
        top_name: str = "苹果",
        bottom_name: str = "梨",
        unit_w: float = 0.46,
        row_gap: float = 1.22,
        line_stroke: float = 4.0,
        tick_h: float = 0.12,
        brace_label_buff: float = 0.08,
        show_hint: bool = True,
        x_shift: float = 0.75,
    ) -> dict[str, Any]:
        if multiple < 1:
            raise ValueError("multiple 必须 ≥ 1")
        if less_by > 0 and more_by > 0:
            raise ValueError("less_by 与 more_by 不能同时大于 0")

        full_width = multiple * unit_w
        left_x = -full_width / 2
        right_x = left_x + full_width
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        apple_right = left_x + unit_w
        apple_line = self._hline_with_caps(
            left_x, apple_right, top_y,
            stroke_width=line_stroke, tick_h=tick_h,
        )

        apple_span = Line(
            np.array([left_x, top_y + tick_h + 0.02, 0]),
            np.array([apple_right, top_y + tick_h + 0.02, 0]),
        )
        apple_brace = Brace(apple_span, direction=UP, buff=brace_label_buff)
        apple_brace.set_color(TEAL_D)
        apple_mult_label = self.safe_text("1 倍", font_size=16, color=TEAL_D)
        apple_mult_label.next_to(apple_brace, UP, buff=0.05)

        apple_val_span = Line(
            np.array([left_x, top_y - tick_h - 0.04, 0]),
            np.array([apple_right, top_y - tick_h - 0.04, 0]),
        )
        apple_val_brace = Brace(apple_val_span, direction=DOWN, buff=brace_label_buff)
        apple_val_brace.set_color(YELLOW)
        apple_val_label = self.safe_text(f"{unit_value} 个", font_size=16, color=YELLOW)
        apple_val_label.next_to(apple_val_brace, DOWN, buff=0.05)

        apple_name = self.safe_text(top_name, font_size=20, color=WHITE)
        apple_name.next_to(apple_line, LEFT, buff=0.22)

        apple_block = VGroup(
            apple_name, apple_line, apple_brace, apple_mult_label,
            apple_val_brace, apple_val_label,
        )

        # 下行多倍量
        if less_by > 0:
            missing_w = (less_by / unit_value) * unit_w
            solid_right = right_x - missing_w
        elif more_by > 0:
            missing_w = 0.0
            solid_right = right_x + (more_by / unit_value) * unit_w
        else:
            missing_w = 0.0
            solid_right = right_x

        pear_solid = self._hline_with_caps(
            left_x, solid_right, bot_y,
            stroke_width=line_stroke, tick_h=tick_h, color=WHITE,
        )

        pear_ticks = VGroup(*[
            self._v_tick(left_x + i * unit_w, bot_y, tick_h=tick_h)
            for i in range(1, multiple)
        ])

        pear_dashed: DashedLine | None = None
        less_block = VGroup()
        if less_by > 0:
            pear_dashed = DashedLine(
                np.array([solid_right, bot_y, 0]),
                np.array([right_x, bot_y, 0]),
                color=RED, stroke_width=line_stroke * 0.75, dash_length=0.08,
            )
            less_span = Line(
                np.array([solid_right, bot_y - tick_h - 0.32, 0]),
                np.array([right_x, bot_y - tick_h - 0.32, 0]),
            )
            less_brace = Brace(less_span, direction=DOWN, buff=0.05)
            less_brace.set_color(RED)
            less_label = self.safe_text(f"少 {less_by} 个", font_size=15, color=RED)
            less_label.next_to(less_brace, DOWN, buff=0.04)
            less_block = VGroup(less_brace, less_label)

        pear_mult_span = Line(
            np.array([left_x, bot_y + tick_h + 0.02, 0]),
            np.array([right_x, bot_y + tick_h + 0.02, 0]),
        )
        pear_mult_brace = Brace(pear_mult_span, direction=UP, buff=brace_label_buff)
        pear_mult_brace.set_color(PURPLE_A)
        pear_mult_label = self.safe_text(f"{multiple} 倍", font_size=16, color=PURPLE_A)
        pear_mult_label.next_to(pear_mult_brace, UP, buff=0.05)

        bottom_qty = multiple * unit_value - less_by + more_by
        qty_span = Line(
            np.array([left_x, bot_y - tick_h - 0.04, 0]),
            np.array([solid_right, bot_y - tick_h - 0.04, 0]),
        )
        qty_brace = Brace(qty_span, direction=DOWN, buff=brace_label_buff)
        qty_brace.set_color(TEAL_D)
        if less_by > 0:
            qty_text = f"（{multiple}×{unit_value}−{less_by}）个"
        elif more_by > 0:
            qty_text = f"（{multiple}×{unit_value}+{more_by}）个"
        else:
            qty_text = f"（{multiple}×{unit_value}）个"
        qty_label = self.safe_text(qty_text, font_size=15, color=TEAL_D)
        qty_label.next_to(qty_brace, DOWN, buff=0.04)
        qty_block = VGroup(qty_brace, qty_label)

        pear_name = self.safe_text(bottom_name, font_size=20, color=WHITE)
        pear_name.next_to(pear_solid, LEFT, buff=0.22)

        pear_block = VGroup(
            pear_name, pear_solid, pear_ticks,
            pear_mult_brace, pear_mult_label,
        )

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "上面 1 倍量，下面多倍量，对齐比较",
                font_size=18, color=GREY_B,
            )

        core = VGroup(apple_block, pear_block)
        if len(less_block) > 0:
            core.add(less_block)
        if pear_dashed is not None:
            core.add(pear_dashed)

        layout_row = VGroup(core, qty_block)

        if show_hint:
            hint.next_to(layout_row, DOWN, buff=0.18)
            diagram = VGroup(layout_row, hint)
        else:
            diagram = VGroup(layout_row)

        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "core": core,
            "hint": hint,
            "apple_block": apple_block,
            "apple_line": apple_line,
            "apple_labels": VGroup(apple_brace, apple_mult_label, apple_val_brace, apple_val_label),
            "pear_block": pear_block,
            "pear_solid": pear_solid,
            "pear_ticks": pear_ticks,
            "pear_dashed": pear_dashed if pear_dashed is not None else VGroup(),
            "pear_mult_labels": VGroup(pear_mult_brace, pear_mult_label),
            "less_block": less_block,
            "qty_block": VGroup(qty_brace, qty_label),
            "unit_value": unit_value,
            "multiple": multiple,
            "less_by": less_by,
            "more_by": more_by,
            "bottom_qty": bottom_qty,
            "total_qty": bottom_qty + unit_value,
        }
