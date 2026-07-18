"""
植树问题 — 第31讲：两端都栽，棵数 = 间隔数 + 1。

公路线段上按间隔栽树；前几棵与间隔括号 + 省略号 + 末端树，与教材示意图一致。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class PlantTreesDiagramMixin:
    """植树问题：路侧等距植树示意图（默认两端都栽）。"""

    def _make_tree_icon(self, *, color=GREEN_C, scale: float = 1.0) -> VGroup:
        trunk = Line(
            ORIGIN, DOWN * 0.20 * scale,
            color="#8B5A2B", stroke_width=3.5,
        )
        crown = Triangle(fill_opacity=1, stroke_width=0, color=color)
        crown.scale(0.17 * scale)
        crown.next_to(trunk.get_top(), UP, buff=-0.02)
        return VGroup(trunk, crown)

    def make_plant_trees_diagram(
        self,
        draw_y: float,
        *,
        distance: int = 100,
        gap: int = 10,
        both_ends: bool = True,
        preview_trees: int = 4,
        total_w: float = 7.0,
        line_stroke: float = 4.0,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "米",
    ) -> dict[str, Any]:
        if distance <= 0 or gap <= 0 or distance % gap != 0:
            raise ValueError("距离须能被间隔整除")
        intervals = distance // gap
        trees_count = intervals + 1 if both_ends else intervals
        if preview_trees < 2:
            raise ValueError("preview_trees 至少为 2")

        left_x = -total_w / 2
        right_x = total_w / 2
        y = 0.05
        tree_y = y + 0.40

        road = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        cap_l = Line(
            np.array([left_x, y + 0.12, 0]),
            np.array([left_x, y - 0.12, 0]),
            color=WHITE, stroke_width=line_stroke * 0.85,
        )
        cap_r = Line(
            np.array([right_x, y + 0.12, 0]),
            np.array([right_x, y - 0.12, 0]),
            color=WHITE, stroke_width=line_stroke * 0.85,
        )
        road_g = VGroup(cap_l, road, cap_r)

        # 总长括号
        dist_span = Line(
            np.array([left_x, y - 0.14, 0]),
            np.array([right_x, y - 0.14, 0]),
        )
        dist_brace = Brace(dist_span, direction=DOWN, buff=0.16)
        dist_brace.set_color(YELLOW)
        dist_lab = self.safe_text(f"{distance} {unit_label}", font_size=18, color=YELLOW)
        dist_lab.next_to(dist_brace, DOWN, buff=0.08)
        dist_block = VGroup(dist_brace, dist_lab)

        # 前几棵树 + 间隔括号（左侧约一半）
        left_span = total_w * 0.48
        preview = VGroup()
        gap_braces = VGroup()
        for i in range(preview_trees):
            x = left_x + left_span * i / (preview_trees - 1)
            t = self._make_tree_icon()
            t.move_to(np.array([x, tree_y, 0]))
            preview.add(t)
        for i in range(preview_trees - 1):
            x0 = left_x + left_span * i / (preview_trees - 1)
            x1 = left_x + left_span * (i + 1) / (preview_trees - 1)
            span = Line(
                np.array([x0, tree_y + 0.28, 0]),
                np.array([x1, tree_y + 0.28, 0]),
            )
            br = Brace(span, direction=UP, buff=0.04)
            br.set_color(TEAL_D)
            lab = self.safe_text(f"{gap}{unit_label}", font_size=14, color=TEAL_D)
            lab.next_to(br, UP, buff=0.04)
            gap_braces.add(VGroup(br, lab))

        dots = self.safe_text("……", font_size=28, color=GREY_B)
        dots.move_to(np.array([(left_x + left_span + right_x) / 2, tree_y, 0]))

        end_tree = self._make_tree_icon()
        end_tree.move_to(np.array([right_x, tree_y, 0]))

        trees = VGroup(preview, dots, end_tree)

        end_note = self.safe_text(
            "两端都栽" if both_ends else "两端不栽",
            font_size=16, color=ORANGE,
        )
        end_note.next_to(dist_block, DOWN, buff=0.14)

        note_iv = self.safe_text(
            f"间隔数：{distance}÷{gap}={intervals}",
            font_size=16, color=TEAL_D,
        )
        note_tree_q = self.safe_text(
            f"棵数：{intervals}+1=?",
            font_size=16, color=YELLOW,
        )
        note_tree_ans = self.safe_text(
            f"棵数：{intervals}+1={trees_count}（棵）",
            font_size=16, color=YELLOW,
        )
        note_iv.set_opacity(0)
        note_tree_q.set_opacity(0)
        note_tree_ans.set_opacity(0)
        notes = VGroup(note_iv, note_tree_q, note_tree_ans)
        note_iv.next_to(end_note, DOWN, buff=0.18)
        note_tree_q.next_to(note_iv, DOWN, buff=0.10)
        note_tree_ans.next_to(note_iv, DOWN, buff=0.10)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "两端都栽：棵数 = 间隔数 + 1",
                font_size=16, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(
            road_g, trees, gap_braces, dist_block, end_note, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "road": road_g,
            "trees": trees,
            "preview": preview,
            "dots": dots,
            "end_tree": end_tree,
            "gap_braces": gap_braces,
            "dist_block": dist_block,
            "end_note": end_note,
            "notes": notes,
            "note_iv": note_iv,
            "note_tree_q": note_tree_q,
            "note_tree_ans": note_tree_ans,
            "hint": hint,
            "distance": distance,
            "gap": gap,
            "intervals": intervals,
            "trees_count": trees_count,
            "both_ends": both_ends,
            "unit_label": unit_label,
        }
