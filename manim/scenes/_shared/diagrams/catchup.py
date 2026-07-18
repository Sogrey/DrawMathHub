"""
追及问题 — 第28讲：同向追及，追及时间 = 路程差 ÷ 速度差。

上下两条平行线段：上方为被追者，下方为追赶者；终点同在「追上」处。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class CatchupDiagramMixin:
    """追及问题：同向而行线段图。"""

    def make_catchup_diagram(
        self,
        draw_y: float,
        *,
        chaser_speed: int = 80,
        ahead_speed: int = 50,
        gap: int = 150,
        chaser_name: str = "方方",
        ahead_name: str = "乐乐",
        row_gap: float = 0.95,
        total_w: float = 6.8,
        line_stroke: float = 4.0,
        tick_h: float = 0.12,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "米",
        time_unit: str = "分",
    ) -> dict[str, Any]:
        if chaser_speed <= ahead_speed or gap <= 0:
            raise ValueError("追赶者须更快，且路程差为正")

        speed_diff = chaser_speed - ahead_speed
        if gap % speed_diff != 0:
            raise ValueError("本讲示例要求路程差能被速度差整除")
        meet_time = gap // speed_diff

        chaser_dist = chaser_speed * meet_time
        ahead_dist = ahead_speed * meet_time

        # 以追赶者全程为总长
        chaser_w = total_w
        gap_w = total_w * gap / chaser_dist
        ahead_w = total_w * ahead_dist / chaser_dist

        left_x = -total_w / 2
        catch_x = left_x + chaser_w
        ahead_start_x = left_x + gap_w
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        # 竖虚线：追赶起点 / 前方起点 / 追上点
        dash_start = DashedLine(
            np.array([left_x, top_y + 0.35, 0]),
            np.array([left_x, bot_y - 0.35, 0]),
            color=GREY_B, stroke_width=1.8, dash_length=0.08,
        )
        dash_ahead = DashedLine(
            np.array([ahead_start_x, top_y + 0.35, 0]),
            np.array([ahead_start_x, bot_y - 0.35, 0]),
            color=GREY_B, stroke_width=1.8, dash_length=0.08,
        )
        dash_catch = DashedLine(
            np.array([catch_x, top_y + 0.45, 0]),
            np.array([catch_x, bot_y - 0.45, 0]),
            color=YELLOW, stroke_width=2.2, dash_length=0.08,
        )
        guides = VGroup(dash_start, dash_ahead, dash_catch)

        # 上方：被追者
        ahead_line = Line(
            np.array([ahead_start_x, top_y, 0]),
            np.array([catch_x, top_y, 0]),
            color=ORANGE, stroke_width=line_stroke,
        )
        ahead_ticks = VGroup(
            Line(
                np.array([ahead_start_x, top_y + tick_h, 0]),
                np.array([ahead_start_x, top_y - tick_h, 0]),
                color=ORANGE, stroke_width=line_stroke * 0.85,
            ),
            Line(
                np.array([catch_x, top_y + tick_h, 0]),
                np.array([catch_x, top_y - tick_h, 0]),
                color=ORANGE, stroke_width=line_stroke * 0.85,
            ),
        )
        ahead_arrow = Arrow(
            np.array([ahead_start_x + 0.15, top_y, 0]),
            np.array([catch_x - 0.08, top_y, 0]),
            buff=0, stroke_width=3, color=ORANGE,
            max_tip_length_to_length_ratio=0.12, tip_length=0.18,
        )
        ahead_name_lab = self.safe_text(ahead_name, font_size=18, color=ORANGE)
        ahead_name_lab.next_to(np.array([ahead_start_x, top_y, 0]), LEFT, buff=0.18)
        ahead_speed_lab = self.safe_text(
            f"每分钟 {ahead_speed} {unit_label}",
            font_size=14, color=ORANGE,
        )
        ahead_speed_lab.next_to(ahead_line, UP, buff=0.14)

        # 下方：追赶者
        chaser_line = Line(
            np.array([left_x, bot_y, 0]),
            np.array([catch_x, bot_y, 0]),
            color=TEAL_D, stroke_width=line_stroke,
        )
        chaser_ticks = VGroup(
            Line(
                np.array([left_x, bot_y + tick_h, 0]),
                np.array([left_x, bot_y - tick_h, 0]),
                color=TEAL_D, stroke_width=line_stroke * 0.85,
            ),
            Line(
                np.array([catch_x, bot_y + tick_h, 0]),
                np.array([catch_x, bot_y - tick_h, 0]),
                color=TEAL_D, stroke_width=line_stroke * 0.85,
            ),
        )
        chaser_arrow = Arrow(
            np.array([left_x + 0.15, bot_y, 0]),
            np.array([catch_x - 0.08, bot_y, 0]),
            buff=0, stroke_width=3, color=TEAL_D,
            max_tip_length_to_length_ratio=0.10, tip_length=0.18,
        )
        chaser_name_lab = self.safe_text(chaser_name, font_size=18, color=TEAL_D)
        chaser_name_lab.next_to(np.array([left_x, bot_y, 0]), LEFT, buff=0.18)
        chaser_speed_lab = self.safe_text(
            f"每分钟 {chaser_speed} {unit_label}",
            font_size=14, color=TEAL_D,
        )
        chaser_speed_lab.next_to(chaser_line, DOWN, buff=0.14)

        # 路程差括号（两起点之间，放在两行中间）
        gap_mid_y = (top_y + bot_y) / 2
        gap_brace_span = Line(
            np.array([left_x, gap_mid_y, 0]),
            np.array([ahead_start_x, gap_mid_y, 0]),
        )
        gap_brace = Brace(gap_brace_span, direction=UP, buff=0.02)
        gap_brace.set_color(YELLOW)
        gap_lab = self.safe_text(f"{gap} {unit_label}", font_size=18, color=YELLOW)
        gap_lab.next_to(gap_brace, UP, buff=0.04)
        gap_block = VGroup(gap_brace, gap_lab)

        catch_tag = self.safe_text("追上", font_size=18, color=YELLOW)
        catch_tag.next_to(np.array([catch_x, top_y, 0]), UP, buff=0.22)

        # 速度差与时间（组内定位，opacity 切换）
        note_diff = self.safe_text(
            f"速度差：{chaser_speed}−{ahead_speed}={speed_diff}（{unit_label}/分）",
            font_size=16, color=ORANGE,
        )
        note_time_q = self.safe_text(
            f"追及时间：{gap}÷{speed_diff}=?（{time_unit}）",
            font_size=16, color=YELLOW,
        )
        note_time_ans = self.safe_text(
            f"追及时间：{gap}÷{speed_diff}={meet_time}（{time_unit}）",
            font_size=16, color=YELLOW,
        )
        note_time_q.next_to(note_diff, DOWN, buff=0.14)
        note_time_ans.next_to(note_diff, DOWN, buff=0.14)
        note_time_ans.set_opacity(0)
        note_diff.set_opacity(0)
        note_time_q.set_opacity(0)
        notes = VGroup(note_diff, note_time_q, note_time_ans)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "同向追及：路程差 ÷ 速度差 = 追及时间",
                font_size=16, color=GREY_B,
            )

        ahead_row = VGroup(
            ahead_line, ahead_ticks, ahead_arrow,
            ahead_name_lab, ahead_speed_lab,
        )
        chaser_row = VGroup(
            chaser_line, chaser_ticks, chaser_arrow,
            chaser_name_lab, chaser_speed_lab,
        )
        annotated = VGroup(
            guides, ahead_row, chaser_row,
            gap_block, catch_tag, notes,
        )
        layout_row = VGroup(annotated)
        if show_hint:
            notes.next_to(VGroup(ahead_row, chaser_row), DOWN, buff=0.32)
            hint.next_to(notes, DOWN, buff=0.16)
            layout_row = VGroup(annotated, hint)
        else:
            notes.next_to(VGroup(ahead_row, chaser_row), DOWN, buff=0.32)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "guides": guides,
            "dash_start": dash_start,
            "dash_ahead": dash_ahead,
            "dash_catch": dash_catch,
            "ahead_row": ahead_row,
            "chaser_row": chaser_row,
            "ahead_line": ahead_line,
            "chaser_line": chaser_line,
            "ahead_arrow": ahead_arrow,
            "chaser_arrow": chaser_arrow,
            "ahead_name_lab": ahead_name_lab,
            "chaser_name_lab": chaser_name_lab,
            "ahead_speed_lab": ahead_speed_lab,
            "chaser_speed_lab": chaser_speed_lab,
            "ahead_ticks": ahead_ticks,
            "chaser_ticks": chaser_ticks,
            "gap_block": gap_block,
            "catch_tag": catch_tag,
            "notes": notes,
            "note_diff": note_diff,
            "note_time_q": note_time_q,
            "note_time_ans": note_time_ans,
            "hint": hint,
            "chaser_speed": chaser_speed,
            "ahead_speed": ahead_speed,
            "gap": gap,
            "speed_diff": speed_diff,
            "meet_time": meet_time,
            "chaser_dist": chaser_dist,
            "ahead_dist": ahead_dist,
            "unit_label": unit_label,
            "time_unit": time_unit,
        }
