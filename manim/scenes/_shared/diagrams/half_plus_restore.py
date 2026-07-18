"""
还原问题（二）— 第26讲：一半多几 / 一半少几 线段图逆推。

线段从左到右：还剩 | 多几 | 一半 | 先减去的量；
视觉上「还剩+多几」与「一半」等长。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class HalfPlusRestoreDiagramMixin:
    """还原问题（二）：一半多几 / 一半少几 线段图。"""

    def make_half_plus_restore_diagram(
        self,
        draw_y: float,
        *,
        left_remain: int = 5,
        extra: int = 2,
        first_take: int = 4,
        unit_w: float = 0.32,
        line_stroke: float = 4.0,
        tick_h: float = 0.12,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "颗",
    ) -> dict[str, Any]:
        if left_remain <= 0 or first_take < 0:
            raise ValueError("还剩与先减去的量须合法")
        # extra 可为负（一半少几）；绝对值参与长度
        more = abs(extra)
        half = left_remain + more
        after_take = half * 2
        original = after_take + first_take

        # 段长：还剩 | 多几 | 一半 | 先减
        lens = [left_remain, more, half, first_take]
        widths = [u * unit_w for u in lens]
        total_w = sum(widths)
        left_x = -total_w / 2
        xs = [left_x]
        for w in widths:
            xs.append(xs[-1] + w)

        y = 0.0
        main = Line(
            np.array([xs[0], y, 0]),
            np.array([xs[-1], y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        ticks = VGroup()
        for x in xs:
            ticks.add(Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.85,
            ))

        colors = [TEAL_D, ORANGE, BLUE_C, PURPLE_B]
        bars = VGroup()
        for i, (w, color) in enumerate(zip(widths, colors)):
            if w <= 1e-6:
                bars.add(VGroup())
                continue
            bar = RoundedRectangle(
                width=w, height=0.22, corner_radius=0.04,
                color=color, stroke_width=0,
            )
            bar.set_fill(color, opacity=0.32)
            bar.move_to(np.array([(xs[i] + xs[i + 1]) / 2, y, 0]))
            bars.add(bar)

        def _brace_block(x0: float, x1: float, text: str, color, direction, buff: float):
            span = Line(
                np.array([x0, y + (tick_h + 0.02) * direction[1], 0]),
                np.array([x1, y + (tick_h + 0.02) * direction[1], 0]),
            )
            br = Brace(span, direction=direction, buff=buff)
            br.set_color(color)
            lab = self.safe_text(text, font_size=17, color=color)
            lab.next_to(br, direction, buff=0.06)
            return VGroup(br, lab), br, lab

        left_block, left_brace, left_lab = _brace_block(
            xs[0], xs[1], f"还剩 {left_remain} {unit_label}", TEAL_D, UP, 0.10,
        )
        extra_txt = (
            f"多 {more} {unit_label}" if extra >= 0 else f"少 {more} {unit_label}"
        )
        extra_block, extra_brace, extra_lab = _brace_block(
            xs[1], xs[2], extra_txt, ORANGE, DOWN, 0.10,
        )
        half_block, half_brace, half_lab = _brace_block(
            xs[2], xs[3], "剩下的一半", BLUE_C, UP, 0.10,
        )
        take_block, take_brace, take_lab = _brace_block(
            xs[3], xs[4], f"{first_take} {unit_label}", PURPLE_B, UP, 0.10,
        )

        # 等长对照：还剩+多几 = 一半（下括号跨前两段）
        half_eq_span = Line(
            np.array([xs[0], y - tick_h - 0.02, 0]),
            np.array([xs[2], y - tick_h - 0.02, 0]),
        )
        half_eq_brace = Brace(half_eq_span, direction=DOWN, buff=0.55)
        half_eq_brace.set_color(YELLOW)
        half_eq_lab = self.safe_text(
            f"{left_remain}+{more}={half}（一半）",
            font_size=16, color=YELLOW,
        )
        half_eq_lab.next_to(half_eq_brace, DOWN, buff=0.06)
        half_eq_block = VGroup(half_eq_brace, half_eq_lab)
        half_eq_block.set_opacity(0)

        note_double = self.safe_text(
            f"一半×2 → 吃前剩 {after_take} {unit_label}",
            font_size=16, color=ORANGE,
        )
        note_double.next_to(half_eq_lab, DOWN, buff=0.16)
        note_double.set_opacity(0)

        note_origin = self.safe_text(
            f"再加上先吃的 {first_take} → 原来 {original} {unit_label}",
            font_size=16, color=YELLOW,
        )
        note_origin.next_to(note_double, DOWN, buff=0.12)
        note_origin.set_opacity(0)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "一半多几：先求出一半，再×2 还原",
                font_size=16, color=GREY_B,
            )

        line_core = VGroup(main, ticks, bars)
        annotated = VGroup(
            line_core,
            left_block, extra_block, half_block, take_block,
            half_eq_block, note_double, note_origin,
        )
        layout_row = VGroup(annotated)
        if show_hint:
            hint.next_to(annotated, DOWN, buff=0.18)
            layout_row = VGroup(annotated, hint)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "line_core": line_core,
            "main": main,
            "ticks": ticks,
            "bars": bars,
            "left_block": left_block,
            "extra_block": extra_block,
            "half_block": half_block,
            "take_block": take_block,
            "half_eq_block": half_eq_block,
            "note_double": note_double,
            "note_origin": note_origin,
            "hint": hint,
            "left_remain": left_remain,
            "extra": extra,
            "more": more,
            "half": half,
            "first_take": first_take,
            "after_take": after_take,
            "original": original,
            "unit_label": unit_label,
        }
