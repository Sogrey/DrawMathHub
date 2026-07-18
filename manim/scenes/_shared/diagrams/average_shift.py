"""
平均数问题（二）— 第38讲：移多补少法。

已知若干人分数，新人比全员平均分多出定值；把多出部分均摊给原有人，求全员平均与新人分数。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class AverageShiftDiagramMixin:
    """垂直柱状移多补少：四人基准 + 均摊补齐 + 新人多出段。"""

    def make_average_shift_diagram(
        self,
        draw_y: float,
        *,
        scores: list[float] | None = None,
        names: list[str] | None = None,
        new_name: str = "小艺",
        extra: float = 0.8,
        bar_w: float = 0.55,
        gap: float = 0.28,
        unit_h: float = 1.15,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "分",
    ) -> dict[str, Any]:
        if scores is None:
            scores = [8.5, 9.0, 8.6, 8.7]
        if names is None:
            names = ["甲", "乙", "丙", "丁"]
        n = len(scores)
        if len(names) != n:
            raise ValueError("姓名与分数个数须一致")

        four_sum = sum(scores)
        four_avg = four_sum / n
        share = extra / n
        five_avg = four_avg + share
        new_score = five_avg + extra

        # 柱高：以 four_avg 为蓝柱高度基准，橙尖 = share，新人蓝=五人平均，虚线橙=extra
        # 视觉比例：用 (value - offset) 拉长差异
        base_ref = four_avg - 0.6  # 截掉公共底座，突出平均上方差

        def h_of(v: float) -> float:
            return max(0.35, (v - base_ref) * unit_h)

        h4 = h_of(four_avg)
        h5 = h_of(five_avg)
        h_new = h_of(new_score)
        tip_h = h5 - h4
        extra_h = h_new - h5

        total_bars = n + 1
        total_w = total_bars * bar_w + (total_bars - 1) * gap
        left_x = -total_w / 2
        y0 = -1.15

        bars_four = VGroup()
        tips_four = VGroup()
        name_labs = VGroup()
        four_blues = VGroup()

        for i in range(n):
            x = left_x + i * (bar_w + gap) + bar_w / 2
            blue = Rectangle(
                width=bar_w, height=h4,
                stroke_width=2.0, stroke_color=TEAL_D,
                fill_color=TEAL_D, fill_opacity=0.55,
            )
            blue.move_to(np.array([x, y0 + h4 / 2, 0]))
            tip = Rectangle(
                width=bar_w, height=tip_h,
                stroke_width=1.5, stroke_color=ORANGE,
                fill_color=ORANGE, fill_opacity=0.85,
            )
            tip.move_to(np.array([x, y0 + h4 + tip_h / 2, 0]))
            tip.set_opacity(0)
            lab = self.safe_text(names[i], font_size=16, color=GREY_B)
            lab.next_to(blue, DOWN, buff=0.12)
            four_blues.add(blue)
            tips_four.add(tip)
            bars_four.add(VGroup(blue, tip))
            name_labs.add(lab)

        # 小艺
        x_new = left_x + n * (bar_w + gap) + bar_w / 2
        new_blue = Rectangle(
            width=bar_w, height=h5,
            stroke_width=2.0, stroke_color=TEAL_D,
            fill_color=TEAL_D, fill_opacity=0.55,
        )
        new_blue.move_to(np.array([x_new, y0 + h5 / 2, 0]))
        new_extra = DashedVMobject(
            Rectangle(
                width=bar_w, height=extra_h,
                stroke_width=2.0, stroke_color=ORANGE,
                fill_opacity=0,
            ),
            num_dashes=14,
        )
        # 用实心淡橙 + 虚线边更清晰
        new_extra_fill = Rectangle(
            width=bar_w, height=extra_h,
            stroke_width=0,
            fill_color=ORANGE, fill_opacity=0.25,
        )
        new_extra_fill.move_to(np.array([x_new, y0 + h5 + extra_h / 2, 0]))
        new_extra.move_to(new_extra_fill.get_center())
        new_extra_g = VGroup(new_extra_fill, new_extra)
        new_extra_g.set_opacity(0)

        new_lab = self.safe_text(new_name, font_size=16, color=GREY_B)
        new_lab.next_to(new_blue, DOWN, buff=0.12)
        name_labs.add(new_lab)

        # 参考线
        x_left = left_x - 0.15
        x_right = x_new + bar_w / 2 + 0.35
        line4 = DashedLine(
            np.array([x_left, y0 + h4, 0]),
            np.array([x_right, y0 + h4, 0]),
            color=GREY_B, stroke_width=1.5, dash_length=0.08,
        )
        lab4 = self.safe_text("四人平均分", font_size=13, color=GREY_B)
        lab4.next_to(line4, LEFT, buff=0.08)

        line5 = DashedLine(
            np.array([x_left, y0 + h5, 0]),
            np.array([x_right, y0 + h5, 0]),
            color=YELLOW, stroke_width=1.6, dash_length=0.08,
        )
        lab5 = self.safe_text("五人平均分", font_size=13, color=YELLOW)
        lab5.next_to(line5, LEFT, buff=0.08)
        line5.set_opacity(0)
        lab5.set_opacity(0)

        # 0.8 标注（小艺多出段）
        extra_brace = Brace(new_extra_fill, direction=RIGHT, buff=0.08)
        extra_brace.set_color(ORANGE)
        extra_lab = self.safe_text(f"{extra} {unit_label}", font_size=14, color=ORANGE)
        extra_lab.next_to(extra_brace, RIGHT, buff=0.06)
        extra_anno = VGroup(extra_brace, extra_lab)
        extra_anno.set_opacity(0)

        # 均摊箭头示意（从小艺多出指向四人橙尖）
        arrows = VGroup()
        for tip in tips_four:
            arr = Arrow(
                new_extra_fill.get_left() + LEFT * 0.05,
                tip.get_top() + UP * 0.02,
                buff=0.06,
                stroke_width=2.0,
                color=ORANGE,
                max_tip_length_to_length_ratio=0.18,
                tip_length=0.12,
            )
            arr.set_opacity(0)
            arrows.add(arr)

        # 批注
        note_four = self.safe_text(
            f"四人平均：({'+'.join(str(s) for s in scores)})÷{n}={four_avg:g}",
            font_size=14, color=GREY_B,
        )
        note_five_q = self.safe_text(
            f"五人平均：{four_avg:g}+({extra}÷{n})=?",
            font_size=15, color=YELLOW,
        )
        note_five_ans = self.safe_text(
            f"五人平均：{four_avg:g}+{share:g}={five_avg:g}（{unit_label}）",
            font_size=15, color=YELLOW,
        )
        note_new = self.safe_text(
            f"{new_name}：{five_avg:g}+{extra}={new_score:g}（{unit_label}）",
            font_size=15, color=ORANGE,
        )
        for m in (note_four, note_five_q, note_five_ans, note_new):
            m.set_opacity(0)

        notes = VGroup(note_four, note_five_q, note_five_ans, note_new)
        chart = VGroup(
            four_blues, tips_four, new_blue, new_extra_g,
            name_labs, line4, lab4, line5, lab5, extra_anno, arrows,
        )
        note_four.next_to(chart, DOWN, buff=0.32)
        note_five_q.next_to(note_four, DOWN, buff=0.10)
        note_five_ans.move_to(note_five_q)
        note_new.next_to(note_five_ans, DOWN, buff=0.10)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "把多出的分数均摊给其他人，求出五人平均分",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.12)

        diagram = VGroup(chart, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "chart": chart,
            "four_blues": four_blues,
            "tips_four": tips_four,
            "new_blue": new_blue,
            "new_extra": new_extra_g,
            "name_labs": name_labs,
            "line4": VGroup(line4, lab4),
            "line5": VGroup(line5, lab5),
            "extra_anno": extra_anno,
            "arrows": arrows,
            "notes": notes,
            "note_four": note_four,
            "note_five_q": note_five_q,
            "note_five_ans": note_five_ans,
            "note_new": note_new,
            "hint": hint,
            "scores": scores,
            "four_avg": four_avg,
            "share": share,
            "five_avg": five_avg,
            "new_score": new_score,
            "extra": extra,
            "new_name": new_name,
            "n": n,
            "unit_label": unit_label,
        }
