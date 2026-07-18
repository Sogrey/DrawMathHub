"""
工程问题（二）— 第57讲：中途撤队，先求全程队工作量。

总量为1；乙丙全程做满总天数，甲的工作量＝1−乙丙量，再÷甲效得甲天数。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class WorkLeaveDiagramMixin:
    """工程问题：乙丙全程 + 甲中途撤出分段线段图。"""

    def make_work_leave_diagram(
        self,
        draw_y: float,
        *,
        a_days: int = 10,
        b_days: int = 15,
        c_days: int = 20,
        total_days: int = 6,
        total_w: float = 7.4,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if min(a_days, b_days, c_days, total_days) <= 0:
            raise ValueError("天数须为正")

        # 乙丙全程： (1/15+1/20)×6 = 7/10
        # 甲工作量： 1−7/10 = 3/10
        # 甲天数： (3/10)÷(1/10) = 3
        bc_rate = 1 / b_days + 1 / c_days
        bc_work = bc_rate * total_days
        a_work = 1 - bc_work
        a_worked = int(round(a_work / (1 / a_days)))  # 3

        if not (0 < bc_work < 1):
            raise ValueError("乙丙工作量须在 (0,1) 内")

        bc_w = total_w * bc_work
        a_w = total_w - bc_w
        left_x = -total_w / 2
        mid_x = left_x + bc_w
        right_x = left_x + total_w
        y = 0.15

        bc_color = TEAL_D
        a_color = ORANGE

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

        bc_bar = RoundedRectangle(
            width=bc_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        bc_bar.set_fill(bc_color, opacity=0.30)
        bc_bar.move_to(np.array([left_x + bc_w / 2, y, 0]))

        a_bar = RoundedRectangle(
            width=a_w, height=0.22, corner_radius=0.04, stroke_width=0,
        )
        a_bar.set_fill(a_color, opacity=0.30)
        a_bar.move_to(np.array([mid_x + a_w / 2, y, 0]))

        # 总量括号在下方，上侧留给乙丙/甲标注，避免重叠
        total_brace = Brace(main, DOWN, buff=0.14, color=GREY_B)
        total_lab = self.safe_text("工作总量 1", font_size=18, color=GREY_B)
        total_lab.next_to(total_brace, DOWN, buff=0.06)

        bc_brace = Brace(bc_bar, UP, buff=0.12, color=bc_color)
        bc_lab = self.safe_text(
            f"乙丙完成：(1/{b_days}+1/{c_days})×{total_days}",
            font_size=14, color=bc_color,
        )
        bc_lab.next_to(bc_brace, UP, buff=0.06)

        a_brace = Brace(a_bar, UP, buff=0.12, color=a_color)
        a_lab = self.safe_text("甲队完成的工作量", font_size=14, color=a_color)
        a_lab.next_to(a_brace, UP, buff=0.06)

        for m in (
            bc_bar, a_bar, total_brace, total_lab,
            bc_brace, bc_lab, a_brace, a_lab,
        ):
            m.set_opacity(0)

        note_bc = self.safe_text(
            f"乙、丙从头干到尾，共{total_days}天",
            font_size=16, color=WHITE,
        )
        note_a = self.safe_text(
            f"[1−(1/{b_days}+1/{c_days})×{total_days}]÷1/{a_days}={a_worked}（天）",
            font_size=16, color=YELLOW,
        )
        for m in (note_bc, note_a):
            m.set_opacity(0)

        notes = VGroup(note_bc, note_a).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT,
        )
        notes.next_to(total_lab, DOWN, buff=0.28)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "先求乙丙全程的工作量",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.10)

        diagram = VGroup(
            main, ticks, bc_bar, a_bar,
            total_brace, total_lab, bc_brace, bc_lab, a_brace, a_lab,
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
            "bc_bar": bc_bar,
            "a_bar": a_bar,
            "total_brace": total_brace,
            "total_lab": total_lab,
            "bc_brace": bc_brace,
            "bc_lab": bc_lab,
            "a_brace": a_brace,
            "a_lab": a_lab,
            "notes": notes,
            "note_bc": note_bc,
            "note_a": note_a,
            "hint": hint,
            "a_days": a_days,
            "b_days": b_days,
            "c_days": c_days,
            "total_days": total_days,
            "a_worked": a_worked,
            "answer": f"甲队实际工作了{a_worked}天",
        }
