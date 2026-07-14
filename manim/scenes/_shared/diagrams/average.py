"""
平均数问题 — 第15讲及同类：重叠区间求中间数。

五个圆圈 + 前三/后三上方括号 + 全体下方括号。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class AverageDiagramMixin:
    """平均数：已知总平均与部分平均，图示重叠求中间数。"""

    def make_middle_average_diagram(
        self,
        draw_y: float,
        *,
        count: int = 5,
        total_avg: float = 40,
        front_avg: float = 32,
        back_avg: float = 46,
        front_n: int = 3,
        back_n: int = 3,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        total_sum = int(total_avg * count)
        front_sum = int(front_avg * front_n)
        back_sum = int(back_avg * back_n)
        middle = front_sum + back_sum - total_sum
        mid_idx = count // 2  # 0-based，五个数时为 2 → ③

        circle_r = 0.34
        gap = 0.22
        step = 2 * circle_r + gap
        start_x = -((count - 1) * step) / 2

        circles: list[Circle] = []
        labels: list[Mobject] = []
        for i in range(count):
            c = Circle(
                radius=circle_r,
                color=WHITE,
                stroke_width=2.5,
            )
            c.move_to(np.array([start_x + i * step, 0.0, 0]))
            lab = self.safe_text(f"①②③④⑤⑥⑦⑧⑨⑩"[i], font_size=22, color=WHITE)
            lab.move_to(c.get_center())
            circles.append(c)
            labels.append(lab)

        circles_g = VGroup(*circles)
        labels_g = VGroup(*labels)
        row = VGroup(circles_g, labels_g)

        # 前三个（上方偏低）
        front_brace = BraceBetweenPoints(
            circles[0].get_top() + UP * 0.10,
            circles[front_n - 1].get_top() + UP * 0.10,
            direction=UP,
            buff=0.08,
        ).set_color(ORANGE)
        front_label = self.safe_text(
            f"{int(front_avg)}×{front_n}={front_sum}",
            font_size=20, color=ORANGE,
        )
        front_label.next_to(front_brace, UP, buff=0.08)
        front_block = VGroup(front_brace, front_label)

        # 后三个（上方更高，避免与前三括号重叠）
        back_brace = BraceBetweenPoints(
            circles[count - back_n].get_top() + UP * 0.10,
            circles[-1].get_top() + UP * 0.10,
            direction=UP,
            buff=0.42,
        ).set_color(BLUE_B)
        back_label = self.safe_text(
            f"{int(back_avg)}×{back_n}={back_sum}",
            font_size=20, color=BLUE_B,
        )
        back_label.next_to(back_brace, UP, buff=0.08)
        back_block = VGroup(back_brace, back_label)

        # 五个数总和（下方）
        total_brace = BraceBetweenPoints(
            circles[0].get_bottom() + DOWN * 0.28,
            circles[-1].get_bottom() + DOWN * 0.28,
            direction=DOWN,
            buff=0.12,
        ).set_color(GREY_A)
        total_label = self.safe_text(
            f"{int(total_avg)}×{count}={total_sum}",
            font_size=20, color=WHITE,
        )
        total_label.next_to(total_brace, DOWN, buff=0.08)
        total_block = VGroup(total_brace, total_label)

        # 中间数高亮（淡入用）
        mid_circle = circles[mid_idx]
        mid_ring = Circle(
            radius=circle_r + 0.06,
            color=YELLOW,
            stroke_width=3.5,
        ).move_to(mid_circle.get_center())
        mid_note = self.safe_text(
            "中间数算了两次",
            font_size=16, color=YELLOW,
        )
        # 放在③下方、总括号上方，避免与左右圆圈重叠
        mid_note.next_to(mid_ring, DOWN, buff=0.10)
        mid_block = VGroup(mid_ring, mid_note)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "前三与后三重叠的中间数，多加一次再减回去",
                font_size=17, color=GREY_B,
            )

        annotated = VGroup(row, front_block, back_block, total_block, mid_block)
        layout_row = VGroup(annotated)
        if show_hint:
            hint.next_to(total_block, DOWN, buff=0.22)
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
            "row": row,
            "circles": circles,
            "circles_g": circles_g,
            "labels_g": labels_g,
            "front_block": front_block,
            "front_brace": front_brace,
            "front_label": front_label,
            "back_block": back_block,
            "back_brace": back_brace,
            "back_label": back_label,
            "total_block": total_block,
            "total_brace": total_brace,
            "total_label": total_label,
            "mid_block": mid_block,
            "mid_ring": mid_ring,
            "mid_note": mid_note,
            "mid_circle": mid_circle,
            "hint": hint,
            "total_sum": total_sum,
            "front_sum": front_sum,
            "back_sum": back_sum,
            "middle": middle,
            "total_avg": int(total_avg),
            "front_avg": int(front_avg),
            "back_avg": int(back_avg),
            "count": count,
            "front_n": front_n,
            "back_n": back_n,
        }
