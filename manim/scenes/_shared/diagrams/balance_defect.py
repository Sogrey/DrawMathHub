"""
找次品问题 — 第42讲：天平法。

外观相同的物品中有一件偏轻；每次三等分，称其中两份，缩小范围。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class BalanceDefectDiagramMixin:
    """天平找次品（偏轻）：三等分两次称量示意。"""

    def _make_circle_num(self, n: int, *, r: float = 0.22, color=WHITE) -> VGroup:
        c = Circle(radius=r, color=color, stroke_width=2.0, fill_opacity=0)
        lab = self.safe_text(str(n), font_size=16, color=color)
        lab.move_to(c.get_center())
        return VGroup(c, lab)

    def _make_balance(
        self,
        *,
        left_ids: list[int],
        right_ids: list[int],
        tip: str = "balance",  # balance | left_light | right_light
        scale: float = 1.0,
    ) -> VGroup:
        """简易天平：横梁 + 左右托盘数字圈。"""
        beam_w = 2.6 * scale
        tilt = 0.0
        if tip == "left_light":
            tilt = 0.18
        elif tip == "right_light":
            tilt = -0.18

        pivot = Dot(radius=0.06 * scale, color=GREY_B)
        stand = Line(ORIGIN, DOWN * 0.55 * scale, color=GREY_B, stroke_width=3)
        stand.move_to(DOWN * 0.28 * scale)

        beam = Line(
            LEFT * beam_w / 2, RIGHT * beam_w / 2,
            color=WHITE, stroke_width=3.5,
        )
        beam.rotate(tilt)
        beam.move_to(ORIGIN)

        def pan(ids: list[int], side: float) -> VGroup:
            base = beam.get_center() + np.array([
                side * beam_w * 0.42 * np.cos(tilt),
                side * beam_w * 0.42 * np.sin(tilt) - 0.35 * scale,
                0,
            ])
            # 托盘横线
            pan_line = Line(
                LEFT * 0.55 * scale, RIGHT * 0.55 * scale,
                color=GREY_A, stroke_width=2.5,
            )
            pan_line.move_to(base)
            string = Line(
                beam.get_center() + np.array([
                    side * beam_w * 0.42 * np.cos(tilt),
                    side * beam_w * 0.42 * np.sin(tilt),
                    0,
                ]),
                base + UP * 0.08 * scale,
                color=GREY_B, stroke_width=1.5,
            )
            circles = VGroup(*[
                self._make_circle_num(i, r=0.18 * scale)
                for i in ids
            ]).arrange(RIGHT, buff=0.08)
            circles.next_to(pan_line, UP, buff=0.06)
            return VGroup(string, pan_line, circles)

        left = pan(left_ids, -1)
        right = pan(right_ids, 1)
        return VGroup(stand, pivot, beam, left, right)

    def make_balance_defect_diagram(
        self,
        draw_y: float,
        *,
        n: int = 9,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if n != 9:
            raise ValueError("本讲母题固定 9 盒")
        # 三组
        g1, g2, g3 = [1, 2, 3], [4, 5, 6], [7, 8, 9]

        # 九个编号总览
        all_circles = VGroup(*[
            self._make_circle_num(i) for i in range(1, 10)
        ]).arrange(RIGHT, buff=0.12)
        group_labels = VGroup(
            self.safe_text("①组", font_size=14, color=TEAL_D),
            self.safe_text("②组", font_size=14, color=ORANGE),
            self.safe_text("③组", font_size=14, color=YELLOW),
        )
        # 分组括号
        b1 = Brace(VGroup(*all_circles[0:3]), DOWN, buff=0.08)
        b1.set_color(TEAL_D)
        b2 = Brace(VGroup(*all_circles[3:6]), DOWN, buff=0.08)
        b2.set_color(ORANGE)
        b3 = Brace(VGroup(*all_circles[6:9]), DOWN, buff=0.08)
        b3.set_color(YELLOW)
        group_labels[0].next_to(b1, DOWN, buff=0.05)
        group_labels[1].next_to(b2, DOWN, buff=0.05)
        group_labels[2].next_to(b3, DOWN, buff=0.05)
        overview = VGroup(all_circles, b1, b2, b3, group_labels)

        # 第一次称：① vs ②（示意平衡，次品在③）
        bal1 = self._make_balance(left_ids=g1, right_ids=g2, tip="balance", scale=0.85)
        bal1_tag = self.safe_text("第1次：①组 vs ②组", font_size=14, color=GREY_B)
        bal1_tag.next_to(bal1, UP, buff=0.12)
        case1 = self.safe_text("平衡 → 次品在③组", font_size=14, color=YELLOW)
        case1.next_to(bal1, DOWN, buff=0.10)
        weigh1 = VGroup(bal1_tag, bal1, case1)

        # 第二次称：7 vs 8
        bal2 = self._make_balance(left_ids=[7], right_ids=[8], tip="balance", scale=0.75)
        bal2_tag = self.safe_text("第2次：7 vs 8", font_size=14, color=GREY_B)
        bal2_tag.next_to(bal2, UP, buff=0.10)
        case2 = self.safe_text("平衡 → 9 是次品（偏轻）", font_size=14, color=ORANGE)
        case2.next_to(bal2, DOWN, buff=0.08)
        weigh2 = VGroup(bal2_tag, bal2, case2)

        # 布局：总览在上，两次称量左右
        weigh1.set_opacity(0)
        weigh2.set_opacity(0)
        weigh_row = VGroup(weigh1, weigh2).arrange(RIGHT, buff=0.55)
        weigh_row.next_to(overview, DOWN, buff=0.45)

        note_ans = self.safe_text(
            "至少称 2 次能保证找出次品",
            font_size=16, color=YELLOW,
        )
        note_ans.set_opacity(0)
        note_ans.next_to(weigh_row, DOWN, buff=0.28)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "每次三等分，称其中两份，逐步缩小范围",
                font_size=14, color=GREY_B,
            )
            hint.next_to(note_ans, DOWN, buff=0.14)

        diagram = VGroup(overview, weigh_row, note_ans, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "overview": overview,
            "all_circles": all_circles,
            "group_braces": VGroup(b1, b2, b3, group_labels),
            "weigh1": weigh1,
            "weigh2": weigh2,
            "weigh_row": weigh_row,
            "note_ans": note_ans,
            "hint": hint,
            "n": n,
            "answer_times": 2,
        }
