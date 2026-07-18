"""
工程问题（一）— 第56讲：总量为1的合作/单独分段线段图。

左段：甲乙合作若干天的工作量；右段：乙单独完成剩余。
先求乙效，再求甲效与甲单独天数。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class WorkProjectDiagramMixin:
    """工程问题：总量1，合作段 + 乙单独段。"""

    def make_work_project_diagram(
        self,
        draw_y: float,
        *,
        together_days: int = 30,
        jointly_days: int = 6,
        b_alone_days: int = 40,
        total_w: float = 7.4,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if together_days <= 0 or jointly_days <= 0 or b_alone_days <= 0:
            raise ValueError("天数须为正")
        if jointly_days >= together_days:
            raise ValueError("合作已做天数应小于合作完工天数")

        # 合作效率 1/30；合作6天工作量 6/30=1/5
        # 剩余 1-1/5=4/5；乙效率 (4/5)/40=1/50
        # 甲效率 1/30-1/50=1/75；甲单独 75 天
        jointly_work = jointly_days / together_days  # 0.2
        remain_work = 1 - jointly_work  # 0.8
        b_rate_den = int(round(b_alone_days / remain_work))  # 50
        # 甲效分母：1/(1/30-1/50)=75
        a_alone_days = int(round(
            1 / (1 / together_days - 1 / b_rate_den)
        ))  # 75

        jointly_w = total_w * jointly_work
        remain_w = total_w - jointly_w
        left_x = -total_w / 2
        mid_x = left_x + jointly_w
        right_x = left_x + total_w
        y = 0.25

        joint_color = TEAL_D
        alone_color = ORANGE

        main = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        ticks = VGroup(*[
            Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.85,
            )
            for x in (left_x, mid_x, right_x)
        ])

        joint_bar = RoundedRectangle(
            width=jointly_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        joint_bar.set_fill(joint_color, opacity=0.30)
        joint_bar.move_to(np.array([left_x + jointly_w / 2, y, 0]))

        alone_bar = RoundedRectangle(
            width=remain_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        alone_bar.set_fill(alone_color, opacity=0.30)
        alone_bar.move_to(np.array([mid_x + remain_w / 2, y, 0]))

        joint_brace = Brace(joint_bar, DOWN, buff=0.14, color=joint_color)
        joint_lab = self.safe_text(
            f"甲乙合作{jointly_days}天：1/{together_days}×{jointly_days}",
            font_size=15, color=joint_color,
        )
        joint_lab.next_to(joint_brace, DOWN, buff=0.08)

        # 乙单独标注贴紧右段上方；总量括号抬高，避免与之重叠
        alone_lab = self.safe_text(
            f"乙单独做{b_alone_days}天",
            font_size=16, color=alone_color,
        )
        alone_lab.next_to(alone_bar, UP, buff=0.10)

        brace_buff = (alone_lab.get_top()[1] - main.get_top()[1]) + 0.20
        total_brace = Brace(main, UP, buff=brace_buff, color=GREY_B)
        total_lab = self.safe_text("工作总量 1", font_size=18, color=GREY_B)
        total_lab.next_to(total_brace, UP, buff=0.06)

        for m in (
            joint_bar, alone_bar, total_brace, total_lab,
            joint_brace, joint_lab, alone_lab,
        ):
            m.set_opacity(0)

        note_coop = self.safe_text(
            f"合作效率＝1/{together_days}",
            font_size=17, color=WHITE,
        )
        note_b = self.safe_text(
            f"(1−1/{together_days}×{jointly_days})÷{b_alone_days}=1/{b_rate_den}",
            font_size=17, color=alone_color,
        )
        note_a = self.safe_text(
            f"1÷(1/{together_days}−1/{b_rate_den})={a_alone_days}（天）",
            font_size=18, color=YELLOW,
        )
        for m in (note_coop, note_b, note_a):
            m.set_opacity(0)

        notes = VGroup(note_coop, note_b, note_a).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT,
        )
        notes.next_to(joint_lab, DOWN, buff=0.32)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "先求乙单独做的工作量",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.10)

        diagram = VGroup(
            main, ticks, joint_bar, alone_bar,
            total_brace, total_lab, joint_brace, joint_lab, alone_lab,
            notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "main": main,
            "ticks": ticks,
            "joint_bar": joint_bar,
            "alone_bar": alone_bar,
            "total_brace": total_brace,
            "total_lab": total_lab,
            "joint_brace": joint_brace,
            "joint_lab": joint_lab,
            "alone_lab": alone_lab,
            "notes": notes,
            "note_coop": note_coop,
            "note_b": note_b,
            "note_a": note_a,
            "hint": hint,
            "together_days": together_days,
            "jointly_days": jointly_days,
            "b_alone_days": b_alone_days,
            "b_rate_den": b_rate_den,
            "a_alone_days": a_alone_days,
            "answer": f"甲单独需要{a_alone_days}天",
        }
