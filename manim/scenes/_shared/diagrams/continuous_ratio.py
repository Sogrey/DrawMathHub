"""
比例问题（一）— 第47讲：两组比 → 找中间项 LCM → 连比 → 求部分量。

三列人名；上行 红:新，下行 新:明；对齐中间「新」的份数后得到 9:12:10。
"""

from __future__ import annotations

from math import gcd
from typing import Any

import numpy as np

from manim import *  # noqa: F403


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


class ContinuousRatioDiagramMixin:
    """两组比化连比：对齐公共项份数。"""

    def make_continuous_ratio_diagram(
        self,
        draw_y: float,
        *,
        names: list[str] | None = None,
        ratio_ab: tuple[int, int] = (3, 4),
        ratio_bc: tuple[int, int] = (6, 5),
        total: int = 62,
        ask_index: int = 2,
        col_w: float = 1.7,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if names is None:
            names = ["小红", "小新", "小明"]
        if len(names) != 3:
            raise ValueError("本讲示例为三人连比")
        a, b1 = ratio_ab
        b2, c = ratio_bc
        if a <= 0 or b1 <= 0 or b2 <= 0 or c <= 0:
            raise ValueError("比的各项须为正")

        mid_lcm = _lcm(b1, b2)
        mul1 = mid_lcm // b1
        mul2 = mid_lcm // b2
        linked = (a * mul1, mid_lcm, c * mul2)
        parts_sum = sum(linked)
        ask_parts = linked[ask_index]
        ask_val = total * ask_parts // parts_sum

        colors = [TEAL_D, ORANGE, BLUE]
        col_xs = [(-1) * col_w, 0.0, col_w]

        def _num(n: int, color, font_size: int = 26) -> Any:
            return self.safe_text(str(n), font_size=font_size, color=color)

        def _colon(font_size: int = 26) -> Any:
            return self.safe_text("∶", font_size=font_size, color=GREY_B)

        # 表头
        headers = VGroup()
        for i, n in enumerate(names):
            h = self.safe_text(n, font_size=22, color=colors[i])
            h.move_to(np.array([col_xs[i], 1.25, 0]))
            headers.add(h)

        # 上行 红∶新
        r1_a = _num(a, colors[0])
        r1_col = _colon()
        r1_b = _num(b1, colors[1])
        r1_a.move_to(np.array([col_xs[0], 0.65, 0]))
        r1_b.move_to(np.array([col_xs[1], 0.65, 0]))
        r1_col.move_to(np.array([(col_xs[0] + col_xs[1]) / 2, 0.65, 0]))
        row1 = VGroup(r1_a, r1_col, r1_b)

        # 下行 新∶明
        r2_b = _num(b2, colors[1])
        r2_col = _colon()
        r2_c = _num(c, colors[2])
        r2_b.move_to(np.array([col_xs[1], 0.15, 0]))
        r2_c.move_to(np.array([col_xs[2], 0.15, 0]))
        r2_col.move_to(np.array([(col_xs[1] + col_xs[2]) / 2, 0.15, 0]))
        row2 = VGroup(r2_b, r2_col, r2_c)

        mid_box = SurroundingRectangle(
            VGroup(r1_b, r2_b),
            buff=0.14, color=YELLOW, stroke_width=2.5, corner_radius=0.08,
        )
        mid_box.set_fill(opacity=0)
        mid_box.set_stroke(opacity=0)

        sep = Line(
            np.array([col_xs[0] - 0.55, -0.25, 0]),
            np.array([col_xs[2] + 0.55, -0.25, 0]),
            stroke_width=1.8, color=GREY_B, stroke_opacity=0.55,
        )
        sep.set_opacity(0)

        # 连比
        link_nums = VGroup()
        for i in range(3):
            n = _num(linked[i], colors[i], font_size=28)
            n.move_to(np.array([col_xs[i], -0.70, 0]))
            n.set_opacity(0)
            link_nums.add(n)
        link_col1 = _colon(28)
        link_col2 = _colon(28)
        link_col1.move_to(np.array([(col_xs[0] + col_xs[1]) / 2, -0.70, 0]))
        link_col2.move_to(np.array([(col_xs[1] + col_xs[2]) / 2, -0.70, 0]))
        link_col1.set_opacity(0)
        link_col2.set_opacity(0)
        link_label = self.safe_text("连比", font_size=16, color=GREY_B)
        link_label.next_to(link_nums, LEFT, buff=0.35)
        link_label.set_opacity(0)
        link_row = VGroup(link_label, *link_nums, link_col1, link_col2)

        # 底部说明（垂直排列，场景分步显现）
        lcm_note = self.safe_text(
            f"{names[1]}：{b1} 与 {b2} 的最小公倍数是 {mid_lcm}",
            font_size=16, color=YELLOW,
        )
        scale_note = self.safe_text(
            f"第一组×{mul1} → {a * mul1}∶{mid_lcm}；"
            f"第二组×{mul2} → {mid_lcm}∶{c * mul2}",
            font_size=15, color=WHITE,
        )
        calc_q = self.safe_mathtex(
            rf"{total} \times \dfrac{{{ask_parts}}}{{{linked[0]}+{linked[1]}+{linked[2]}}} = ?",
            font_size=28, color=WHITE,
        )
        calc_ans_math = self.safe_mathtex(
            rf"{total} \times \dfrac{{{ask_parts}}}{{{linked[0]}+{linked[1]}+{linked[2]}}} = {ask_val}",
            font_size=28, color=YELLOW,
        )
        calc_ans_unit = self.safe_text("（枚）", font_size=22, color=YELLOW)
        calc_ans = VGroup(calc_ans_math, calc_ans_unit).arrange(RIGHT, buff=0.12)
        for m in (lcm_note, scale_note, calc_q, calc_ans):
            m.set_opacity(0)

        notes = VGroup(lcm_note, scale_note, calc_q).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT,
        )
        notes.next_to(link_row, DOWN, buff=0.32)
        calc_ans.move_to(calc_q.get_center())

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "公共项对齐份数 → 两组比化成连比",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.16)

        diagram = VGroup(
            headers, row1, row2, mid_box, sep, link_row, notes, calc_ans, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "headers": headers,
            "row1": row1,
            "row2": row2,
            "mid_box": mid_box,
            "sep": sep,
            "link_row": link_row,
            "link_nums": link_nums,
            "link_col1": link_col1,
            "link_col2": link_col2,
            "link_label": link_label,
            "notes": notes,
            "lcm_note": lcm_note,
            "scale_note": scale_note,
            "calc_q": calc_q,
            "calc_ans": calc_ans,
            "hint": hint,
            "names": names,
            "ratio_ab": ratio_ab,
            "ratio_bc": ratio_bc,
            "linked": linked,
            "mul1": mul1,
            "mul2": mul2,
            "mid_lcm": mid_lcm,
            "total": total,
            "ask_index": ask_index,
            "ask_parts": ask_parts,
            "ask_val": ask_val,
            "answer": f"{names[ask_index]}有{ask_val}枚邮票",
        }
