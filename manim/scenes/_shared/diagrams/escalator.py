"""
扶梯问题 — 第59讲：兄妹上行速度分段线段图。

两行等比例速度条：左段扶梯速度相同，右段为各自行走速度；
实际速度×时间＝静止可见台阶数。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class EscalatorDiagramMixin:
    """扶梯：上行速度＝扶梯速＋行走速，同程列方程。"""

    def make_escalator_diagram(
        self,
        draw_y: float,
        *,
        bro_walk: int = 2,
        sis_walk: int = 1,
        bro_time: int = 20,
        sis_time: int = 30,
        unit_w: float = 1.15,
        bar_h: float = 0.36,
        row_gap: float = 1.70,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if min(bro_walk, sis_walk, bro_time, sis_time) <= 0:
            raise ValueError("速度与时间须为正")

        # 20(2+x)=30(1+x) → x=1；台阶=20×3=60
        # 解：20*2 + 20x = 30*1 + 30x → 40-30 = 30x-20x → 10=10x
        esc_speed = (bro_walk * bro_time - sis_walk * sis_time) // (
            sis_time - bro_time
        )  # 1
        steps = bro_time * (bro_walk + esc_speed)  # 60

        esc_color = TEAL_D
        walk_color = ORANGE
        total_color = BLUE_C

        # 速度条长度按「扶梯速 + 行走速」比例（示意 x=1）
        esc_w = unit_w * esc_speed if esc_speed > 0 else unit_w
        bro_walk_w = unit_w * bro_walk
        sis_walk_w = unit_w * sis_walk
        bro_total_w = esc_w + bro_walk_w
        sis_total_w = esc_w + sis_walk_w

        left_x = -max(bro_total_w, sis_total_w) / 2 - 0.85
        mid_x = left_x + esc_w
        y_bro = row_gap / 2
        y_sis = -row_gap / 2

        def make_row(y: float, walk_w: float, name: str, walk_lab: str):
            total_w = esc_w + walk_w
            esc_bar = RoundedRectangle(
                width=esc_w, height=bar_h, corner_radius=0.05, stroke_width=0,
            )
            esc_bar.set_fill(esc_color, opacity=0.55)
            esc_bar.move_to(np.array([left_x + esc_w / 2, y, 0]))

            walk_bar = RoundedRectangle(
                width=walk_w, height=bar_h, corner_radius=0.05, stroke_width=0,
            )
            walk_bar.set_fill(walk_color, opacity=0.55)
            walk_bar.move_to(np.array([mid_x + walk_w / 2, y, 0]))

            outline = RoundedRectangle(
                width=total_w, height=bar_h + 0.06, corner_radius=0.06,
                color=WHITE, stroke_width=2.0,
            )
            outline.set_fill(opacity=0)
            outline.move_to(np.array([left_x + total_w / 2, y, 0]))

            name_lab = self.safe_text(name, font_size=16, color=WHITE)
            name_lab.next_to(outline, LEFT, buff=0.18)

            brace = Brace(outline, DOWN, buff=0.08, color=total_color)
            speed_lab = self.safe_text("上行速度", font_size=13, color=total_color)
            speed_lab.next_to(brace, DOWN, buff=0.04)

            return {
                "esc_bar": esc_bar,
                "walk_bar": walk_bar,
                "outline": outline,
                "name_lab": name_lab,
                "brace": brace,
                "speed_lab": speed_lab,
                "walk_lab_text": walk_lab,
                "total_w": total_w,
            }

        bro = make_row(y_bro, bro_walk_w, "哥哥", f"{bro_walk}级/秒")
        sis = make_row(y_sis, sis_walk_w, "妹妹", f"{sis_walk}级/秒")

        # 扶梯速度共用标签（两行左段上方）
        esc_span = Line(
            np.array([left_x, y_bro + bar_h / 2, 0]),
            np.array([mid_x, y_bro + bar_h / 2, 0]),
            stroke_width=0,
        )
        esc_brace = Brace(esc_span, UP, buff=0.12, color=esc_color)
        esc_lab = self.safe_text("扶梯运行速度", font_size=14, color=esc_color)
        esc_lab.next_to(esc_brace, UP, buff=0.05)

        # 哥哥行走标在条上方；妹妹行走标在条右侧，避免与哥哥「上行速度」重叠
        bro_walk_lab = self.safe_text(
            f"行走{bro_walk}级/秒", font_size=13, color=walk_color,
        )
        bro_walk_lab.next_to(bro["walk_bar"], UP, buff=0.10)
        sis_walk_lab = self.safe_text(
            f"行走{sis_walk}级/秒", font_size=13, color=walk_color,
        )
        sis_walk_lab.next_to(sis["walk_bar"], RIGHT, buff=0.14)

        # 虚线对齐扶梯/行走分界
        divider = DashedLine(
            np.array([mid_x, y_bro + bar_h / 2 + 0.35, 0]),
            np.array([mid_x, y_sis - bar_h / 2 - 0.15, 0]),
            color=GREY_B, stroke_width=1.5, dash_length=0.08,
        )

        note_eq = self.safe_text(
            f"{bro_time}×({bro_walk}+x)={sis_time}×({sis_walk}+x)",
            font_size=17, color=WHITE,
        )
        note_x = self.safe_text(f"x={esc_speed}", font_size=17, color=ORANGE)
        note_ans = self.safe_text(
            f"{bro_time}×({bro_walk}+{esc_speed})={steps}（级）",
            font_size=17, color=YELLOW,
        )
        for m in (
            esc_lab, bro_walk_lab, sis_walk_lab,
            bro["speed_lab"], sis["speed_lab"],
            note_eq, note_x, note_ans,
        ):
            m.set_opacity(0)

        # brace / divider 保持不透明，场景里 FadeIn（勿先 set_opacity(0)）
        esc_brace.set_opacity(1)
        bro["brace"].set_opacity(1)
        sis["brace"].set_opacity(1)
        divider.set_opacity(1)

        notes = VGroup(note_eq, note_x, note_ans).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT,
        )
        notes.next_to(
            VGroup(bro["outline"], sis["outline"], sis["brace"], sis["speed_lab"]),
            DOWN, buff=0.28,
        )

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "实际速度＝扶梯速＋行走速",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.08)

        # 图元保持不透明，场景内 FadeIn（勿先 set_opacity(0) 再 FadeIn）
        diagram = VGroup(
            bro["esc_bar"], bro["walk_bar"], bro["outline"], bro["name_lab"],
            bro["brace"], bro["speed_lab"], bro_walk_lab,
            sis["esc_bar"], sis["walk_bar"], sis["outline"], sis["name_lab"],
            sis["brace"], sis["speed_lab"], sis_walk_lab,
            esc_brace, esc_lab, divider, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "bro": bro,
            "sis": sis,
            "bro_walk_lab": bro_walk_lab,
            "sis_walk_lab": sis_walk_lab,
            "esc_brace": esc_brace,
            "esc_lab": esc_lab,
            "divider": divider,
            "notes": notes,
            "note_eq": note_eq,
            "note_x": note_x,
            "note_ans": note_ans,
            "hint": hint,
            "bro_walk": bro_walk,
            "sis_walk": sis_walk,
            "bro_time": bro_time,
            "sis_time": sis_time,
            "esc_speed": esc_speed,
            "steps": steps,
            "answer": f"可见台阶有{steps}级",
        }
