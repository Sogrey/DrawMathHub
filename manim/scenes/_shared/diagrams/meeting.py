"""
相遇问题 — 第27讲：相向而行，路程和 = 速度和 × 相遇时间。

线段两端为两家，中间虚线为相遇点；两侧箭头指向相遇处。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class MeetingDiagramMixin:
    """相遇问题：相向而行线段图。"""

    def make_meeting_diagram(
        self,
        draw_y: float,
        *,
        left_speed: int = 60,
        right_speed: int = 64,
        meet_time: int = 5,
        left_name: str = "小星家",
        right_name: str = "小明家",
        left_person: str = "小星",
        right_person: str = "小明",
        total_w: float = 7.2,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "米",
    ) -> dict[str, Any]:
        if left_speed <= 0 or right_speed <= 0 or meet_time <= 0:
            raise ValueError("速度与时间须为正")

        left_dist = left_speed * meet_time
        right_dist = right_speed * meet_time
        total_dist = left_dist + right_dist
        left_w = total_w * left_dist / total_dist
        right_w = total_w - left_w

        left_x = -total_w / 2
        meet_x = left_x + left_w
        right_x = left_x + total_w
        y = 0.0

        main = Line(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        ticks = VGroup(
            Line(
                np.array([left_x, y + tick_h, 0]),
                np.array([left_x, y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.9,
            ),
            Line(
                np.array([right_x, y + tick_h, 0]),
                np.array([right_x, y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.9,
            ),
        )

        meet_line = DashedLine(
            np.array([meet_x, y + 0.55, 0]),
            np.array([meet_x, y - 0.55, 0]),
            color=YELLOW, stroke_width=2.2, dash_length=0.08,
        )
        meet_tag = self.safe_text("两人相遇", font_size=16, color=YELLOW)
        meet_tag.next_to(meet_line, DOWN, buff=0.12)
        meet_block = VGroup(meet_line, meet_tag)

        left_home = self.safe_text(left_name, font_size=18, color=TEAL_D)
        left_home.next_to(np.array([left_x, y, 0]), DOWN, buff=0.28)
        right_home = self.safe_text(right_name, font_size=18, color=ORANGE)
        right_home.next_to(np.array([right_x, y, 0]), DOWN, buff=0.28)
        homes = VGroup(left_home, right_home)

        # 左侧：向右指向相遇点的箭头（速度 / 时间）
        def _side_arrows(x0: float, x1: float, direction: str, color):
            # direction 'right' means arrows point right (toward meet from left)
            y1, y2 = y + 0.28, y - 0.22
            if direction == "right":
                a1 = Arrow(
                    np.array([x0 + 0.12, y1, 0]),
                    np.array([x1 - 0.10, y1, 0]),
                    buff=0, stroke_width=3, color=color,
                    max_tip_length_to_length_ratio=0.15, tip_length=0.16,
                )
                a2 = Arrow(
                    np.array([x0 + 0.12, y2, 0]),
                    np.array([x1 - 0.10, y2, 0]),
                    buff=0, stroke_width=3, color=color,
                    max_tip_length_to_length_ratio=0.15, tip_length=0.16,
                )
            else:
                a1 = Arrow(
                    np.array([x0 - 0.12, y1, 0]),
                    np.array([x1 + 0.10, y1, 0]),
                    buff=0, stroke_width=3, color=color,
                    max_tip_length_to_length_ratio=0.15, tip_length=0.16,
                )
                a2 = Arrow(
                    np.array([x0 - 0.12, y2, 0]),
                    np.array([x1 + 0.10, y2, 0]),
                    buff=0, stroke_width=3, color=color,
                    max_tip_length_to_length_ratio=0.15, tip_length=0.16,
                )
            return VGroup(a1, a2)

        left_arrows = _side_arrows(left_x, meet_x, "right", TEAL_D)
        right_arrows = _side_arrows(right_x, meet_x, "left", ORANGE)

        left_speed_lab = self.safe_text(
            f"每分钟走 {left_speed} {unit_label}",
            font_size=15, color=TEAL_D,
        )
        left_speed_lab.next_to(left_arrows[0], UP, buff=0.08)
        left_time_lab = self.safe_text(
            f"{meet_time} 分钟",
            font_size=15, color=TEAL_D,
        )
        left_time_lab.next_to(left_arrows[1], DOWN, buff=0.08)
        left_info = VGroup(left_speed_lab, left_time_lab)

        right_speed_lab = self.safe_text(
            f"每分钟走 {right_speed} {unit_label}",
            font_size=15, color=ORANGE,
        )
        right_speed_lab.next_to(right_arrows[0], UP, buff=0.08)
        right_time_lab = self.safe_text(
            f"{meet_time} 分钟",
            font_size=15, color=ORANGE,
        )
        right_time_lab.next_to(right_arrows[1], DOWN, buff=0.08)
        right_info = VGroup(right_speed_lab, right_time_lab)

        # 总路程上括号：? → 答案
        total_span = Line(
            np.array([left_x, y + tick_h + 0.04, 0]),
            np.array([right_x, y + tick_h + 0.04, 0]),
        )
        total_brace = Brace(total_span, direction=UP, buff=0.55)
        total_brace.set_color(YELLOW)
        total_q = self.safe_text(f"? {unit_label}", font_size=20, color=YELLOW)
        total_q.next_to(total_brace, UP, buff=0.06)
        total_ans = self.safe_text(
            f"{total_dist} {unit_label}",
            font_size=20, color=YELLOW,
        )
        total_ans.next_to(total_brace, UP, buff=0.06)
        total_ans.set_opacity(0)
        total_block = VGroup(total_brace, total_q, total_ans)

        # 方法提示（写入组内再定位）
        note_m1 = self.safe_text(
            f"方法一：{left_speed}×{meet_time}+{right_speed}×{meet_time}={total_dist}",
            font_size=15, color=GREY_A,
        )
        note_m2 = self.safe_text(
            f"方法二：({left_speed}+{right_speed})×{meet_time}={total_dist}",
            font_size=15, color=GREY_A,
        )
        notes = VGroup(note_m1, note_m2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        notes.set_opacity(0)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "相向而行：两人所走路程的和 = 两家距离",
                font_size=16, color=GREY_B,
            )

        line_core = VGroup(main, ticks)
        travel = VGroup(left_arrows, right_arrows, left_info, right_info)
        annotated = VGroup(
            line_core, meet_block, homes, travel, total_block, notes,
        )
        layout_row = VGroup(annotated)
        if show_hint:
            hint.next_to(annotated, DOWN, buff=0.22)
            # notes 放 hint 上方内侧
            notes.next_to(meet_tag, DOWN, buff=0.55)
            layout_row = VGroup(annotated, hint)
        else:
            notes.next_to(meet_tag, DOWN, buff=0.55)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "line_core": line_core,
            "main": main,
            "ticks": ticks,
            "meet_block": meet_block,
            "meet_line": meet_line,
            "meet_tag": meet_tag,
            "homes": homes,
            "left_home": left_home,
            "right_home": right_home,
            "left_arrows": left_arrows,
            "right_arrows": right_arrows,
            "left_info": left_info,
            "right_info": right_info,
            "travel": travel,
            "total_block": total_block,
            "total_brace": total_brace,
            "total_q": total_q,
            "total_ans": total_ans,
            "notes": notes,
            "note_m1": note_m1,
            "note_m2": note_m2,
            "hint": hint,
            "left_speed": left_speed,
            "right_speed": right_speed,
            "meet_time": meet_time,
            "left_dist": left_dist,
            "right_dist": right_dist,
            "total_dist": total_dist,
            "unit_label": unit_label,
            "left_person": left_person,
            "right_person": right_person,
        }
