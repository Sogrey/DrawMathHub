"""
周期问题（珠子）图解 — 第21讲及同类题型。

约定：仅本模块维护周期珠子相关逻辑；勿在 lesson_base 内联修改。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class PeriodDiagramMixin:
    """周期问题：上层规律预览 + 中层说明 + 下层分组示意。"""

    def _bead_circle(self, radius: float, color, *, stroke_width: int = 2) -> Circle:
        c = Circle(radius=radius, color=color, stroke_width=stroke_width)
        c.set_fill(color, opacity=0.85)
        return c

    def _make_bead_group(
        self,
        colors: list,
        *,
        bead_r: float,
        bead_gap: float,
        label: str | None = None,
        box_color=GREY_B,
    ) -> dict[str, Any]:
        beads = VGroup(*[
            self._bead_circle(bead_r, c) for c in colors
        ]).arrange(RIGHT, buff=bead_gap)
        box = DashedVMobject(
            SurroundingRectangle(beads, color=box_color, buff=0.10, corner_radius=0.06),
            num_dashes=14,
        )
        box.set_stroke(box_color, width=1.5, opacity=0.75)
        # 珠子与虚线框必须成块，不可 arrange 拆开（否则框会漂到珠子下方）
        bead_block = VGroup(beads, box)
        group_label = None
        if label:
            group_label = self.safe_text(label, font_size=20, color=YELLOW)
            group_label.next_to(bead_block, UP, buff=0.12)
            unit = VGroup(group_label, bead_block).arrange(DOWN, buff=0.10, aligned_edge=ORIGIN)
        else:
            unit = bead_block
        return {
            "beads": beads,
            "box": box,
            "label": group_label,
            "unit": unit,
            "group": unit,
        }

    def make_period_bead_diagram(
        self,
        pattern_colors: list,
        pattern_names: list[str],
        total_index: int,
        draw_y: float,
        *,
        draw_area_top: float | None = None,
        draw_area_bottom: float | None = None,
        step_y: float | None = None,
        preview_bead_r: float = 0.17,
        group_bead_r: float = 0.13,
        preview_bead_gap: float = 0.09,
        bead_gap: float = 0.07,
        group_gap: float = 0.20,
        head_group_count: int = 2,
        tail_group_label: str = "第6组",
    ) -> dict[str, Any]:
        period = len(pattern_colors)
        full_groups = total_index // period
        remainder = total_index % period
        target_pos = remainder if remainder > 0 else period

        preview_colors = pattern_colors * 2
        preview_beads = VGroup(*[
            self._bead_circle(preview_bead_r, c, stroke_width=2) for c in preview_colors
        ]).arrange(RIGHT, buff=preview_bead_gap)
        preview_line = Line(
            preview_beads.get_left() + LEFT * 0.08 + DOWN * (preview_bead_r + 0.06),
            preview_beads.get_right() + RIGHT * 0.08 + DOWN * (preview_bead_r + 0.06),
            color=GREY_B, stroke_width=1.5, stroke_opacity=0.45,
        )
        preview = VGroup(preview_line, preview_beads)

        pattern_hint = self.safe_text(
            "，".join(pattern_names) + "，重复出现",
            font_size=20, color=WHITE,
        )
        header = VGroup(preview, pattern_hint).arrange(DOWN, buff=0.16, aligned_edge=ORIGIN)

        row_parts: list[Mobject] = []
        group_infos: list[dict[str, Any]] = []
        for i in range(head_group_count):
            info = self._make_bead_group(
                pattern_colors, bead_r=group_bead_r, bead_gap=bead_gap,
                label=f"第{i + 1}组",
            )
            group_infos.append(info)
            row_parts.append(info["unit"])

        ellipsis = self._horizontal_ellipsis(color=GREY_B, dot_r=0.06, count=3, buff=0.10)

        tail_info = self._make_bead_group(
            pattern_colors, bead_r=group_bead_r, bead_gap=bead_gap,
            label=tail_group_label,
        )
        group_infos.append(tail_info)
        row_parts.append(tail_info["unit"])

        rem_colors = pattern_colors[:remainder] if remainder > 0 else []
        rem_beads = VGroup(*[
            self._bead_circle(group_bead_r, c, stroke_width=2) for c in rem_colors
        ]).arrange(RIGHT, buff=bead_gap) if rem_colors else VGroup()
        rem_box = None
        rem_unit = None
        if len(rem_beads) > 0:
            rem_box = DashedVMobject(
                SurroundingRectangle(rem_beads, color=GREY_B, buff=0.08, corner_radius=0.06),
                num_dashes=10,
            )
            rem_box.set_stroke(GREY_B, width=1.5, opacity=0.55)
            rem_unit = VGroup(rem_beads, rem_box)
            row_parts.append(rem_unit)

        grouped_row = VGroup(
            row_parts[0], row_parts[1], ellipsis, *row_parts[2:],
        ).arrange(RIGHT, buff=group_gap, aligned_edge=DOWN)

        # 预览区保持原位；仅把算式/分组等下方内容下移拉开间距
        grouped_row.next_to(header, DOWN, buff=0.52)
        stack = VGroup(header, grouped_row)
        stack.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(stack)

        target_bead = rem_beads[target_pos - 1] if remainder > 0 else tail_info["beads"][-1]
        target_color_name = pattern_names[target_pos - 1]

        return {
            "diagram": stack,
            "stack": stack,
            "header": header,
            "preview": preview,
            "preview_beads": preview_beads,
            "preview_line": preview_line,
            "pattern_hint": pattern_hint,
            "grouped_row": grouped_row,
            "group_infos": group_infos,
            "ellipsis": ellipsis,
            "rem_beads": rem_beads,
            "rem_box": rem_box,
            "rem_unit": rem_unit,
            "target_bead": target_bead,
            "target_color_name": target_color_name,
            "period": period,
            "full_groups": full_groups,
            "remainder": remainder,
            "target_pos": target_pos,
            "preview_bead_r": preview_bead_r,
            "group_bead_r": group_bead_r,
        }

    def pack_period_diagram(
        self,
        diag: dict[str, Any],
        draw_y: float,
        *,
        div_label: Mobject | None = None,
        color_hint: Mobject | None = None,
        draw_area_top: float | None = None,
        header_to_div_buff: float = 0.26,
        div_to_group_buff: float = 0.30,
        group_to_hint_buff: float = 0.20,
    ) -> VGroup:
        """将图解部件压紧为纵向栈；标注已挂在 grouped_row 内时随整体缩放。"""
        header = diag["header"]
        header_top = header.get_top()[1]
        parts: list[Mobject] = [header]
        cursor = header

        if div_label is not None:
            div_label.next_to(cursor, DOWN, buff=header_to_div_buff)
            parts.append(div_label)
            cursor = div_label

        diag["grouped_row"].next_to(cursor, DOWN, buff=div_to_group_buff if div_label else 0.52)
        parts.append(diag["grouped_row"])

        if color_hint is not None:
            color_hint.next_to(diag["grouped_row"], DOWN, buff=group_to_hint_buff)
            parts.append(color_hint)

        stack = VGroup(*parts)
        # 固定预览区顶边不动，只重排下方图层
        stack.shift(UP * (header_top - stack.get_top()[1]))
        self.clamp_content(stack)
        return stack
