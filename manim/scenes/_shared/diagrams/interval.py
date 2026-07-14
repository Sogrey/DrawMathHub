"""
间隔问题（锯木头）图解 — 第8讲及同类题型。

用水平实线表示木头，竖虚线表示锯的位置，段数 = 锯的次数 + 1。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class IntervalDiagramMixin:
    """锯木头：参数化锯的次数、每段长度，自动算段数与原长。"""

    def _wood_line_with_caps(
        self,
        left_x: float,
        right_x: float,
        y: float,
        *,
        stroke_width: float = 5.0,
        cap_h: float = 0.12,
        color=WHITE,
    ) -> VGroup:
        base = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=color, stroke_width=stroke_width,
        )
        cap_l = Line(
            np.array([left_x, y + cap_h, 0]),
            np.array([left_x, y - cap_h, 0]),
            color=color, stroke_width=stroke_width * 0.7,
        )
        cap_r = Line(
            np.array([right_x, y + cap_h, 0]),
            np.array([right_x, y - cap_h, 0]),
            color=color, stroke_width=stroke_width * 0.7,
        )
        return VGroup(cap_l, base, cap_r)

    def make_saw_diagram(
        self,
        cuts: int,
        seg_len: int,
        draw_y: float,
        *,
        seg_width: float = 1.38,
        cut_dash_height: float = 0.42,
        wood_stroke: float = 5.0,
    ) -> dict[str, Any]:
        """
        构建锯木头图解。

        cuts: 锯的次数
        seg_len: 每段长度（米）
        """
        if cuts < 1:
            raise ValueError("锯的次数至少为 1")
        segments = cuts + 1
        total_len = segments * seg_len

        left_x = -seg_width * segments / 2
        right_x = seg_width * segments / 2
        base_y = 0.0

        wood = self._wood_line_with_caps(
            left_x, right_x, base_y, stroke_width=wood_stroke,
        )

        cut_marks: list[dict[str, Any]] = []
        for i in range(1, cuts + 1):
            x = left_x + i * seg_width
            cut_line = DashedLine(
                np.array([x, base_y + cut_dash_height, 0]),
                np.array([x, base_y - cut_dash_height, 0]),
                color=YELLOW, stroke_width=2.2, dash_length=0.06,
            )
            cut_label = self.safe_text(f"{i}次", font_size=20, color=YELLOW)
            cut_label.next_to(cut_line, UP, buff=0.14)
            cut_parts = VGroup(cut_line, cut_label)
            cut_marks.append({
                "index": i,
                "x": x,
                "cut_line": cut_line,
                "cut_label": cut_label,
                "parts": cut_parts,
            })

        seg_marks: list[dict[str, Any]] = []
        for i in range(segments):
            seg_left = left_x + i * seg_width
            seg_right = seg_left + seg_width
            seg_center_x = (seg_left + seg_right) / 2
            seg_label = self.safe_text(f"第{i + 1}段", font_size=18, color=TEAL_D)
            seg_label.move_to(np.array([seg_center_x, base_y - 0.38, 0]))
            seg_tick = Line(
                np.array([seg_center_x - 0.08, base_y - 0.18, 0]),
                np.array([seg_center_x + 0.08, base_y - 0.18, 0]),
                color=TEAL_D, stroke_width=1.6,
            )
            seg_parts = VGroup(seg_tick, seg_label)
            seg_marks.append({
                "index": i + 1,
                "center_x": seg_center_x,
                "seg_left": seg_left,
                "seg_right": seg_right,
                "seg_label": seg_label,
                "seg_tick": seg_tick,
                "parts": seg_parts,
            })

        sample_seg = seg_marks[0]
        seg_len_brace = Brace(
            Line(
                np.array([sample_seg["seg_left"], base_y - 0.55, 0]),
                np.array([sample_seg["seg_right"], base_y - 0.55, 0]),
            ),
            direction=DOWN, buff=0.06,
        )
        seg_len_brace.set_color(RED)
        seg_len_text = self.safe_text(f"{seg_len}米", font_size=18, color=RED)
        seg_len_text.next_to(seg_len_brace, DOWN, buff=0.08)

        seg_len_note = self.safe_text(
            f"每段长 {seg_len} 米", font_size=17, color=GREY_B,
        )
        seg_len_note.next_to(seg_len_text, DOWN, buff=0.12)

        rule_label = self.safe_text(
            f"段数 = 锯的次数 + 1  →  {cuts}+1={segments}（段）",
            font_size=20, color=YELLOW,
        )
        rule_label.next_to(wood, UP, buff=0.72)

        relation_note = self.safe_text(
            f"锯 {cuts} 次 → {segments} 段", font_size=18, color=RED,
        )
        relation_note.next_to(rule_label, UP, buff=0.14)

        hint = self.safe_text(
            "实线表示木头，虚线表示锯的位置", font_size=18, color=GREY_B,
        )

        wood_block = VGroup(wood)
        cuts_block = VGroup(*[m["parts"] for m in cut_marks])
        segs_block = VGroup(*[m["parts"] for m in seg_marks])
        len_block = VGroup(seg_len_brace, seg_len_text, seg_len_note)
        rule_block = VGroup(relation_note, rule_label)

        diagram_core = VGroup(wood_block, cuts_block, segs_block, len_block, rule_block)
        hint.next_to(diagram_core, DOWN, buff=0.22)
        full = VGroup(diagram_core, hint)
        full.move_to(np.array([0.0, draw_y, 0.0]))
        self.clamp_content(full)

        return {
            "diagram": full,
            "layout_row": full,
            "hint": hint,
            "wood": wood,
            "wood_block": wood_block,
            "cut_marks": cut_marks,
            "cuts_block": cuts_block,
            "seg_marks": seg_marks,
            "segs_block": segs_block,
            "seg_len_brace": seg_len_brace,
            "seg_len_text": seg_len_text,
            "seg_len_note": seg_len_note,
            "len_block": len_block,
            "rule_label": rule_label,
            "relation_note": relation_note,
            "rule_block": rule_block,
            "cuts": cuts,
            "segments": segments,
            "seg_len": seg_len,
            "total_len": total_len,
        }
