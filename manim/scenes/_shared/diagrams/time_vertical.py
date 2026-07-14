"""
时间减法竖式 — 第11讲及同类题型。

终止时间在上、起始时间在下，时/分两列对齐，60 进制借位。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class TimeVerticalDiagramMixin:
    """时间问题：竖式求经过时间（终止 − 起始）。"""

    def _time_row_parts(
        self,
        hour: int,
        minute: int,
        *,
        num_size: int = 32,
        unit_size: int = 26,
        num_color=WHITE,
        unit_color=GREY_B,
    ) -> dict[str, Any]:
        hour_t = self.safe_text(str(hour), font_size=num_size, color=num_color)
        shi = self.safe_text("时", font_size=unit_size, color=unit_color)
        min_t = self.safe_text(str(minute), font_size=num_size, color=num_color)
        fen = self.safe_text("分", font_size=unit_size, color=unit_color)
        shi.move_to(ORIGIN)
        hour_t.next_to(shi, LEFT, buff=0.14)
        min_t.next_to(shi, RIGHT, buff=0.14)
        fen.next_to(min_t, RIGHT, buff=0.10)
        row = VGroup(hour_t, shi, min_t, fen)
        return {
            "row": row,
            "hour_t": hour_t,
            "shi": shi,
            "min_t": min_t,
            "fen": fen,
        }

    def make_time_subtract_vertical(
        self,
        end_h: int,
        end_m: int,
        start_h: int,
        start_m: int,
        draw_y: float,
        *,
        result_h: int | None = None,
        result_m: int | None = None,
        borrow_h_mark: int | None = None,
        borrow_m_mark: int | None = None,
    ) -> dict[str, Any]:
        """
        构建时间减法竖式（经过时间 = 终止 − 起始）。

        borrow_h_mark / borrow_m_mark: 借位后标注（如 9、81）；默认自动推算。
        """
        if result_h is None or result_m is None:
            # 默认按母题借位结果，调用方应传入准确值
            result_h = result_h if result_h is not None else 0
            result_m = result_m if result_m is not None else 0

        if borrow_h_mark is None:
            borrow_h_mark = end_h - 1 if end_m < start_m else end_h
        if borrow_m_mark is None:
            borrow_m_mark = end_m + 60 if end_m < start_m else end_m

        end_parts = self._time_row_parts(end_h, end_m)
        start_parts = self._time_row_parts(start_h, start_m)
        result_parts = self._time_row_parts(result_h, result_m, num_color=YELLOW)

        row_gap = 0.52
        end_parts["row"].move_to(np.array([0, row_gap, 0]))
        start_parts["row"].move_to(np.array([0, 0, 0]))
        result_parts["row"].move_to(np.array([0, -row_gap * 1.55, 0]))

        # 「时」列 x 对齐
        anchor_shi_x = end_parts["shi"].get_center()[0]
        for parts in (start_parts, result_parts):
            dx = anchor_shi_x - parts["shi"].get_center()[0]
            parts["row"].shift(RIGHT * dx)

        minus = self.safe_text("−", font_size=36, color=WHITE)
        minus.next_to(start_parts["row"], LEFT, buff=0.22)

        hline = Line(
            start_parts["row"].get_left() + LEFT * 0.08,
            start_parts["row"].get_right() + RIGHT * 0.18,
            color=WHITE, stroke_width=2,
        )
        hline.next_to(start_parts["row"], DOWN, buff=0.18)

        result_parts["row"].next_to(hline, DOWN, buff=0.22)
        dx_res = anchor_shi_x - result_parts["shi"].get_center()[0]
        result_parts["row"].shift(RIGHT * dx_res)

        borrow_h = self.safe_text(str(borrow_h_mark), font_size=20, color=TEAL_D)
        borrow_h.next_to(end_parts["hour_t"], UP, buff=0.32)
        borrow_m = self.safe_text(str(borrow_m_mark), font_size=20, color=TEAL_D)
        borrow_m.next_to(end_parts["min_t"], UP, buff=0.32)
        borrow_marks = VGroup(borrow_h, borrow_m)

        need_borrow_note = self.safe_text(
            f"{end_m} < {start_m}，分不够减", font_size=22, color=RED,
        )
        need_borrow_note.next_to(end_parts["min_t"], RIGHT, buff=0.55)

        hint = self.safe_text(
            "终止时间在上，起始时间在下，仿减法竖式计算",
            font_size=22, color=GREY_B,
        )

        vertical_core = VGroup(
            end_parts["row"], start_parts["row"],
            minus, hline, result_parts["row"],
        )
        hint.next_to(vertical_core, UP, buff=0.48)
        hint.shift(UP * 0.5)

        all_parts = VGroup(hint, vertical_core, borrow_marks, need_borrow_note)
        all_parts.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(all_parts)

        layout_row = VGroup(
            borrow_marks, end_parts["row"],
            start_parts["row"], minus, hline, result_parts["row"],
        )

        return {
            "diagram": all_parts,
            "hint": hint,
            "end_row": end_parts["row"],
            "end_hour_t": end_parts["hour_t"],
            "end_min_t": end_parts["min_t"],
            "start_row": start_parts["row"],
            "start_hour_t": start_parts["hour_t"],
            "start_min_t": start_parts["min_t"],
            "minus_sign": minus,
            "hline": hline,
            "borrow_marks": borrow_marks,
            "borrow_h": borrow_h,
            "borrow_m": borrow_m,
            "result_row": result_parts["row"],
            "result_hour_t": result_parts["hour_t"],
            "result_min_t": result_parts["min_t"],
            "hour_col": VGroup(end_parts["hour_t"], start_parts["hour_t"], result_parts["hour_t"]),
            "min_col": VGroup(end_parts["min_t"], start_parts["min_t"], result_parts["min_t"]),
            "need_borrow_note": need_borrow_note,
            "layout_row": layout_row,
            "vertical_core": vertical_core,
        }
