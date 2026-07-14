"""
方阵问题 — 第24讲：单层空心方阵人数。

用圆表示人，按外圈排布；支持方法一（四角重复减 4）与方法二（每边 n−1）。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class HollowSquareDiagramMixin:
    """单层空心方阵：每边 n 人，总人数 (n−1)×4。"""

    def make_hollow_square_diagram(
        self,
        draw_y: float,
        *,
        side_n: int = 9,
        circle_r: float = 0.14,
        gap: float = 0.05,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if side_n < 2:
            raise ValueError("side_n 必须 ≥ 2")

        total = (side_n - 1) * 4
        step = 2 * circle_r + gap
        half = (side_n - 1) * step / 2
        n = side_n

        # 上 → 右中 → 下 → 左中（角不重复）
        positions: list[np.ndarray] = []
        for i in range(n):
            positions.append(np.array([-half + i * step, half, 0]))
        for i in range(1, n - 1):
            positions.append(np.array([half, half - i * step, 0]))
        for i in range(n):
            positions.append(np.array([half - i * step, -half, 0]))
        for i in range(1, n - 1):
            positions.append(np.array([-half, -half + i * step, 0]))

        assert len(positions) == total

        corner_keys = {
            (round(-half, 5), round(half, 5)),
            (round(half, 5), round(half, 5)),
            (round(half, 5), round(-half, 5)),
            (round(-half, 5), round(-half, 5)),
        }
        corner_idx: list[int] = []
        edge_idx: list[int] = []
        for i, p in enumerate(positions):
            key = (round(p[0], 5), round(p[1], 5))
            if key in corner_keys:
                corner_idx.append(i)
            else:
                edge_idx.append(i)

        circles = VGroup()
        for p in positions:
            c = Circle(radius=circle_r, color=WHITE, stroke_width=2)
            c.set_fill(WHITE, opacity=0.08)
            c.move_to(p)
            circles.add(c)

        corner_circles = VGroup(*[circles[i] for i in corner_idx])
        edge_circles = VGroup(*[circles[i] for i in edge_idx])

        i_top0 = 0
        i_right0 = n
        i_bottom0 = n + (n - 2)
        i_left0 = i_bottom0 + n

        # 方法二：每边取 n−1（含本边左侧角，不含下一角）
        side_groups_idx = [
            list(range(i_top0, i_top0 + n - 1)),
            [i_top0 + n - 1] + list(range(i_right0, i_right0 + n - 2)),
            [i_bottom0] + list(range(i_bottom0 + 1, i_bottom0 + n - 1)),
            [i_bottom0 + n - 1] + list(range(i_left0, i_left0 + n - 2)),
        ]
        for idxs in side_groups_idx:
            assert len(idxs) == n - 1

        side_groups = VGroup(*[
            VGroup(*[circles[i] for i in idxs]) for idxs in side_groups_idx
        ])

        side_colors = [ORANGE, TEAL_D, BLUE_C, PURPLE_B]
        side_dirs = [UP, RIGHT, DOWN, LEFT]
        side_brackets = VGroup()
        for idxs, color, direction in zip(side_groups_idx, side_colors, side_dirs):
            grp = VGroup(*[circles[i] for i in idxs])
            br = Brace(grp, direction=direction, color=color, buff=0.08)
            tip = self.safe_text(f"{n - 1}", font_size=16, color=color)
            tip.next_to(br, direction, buff=0.08)
            side_brackets.add(VGroup(br, tip))
        side_brackets.set_opacity(0)

        side_label = self.safe_text(f"每边 {side_n} 人", font_size=18, color=YELLOW)
        side_label.next_to(circles, UP, buff=0.28)

        m1_note = self.safe_text(
            f"方法一：{side_n}×4−4={total}（人）",
            font_size=16, color=ORANGE,
        )
        m2_note = self.safe_text(
            f"方法二：({side_n}−1)×4={total}（人）",
            font_size=16, color=TEAL_D,
        )
        m1_note.next_to(circles, DOWN, buff=0.28)
        m2_note.next_to(m1_note, DOWN, buff=0.14)
        m1_note.set_opacity(0)
        m2_note.set_opacity(0)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "1 个圆代表 1 人；角上的人属于两条边",
                font_size=16, color=GREY_B,
            )
            hint.next_to(m2_note, DOWN, buff=0.14)

        annotated = VGroup(circles, side_brackets, side_label, m1_note, m2_note)
        layout_row = VGroup(annotated)
        if show_hint:
            layout_row = VGroup(annotated, hint)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "circles": circles,
            "corner_circles": corner_circles,
            "edge_circles": edge_circles,
            "side_groups": side_groups,
            "side_brackets": side_brackets,
            "side_label": side_label,
            "m1_note": m1_note,
            "m2_note": m2_note,
            "hint": hint,
            "side_n": side_n,
            "total": total,
            "corner_idx": corner_idx,
            "edge_idx": edge_idx,
            "side_colors": side_colors,
        }
