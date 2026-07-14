"""
爬井问题图解 — 第7讲及同类题型。

左→右分区：一天循环 | 竖井+蜗牛 | 各天箭头列 | 第5天+算式
"""

from __future__ import annotations

from typing import Any

import numpy as np

from diagrams.icon_assets import load_icon_png  # noqa: E402
from manim import *  # noqa: F403


class WellClimbDiagramMixin:
    """蜗牛爬井：参数化井深、上爬、下滑，自动算天数与刻度。"""

    SNAIL_ICON = "animals/snail.png"
    WELL_UNIT_H = 0.38
    SNAIL_HEIGHT = 0.76
    SNAIL_OFFSET_X = -0.62

    def _well_y(self, meters: float, unit_h: float) -> float:
        return meters * unit_h

    def _place_snail(
        self,
        snail: Mobject,
        well_x: float,
        meters: float,
        unit_h: float,
        *,
        offset_x: float | None = None,
    ) -> None:
        y = self._well_y(meters, unit_h)
        ox = self.SNAIL_OFFSET_X if offset_x is None else offset_x
        snail.move_to(np.array([well_x + ox, y + 0.05, 0]))

    def _dual_side_day_arrows(
        self,
        axis_x: float,
        start_y: float,
        climb_top_y: float,
        end_y: float,
        *,
        side_offset: float = 0.14,
        climb_color=TEAL_D,
        slide_color=ORANGE,
        stroke_width: float = 2.0,
        with_axis: bool = True,
        axis_color=GREY_B,
    ) -> tuple[Arrow, Arrow, VGroup | None]:
        """竖线轴居中，白天上爬画左侧，晚上下滑画右侧。"""
        climb_arrow = Arrow(
            np.array([axis_x - side_offset, start_y, 0]),
            np.array([axis_x - side_offset, climb_top_y, 0]),
            color=climb_color, stroke_width=stroke_width, buff=0,
            max_tip_length_to_length_ratio=0.14,
        )
        slide_arrow = Arrow(
            np.array([axis_x + side_offset, climb_top_y, 0]),
            np.array([axis_x + side_offset, end_y, 0]),
            color=slide_color, stroke_width=stroke_width, buff=0,
            max_tip_length_to_length_ratio=0.14,
        )
        axis_line = None
        if with_axis:
            axis_top = max(climb_top_y, end_y) + 0.04
            axis_line = VGroup(
                Line(
                    np.array([axis_x, start_y, 0]),
                    np.array([axis_x, axis_top, 0]),
                    color=axis_color, stroke_width=1.6,
                ),
                Line(
                    np.array([axis_x - 0.10, start_y, 0]),
                    np.array([axis_x + 0.10, start_y, 0]),
                    color=axis_color, stroke_width=1.4,
                ),
            )
        return climb_arrow, slide_arrow, axis_line

    def _axis_meter_ticks(
        self,
        axis_x: float,
        unit_h: float,
        max_meter: int,
        *,
        tick_half: float = 0.11,
        font_size: int = 13,
        label_buff: float = 0.07,
        tick_color=GREY_B,
        label_color=GREY_B,
    ) -> VGroup:
        """竖轴刻度：0米 ~ max_meter米。"""
        ticks = VGroup()
        for m in range(max_meter + 1):
            y = self._well_y(m, unit_h)
            tick = Line(
                np.array([axis_x - tick_half, y, 0]),
                np.array([axis_x + tick_half, y, 0]),
                color=tick_color, stroke_width=1.5,
            )
            lbl = self.safe_text(f"{m}米", font_size=font_size, color=label_color)
            lbl.next_to(tick, LEFT, buff=label_buff)
            ticks.add(VGroup(tick, lbl))
        return ticks

    def _sync_block_floor_to_well(
        self,
        block: Mobject,
        well_line: Line,
        unit_h: float,
    ) -> None:
        """把 block 的 0 米刻度与井竖轴井底对齐（只调 y）。"""
        floor_y = well_line.get_bottom()[1]
        block.shift(np.array([0.0, floor_y - self._well_y(0.0, unit_h), 0.0]))

    def _place_right_of(
        self,
        block: Mobject,
        anchor: Mobject,
        *,
        buff: float,
    ) -> None:
        """仅水平排布，不改变 block 已有的竖向坐标。"""
        block.shift(
            np.array([anchor.get_right()[0] + buff - block.get_left()[0], 0.0, 0.0]),
        )

    def _guide_to_well_axis(
        self,
        well_x: float,
        y: float,
        target_x: float,
        *,
        color=YELLOW,
        stroke_opacity: float = 0.7,
    ) -> DashedLine:
        """引导虚线：从主井竖轴连到每日箭头列。"""
        left_x = min(well_x, target_x)
        right_x = max(well_x, target_x)
        return DashedLine(
            np.array([left_x, y, 0]),
            np.array([right_x, y, 0]),
            color=color, stroke_width=1.2, dash_length=0.05,
            stroke_opacity=stroke_opacity,
        )

    def _arrange_preserve_y(
        self,
        items: list[Mobject],
        *,
        buff: float,
        start_x: float = 0.0,
    ) -> VGroup:
        """横向排布，不改变各元素已有的竖向坐标。"""
        group = VGroup(*items)
        if not items:
            return group
        x = start_x
        for item in items:
            item.move_to(
                np.array([x + item.width / 2, item.get_center()[1], 0]),
            )
            x += item.width + buff
        return group

    def _make_day_cycle_panel(
        self,
        climb: int,
        slide: int,
        unit_h: float,
        *,
        cycle_scale: float = 1.0,
    ) -> tuple[VGroup, Mobject]:
        """最左区：加高竖轴 + 米刻度，两侧分别画上爬 / 下滑。"""
        u = unit_h * cycle_scale
        base_y = 0.0
        axis_x = 0.0
        side_offset = 0.18
        climb_top_y = base_y + climb * u
        slide_end_y = climb_top_y - slide * u
        axis_top = climb_top_y + u * 0.12

        main_axis = Line(
            np.array([axis_x, base_y, 0]),
            np.array([axis_x, axis_top, 0]),
            color=WHITE, stroke_width=2.4,
        )
        bottom_cap = Line(
            np.array([axis_x - 0.14, base_y, 0]),
            np.array([axis_x + 0.14, base_y, 0]),
            color=WHITE, stroke_width=2.0,
        )
        meter_ticks = self._axis_meter_ticks(
            axis_x, u, climb,
            tick_half=0.12, font_size=14, label_buff=0.08,
            tick_color=GREY_B, label_color=GREY_B,
        )

        climb_arrow, slide_arrow, _ = self._dual_side_day_arrows(
            axis_x, base_y, climb_top_y, slide_end_y,
            side_offset=side_offset, stroke_width=2.6,
            with_axis=False,
        )
        climb_lbl = self.safe_text(f"向上爬{climb}米", font_size=15, color=TEAL_D)
        climb_lbl.next_to(climb_arrow, LEFT, buff=0.08)
        slide_lbl = self.safe_text(f"向下滑{slide}米", font_size=15, color=ORANGE)
        slide_lbl.next_to(slide_arrow, RIGHT, buff=0.08)

        net = climb - slide
        net_tick = Line(
            np.array([axis_x - 0.14, slide_end_y, 0]),
            np.array([axis_x + 0.14, slide_end_y, 0]),
            color=YELLOW, stroke_width=2.2,
        )
        net_tick_lbl = self.safe_text(f"净+{net}米", font_size=13, color=YELLOW)
        net_tick_lbl.next_to(net_tick, RIGHT, buff=0.08)

        net_lbl = self.safe_text(f"净爬 {net} 米/天", font_size=17, color=RED)
        net_lbl.next_to(main_axis, DOWN, buff=0.22)

        panel = VGroup(
            main_axis, bottom_cap, meter_ticks,
            climb_arrow, climb_lbl, slide_arrow, slide_lbl,
            net_tick, net_tick_lbl,
        )
        return panel, net_lbl

    def make_well_climb_diagram(
        self,
        depth: int,
        climb: int,
        slide: int,
        draw_y: float,
        *,
        unit_h: float | None = None,
        snail_icon: str | None = None,
        snail_height: float | None = None,
        day_col_buff: float = 0.52,
        zone_buff: float = 0.38,
        arrow_side_offset: float = 0.13,
    ) -> dict[str, Any]:
        """构建爬井图解，整体左→右排布后居中到 draw_y。"""
        unit_h = unit_h if unit_h is not None else self.WELL_UNIT_H
        icon_path = snail_icon or self.SNAIL_ICON
        net = climb - slide
        if net <= 0:
            raise ValueError("白天上爬必须大于晚上下滑")
        pre_height = depth - climb
        if pre_height < 0 or pre_height % net != 0:
            raise ValueError(f"参数不合法: depth={depth}, climb={climb}, slide={slide}")
        pre_days = pre_height // net
        total_days = pre_days + 1

        well_x = 0.0
        bottom = np.array([well_x, 0.0, 0.0])
        top = np.array([well_x, self._well_y(depth, unit_h), 0.0])
        cap_w = 0.32

        well_line = Line(bottom, top, color=WHITE, stroke_width=2.6)
        bottom_cap = Line(
            bottom + LEFT * cap_w, bottom + RIGHT * cap_w,
            color=WHITE, stroke_width=2.2,
        )
        top_cap = Line(
            top + LEFT * cap_w, top + RIGHT * cap_w,
            color=WHITE, stroke_width=2.2,
        )
        bottom_label = self.safe_text("井底", font_size=18, color=GREY_B)
        bottom_label.next_to(bottom_cap, DOWN, buff=0.10)
        top_label = self.safe_text("井口", font_size=18, color=GREY_B)
        top_label.next_to(top_cap, UP, buff=0.10)

        depth_brace = BraceBetweenPoints(bottom, top, direction=RIGHT, buff=0.14)
        depth_brace.set_color(TEAL_D)
        depth_label = self.safe_text(f"{depth}米", font_size=18, color=TEAL_D)
        depth_label.next_to(depth_brace, RIGHT, buff=0.08)

        meter_ticks: list[Line] = []
        meter_labels: list[Mobject] = []
        for m in range(depth + 1):
            y = self._well_y(m, unit_h)
            tick = Line(
                np.array([well_x - 0.12, y, 0]),
                np.array([well_x + 0.12, y, 0]),
                color=GREY_B, stroke_width=1.0, stroke_opacity=0.5,
            )
            meter_ticks.append(tick)
            if m == 0 or 0 < m < depth:
                ml = self.safe_text(f"{m}米", font_size=13, color=GREY_B)
                ml.next_to(tick, LEFT, buff=0.08)
                meter_labels.append(ml)

        snail_h = snail_height if snail_height is not None else self.SNAIL_HEIGHT
        snail = load_icon_png(icon_path, height=snail_h)
        self._place_snail(snail, well_x, 0.0, unit_h)

        scaffold = VGroup(
            well_line, bottom_cap, top_cap,
            bottom_label, top_label,
            depth_brace, depth_label,
            *meter_ticks, *meter_labels,
        )
        # well_block 在下方与 days_block 排布后组装

        cycle_panel, net_label = self._make_day_cycle_panel(climb, slide, unit_h)
        cycle_title = self.safe_text("一天", font_size=15, color=GREY_B)
        cycle_title.next_to(cycle_panel, UP, buff=0.12)
        cycle_block = VGroup(cycle_title, cycle_panel, net_label)

        day_marks: list[dict[str, Any]] = []
        day_parts: list[Mobject] = []

        # 共用主井竖轴（well_line），右侧画每日爬升箭头
        col_start_x = 0.72
        col_x = col_start_x
        col_step = 0.78

        for d in range(1, pre_days + 1):
            start_m = net * (d - 1)
            end_m = net * d
            climb_top_m = start_m + climb
            start_y = self._well_y(start_m, unit_h)
            climb_top_y = self._well_y(climb_top_m, unit_h)
            end_y = self._well_y(end_m, unit_h)
            axis_x = col_x

            climb_arrow, slide_arrow, day_axis = self._dual_side_day_arrows(
                axis_x, start_y, climb_top_y, end_y,
                side_offset=arrow_side_offset, stroke_width=2.2,
            )

            guide_start = self._guide_to_well_axis(
                well_x, start_y, axis_x - arrow_side_offset - 0.04,
                color=YELLOW,
            )
            guide_climb = self._guide_to_well_axis(
                well_x, climb_top_y, axis_x - arrow_side_offset - 0.04,
                color=TEAL_D, stroke_opacity=0.55,
            )
            guide_net = self._guide_to_well_axis(
                well_x, end_y, axis_x + arrow_side_offset + 0.04,
                color=YELLOW,
            )

            start_tick = Line(
                np.array([axis_x - 0.14, start_y, 0]),
                np.array([axis_x + 0.14, start_y, 0]),
                color=YELLOW, stroke_width=2.0,
            )
            climb_tick = Line(
                np.array([axis_x - 0.10, climb_top_y, 0]),
                np.array([axis_x + 0.10, climb_top_y, 0]),
                color=TEAL_D, stroke_width=2.0,
            )
            climb_lbl = self.safe_text(f"+{climb}米", font_size=11, color=TEAL_D)
            climb_lbl.next_to(climb_tick, RIGHT, buff=0.05)

            end_tick = Line(
                np.array([axis_x - 0.14, end_y, 0]),
                np.array([axis_x + 0.14, end_y, 0]),
                color=YELLOW, stroke_width=2.0,
            )
            start_lbl = self.safe_text(f"起点{start_m}米", font_size=11, color=YELLOW)
            start_lbl.next_to(
                np.array([axis_x + 0.22, start_y, 0]), RIGHT, buff=0.02,
            )
            day_lbl = self.safe_text(f"第{d}天末{end_m}米", font_size=12, color=YELLOW)
            day_lbl.next_to(
                np.array([axis_x + 0.22, end_y, 0]), RIGHT, buff=0.02,
            )
            day_title = self.safe_text(f"第{d}天", font_size=13, color=GREY_B)
            day_title.next_to(
                np.array([axis_x, start_y, 0]), UP, buff=0.14,
            )

            column = VGroup(
                day_axis, climb_arrow, slide_arrow,
                guide_start, guide_climb, guide_net,
                start_tick, climb_tick, climb_lbl, end_tick,
                start_lbl, day_lbl, day_title,
            )
            day_parts.append(column)
            col_x += col_step
            day_marks.append({
                "day": d,
                "start_m": start_m,
                "end_m": end_m,
                "climb_top_m": climb_top_m,
                "meters": end_m,
                "start_y": start_y,
                "climb_top_y": climb_top_y,
                "net_y": end_y,
                "climb_arrow": climb_arrow,
                "slide_arrow": slide_arrow,
                "axis_line": day_axis,
                "guide_start": guide_start,
                "guide_climb": guide_climb,
                "guide_net": guide_net,
                "start_tick": start_tick,
                "climb_tick": climb_tick,
                "climb_label": climb_lbl,
                "start_label": start_lbl,
                "net_tick": end_tick,
                "label": day_lbl,
                "day_title": day_title,
                "column": column,
                "parts": column,
            })

        final_start_y = self._well_y(pre_height, unit_h)
        final_top_y = self._well_y(depth, unit_h)
        final_axis_x = col_x
        final_axis = Line(
            np.array([final_axis_x, final_start_y, 0]),
            np.array([final_axis_x, final_top_y + 0.04, 0]),
            color=GREY_B, stroke_width=1.8,
        )
        final_arrow = Arrow(
            np.array([final_axis_x - arrow_side_offset, final_start_y, 0]),
            np.array([final_axis_x - arrow_side_offset, final_top_y, 0]),
            color=BLUE_B, stroke_width=2.8, buff=0,
            max_tip_length_to_length_ratio=0.12,
        )
        final_guides = VGroup(
            self._guide_to_well_axis(
                well_x, final_start_y, final_axis_x - arrow_side_offset - 0.04,
                color=RED,
            ),
            self._guide_to_well_axis(
                well_x, final_top_y, final_axis_x - arrow_side_offset - 0.04,
                color=BLUE_B,
            ),
        )
        final_start_tick = Line(
            np.array([final_axis_x - 0.14, final_start_y, 0]),
            np.array([final_axis_x + 0.14, final_start_y, 0]),
            color=RED, stroke_width=2.0,
        )
        final_top_tick = Line(
            np.array([final_axis_x - 0.14, final_top_y, 0]),
            np.array([final_axis_x + 0.14, final_top_y, 0]),
            color=BLUE_B, stroke_width=2.5,
        )
        final_climb_tick_lbl = self.safe_text(f"+{climb}米", font_size=11, color=BLUE_B)
        final_climb_tick_lbl.next_to(final_top_tick, LEFT, buff=0.05)
        final_start_lbl = self.safe_text(f"起点{pre_height}米", font_size=11, color=RED)
        final_start_lbl.next_to(
            np.array([final_axis_x + 0.20, final_start_y, 0]), RIGHT, buff=0.02,
        )
        final_day_title = self.safe_text(f"第{total_days}天", font_size=13, color=GREY_B)
        final_day_title.next_to(
            np.array([final_axis_x, final_start_y, 0]), UP, buff=0.14,
        )

        # 图形与文字分离：图形留在刻度坐标系，说明写右侧空白
        final_graphics = VGroup(
            final_axis, final_arrow, final_guides,
            final_start_tick, final_top_tick, final_climb_tick_lbl,
            final_start_lbl, final_day_title,
        )

        days_block = Group(*day_parts, final_graphics)
        final_notes = VGroup(
            self.safe_text(f"第{total_days}天", font_size=16, color=RED),
            self.safe_text(
                f"从{pre_height}米处再向上爬{climb}米", font_size=14, color=BLUE_B,
            ),
            self.safe_text(f"到达{depth}米井口", font_size=14, color=BLUE_B),
            self.safe_text("到井口后不再下滑", font_size=14, color=RED),
            self.safe_text(f"{depth}-{climb}={pre_height}（米）", font_size=14, color=WHITE),
            self.safe_text(f"{pre_height}÷{net}={pre_days}（天）", font_size=14, color=WHITE),
            self.safe_text(f"{pre_days}+1={total_days}（天）", font_size=15, color=YELLOW),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT)

        well_rail = VGroup(well_line, bottom_cap, top_cap, *meter_ticks)
        days_title = self.safe_text("每日爬升", font_size=15, color=GREY_B)
        well_block = Group(scaffold, snail)
        self._sync_block_floor_to_well(days_block, well_line, unit_h)
        self._place_right_of(days_block, well_block, buff=0.32)
        progress_row = Group(well_block, days_block)
        progress_width = days_block.get_right()[0] - well_block.get_left()[0]
        progress_row.move_to(np.array([progress_width / 2, 0.0, 0.0]))
        days_title.next_to(progress_row, UP, buff=0.12)

        final_notes.next_to(progress_row, RIGHT, buff=0.38)
        final_notes.align_to(
            np.array([0.0, self._well_y((pre_height + depth) / 2, unit_h), 0.0]),
            UP,
        )

        chart_block = Group(days_title, progress_row)
        chart_with_notes = Group(chart_block, final_notes)
        days_zone = Group(days_title, days_block)

        layout_row = Group(cycle_block, chart_with_notes).arrange(
            RIGHT, buff=zone_buff, aligned_edge=DOWN,
        )

        progress_block = chart_with_notes
        final_zone = chart_with_notes

        hint = self.safe_text("白天上爬，晚上下滑", font_size=18, color=GREY_B)
        hint.next_to(layout_row, DOWN, buff=0.16)

        full = Group(layout_row, hint)
        full.move_to(np.array([0.0, draw_y, 0.0]))
        self.clamp_content(full)

        return {
            "diagram": full,
            "layout_row": layout_row,
            "well_block": well_block,
            "scaffold": scaffold,
            "hint": hint,
            "snail": snail,
            "well_line": well_line,
            "well_rail": well_rail,
            "snail_offset_x": self.SNAIL_OFFSET_X,
            "chart_block": chart_block,
            "chart_with_notes": chart_with_notes,
            "well_x": well_x,
            "unit_h": unit_h,
            "bottom": bottom,
            "top": top,
            "cycle_block": cycle_block,
            "cycle_panel": cycle_panel,
            "net_label": net_label,
            "days_title": days_title,
            "days_block": days_block,
            "days_zone": days_zone,
            "day_marks": day_marks,
            "progress_block": progress_block,
            "final_zone": final_zone,
            "final_graphics": final_graphics,
            "final_notes": final_notes,
            "final_climb": {
                "arrow": final_arrow,
                "day_label": final_day_title,
                "graphics": final_graphics,
                "notes": final_notes,
                "parts": final_graphics,
                "start_meters": pre_height,
                "end_meters": depth,
            },
            "depth": depth,
            "climb": climb,
            "slide": slide,
            "net_per_day": net,
            "pre_height": pre_height,
            "pre_days": pre_days,
            "total_days": total_days,
        }
