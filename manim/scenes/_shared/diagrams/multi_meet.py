"""
行程综合（二）— 第60讲：往返多次相遇，求两次相遇点距离。

AB 全程；第一次相遇共走 1 个全程，第二次相遇共走 3 个全程。
速度比＝路程比，先求两遇点相对 A/B 的位置，再求间距。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class MultiMeetDiagramMixin:
    """多次相遇：第一次 / 第二次相遇点间距。"""

    def make_multi_meet_diagram(
        self,
        draw_y: float,
        *,
        distance: int = 400,
        speed_a: int = 3,
        speed_b: int = 5,
        total_w: float = 7.2,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if distance <= 0 or speed_a <= 0 or speed_b <= 0:
            raise ValueError("路程与速度份数须为正")

        parts = speed_a + speed_b  # 8
        first_from_a = distance * speed_a // parts  # 150
        a_at_second = 3 * distance * speed_a // parts  # 450
        second_from_b = a_at_second - distance  # 50
        gap = distance - first_from_a - second_from_b  # 200

        left_x = -total_w / 2
        right_x = left_x + total_w
        y = 0.35
        meet1_x = left_x + total_w * first_from_a / distance
        meet2_x = right_x - total_w * second_from_b / distance

        a_color = TEAL_D
        b_color = ORANGE
        meet_color = YELLOW

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
            for x in (left_x, meet1_x, meet2_x, right_x)
        ])

        lab_a = self.safe_text("A地", font_size=15, color=WHITE)
        lab_a.next_to(np.array([left_x, y, 0]), LEFT, buff=0.12)
        lab_b = self.safe_text("B地", font_size=15, color=WHITE)
        lab_b.next_to(np.array([right_x, y, 0]), RIGHT, buff=0.12)

        # 甲：A→B 直角折回→第二次相遇（不外绕）
        # ───────────────┐
        #         ◁──────┘
        a_out_y = y + 0.48
        a_back_y = y + 0.26
        path_a = VMobject(color=a_color, stroke_width=3.0)
        path_a.set_points_as_corners([
            np.array([left_x, a_out_y, 0]),
            np.array([right_x, a_out_y, 0]),
            np.array([right_x, a_back_y, 0]),
            np.array([meet2_x, a_back_y, 0]),
        ])
        start_a = Dot(np.array([left_x, a_out_y, 0]), radius=0.06, color=a_color)
        lab_jia = self.safe_text("甲", font_size=14, color=a_color)
        lab_jia.next_to(start_a, UP, buff=0.06)
        arr_a_go = Arrow(
            np.array([meet1_x - 0.22, a_out_y, 0]),
            np.array([meet1_x + 0.22, a_out_y, 0]),
            buff=0, stroke_width=2.5, color=a_color,
            max_tip_length_to_length_ratio=0.40,
            max_stroke_width_to_length_ratio=8,
        )
        arr_a_back = Arrow(
            np.array([meet2_x + 0.30, a_back_y, 0]),
            np.array([meet2_x + 0.02, a_back_y, 0]),
            buff=0, stroke_width=2.5, color=a_color,
            max_tip_length_to_length_ratio=0.40,
            max_stroke_width_to_length_ratio=8,
        )
        turn_a_lab = self.safe_text("折返", font_size=11, color=a_color)
        turn_a_lab.next_to(
            np.array([right_x, (a_out_y + a_back_y) / 2, 0]), RIGHT, buff=0.08,
        )

        # 乙：B→A 直角折回→第二次相遇
        # ┌───────────────
        # └─────▷
        b_out_y = y - 0.48
        b_back_y = y - 0.26
        path_b = VMobject(color=b_color, stroke_width=3.0)
        path_b.set_points_as_corners([
            np.array([right_x, b_out_y, 0]),
            np.array([left_x, b_out_y, 0]),
            np.array([left_x, b_back_y, 0]),
            np.array([meet2_x, b_back_y, 0]),
        ])
        start_b = Dot(np.array([right_x, b_out_y, 0]), radius=0.06, color=b_color)
        lab_yi = self.safe_text("乙", font_size=14, color=b_color)
        lab_yi.next_to(start_b, DOWN, buff=0.06)
        arr_b_go = Arrow(
            np.array([meet1_x + 0.22, b_out_y, 0]),
            np.array([meet1_x - 0.22, b_out_y, 0]),
            buff=0, stroke_width=2.5, color=b_color,
            max_tip_length_to_length_ratio=0.40,
            max_stroke_width_to_length_ratio=8,
        )
        arr_b_back = Arrow(
            np.array([meet2_x - 0.30, b_back_y, 0]),
            np.array([meet2_x - 0.02, b_back_y, 0]),
            buff=0, stroke_width=2.5, color=b_color,
            max_tip_length_to_length_ratio=0.40,
            max_stroke_width_to_length_ratio=8,
        )
        turn_b_lab = self.safe_text("折返", font_size=11, color=b_color)
        turn_b_lab.next_to(
            np.array([left_x, (b_out_y + b_back_y) / 2, 0]), LEFT, buff=0.08,
        )

        paths = VGroup(path_a, path_b, start_a, start_b)
        arrows = VGroup(arr_a_go, arr_a_back, arr_b_go, arr_b_back)
        turn_labs = VGroup(turn_a_lab, turn_b_lab)

        v1 = DashedLine(
            np.array([meet1_x, y + 0.62, 0]),
            np.array([meet1_x, y - 0.62, 0]),
            color=meet_color, stroke_width=2.0, dash_length=0.08,
        )
        v2 = DashedLine(
            np.array([meet2_x, y + 0.62, 0]),
            np.array([meet2_x, y - 0.62, 0]),
            color=meet_color, stroke_width=2.0, dash_length=0.08,
        )
        meet1_lab = self.safe_text("第一次相遇", font_size=12, color=meet_color)
        meet1_lab.next_to(np.array([meet1_x, y + 0.62, 0]), UP, buff=0.05)
        meet2_lab = self.safe_text("第二次相遇", font_size=12, color=meet_color)
        meet2_lab.next_to(np.array([meet2_x, y + 0.62, 0]), UP, buff=0.05)

        # 间距标在两遇点之间主线下方
        gap_line = Line(
            np.array([meet1_x, y, 0]),
            np.array([meet2_x, y, 0]),
            stroke_width=0,
        )
        gap_brace = Brace(gap_line, DOWN, buff=0.10, color=RED)
        gap_lab = self.safe_text(f"相距{gap}千米", font_size=13, color=RED)
        gap_lab.next_to(gap_brace, DOWN, buff=0.03)

        total_brace = Brace(main, DOWN, buff=0.68, color=GREY_B)
        total_lab = self.safe_text(f"{distance}千米", font_size=15, color=GREY_B)
        total_lab.next_to(total_brace, DOWN, buff=0.05)

        note1 = self.safe_text(
            f"第一次：{distance}×{speed_a}/({speed_a}+{speed_b})={first_from_a}（千米）",
            font_size=14, color=WHITE,
        )
        note2 = self.safe_text(
            f"第二次：3×{distance}×{speed_a}/({speed_a}+{speed_b})-{distance}={second_from_b}（千米）",
            font_size=13, color=WHITE,
        )
        note3 = self.safe_text(
            f"{distance}-{first_from_a}-{second_from_b}={gap}（千米）",
            font_size=15, color=YELLOW,
        )
        # 仅文字预置透明；图元保持不透明，场景里 FadeIn/Create
        for m in (
            meet1_lab, meet2_lab, gap_lab, note1, note2, note3,
            lab_jia, lab_yi, turn_a_lab, turn_b_lab,
        ):
            m.set_opacity(0)

        notes = VGroup(note1, note2, note3).arrange(
            DOWN, buff=0.10, aligned_edge=LEFT,
        )
        notes.next_to(total_lab, DOWN, buff=0.18)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "第二次相遇时两车共走了3个全程",
                font_size=13, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.06)

        diagram = VGroup(
            main, ticks, lab_a, lab_b, total_brace, total_lab,
            paths, arrows, turn_labs, lab_jia, lab_yi,
            v1, v2, meet1_lab, meet2_lab,
            gap_brace, gap_lab, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "main": main,
            "ticks": ticks,
            "lab_a": lab_a,
            "lab_b": lab_b,
            "total_brace": total_brace,
            "total_lab": total_lab,
            "path_a": path_a,
            "path_b": path_b,
            "paths": paths,
            "arrows": arrows,
            "turn_labs": turn_labs,
            "turn_a_lab": turn_a_lab,
            "turn_b_lab": turn_b_lab,
            "start_a": start_a,
            "start_b": start_b,
            "lab_jia": lab_jia,
            "lab_yi": lab_yi,
            "v1": v1,
            "v2": v2,
            "meet1_lab": meet1_lab,
            "meet2_lab": meet2_lab,
            "gap_brace": gap_brace,
            "gap_lab": gap_lab,
            "notes": notes,
            "note1": note1,
            "note2": note2,
            "note3": note3,
            "hint": hint,
            "distance": distance,
            "speed_a": speed_a,
            "speed_b": speed_b,
            "first_from_a": first_from_a,
            "second_from_b": second_from_b,
            "gap": gap,
            "answer": f"相距{gap}千米",
        }
