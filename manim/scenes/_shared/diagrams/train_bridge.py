"""
火车过桥问题 — 第29讲：插旗法。

两面旗插在「开始过桥」与「完全过桥」时的车尾位置；
两旗之间路程 = 火车长 + 桥长。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class TrainBridgeDiagramMixin:
    """插旗法：火车过桥路程 = 车长 + 桥长。"""

    def _make_flag(self, color=RED, pole_h: float = 0.55) -> VGroup:
        pole = Line(ORIGIN, UP * pole_h, color=GREY_A, stroke_width=2.5)
        cloth = Triangle(fill_opacity=1, stroke_width=0, color=color)
        cloth.scale(0.16)
        cloth.rotate(-PI / 2)
        cloth.next_to(pole.get_top(), RIGHT, buff=0)
        cloth.shift(DOWN * 0.08)
        tag = self.safe_text("车尾", font_size=12, color=color)
        tag.next_to(pole, DOWN, buff=0.06)
        return VGroup(pole, cloth, tag)

    def _make_train(
        self,
        width: float,
        *,
        color=TEAL_D,
        height: float = 0.42,
    ) -> VGroup:
        body = RoundedRectangle(
            width=width, height=height,
            corner_radius=0.06,
            color=color, stroke_width=2.5,
        )
        body.set_fill(color, opacity=0.35)
        # 简易车窗
        windows = VGroup()
        n = max(2, int(width / 0.55))
        for i in range(n):
            w = RoundedRectangle(
                width=0.22, height=0.18,
                corner_radius=0.03,
                color=WHITE, stroke_width=1.2,
            )
            w.set_fill(WHITE, opacity=0.25)
            windows.add(w)
        windows.arrange(RIGHT, buff=0.12)
        windows.move_to(body.get_center())
        if windows.width > width * 0.85:
            windows.set_width(width * 0.85)
        lab = self.safe_text("火车长", font_size=14, color=color)
        lab.next_to(body, UP, buff=0.08)
        return VGroup(body, windows, lab)

    def make_train_bridge_diagram(
        self,
        draw_y: float,
        *,
        train_len: int = 360,
        bridge_len: int = 1260,
        tree_time: int = 8,
        train_w: float = 1.35,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "米",
    ) -> dict[str, Any]:
        if train_len <= 0 or bridge_len <= 0 or tree_time <= 0:
            raise ValueError("车长、桥长、过树时间须为正")

        speed = train_len / tree_time
        bridge_time = (train_len + bridge_len) / speed
        # 成片数值取整（母题为整数）
        if abs(bridge_time - round(bridge_time)) < 1e-9:
            bridge_time = int(round(bridge_time))

        bridge_w = train_w * (bridge_len / train_len)
        # 总示意宽：车1 + 间距(桥示意) + 车2，控制在安全区内
        gap = min(bridge_w, 3.8)  # 桥段屏幕宽度
        y = 0.15

        train1 = self._make_train(train_w, color=TEAL_D)
        train2 = self._make_train(train_w, color=TEAL_D)
        # 车尾在左，车头朝右；两车位置：train1 | 桥示意 | train2
        left_train_x = -(gap / 2 + train_w)
        right_train_x = gap / 2
        train1.move_to(np.array([left_train_x + train_w / 2, y, 0]))
        train2.move_to(np.array([right_train_x + train_w / 2, y, 0]))

        flag1 = self._make_flag(color=RED)
        flag2 = self._make_flag(color=RED)
        rear1_x = left_train_x
        rear2_x = right_train_x
        flag1.move_to(np.array([rear1_x, y - 0.55, 0]))
        flag2.move_to(np.array([rear2_x, y - 0.55, 0]))
        # 旗杆底对齐车底略下
        flag1.shift(UP * 0.15)
        flag2.shift(UP * 0.15)

        # 桥长：左车「车头上桥」→ 右车「车尾离桥」（两车之间的空隙）
        # 注意：左车头→右车头 = 行驶全程（车长+桥长），不是桥长
        front1_x = left_train_x + train_w
        bridge_line = Line(
            np.array([front1_x, y - 0.55, 0]),
            np.array([rear2_x, y - 0.55, 0]),
            color=ORANGE, stroke_width=4,
        )
        bridge_brace_span = Line(
            np.array([front1_x, y - 0.55, 0]),
            np.array([rear2_x, y - 0.55, 0]),
        )
        bridge_brace = Brace(bridge_brace_span, direction=DOWN, buff=0.08)
        bridge_brace.set_color(ORANGE)
        bridge_lab = self.safe_text(f"桥长 {bridge_len}{unit_label}", font_size=16, color=ORANGE)
        bridge_lab.next_to(bridge_brace, DOWN, buff=0.06)
        bridge_block = VGroup(bridge_line, bridge_brace, bridge_lab)

        # 两旗之间 = 行驶路程
        path_span = Line(
            np.array([rear1_x, y + 0.55, 0]),
            np.array([rear2_x, y + 0.55, 0]),
        )
        path_brace = Brace(path_span, direction=UP, buff=0.42)
        path_brace.set_color(YELLOW)
        path_lab_q = self.safe_text(
            f"火车行驶路程 = ? {unit_label}",
            font_size=16, color=YELLOW,
        )
        path_lab_ans = self.safe_text(
            f"火车行驶路程 = {train_len}+{bridge_len}={train_len + bridge_len}{unit_label}",
            font_size=15, color=YELLOW,
        )
        path_lab_q.next_to(path_brace, UP, buff=0.06)
        path_lab_ans.next_to(path_brace, UP, buff=0.06)
        path_lab_ans.set_opacity(0)
        path_block = VGroup(path_brace, path_lab_q, path_lab_ans)

        # 双向箭头强调两旗距离
        path_arrow = DoubleArrow(
            np.array([rear1_x + 0.08, y + 0.72, 0]),
            np.array([rear2_x - 0.08, y + 0.72, 0]),
            buff=0, stroke_width=2.5, color=YELLOW,
            max_tip_length_to_length_ratio=0.08, tip_length=0.16,
        )

        note_speed = self.safe_text(
            f"过树求速度：{train_len}÷{tree_time}={int(speed)}（{unit_label}/秒）",
            font_size=15, color=TEAL_D,
        )
        note_time = self.safe_text(
            f"过桥时间：({train_len}+{bridge_len})÷{int(speed)}={bridge_time}（秒）",
            font_size=15, color=YELLOW,
        )
        notes = VGroup(note_speed, note_time).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        note_speed.set_opacity(0)
        note_time.set_opacity(0)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "插旗看车尾：过桥路程 = 车长 + 桥长",
                font_size=16, color=GREY_B,
            )

        trains = VGroup(train1, train2)
        flags = VGroup(flag1, flag2)
        annotated = VGroup(
            trains, flags, bridge_block, path_arrow, path_block, notes,
        )
        layout_row = VGroup(annotated)
        if show_hint:
            notes.next_to(bridge_block, DOWN, buff=0.28)
            hint.next_to(notes, DOWN, buff=0.14)
            layout_row = VGroup(annotated, hint)
        else:
            notes.next_to(bridge_block, DOWN, buff=0.28)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "trains": trains,
            "train1": train1,
            "train2": train2,
            "flags": flags,
            "flag1": flag1,
            "flag2": flag2,
            "bridge_block": bridge_block,
            "bridge_line": bridge_line,
            "path_block": path_block,
            "path_arrow": path_arrow,
            "path_lab_q": path_lab_q,
            "path_lab_ans": path_lab_ans,
            "notes": notes,
            "note_speed": note_speed,
            "note_time": note_time,
            "hint": hint,
            "train_len": train_len,
            "bridge_len": bridge_len,
            "tree_time": tree_time,
            "speed": int(speed) if abs(speed - int(speed)) < 1e-9 else speed,
            "bridge_time": bridge_time,
            "unit_label": unit_label,
        }
