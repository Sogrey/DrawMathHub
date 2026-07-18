"""
流水行船问题 — 第54讲：顺水/逆水同程线段图。

左右（或上下）两条等长甲→乙线段，分别标顺水用时与逆水用时；
先求顺/逆水速，再求船速与水速。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class BoatCurrentDiagramMixin:
    """船速=(顺+逆)/2，水速=(顺−逆)/2。"""

    def make_boat_current_diagram(
        self,
        draw_y: float,
        *,
        distance: int = 168,
        down_hours: int = 6,
        up_hours: int = 8,
        seg_w: float = 3.6,
        col_gap: float = 0.85,
        line_stroke: float = 4.0,
        tick_h: float = 0.14,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if distance <= 0 or down_hours <= 0 or up_hours <= 0:
            raise ValueError("路程与用时须为正")
        if up_hours <= down_hours:
            raise ValueError("逆水用时应大于顺水用时")

        down_speed = distance / down_hours  # 28
        up_speed = distance / up_hours  # 21
        boat_speed = (down_speed + up_speed) / 2  # 24.5
        water_speed = (down_speed - up_speed) / 2  # 3.5

        # 格式化：整数不带小数，否则保留一位
        def fmt(v: float) -> str:
            if abs(v - round(v)) < 1e-9:
                return str(int(round(v)))
            return f"{v:.1f}"

        down_s = fmt(down_speed)
        up_s = fmt(up_speed)
        boat_s = fmt(boat_speed)
        water_s = fmt(water_speed)

        down_color = TEAL_D
        up_color = ORANGE
        y = 0.35

        # 两列中心
        half = seg_w / 2 + col_gap / 2
        cx_down = -half
        cx_up = half

        def make_port_seg(cx: float, color):
            left = cx - seg_w / 2
            right = cx + seg_w / 2
            main = Line(
                np.array([left, y, 0]),
                np.array([right, y, 0]),
                color=WHITE, stroke_width=line_stroke,
            )
            ticks = VGroup(
                Line(
                    np.array([left, y + tick_h, 0]),
                    np.array([left, y - tick_h, 0]),
                    color=WHITE, stroke_width=line_stroke * 0.85,
                ),
                Line(
                    np.array([right, y + tick_h, 0]),
                    np.array([right, y - tick_h, 0]),
                    color=WHITE, stroke_width=line_stroke * 0.85,
                ),
            )
            bar = RoundedRectangle(
                width=seg_w, height=0.20, corner_radius=0.04, stroke_width=0,
            )
            bar.set_fill(color, opacity=0.28)
            bar.move_to(np.array([cx, y, 0]))

            lab_a = self.safe_text("甲", font_size=18, color=WHITE)
            lab_a.next_to(np.array([left, y, 0]), LEFT, buff=0.12)
            lab_b = self.safe_text("乙", font_size=18, color=WHITE)
            lab_b.next_to(np.array([right, y, 0]), RIGHT, buff=0.12)

            brace = Brace(main, UP, buff=0.12, color=GREY_B)
            dist_lab = self.safe_text(f"{distance}千米", font_size=16, color=GREY_B)
            dist_lab.next_to(brace, UP, buff=0.06)

            return {
                "main": main,
                "ticks": ticks,
                "bar": bar,
                "lab_a": lab_a,
                "lab_b": lab_b,
                "brace": brace,
                "dist_lab": dist_lab,
                "left": left,
                "right": right,
                "cx": cx,
            }

        down = make_port_seg(cx_down, down_color)
        up = make_port_seg(cx_up, up_color)

        title_down = self.safe_text("顺水：", font_size=20, color=down_color)
        title_down.next_to(down["dist_lab"], UP, buff=0.14)

        title_up = self.safe_text("逆水：", font_size=20, color=up_color)
        title_up.next_to(up["dist_lab"], UP, buff=0.14)

        time_down = self.safe_text(
            f"行驶{down_hours}小时", font_size=16, color=down_color,
        )
        time_down.next_to(down["main"], DOWN, buff=0.22)

        time_up = self.safe_text(
            f"行驶{up_hours}小时", font_size=16, color=up_color,
        )
        time_up.next_to(up["main"], DOWN, buff=0.22)

        # 速度注记（出现在时间下方）
        speed_down = self.safe_text(
            f"顺水速度={distance}÷{down_hours}={down_s}",
            font_size=15, color=down_color,
        )
        speed_down.next_to(time_down, DOWN, buff=0.14)

        speed_up = self.safe_text(
            f"逆水速度={distance}÷{up_hours}={up_s}",
            font_size=15, color=up_color,
        )
        speed_up.next_to(time_up, DOWN, buff=0.14)

        for m in (
            down["main"], down["ticks"], down["bar"], down["lab_a"], down["lab_b"],
            down["brace"], down["dist_lab"], title_down, time_down, speed_down,
            up["main"], up["ticks"], up["bar"], up["lab_a"], up["lab_b"],
            up["brace"], up["dist_lab"], title_up, time_up, speed_up,
        ):
            m.set_opacity(0)

        note_boat = self.safe_text(
            f"船速=({down_s}+{up_s})÷2={boat_s}（千米/时）",
            font_size=18, color=YELLOW,
        )
        note_water = self.safe_text(
            f"水速=({down_s}−{up_s})÷2={water_s}（千米/时）",
            font_size=18, color=YELLOW,
        )
        for m in (note_boat, note_water):
            m.set_opacity(0)

        notes = VGroup(note_boat, note_water).arrange(
            DOWN, buff=0.16, aligned_edge=LEFT,
        )
        notes.next_to(
            VGroup(speed_down, speed_up), DOWN, buff=0.32,
        )

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "船速=(顺+逆)÷2，水速=(顺−逆)÷2",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.10)

        diagram = VGroup(
            title_down, down["main"], down["ticks"], down["bar"],
            down["lab_a"], down["lab_b"], down["brace"], down["dist_lab"],
            time_down, speed_down,
            title_up, up["main"], up["ticks"], up["bar"],
            up["lab_a"], up["lab_b"], up["brace"], up["dist_lab"],
            time_up, speed_up,
            notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "down": down,
            "up": up,
            "title_down": title_down,
            "title_up": title_up,
            "time_down": time_down,
            "time_up": time_up,
            "speed_down": speed_down,
            "speed_up": speed_up,
            "notes": notes,
            "note_boat": note_boat,
            "note_water": note_water,
            "hint": hint,
            "distance": distance,
            "down_hours": down_hours,
            "up_hours": up_hours,
            "down_speed": down_speed,
            "up_speed": up_speed,
            "boat_speed": boat_speed,
            "water_speed": water_speed,
            "down_s": down_s,
            "up_s": up_s,
            "boat_s": boat_s,
            "water_s": water_s,
            "answer": f"船速{boat_s}千米/时，水速{water_s}千米/时",
        }
