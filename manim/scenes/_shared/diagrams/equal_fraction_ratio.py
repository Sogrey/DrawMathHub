"""
比例问题（二）— 第48讲：等量分数 → 线段对齐 → 化成比。

男生均分 a 份取 b 份，女生均分 c 份取 d 份；竖虚线对齐相等段，推出甲:乙 = d/c : b/a。
"""

from __future__ import annotations

from math import gcd
from typing import Any

import numpy as np

from manim import *  # noqa: F403


def _simplify_ratio(p: int, q: int) -> tuple[int, int]:
    g = gcd(p, q)
    return p // g, q // g


class EqualFractionRatioDiagramMixin:
    """甲×b/a = 乙×d/c → 线段对齐化比。"""

    def make_equal_fraction_ratio_diagram(
        self,
        draw_y: float,
        *,
        boy_den: int = 4,
        boy_num: int = 3,
        girl_den: int = 6,
        girl_num: int = 5,
        total: int = 38,
        boy_name: str = "男生",
        girl_name: str = "女生",
        equal_w: float = 3.6,
        row_gap: float = 0.95,
        line_stroke: float = 4.0,
        tick_h: float = 0.12,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if not (0 < boy_num < boy_den and 0 < girl_num < girl_den):
            raise ValueError("分数须为真分数且分母为正")

        # 甲:乙 = (d/c):(b/a) = (d*a):(b*c)，再约分
        raw_boy = girl_num * boy_den   # 5*4=20
        raw_girl = boy_num * girl_den  # 3*6=18
        ratio_boy, ratio_girl = _simplify_ratio(raw_boy, raw_girl)  # 10:9
        parts_sum = ratio_boy + ratio_girl
        boy_val = total * ratio_boy // parts_sum
        girl_val = total * ratio_girl // parts_sum

        boy_unit = equal_w / boy_num
        girl_unit = equal_w / girl_num
        boy_w = boy_den * boy_unit
        girl_w = girl_den * girl_unit

        left_x = -max(boy_w, girl_w) / 2
        # 左端对齐，相等段右端同 x
        eq_x = left_x + equal_w
        boy_right = left_x + boy_w
        girl_right = left_x + girl_w
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        boy_color = TEAL_D
        girl_color = ORANGE
        eq_color = YELLOW

        def _ticks(n: int, unit: float, y: float, color) -> VGroup:
            g = VGroup()
            for i in range(n + 1):
                x = left_x + i * unit
                g.add(Line(
                    np.array([x, y + tick_h, 0]),
                    np.array([x, y - tick_h, 0]),
                    color=color, stroke_width=line_stroke * 0.85,
                ))
            return g

        # 男生线
        boy_line = Line(
            np.array([left_x, top_y, 0]),
            np.array([boy_right, top_y, 0]),
            color=boy_color, stroke_width=line_stroke,
        )
        boy_ticks = _ticks(boy_den, boy_unit, top_y, boy_color)
        # 相等段浅填
        boy_eq_bar = RoundedRectangle(
            width=equal_w, height=0.20, corner_radius=0.04,
            stroke_width=0,
        )
        boy_eq_bar.set_fill(eq_color, opacity=0.28)
        boy_eq_bar.move_to(np.array([left_x + equal_w / 2, top_y, 0]))
        boy_eq_bar.set_opacity(0)

        boy_lab = self.safe_text(f"{boy_name}人数", font_size=16, color=boy_color)
        boy_lab.next_to(np.array([left_x, top_y, 0]), LEFT, buff=0.18)

        boy_frac = self.safe_mathtex(
            rf"\dfrac{{{boy_num}}}{{{boy_den}}}",
            font_size=22, color=eq_color,
        )
        boy_frac.next_to(boy_eq_bar, UP, buff=0.10)
        boy_frac.set_opacity(0)

        # 女生线
        girl_line = Line(
            np.array([left_x, bot_y, 0]),
            np.array([girl_right, bot_y, 0]),
            color=girl_color, stroke_width=line_stroke,
        )
        girl_ticks = _ticks(girl_den, girl_unit, bot_y, girl_color)
        girl_eq_bar = RoundedRectangle(
            width=equal_w, height=0.20, corner_radius=0.04,
            stroke_width=0,
        )
        girl_eq_bar.set_fill(eq_color, opacity=0.28)
        girl_eq_bar.move_to(np.array([left_x + equal_w / 2, bot_y, 0]))
        girl_eq_bar.set_opacity(0)

        girl_lab = self.safe_text(f"{girl_name}人数", font_size=16, color=girl_color)
        girl_lab.next_to(np.array([left_x, bot_y, 0]), LEFT, buff=0.18)

        girl_frac = self.safe_mathtex(
            rf"\dfrac{{{girl_num}}}{{{girl_den}}}",
            font_size=22, color=eq_color,
        )
        girl_frac.next_to(girl_eq_bar, DOWN, buff=0.10)
        girl_frac.set_opacity(0)

        # 竖虚线：相等段右端
        dash_eq = DashedLine(
            np.array([eq_x, top_y + 0.45, 0]),
            np.array([eq_x, bot_y - 0.45, 0]),
            color=eq_color, stroke_width=2.2, dash_length=0.08,
        )
        dash_eq.set_opacity(0)
        eq_tag = self.safe_text("相等", font_size=14, color=eq_color)
        eq_tag.next_to(dash_eq, RIGHT, buff=0.10)
        eq_tag.set_opacity(0)

        boy_row = VGroup(boy_line, boy_ticks, boy_eq_bar, boy_lab, boy_frac)
        girl_row = VGroup(girl_line, girl_ticks, girl_eq_bar, girl_lab, girl_frac)

        # 底部推导
        note_eq = VGroup(
            self.safe_text(f"{boy_name}×", font_size=18, color=WHITE),
            self.safe_mathtex(rf"\dfrac{{{boy_num}}}{{{boy_den}}}", font_size=22, color=WHITE),
            self.safe_text("=", font_size=20, color=WHITE),
            self.safe_text(f"{girl_name}×", font_size=18, color=WHITE),
            self.safe_mathtex(rf"\dfrac{{{girl_num}}}{{{girl_den}}}", font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.08)

        note_ratio_q = VGroup(
            self.safe_text(f"{boy_name}:{girl_name}=", font_size=18, color=WHITE),
            self.safe_mathtex(
                rf"\dfrac{{{girl_num}}}{{{girl_den}}}:\dfrac{{{boy_num}}}{{{boy_den}}}",
                font_size=22, color=WHITE,
            ),
        ).arrange(RIGHT, buff=0.08)

        note_ratio_ans = self.safe_text(
            f"{boy_name}:{girl_name}={ratio_boy}:{ratio_girl}",
            font_size=20, color=YELLOW,
        )

        calc_boy = VGroup(
            self.safe_mathtex(
                rf"{total}\times\dfrac{{{ratio_boy}}}{{{ratio_boy}+{ratio_girl}}}={boy_val}",
                font_size=24, color=YELLOW,
            ),
            self.safe_text("（人）", font_size=18, color=YELLOW),
        ).arrange(RIGHT, buff=0.10)

        calc_girl = VGroup(
            self.safe_mathtex(
                rf"{total}\times\dfrac{{{ratio_girl}}}{{{ratio_boy}+{ratio_girl}}}={girl_val}",
                font_size=24, color=YELLOW,
            ),
            self.safe_text("（人）", font_size=18, color=YELLOW),
        ).arrange(RIGHT, buff=0.10)

        for m in (note_eq, note_ratio_q, note_ratio_ans, calc_boy, calc_girl):
            m.set_opacity(0)

        # 左列：等量化比；右列：求人数（两列节省纵向空间）
        notes_left = VGroup(note_eq, note_ratio_q, note_ratio_ans).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT,
        )
        notes_right = VGroup(calc_boy, calc_girl).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT,
        )
        notes = VGroup(notes_left, notes_right).arrange(
            RIGHT, buff=0.55, aligned_edge=UP,
        )
        notes.next_to(VGroup(boy_row, girl_row), DOWN, buff=0.28)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "等量齐观：把相等的两段对齐，再化成比",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.12)

        diagram = VGroup(
            boy_row, girl_row, dash_eq, eq_tag, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "boy_row": boy_row,
            "girl_row": girl_row,
            "boy_line": boy_line,
            "boy_ticks": boy_ticks,
            "boy_eq_bar": boy_eq_bar,
            "boy_lab": boy_lab,
            "boy_frac": boy_frac,
            "girl_line": girl_line,
            "girl_ticks": girl_ticks,
            "girl_eq_bar": girl_eq_bar,
            "girl_lab": girl_lab,
            "girl_frac": girl_frac,
            "dash_eq": dash_eq,
            "eq_tag": eq_tag,
            "notes": notes,
            "notes_left": notes_left,
            "notes_right": notes_right,
            "note_eq": note_eq,
            "note_ratio_q": note_ratio_q,
            "note_ratio_ans": note_ratio_ans,
            "calc_boy": calc_boy,
            "calc_girl": calc_girl,
            "hint": hint,
            "ratio_boy": ratio_boy,
            "ratio_girl": ratio_girl,
            "boy_val": boy_val,
            "girl_val": girl_val,
            "total": total,
            "boy_num": boy_num,
            "boy_den": boy_den,
            "girl_num": girl_num,
            "girl_den": girl_den,
            "answer": f"{boy_name}{boy_val}人，{girl_name}{girl_val}人",
        }
