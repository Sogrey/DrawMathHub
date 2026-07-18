"""
容斥问题 — 第44讲：韦恩图法。

两个集合有重叠，全集人数已知且每人至少属于一个集合时，
交集人数 = |A| + |B| − |全集|。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class VennSetsDiagramMixin:
    """两椭圆韦恩图：求交集（两题都做对）。"""

    def make_venn_sets_diagram(
        self,
        draw_y: float,
        *,
        set_a: int = 21,
        set_b: int = 18,
        total: int = 36,
        label_a: str = "做对第一题",
        label_b: str = "做对第二题",
        label_both: str = "两题都对",
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "人",
        ellipse_w: float = 2.75,
        ellipse_h: float = 1.85,
        center_gap: float = 1.85,
    ) -> dict[str, Any]:
        both = set_a + set_b - total
        if both < 0:
            raise ValueError("交集不能为负")
        only_a = set_a - both
        only_b = set_b - both

        # 圆心距加大 → 重叠区变窄；椭圆横向更长，便于标文字
        left_c = np.array([-center_gap / 2, 0.20, 0])
        right_c = np.array([center_gap / 2, 0.20, 0])

        oval_a = Ellipse(
            width=ellipse_w, height=ellipse_h,
            color=TEAL_D, stroke_width=3.0,
            fill_opacity=0.12, fill_color=TEAL_D,
        ).move_to(left_c)
        oval_b = Ellipse(
            width=ellipse_w, height=ellipse_h,
            color=ORANGE, stroke_width=3.0,
            fill_opacity=0.12, fill_color=ORANGE,
        ).move_to(right_c)

        lab_a = VGroup(
            self.safe_text(label_a, font_size=15, color=TEAL_D),
            self.safe_text(f"{set_a} {unit_label}", font_size=16, color=TEAL_D),
        ).arrange(DOWN, buff=0.08)
        lab_a.move_to(left_c + LEFT * 0.70 + UP * 0.08)

        lab_b = VGroup(
            self.safe_text(label_b, font_size=15, color=ORANGE),
            self.safe_text(f"{set_b} {unit_label}", font_size=16, color=ORANGE),
        ).arrange(DOWN, buff=0.08)
        lab_b.move_to(right_c + RIGHT * 0.70 + UP * 0.08)

        both_q = self.safe_text(f"? {unit_label}", font_size=20, color=YELLOW)
        both_ans = self.safe_text(f"{both} {unit_label}", font_size=20, color=YELLOW)
        both_q.move_to(np.array([0, 0.18, 0]))
        both_ans.move_to(both_q.get_center())
        both_ans.set_opacity(0)

        # 全集括号
        half_w = ellipse_w / 2
        span = Line(
            left_c + LEFT * half_w * 0.92 + DOWN * (ellipse_h * 0.52),
            right_c + RIGHT * half_w * 0.92 + DOWN * (ellipse_h * 0.52),
        )
        total_brace = Brace(span, DOWN, buff=0.16)
        total_brace.set_color(WHITE)
        total_lab = self.safe_text(
            f"全班 {total} {unit_label}",
            font_size=18, color=WHITE,
        )
        total_lab.next_to(total_brace, DOWN, buff=0.08)
        total_block = VGroup(total_brace, total_lab)

        # 批注
        note_sum = self.safe_text(
            f"{set_a}+{set_b}={set_a + set_b}（比总人数多）",
            font_size=15, color=GREY_B,
        )
        note_why = self.safe_text(
            "重叠部分被重复计算了一次",
            font_size=15, color=GREY_B,
        )
        note_calc_q = self.safe_text(
            f"{label_both}：{set_a}+{set_b}－{total}=?",
            font_size=16, color=YELLOW,
        )
        note_calc_ans = self.safe_text(
            f"{label_both}：{set_a}+{set_b}－{total}={both}（{unit_label}）",
            font_size=16, color=YELLOW,
        )
        for m in (note_sum, note_why, note_calc_q, note_calc_ans):
            m.set_opacity(0)

        notes = VGroup(note_sum, note_why, note_calc_q, note_calc_ans)
        note_sum.next_to(total_block, DOWN, buff=0.28)
        note_why.next_to(note_sum, DOWN, buff=0.10)
        note_calc_q.next_to(note_why, DOWN, buff=0.12)
        note_calc_ans.move_to(note_calc_q)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "交集＝两集人数之和－全集人数",
                font_size=15, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        venn = VGroup(oval_a, oval_b, lab_a, lab_b, both_q, both_ans)
        diagram = VGroup(venn, total_block, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "venn": venn,
            "oval_a": oval_a,
            "oval_b": oval_b,
            "lab_a": lab_a,
            "lab_b": lab_b,
            "both_q": both_q,
            "both_ans": both_ans,
            "total_block": total_block,
            "notes": notes,
            "note_sum": note_sum,
            "note_why": note_why,
            "note_calc_q": note_calc_q,
            "note_calc_ans": note_calc_ans,
            "hint": hint,
            "set_a": set_a,
            "set_b": set_b,
            "total": total,
            "both": both,
            "only_a": only_a,
            "only_b": only_b,
            "unit_label": unit_label,
        }
