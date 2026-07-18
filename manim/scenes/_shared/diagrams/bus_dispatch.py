"""
发车问题 — 第55讲：车间距 + 人车迎面相遇。

上排：等间距公交车；下排：乐乐与下一辆车相向而行（相遇模型）。
相遇间隔 = 相邻车距 ÷ (人速 + 车速)。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from diagrams.icon_assets import load_icon_png  # noqa: E402
from manim import *  # noqa: F403


class BusDispatchDiagramMixin:
    """发车间隔 → 车距 → 迎面相遇时间。"""

    BUS_ICON = "vehicles/bus.png"
    BUS_ICON_H = 0.48

    def make_bus_dispatch_diagram(
        self,
        draw_y: float,
        *,
        person_speed: int = 2,
        bus_speed: int = 10,
        dispatch_min: int = 5,
        total_w: float = 7.6,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if person_speed <= 0 or bus_speed <= 0 or dispatch_min <= 0:
            raise ValueError("速度与发车间隔须为正")

        dispatch_sec = dispatch_min * 60  # 300
        spacing = dispatch_sec * bus_speed  # 3000
        meet_sec = spacing // (bus_speed + person_speed)  # 250

        bus_color = ORANGE
        person_color = TEAL_D
        gap_color = YELLOW

        # 上排略抬高，给右侧算式留宽
        top_y = 0.95
        left_x = -total_w / 2
        right_x = left_x + total_w
        # 三车略靠左，右侧留给算式
        x1 = left_x + total_w * 0.08
        x2 = left_x + total_w * 0.38
        x3 = left_x + total_w * 0.68

        road = Line(
            np.array([left_x, top_y, 0]),
            np.array([right_x, top_y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        bus_icons = Group()
        bus_labs = VGroup()
        for i, x in enumerate((x1, x2, x3), start=1):
            icon = load_icon_png(self.BUS_ICON, height=self.BUS_ICON_H)
            icon.move_to(np.array([x, top_y + icon.height / 2 + 0.02, 0]))
            lab = self.safe_text(f"公交车{i}", font_size=13, color=bus_color)
            lab.next_to(icon, UP, buff=0.06)
            bus_icons.add(icon)
            bus_labs.add(lab)

        # 括号紧贴路面下方
        gap1 = Line(
            np.array([x1, top_y, 0]), np.array([x2, top_y, 0]),
            color=gap_color, stroke_width=2.0,
        )
        gap2 = Line(
            np.array([x2, top_y, 0]), np.array([x3, top_y, 0]),
            color=GREY_B, stroke_width=1.2,
        )
        brace1 = Brace(gap1, DOWN, buff=0.08, color=gap_color)
        brace2 = Brace(gap2, DOWN, buff=0.08, color=GREY_B)
        gap_lab = self.safe_text(
            "相遇路程＝1到2的间距",
            font_size=14, color=gap_color,
        )
        gap_lab.next_to(brace1, DOWN, buff=0.06)
        gap_lab.set_x(brace1.get_center()[0])
        same_lab = self.safe_text("同样间距", font_size=13, color=GREY_B)
        same_lab.next_to(brace2, DOWN, buff=0.06)
        same_lab.set_x(brace2.get_center()[0])
        gap1_block = VGroup(brace1, gap_lab)
        gap2_block = VGroup(brace2, same_lab)

        # ── 下排：相遇模型（抬高，为底部字幕留空）──
        bot_y = -0.20
        meet_left = x1
        meet_right = x2
        meet_mid = (meet_left + meet_right) / 2

        meet_line = Line(
            np.array([meet_left, bot_y, 0]),
            np.array([meet_right, bot_y, 0]),
            color=WHITE, stroke_width=line_stroke,
        )
        meet_ticks = VGroup(
            Line(
                np.array([meet_left, bot_y + tick_h, 0]),
                np.array([meet_left, bot_y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.85,
            ),
            Line(
                np.array([meet_right, bot_y + tick_h, 0]),
                np.array([meet_right, bot_y - tick_h, 0]),
                color=WHITE, stroke_width=line_stroke * 0.85,
            ),
        )

        # 三辆车竖虚线：从路面下缘落到相遇行
        guide_top = top_y - 0.08
        guide_bot = bot_y + 0.12
        guide1 = DashedLine(
            np.array([x1, guide_top, 0]),
            np.array([x1, guide_bot, 0]),
            color=GREY_B, stroke_width=1.8, dash_length=0.08,
        )
        guide2 = DashedLine(
            np.array([x2, guide_top, 0]),
            np.array([x2, guide_bot, 0]),
            color=GREY_B, stroke_width=1.8, dash_length=0.08,
        )
        guide3 = DashedLine(
            np.array([x3, guide_top, 0]),
            np.array([x3, guide_bot, 0]),
            color=GREY_B, stroke_width=1.8, dash_length=0.08,
        )
        guides = VGroup(guide1, guide2, guide3)

        # 箭头在线段上方；人名在线段下方（紧凑）
        arrow_y = bot_y + 0.24
        arrow_person = Arrow(
            np.array([meet_left + 0.18, arrow_y, 0]),
            np.array([meet_mid - 0.10, arrow_y, 0]),
            buff=0, stroke_width=3, color=person_color,
            max_tip_length_to_length_ratio=0.22, tip_length=0.14,
        )
        arrow_bus = Arrow(
            np.array([meet_right - 0.18, arrow_y, 0]),
            np.array([meet_mid + 0.10, arrow_y, 0]),
            buff=0, stroke_width=3, color=bus_color,
            max_tip_length_to_length_ratio=0.22, tip_length=0.14,
        )
        person_lab = self.safe_text("乐乐", font_size=15, color=person_color)
        person_lab.next_to(
            np.array([(meet_left + meet_mid) / 2, bot_y, 0]),
            DOWN, buff=0.12,
        )
        bus2_lab = self.safe_text("公交车2", font_size=15, color=bus_color)
        bus2_lab.next_to(
            np.array([(meet_mid + meet_right) / 2, bot_y, 0]),
            DOWN, buff=0.12,
        )

        meet_tag = self.safe_text("相向相遇", font_size=14, color=YELLOW)
        meet_tag.next_to(
            VGroup(person_lab, bus2_lab), DOWN, buff=0.10,
        )
        meet_tag.set_x(meet_mid)

        for m in (
            road, bus_icons, bus_labs, gap1_block, gap2_block,
            guides, meet_line, meet_ticks,
            arrow_person, arrow_bus, person_lab, bus2_lab, meet_tag,
        ):
            m.set_opacity(0)

        note_time = self.safe_text(
            f"{dispatch_min}分钟={dispatch_sec}秒",
            font_size=16, color=WHITE,
        )
        note_space = self.safe_text(
            f"车距={dispatch_sec}×{bus_speed}={spacing}（米）",
            font_size=16, color=gap_color,
        )
        note_meet = self.safe_text(
            f"相遇间隔={spacing}÷({bus_speed}+{person_speed})={meet_sec}（秒）",
            font_size=17, color=YELLOW,
        )
        for m in (note_time, note_space, note_meet):
            m.set_opacity(0)

        # 算式放在相遇段右侧，避免沉底与字幕叠字
        notes = VGroup(note_time, note_space, note_meet).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT,
        )
        notes.next_to(meet_line, RIGHT, buff=0.55)
        notes.set_y((arrow_y + meet_tag.get_bottom()[1]) / 2)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "迎面走 → 转化为相遇问题",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.08)

        diagram = Group(
            road, bus_icons, bus_labs, gap1_block, gap2_block,
            guides, meet_line, meet_ticks,
            arrow_person, arrow_bus, person_lab, bus2_lab, meet_tag,
            notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "road": road,
            "bus_icons": bus_icons,
            "bus_dots": bus_icons,
            "bus_labs": bus_labs,
            "brace1": brace1,
            "brace2": brace2,
            "gap_lab": gap_lab,
            "same_lab": same_lab,
            "gap1_block": gap1_block,
            "gap2_block": gap2_block,
            "guide1": guide1,
            "guide2": guide2,
            "guide3": guide3,
            "guides": guides,
            "meet_line": meet_line,
            "meet_ticks": meet_ticks,
            "arrow_person": arrow_person,
            "arrow_bus": arrow_bus,
            "person_lab": person_lab,
            "bus2_lab": bus2_lab,
            "meet_tag": meet_tag,
            "notes": notes,
            "note_time": note_time,
            "note_space": note_space,
            "note_meet": note_meet,
            "hint": hint,
            "person_speed": person_speed,
            "bus_speed": bus_speed,
            "dispatch_min": dispatch_min,
            "dispatch_sec": dispatch_sec,
            "spacing": spacing,
            "meet_sec": meet_sec,
            "answer": f"每隔{meet_sec}秒相遇一次",
        }
