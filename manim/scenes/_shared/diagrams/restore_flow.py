"""
还原问题（一）— 第25讲：流程图正向运算 + 逆向逆推。

方框表示中间结果；上方黑箭头为正运算，下方蓝弧箭头为逆运算。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


_INV_SYM = {"×": "÷", "÷": "×", "+": "−", "−": "+", "*": "/", "/": "*"}


def _parse_op(op: str) -> tuple[str, str]:
    """'×6' → ('×', '6')；支持 ×÷+−×/."""
    op = op.strip().replace("*", "×").replace("/", "÷").replace("-", "−")
    if len(op) < 2:
        raise ValueError(f"非法运算: {op}")
    return op[0], op[1:]


def _inverse_label(op: str) -> str:
    sym, num = _parse_op(op)
    inv = _INV_SYM.get(sym)
    if inv is None:
        raise ValueError(f"不支持的运算符号: {sym}")
    return f"{inv}{num}"


def _apply_op(value: int, op: str) -> int:
    sym, num_s = _parse_op(op)
    num = int(num_s)
    if sym == "×":
        return value * num
    if sym == "÷":
        return value // num
    if sym == "+":
        return value + num
    if sym == "−":
        return value - num
    raise ValueError(f"不支持的运算符号: {sym}")


def _apply_inverse(value: int, forward_op: str) -> int:
    return _apply_op(value, _inverse_label(forward_op))


class RestoreFlowDiagramMixin:
    """还原问题：流程图 + 逆推。"""

    def make_restore_flow_diagram(
        self,
        draw_y: float,
        *,
        forward_ops: list[str] | None = None,
        result: int = 6,
        show_hint: bool = True,
        x_shift: float = 0.0,
        box_side: float = 0.72,
        gap: float = 0.95,
    ) -> dict[str, Any]:
        ops = list(forward_ops or ["×6", "+6", "÷6", "−6"])
        n_boxes = len(ops)

        # 从结果逆推得到各方框数（含起始数）
        box_values: list[int] = []
        cur = result
        for op in reversed(ops):
            cur = _apply_inverse(cur, op)
            box_values.append(cur)
        box_values.reverse()

        inv_ops = [_inverse_label(op) for op in ops]

        boxes = VGroup()
        box_frames = VGroup()
        box_qs = VGroup()
        box_ans = VGroup()
        for i in range(n_boxes):
            frame = Square(side_length=box_side, color=WHITE, stroke_width=2.5)
            q = self.safe_text("?", font_size=28, color=GREY_B)
            q.move_to(frame.get_center())
            ans = self.safe_text(str(box_values[i]), font_size=28, color=YELLOW)
            ans.move_to(frame.get_center())
            ans.set_opacity(0)
            box = VGroup(frame, q, ans)
            boxes.add(box)
            box_frames.add(frame)
            box_qs.add(q)
            box_ans.add(ans)

        result_frame = RoundedRectangle(
            width=box_side * 0.95,
            height=box_side * 0.95,
            corner_radius=0.12,
            color=TEAL_D,
            stroke_width=2.5,
        )
        result_txt = self.safe_text(str(result), font_size=30, color=TEAL_D)
        result_txt.move_to(result_frame.get_center())
        result_node = VGroup(result_frame, result_txt)

        # 横向排布：boxes + result
        nodes = VGroup(*boxes, result_node).arrange(RIGHT, buff=gap)

        # 双层直箭头：上正向（白/橙，左→右），下逆向（蓝，右→左）
        fwd_arrows = VGroup()
        fwd_labels = VGroup()
        rev_arrows = VGroup()
        rev_labels = VGroup()
        for i, (op, inv) in enumerate(zip(ops, inv_ops)):
            left = nodes[i]
            right = nodes[i + 1]
            x0 = left.get_right()[0] + 0.08
            x1 = right.get_left()[0] - 0.08
            y_mid = 0.5 * (left.get_center()[1] + right.get_center()[1])
            y_fwd = y_mid + 0.16
            y_rev = y_mid - 0.16

            fwd = Arrow(
                np.array([x0, y_fwd, 0.0]),
                np.array([x1, y_fwd, 0.0]),
                buff=0.0,
                stroke_width=3,
                color=WHITE,
                max_tip_length_to_length_ratio=0.18,
                tip_length=0.18,
            )
            fwd_lab = self.safe_text(op, font_size=20, color=ORANGE)
            fwd_lab.next_to(fwd, UP, buff=0.08)

            rev = Arrow(
                np.array([x1, y_rev, 0.0]),
                np.array([x0, y_rev, 0.0]),
                buff=0.0,
                stroke_width=3.5,
                color=BLUE_C,
                max_tip_length_to_length_ratio=0.22,
                tip_length=0.20,
            )
            rev_lab = self.safe_text(inv, font_size=18, color=BLUE_C)
            rev_lab.next_to(rev, DOWN, buff=0.08)

            fwd_arrows.add(fwd)
            fwd_labels.add(fwd_lab)
            rev_arrows.add(rev)
            rev_labels.add(rev_lab)
        rev_arrows.set_opacity(0)
        rev_labels.set_opacity(0)

        start_tag = self.safe_text("起始", font_size=16, color=YELLOW)
        start_tag.next_to(boxes[0], UP, buff=0.18)
        result_tag = self.safe_text("结果", font_size=16, color=TEAL_D)
        result_tag.next_to(result_node, UP, buff=0.18)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "逆推时：+↔−，×↔÷（每步都是逆运算）",
                font_size=16, color=GREY_B,
            )
            hint.next_to(nodes, DOWN, buff=0.85)

        flow = VGroup(
            nodes, fwd_arrows, fwd_labels,
            rev_arrows, rev_labels,
            start_tag, result_tag,
        )
        layout_row = VGroup(flow)
        if show_hint:
            layout_row = VGroup(flow, hint)

        diagram = VGroup(layout_row)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "layout_row": layout_row,
            "flow": flow,
            "nodes": nodes,
            "boxes": boxes,
            "box_frames": box_frames,
            "box_qs": box_qs,
            "box_ans": box_ans,
            "box_values": box_values,
            "result_node": result_node,
            "fwd_arrows": fwd_arrows,
            "fwd_labels": fwd_labels,
            "rev_arrows": rev_arrows,
            "rev_labels": rev_labels,
            "start_tag": start_tag,
            "result_tag": result_tag,
            "hint": hint,
            "forward_ops": ops,
            "inv_ops": inv_ops,
            "result": result,
        }
