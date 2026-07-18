"""
鸡兔同笼（一）— 第32讲：假设法。

用 ○ 表示头、斜线表示腿；先假设全是鸡，再把部分「鸡」加腿变回兔。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class ChickenRabbitDiagramMixin:
    """鸡兔同笼假设法：头圈 + 腿线示意图。"""

    def _make_animal(
        self,
        *,
        head_r: float = 0.15,
        head_color=WHITE,
        leg_color=TEAL_D,
        rabbit_color=ORANGE,
    ) -> dict[str, Any]:
        head = Circle(
            radius=head_r,
            color=head_color,
            stroke_width=2.5,
            fill_opacity=0,
        )
        # 鸡的 2 条腿（斜线）
        leg_len = head_r * 1.15
        cx, cy = 0.0, -head_r * 0.15
        chicken_legs = VGroup(
            Line(
                np.array([-0.05, cy, 0]),
                np.array([-0.05 - leg_len * 0.45, cy - leg_len, 0]),
                color=leg_color, stroke_width=2.2,
            ),
            Line(
                np.array([0.05, cy, 0]),
                np.array([0.05 + leg_len * 0.45, cy - leg_len, 0]),
                color=leg_color, stroke_width=2.2,
            ),
        )
        # 兔多出的 2 条腿（初始透明）
        rabbit_extra = VGroup(
            Line(
                np.array([-0.12, cy, 0]),
                np.array([-0.12 - leg_len * 0.35, cy - leg_len * 0.95, 0]),
                color=rabbit_color, stroke_width=2.2,
            ),
            Line(
                np.array([0.12, cy, 0]),
                np.array([0.12 + leg_len * 0.35, cy - leg_len * 0.95, 0]),
                color=rabbit_color, stroke_width=2.2,
            ),
        )
        rabbit_extra.set_opacity(0)

        body = VGroup(head, chicken_legs, rabbit_extra)
        return {
            "body": body,
            "head": head,
            "chicken_legs": chicken_legs,
            "rabbit_extra": rabbit_extra,
        }

    def make_chicken_rabbit_diagram(
        self,
        draw_y: float,
        *,
        heads: int = 14,
        legs: int = 38,
        chicken_legs: int = 2,
        rabbit_legs: int = 4,
        spacing: float = 0.48,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if heads <= 0:
            raise ValueError("头数须为正")
        assume_legs = heads * chicken_legs
        short = legs - assume_legs
        per_diff = rabbit_legs - chicken_legs
        if per_diff <= 0 or short % per_diff != 0:
            raise ValueError("总腿数与假设腿数须能解出兔数")
        rabbits = short // per_diff
        chickens = heads - rabbits
        if rabbits < 0 or chickens < 0:
            raise ValueError("兔/鸡数量无效")

        total_w = (heads - 1) * spacing
        left_x = -total_w / 2
        y = 0.35

        animals = []
        heads_g = VGroup()
        chicken_legs_g = VGroup()
        rabbit_extra_g = VGroup()
        bodies = VGroup()
        for i in range(heads):
            x = left_x + i * spacing
            a = self._make_animal()
            a["body"].move_to(np.array([x, y, 0]))
            animals.append(a)
            heads_g.add(a["head"])
            chicken_legs_g.add(a["chicken_legs"])
            rabbit_extra_g.add(a["rabbit_extra"])
            bodies.add(a["body"])

        # 假设全是鸡：上方括号
        assume_span = Line(
            np.array([left_x, y + 0.22, 0]),
            np.array([left_x + total_w, y + 0.22, 0]),
        )
        assume_brace = Brace(assume_span, direction=UP, buff=0.10)
        assume_brace.set_color(TEAL_D)
        assume_lab = self.safe_text(f"{heads} 只鸡", font_size=16, color=TEAL_D)
        assume_lab.next_to(assume_brace, UP, buff=0.06)
        assume_top = VGroup(assume_brace, assume_lab)

        # 下方：14×2 条腿
        legs_span = Line(
            np.array([left_x, y - 0.42, 0]),
            np.array([left_x + total_w, y - 0.42, 0]),
        )
        legs_brace = Brace(legs_span, direction=DOWN, buff=0.08)
        legs_brace.set_color(GREY_B)
        legs_lab = self.safe_text(
            f"{heads}×{chicken_legs}={assume_legs} 条腿",
            font_size=15, color=GREY_B,
        )
        legs_lab.next_to(legs_brace, DOWN, buff=0.06)
        assume_bot = VGroup(legs_brace, legs_lab)

        # 结果括号：左兔右鸡（初始透明）
        rabbit_w = (rabbits - 1) * spacing if rabbits > 1 else 0
        rabbit_cx = left_x + rabbit_w / 2 if rabbits > 0 else left_x
        if rabbits == 1:
            rabbit_span = Line(
                np.array([left_x - 0.12, y + 0.22, 0]),
                np.array([left_x + 0.12, y + 0.22, 0]),
            )
        else:
            rabbit_span = Line(
                np.array([left_x, y + 0.22, 0]),
                np.array([left_x + (rabbits - 1) * spacing, y + 0.22, 0]),
            )
        rabbit_brace = Brace(rabbit_span, direction=UP, buff=0.10)
        rabbit_brace.set_color(ORANGE)
        rabbit_lab = self.safe_text(f"{rabbits} 只兔", font_size=16, color=ORANGE)
        rabbit_lab.next_to(rabbit_brace, UP, buff=0.06)
        result_rabbit = VGroup(rabbit_brace, rabbit_lab)
        result_rabbit.set_opacity(0)

        chicken_left = left_x + rabbits * spacing
        if chickens == 1:
            chicken_span = Line(
                np.array([chicken_left - 0.12, y + 0.22, 0]),
                np.array([chicken_left + 0.12, y + 0.22, 0]),
            )
        else:
            chicken_span = Line(
                np.array([chicken_left, y + 0.22, 0]),
                np.array([left_x + total_w, y + 0.22, 0]),
            )
        chicken_brace = Brace(chicken_span, direction=UP, buff=0.10)
        chicken_brace.set_color(TEAL_D)
        chicken_lab = self.safe_text(f"{chickens} 只鸡", font_size=16, color=TEAL_D)
        chicken_lab.next_to(chicken_brace, UP, buff=0.06)
        result_chicken = VGroup(chicken_brace, chicken_lab)
        result_chicken.set_opacity(0)

        # 推理批注（先建再定位，答案走透明度）
        note_short = self.safe_text(
            f"比实际少 {legs}－{assume_legs}={short} 条腿",
            font_size=15, color=YELLOW,
        )
        note_diff = self.safe_text(
            f"每只兔比鸡多 {rabbit_legs}－{chicken_legs}={per_diff} 条腿",
            font_size=15, color=GREY_B,
        )
        note_rab_q = self.safe_text(
            f"兔：{short}÷{per_diff}=?",
            font_size=15, color=ORANGE,
        )
        note_rab_ans = self.safe_text(
            f"兔：{short}÷{per_diff}={rabbits}（只）",
            font_size=15, color=ORANGE,
        )
        note_chi_ans = self.safe_text(
            f"鸡：{heads}－{rabbits}={chickens}（只）",
            font_size=15, color=TEAL_D,
        )
        for m in (note_short, note_diff, note_rab_q, note_rab_ans, note_chi_ans):
            m.set_opacity(0)

        notes = VGroup(note_short, note_diff, note_rab_q, note_rab_ans, note_chi_ans)
        note_short.next_to(assume_bot, DOWN, buff=0.20)
        note_diff.next_to(note_short, DOWN, buff=0.10)
        note_rab_q.next_to(note_diff, DOWN, buff=0.10)
        note_rab_ans.move_to(note_rab_q)
        note_chi_ans.next_to(note_rab_ans, DOWN, buff=0.10)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "假设全是鸡 → 少的腿数 ÷ 每只相差腿数 = 兔数",
                font_size=15, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        # 先组图再整体移到 draw_y（notes 已相对定位）
        diagram = VGroup(
            bodies, assume_top, assume_bot,
            result_rabbit, result_chicken, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        # 兔的身体子集（前 rabbits 只）
        rabbit_bodies = VGroup(*[animals[i]["body"] for i in range(rabbits)])
        chicken_bodies = VGroup(*[animals[i]["body"] for i in range(rabbits, heads)])
        rabbit_extras = VGroup(*[animals[i]["rabbit_extra"] for i in range(rabbits)])

        return {
            "diagram": diagram,
            "bodies": bodies,
            "animals": animals,
            "heads": heads_g,
            "chicken_legs_g": chicken_legs_g,
            "rabbit_extra_g": rabbit_extra_g,
            "rabbit_extras": rabbit_extras,
            "rabbit_bodies": rabbit_bodies,
            "chicken_bodies": chicken_bodies,
            "assume_top": assume_top,
            "assume_bot": assume_bot,
            "result_rabbit": result_rabbit,
            "result_chicken": result_chicken,
            "notes": notes,
            "note_short": note_short,
            "note_diff": note_diff,
            "note_rab_q": note_rab_q,
            "note_rab_ans": note_rab_ans,
            "note_chi_ans": note_chi_ans,
            "hint": hint,
            "heads_count": heads,
            "legs_count": legs,
            "assume_legs": assume_legs,
            "short": short,
            "per_diff": per_diff,
            "rabbits": rabbits,
            "chickens": chickens,
            "chicken_leg_n": chicken_legs,
            "rabbit_leg_n": rabbit_legs,
        }
