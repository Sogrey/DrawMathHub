"""
最优化问题 — 第34讲：流程图法（合理安排时间）。

上方：洗衣机 → 晾衣服（串行关键路径）；
下方：扫地 → 拖地 → 擦桌子（与洗衣并行）。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class ChoresFlowDiagramMixin:
    """家务时间安排流程图：并行 + 串行关键路径。"""

    def _make_task_box(
        self,
        line1: str,
        line2: str,
        *,
        width: float | None = None,
        color=WHITE,
        font_size: int = 16,
    ) -> VGroup:
        t1 = self.safe_text(line1, font_size=font_size, color=color)
        t2 = self.safe_text(line2, font_size=font_size - 1, color=GREY_B)
        label = VGroup(t1, t2).arrange(DOWN, buff=0.08)
        pad_x, pad_y = 0.28, 0.18
        w = width if width is not None else label.width + pad_x * 2
        h = label.height + pad_y * 2
        box = RoundedRectangle(
            width=w, height=h,
            corner_radius=0.06,
            stroke_width=2.0,
            stroke_color=color,
            fill_opacity=0,
        )
        # 虚线框感：改用 DashedVMobject 包住实线矩形更稳
        dashed = DashedVMobject(box, num_dashes=max(16, int(w * 8)))
        label.move_to(dashed.get_center())
        return VGroup(dashed, label)

    def make_chores_flow_diagram(
        self,
        draw_y: float,
        *,
        wash: int = 30,
        hang: int = 3,
        sweep: int = 8,
        mop: int = 10,
        wipe: int = 5,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "分钟",
    ) -> dict[str, Any]:
        manual_sum = sweep + mop + wipe
        total = wash + hang  # 关键路径（手动之和 < 洗衣）
        if manual_sum > wash:
            # 仍按教材：若手动更长，总时间应为 manual_sum + hang；本母题不会
            total = manual_sum + hang

        wash_box = self._make_task_box(
            "洗衣机洗衣服", f"{wash} {unit_label}", color=TEAL_D, font_size=15,
        )
        hang_box = self._make_task_box(
            "晾衣服", f"{hang} {unit_label}", color=ORANGE, font_size=15,
        )
        sweep_box = self._make_task_box(
            "扫地", f"{sweep} {unit_label}", color=WHITE, font_size=14,
        )
        mop_box = self._make_task_box(
            "拖地", f"{mop} {unit_label}", color=WHITE, font_size=14,
        )
        wipe_box = self._make_task_box(
            "擦桌子", f"{wipe} {unit_label}", color=WHITE, font_size=14,
        )

        # 上行：洗衣 → 晾衣
        top_arrow = Arrow(
            LEFT, RIGHT, buff=0.08,
            stroke_width=3, color=GREY_B,
            max_tip_length_to_length_ratio=0.25, tip_length=0.14,
        )
        top_arrow.set_width(0.45)
        top_row = VGroup(wash_box, top_arrow, hang_box).arrange(RIGHT, buff=0.22)

        # 下行：扫地 → 拖地 → 擦桌子
        a1 = Arrow(
            LEFT, RIGHT, buff=0.06,
            stroke_width=2.5, color=GREY_B,
            max_tip_length_to_length_ratio=0.28, tip_length=0.12,
        )
        a1.set_width(0.32)
        a2 = a1.copy()
        bottom_inner = VGroup(sweep_box, a1, mop_box, a2, wipe_box).arrange(
            RIGHT, buff=0.14,
        )
        bottom_frame = DashedVMobject(
            SurroundingRectangle(
                bottom_inner, buff=0.16, color=GREY_B, stroke_width=1.8,
                corner_radius=0.08,
            ),
            num_dashes=36,
        )
        bottom_block = VGroup(bottom_frame, bottom_inner)

        # 上下对齐：下行与洗衣盒水平居中对齐
        bottom_block.next_to(wash_box, DOWN, buff=0.55)
        bottom_block.align_to(wash_box, LEFT)
        # 微调：使底行大致落在洗衣宽度下方
        if bottom_block.width < wash_box.width * 1.15:
            bottom_block.move_to(
                np.array([wash_box.get_center()[0], bottom_block.get_center()[1], 0])
            )

        # 竖线表示「洗衣期间」并行
        link_top = wash_box.get_bottom()
        link_bot = bottom_block.get_top()
        parallel_link = Line(
            np.array([wash_box.get_center()[0], link_top[1], 0]),
            np.array([wash_box.get_center()[0], link_bot[1], 0]),
            color=YELLOW, stroke_width=2.5,
        )
        # 短横 tip
        tick_l = Line(
            parallel_link.get_end() + LEFT * 0.12,
            parallel_link.get_end() + RIGHT * 0.12,
            color=YELLOW, stroke_width=2.5,
        )

        parallel_note = self.safe_text(
            "洗衣同时可做",
            font_size=13, color=YELLOW,
        )
        parallel_note.next_to(parallel_link, RIGHT, buff=0.10)

        flow = VGroup(
            top_row, bottom_block, parallel_link, tick_l, parallel_note,
        )

        # 推理批注
        note_fit = self.safe_text(
            f"扫地＋拖地＋擦桌子＝{manual_sum} ＜ {wash}（洗衣）",
            font_size=15, color=GREY_B,
        )
        note_path = self.safe_text(
            "关键路径：洗衣 → 晾衣服",
            font_size=15, color=TEAL_D,
        )
        note_calc_q = self.safe_text(
            f"至少：{wash}＋{hang}=?",
            font_size=16, color=YELLOW,
        )
        note_calc_ans = self.safe_text(
            f"至少：{wash}＋{hang}={total}（分）",
            font_size=16, color=YELLOW,
        )
        for m in (note_fit, note_path, note_calc_q, note_calc_ans):
            m.set_opacity(0)

        notes = VGroup(note_fit, note_path, note_calc_q, note_calc_ans)
        note_fit.next_to(flow, DOWN, buff=0.28)
        note_path.next_to(note_fit, DOWN, buff=0.10)
        note_calc_q.next_to(note_path, DOWN, buff=0.10)
        note_calc_ans.move_to(note_calc_q)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "能同时做的事尽量同时做，取最长并行段＋后续串行",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(flow, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "flow": flow,
            "top_row": top_row,
            "wash_box": wash_box,
            "hang_box": hang_box,
            "top_arrow": top_arrow,
            "bottom_block": bottom_block,
            "bottom_inner": bottom_inner,
            "sweep_box": sweep_box,
            "mop_box": mop_box,
            "wipe_box": wipe_box,
            "parallel_link": VGroup(parallel_link, tick_l),
            "parallel_note": parallel_note,
            "notes": notes,
            "note_fit": note_fit,
            "note_path": note_path,
            "note_calc_q": note_calc_q,
            "note_calc_ans": note_calc_ans,
            "hint": hint,
            "wash": wash,
            "hang": hang,
            "sweep": sweep,
            "mop": mop,
            "wipe": wipe,
            "manual_sum": manual_sum,
            "total": total,
            "unit_label": unit_label,
        }
