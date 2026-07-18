"""
行程综合（一）— 第46讲：快车提前到达 → 慢车剩余路程 = 速度差×快车用时。

上下两条平行全程线段：甲（慢）拆成 7小时+2小时；乙（快）全程 7小时。
竖虚线对齐甲车「7小时」分界，标出剩余路程与算式。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class TravelEarlyDiagramMixin:
    """甲乙同向同程：快车提前到达型线段图。"""

    def make_travel_early_diagram(
        self,
        draw_y: float,
        *,
        slow_hours: int = 9,
        early_hours: int = 2,
        speed_diff: int = 24,
        slow_name: str = "甲",
        fast_name: str = "乙",
        place_a: str = "A地",
        place_b: str = "B地",
        row_gap: float = 1.35,
        total_w: float = 7.2,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if early_hours <= 0 or early_hours >= slow_hours:
            raise ValueError("提前时间须为正且小于慢车用时")
        if speed_diff <= 0:
            raise ValueError("速度差须为正")

        fast_hours = slow_hours - early_hours
        remain_dist = speed_diff * fast_hours  # 24×7=168
        # 慢车速度 = 剩余路程 ÷ 提前时间；全程 = 慢速 × 慢车用时
        slow_speed = remain_dist // early_hours  # 84
        total_dist = slow_speed * slow_hours  # 756

        # 甲车：全程按时间比例拆成 fast_hours : early_hours
        split_w = total_w * fast_hours / slow_hours
        remain_w = total_w - split_w

        left_x = -total_w / 2
        split_x = left_x + split_w
        right_x = left_x + total_w
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        # 端点竖线 A / B
        dash_a = DashedLine(
            np.array([left_x, top_y + 0.42, 0]),
            np.array([left_x, bot_y - 0.42, 0]),
            color=GREY_B, stroke_width=1.8, dash_length=0.08,
        )
        dash_b = DashedLine(
            np.array([right_x, top_y + 0.42, 0]),
            np.array([right_x, bot_y - 0.42, 0]),
            color=GREY_B, stroke_width=1.8, dash_length=0.08,
        )
        # 甲车 7小时分界 ↔ 乙车仍在走同一时刻的对照
        dash_split = DashedLine(
            np.array([split_x, top_y + 0.48, 0]),
            np.array([split_x, bot_y - 0.35, 0]),
            color=YELLOW, stroke_width=2.2, dash_length=0.08,
        )
        guides = VGroup(dash_a, dash_b, dash_split)

        lab_a = self.safe_text(place_a, font_size=16, color=WHITE)
        lab_a.next_to(np.array([left_x, top_y, 0]), LEFT, buff=0.18)
        lab_b = self.safe_text(place_b, font_size=16, color=WHITE)
        lab_b.next_to(np.array([right_x, top_y, 0]), RIGHT, buff=0.18)
        place_labs = VGroup(lab_a, lab_b)

        def _tick(x: float, y: float, color) -> Line:
            return Line(
                np.array([x, y + tick_h, 0]),
                np.array([x, y - tick_h, 0]),
                color=color, stroke_width=line_stroke * 0.85,
            )

        # ── 甲（慢）上排：7小时 + 2小时 ──
        slow_color = TEAL_D
        remain_color = ORANGE
        slow_main = Line(
            np.array([left_x, top_y, 0]),
            np.array([split_x, top_y, 0]),
            color=slow_color, stroke_width=line_stroke,
        )
        slow_remain = Line(
            np.array([split_x, top_y, 0]),
            np.array([right_x, top_y, 0]),
            color=remain_color, stroke_width=line_stroke,
        )
        slow_ticks = VGroup(
            _tick(left_x, top_y, slow_color),
            _tick(split_x, top_y, YELLOW),
            _tick(right_x, top_y, remain_color),
        )
        slow_name_lab = self.safe_text(f"{slow_name}车", font_size=18, color=slow_color)
        slow_name_lab.next_to(np.array([(left_x + split_x) / 2, top_y, 0]), UP, buff=0.38)

        t7 = self.safe_text(f"{fast_hours}小时", font_size=16, color=slow_color)
        t7.next_to(slow_main, UP, buff=0.10)
        t2 = self.safe_text(f"{early_hours}小时", font_size=16, color=remain_color)
        t2.next_to(slow_remain, UP, buff=0.10)
        t2.set_opacity(0)

        # ── 乙（快）下排：全程 7小时 ──
        fast_color = BLUE
        fast_line = Line(
            np.array([left_x, bot_y, 0]),
            np.array([right_x, bot_y, 0]),
            color=fast_color, stroke_width=line_stroke,
        )
        fast_ticks = VGroup(
            _tick(left_x, bot_y, fast_color),
            _tick(right_x, bot_y, fast_color),
        )
        fast_name_lab = self.safe_text(f"{fast_name}车", font_size=18, color=fast_color)
        fast_name_lab.next_to(np.array([(left_x + right_x) / 2, bot_y, 0]), DOWN, buff=0.42)

        t7_fast = self.safe_text(f"{fast_hours}小时", font_size=16, color=fast_color)
        t7_fast.next_to(fast_line, DOWN, buff=0.10)
        t7_fast.set_opacity(0)

        slow_row = VGroup(
            slow_main, slow_remain, slow_ticks, slow_name_lab, t7, t2,
        )
        fast_row = VGroup(fast_line, fast_ticks, fast_name_lab, t7_fast)

        # 剩余路程括号 + 说明
        remain_brace = Brace(slow_remain, direction=DOWN, buff=0.08)
        remain_brace.set_color(remain_color)
        remain_brace.set_opacity(0)
        remain_q = self.safe_text("？千米", font_size=15, color=remain_color)
        remain_q.next_to(remain_brace, DOWN, buff=0.06)
        remain_q.set_opacity(0)
        remain_ans = self.safe_text(
            f"{speed_diff}×{fast_hours}={remain_dist}千米",
            font_size=15, color=YELLOW,
        )
        remain_ans.move_to(remain_q.get_center())
        remain_ans.set_opacity(0)
        remain_block = VGroup(remain_brace, remain_q, remain_ans)

        # 底部算式备注
        note_time = self.safe_text(
            f"乙用时：{slow_hours}−{early_hours}={fast_hours}（时）",
            font_size=16, color=GREY_B,
        )
        note_gap = self.safe_text(
            f"乙到达时，甲还剩：{speed_diff}×{fast_hours}={remain_dist}（千米）",
            font_size=16, color=WHITE,
        )
        note_total_q = self.safe_text(
            f"{remain_dist}÷{early_hours}×{slow_hours}=？",
            font_size=18, color=WHITE,
        )
        note_total_ans = self.safe_text(
            f"{remain_dist}÷{early_hours}×{slow_hours}={total_dist}（千米）",
            font_size=18, color=YELLOW,
        )
        for n in (note_time, note_gap, note_total_q, note_total_ans):
            n.set_opacity(0)
        notes = VGroup(note_time, note_gap, note_total_q, note_total_ans).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT,
        )
        notes.next_to(VGroup(slow_row, fast_row), DOWN, buff=0.55)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "快车提前到站时，多走的路程＝慢车还剩的路程",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.16)

        diagram = VGroup(
            guides, place_labs, slow_row, fast_row, remain_block, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "guides": guides,
            "dash_a": dash_a,
            "dash_b": dash_b,
            "dash_split": dash_split,
            "place_labs": place_labs,
            "lab_a": lab_a,
            "lab_b": lab_b,
            "slow_row": slow_row,
            "slow_main": slow_main,
            "slow_remain": slow_remain,
            "slow_ticks": slow_ticks,
            "slow_name_lab": slow_name_lab,
            "t7": t7,
            "t2": t2,
            "fast_row": fast_row,
            "fast_line": fast_line,
            "fast_ticks": fast_ticks,
            "fast_name_lab": fast_name_lab,
            "t7_fast": t7_fast,
            "remain_block": remain_block,
            "remain_brace": remain_brace,
            "remain_q": remain_q,
            "remain_ans": remain_ans,
            "notes": notes,
            "note_time": note_time,
            "note_gap": note_gap,
            "note_total_q": note_total_q,
            "note_total_ans": note_total_ans,
            "hint": hint,
            "slow_hours": slow_hours,
            "early_hours": early_hours,
            "fast_hours": fast_hours,
            "speed_diff": speed_diff,
            "remain_dist": remain_dist,
            "slow_speed": slow_speed,
            "total_dist": total_dist,
            "answer": f"A、B两地间的距离是{total_dist}千米",
        }
