"""
重叠问题 — 第20讲及同类：多根等长木条搭接求每段重叠长。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class OverlapDiagramMixin:
    """重叠问题：几根木条串接，标原长、总长与重叠段。"""

    def make_overlap_bars_diagram(
        self,
        draw_y: float,
        *,
        piece_len: int = 60,
        count: int = 3,
        joined_len: int = 140,
        unit_label: str = "厘米",
        bar_h: float = 0.28,
        row_gap: float = 0.42,
        joined_w: float = 5.2,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if count < 2:
            raise ValueError("count 必须 ≥ 2")
        overlaps_n = count - 1
        raw_total = piece_len * count
        overlap_total = raw_total - joined_len
        if overlap_total <= 0 or overlap_total % overlaps_n != 0:
            # 允许非整除时仍按浮点比例画图
            one_overlap = overlap_total / overlaps_n
        else:
            one_overlap = overlap_total // overlaps_n

        unit = joined_w / joined_len
        piece_w = piece_len * unit
        ov_w = one_overlap * unit
        step = piece_w - ov_w  # 相邻木条起点间距

        # 以拼成后总长居中
        left0 = -joined_w / 2
        top_y = (count - 1) * row_gap / 2

        bars: list[Mobject] = []
        bar_groups = VGroup()
        for i in range(count):
            x0 = left0 + i * step
            y = top_y - i * row_gap
            bar = RoundedRectangle(
                width=piece_w,
                height=bar_h,
                corner_radius=0.06,
                color=BLUE_B,
                stroke_width=2,
            )
            bar.set_fill(BLUE_B, opacity=0.28)
            bar.move_to(np.array([x0 + piece_w / 2, y, 0]))
            bars.append(bar)
            bar_groups.add(bar)

        # 重叠区高亮（半透明）
        ov_highlights = VGroup()
        for i in range(overlaps_n):
            x0 = left0 + (i + 1) * step  # 下一根起点 = 重叠区左端
            y_mid = (top_y - i * row_gap + top_y - (i + 1) * row_gap) / 2
            hi = RoundedRectangle(
                width=ov_w,
                height=bar_h * 2 + row_gap * 0.35,
                corner_radius=0.05,
                color=ORANGE,
                stroke_width=1.5,
            )
            hi.set_fill(ORANGE, opacity=0.22)
            hi.move_to(np.array([x0 + ov_w / 2, y_mid, 0]))
            ov_highlights.add(hi)

        # 第一根上方：单根长度
        piece_span = Line(
            bars[0].get_left() + UP * 0.02,
            bars[0].get_right() + UP * 0.02,
        )
        piece_brace = Brace(piece_span, direction=UP, buff=0.10)
        piece_brace.set_color(TEAL_D)
        piece_label = self.safe_text(
            f"{piece_len} {unit_label}",
            font_size=18, color=TEAL_D,
        )
        piece_label.next_to(piece_brace, UP, buff=0.06)
        piece_block = VGroup(piece_brace, piece_label)

        # 第一处重叠上方：?
        ov0_left = left0 + step
        ov_span = Line(
            np.array([ov0_left, top_y + bar_h / 2 + 0.06, 0]),
            np.array([ov0_left + ov_w, top_y + bar_h / 2 + 0.06, 0]),
        )
        ov_brace = Brace(ov_span, direction=UP, buff=0.08)
        ov_brace.set_color(ORANGE)
        ov_q = self.safe_text(f"? {unit_label}", font_size=16, color=ORANGE)
        ov_q.next_to(ov_brace, UP, buff=0.05)
        ov_ans = self.safe_text(
            f"{int(one_overlap) if one_overlap == int(one_overlap) else one_overlap} {unit_label}",
            font_size=16, color=ORANGE,
        )
        ov_ans.move_to(ov_q.get_center())
        ov_block = VGroup(ov_brace, ov_q)

        # 下方总长
        total_span = Line(
            np.array([left0, top_y - (count - 1) * row_gap - bar_h / 2 - 0.08, 0]),
            np.array([left0 + joined_w, top_y - (count - 1) * row_gap - bar_h / 2 - 0.08, 0]),
        )
        total_brace = Brace(total_span, direction=DOWN, buff=0.10)
        total_brace.set_color(YELLOW)
        total_label = self.safe_text(
            f"{joined_len} {unit_label}",
            font_size=18, color=YELLOW,
        )
        total_label.next_to(total_brace, DOWN, buff=0.06)
        total_block = VGroup(total_brace, total_label)

        count_note = self.safe_text(
            f"{count} 根木条 → {overlaps_n} 处重叠",
            font_size=16, color=GREY_B,
        )

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "拼成长度 = 原总长 − 各段重叠之和",
                font_size=17, color=GREY_B,
            )

        bars_core = VGroup(bar_groups)
        annotated = VGroup(
            bars_core, ov_highlights, piece_block, ov_block, total_block, count_note,
        )
        # count_note / hint 位置
        count_note.next_to(total_block, DOWN, buff=0.18)
        layout_row = VGroup(annotated)
        if show_hint:
            hint.next_to(count_note, DOWN, buff=0.12)
            layout_row = VGroup(annotated, hint)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "bars": bars,
            "bar_groups": bar_groups,
            "ov_highlights": ov_highlights,
            "piece_block": piece_block,
            "ov_block": ov_block,
            "ov_brace": ov_brace,
            "ov_q": ov_q,
            "ov_ans": ov_ans,
            "total_block": total_block,
            "count_note": count_note,
            "hint": hint,
            "piece_len": piece_len,
            "count": count,
            "joined_len": joined_len,
            "overlaps_n": overlaps_n,
            "raw_total": raw_total,
            "overlap_total": overlap_total,
            "one_overlap": int(one_overlap) if one_overlap == int(one_overlap) else one_overlap,
            "unit_label": unit_label,
        }
