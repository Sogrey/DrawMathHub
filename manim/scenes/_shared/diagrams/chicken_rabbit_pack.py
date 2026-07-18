"""
鸡兔同笼（二）— 第33讲：打包法。

按倍数关系把「1 只鸡 + n 只兔」打成一组，用总腿数 ÷ 每组腿数求组数。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class ChickenRabbitPackDiagramMixin:
    """鸡兔同笼打包法：成组框 + 头腿示意。"""

    def _make_pack_animal(
        self,
        *,
        is_rabbit: bool,
        head_r: float = 0.13,
    ) -> VGroup:
        head = Circle(
            radius=head_r,
            color=WHITE,
            stroke_width=2.2,
            fill_opacity=0,
        )
        leg_len = head_r * 1.1
        cy = -head_r * 0.12
        color = ORANGE if is_rabbit else TEAL_D
        if is_rabbit:
            legs = VGroup(
                Line(
                    np.array([-0.10, cy, 0]),
                    np.array([-0.10 - leg_len * 0.40, cy - leg_len, 0]),
                    color=color, stroke_width=2.0,
                ),
                Line(
                    np.array([-0.03, cy, 0]),
                    np.array([-0.03 - leg_len * 0.25, cy - leg_len * 0.95, 0]),
                    color=color, stroke_width=2.0,
                ),
                Line(
                    np.array([0.03, cy, 0]),
                    np.array([0.03 + leg_len * 0.25, cy - leg_len * 0.95, 0]),
                    color=color, stroke_width=2.0,
                ),
                Line(
                    np.array([0.10, cy, 0]),
                    np.array([0.10 + leg_len * 0.40, cy - leg_len, 0]),
                    color=color, stroke_width=2.0,
                ),
            )
        else:
            legs = VGroup(
                Line(
                    np.array([-0.05, cy, 0]),
                    np.array([-0.05 - leg_len * 0.45, cy - leg_len, 0]),
                    color=color, stroke_width=2.0,
                ),
                Line(
                    np.array([0.05, cy, 0]),
                    np.array([0.05 + leg_len * 0.45, cy - leg_len, 0]),
                    color=color, stroke_width=2.0,
                ),
            )
        return VGroup(head, legs)

    def _make_pack_group(
        self,
        *,
        rabbit_mult: int,
        animal_gap: float = 0.38,
        box_buff: float = 0.16,
    ) -> dict[str, Any]:
        # 布局：1 鸡 + n 兔（横向）
        items = VGroup()
        chicken = self._make_pack_animal(is_rabbit=False)
        items.add(chicken)
        rabbits = VGroup()
        for _ in range(rabbit_mult):
            r = self._make_pack_animal(is_rabbit=True)
            rabbits.add(r)
            items.add(r)
        items.arrange(RIGHT, buff=animal_gap)

        box = DashedVMobject(
            SurroundingRectangle(
                items, buff=box_buff, color=GREY_B, stroke_width=2.0,
                corner_radius=0.06,
            ),
            num_dashes=28,
        )
        pack = VGroup(box, items)
        return {
            "pack": pack,
            "box": box,
            "items": items,
            "chicken": chicken,
            "rabbits": rabbits,
        }

    def make_chicken_rabbit_pack_diagram(
        self,
        draw_y: float,
        *,
        rabbit_mult: int = 3,
        total_legs: int = 280,
        chicken_legs: int = 2,
        rabbit_legs: int = 4,
        show_packs: int = 3,
        pack_gap: float = 0.28,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if rabbit_mult <= 0:
            raise ValueError("倍数须为正")
        legs_per = rabbit_mult * rabbit_legs + chicken_legs
        if total_legs % legs_per != 0:
            raise ValueError("总腿数须能被每组腿数整除")
        groups = total_legs // legs_per
        chickens = groups  # 每组 1 鸡
        rabbits = rabbit_mult * groups

        # 展示：前 show_packs-1 组 + 省略号 + 最后 1 组（教材风格）
        n_left = max(1, show_packs - 1)
        packs_left = VGroup()
        pack_dicts = []
        for _ in range(n_left):
            d = self._make_pack_group(rabbit_mult=rabbit_mult)
            pack_dicts.append(d)
            packs_left.add(d["pack"])
        packs_left.arrange(RIGHT, buff=pack_gap)

        dots = self.safe_text("……", font_size=26, color=GREY_B)
        last_d = self._make_pack_group(rabbit_mult=rabbit_mult)
        pack_dicts.append(last_d)

        packs_row = VGroup(packs_left, dots, last_d["pack"]).arrange(
            RIGHT, buff=0.22,
        )

        # 总腿数括号
        legs_brace = Brace(packs_row, direction=DOWN, buff=0.18)
        legs_brace.set_color(YELLOW)
        legs_lab = self.safe_text(f"{total_legs} 条腿", font_size=18, color=YELLOW)
        legs_lab.next_to(legs_brace, DOWN, buff=0.08)
        legs_block = VGroup(legs_brace, legs_lab)

        # 单组说明（可指向第一组）
        unit_note = self.safe_text(
            f"每组：1 鸡 + {rabbit_mult} 兔",
            font_size=15, color=GREY_B,
        )
        unit_note.next_to(packs_row, UP, buff=0.18)

        note_legs = self.safe_text(
            f"每组腿数：{rabbit_mult}×{rabbit_legs}＋{chicken_legs}={legs_per}",
            font_size=15, color=TEAL_D,
        )
        note_groups_q = self.safe_text(
            f"组数：{total_legs}÷{legs_per}=?",
            font_size=15, color=YELLOW,
        )
        note_groups_ans = self.safe_text(
            f"组数：{total_legs}÷{legs_per}={groups}（组）",
            font_size=15, color=YELLOW,
        )
        note_chi = self.safe_text(
            f"鸡：1×{groups}={chickens}（只）",
            font_size=15, color=TEAL_D,
        )
        note_rab = self.safe_text(
            f"兔：{rabbit_mult}×{groups}={rabbits}（只）",
            font_size=15, color=ORANGE,
        )
        for m in (note_legs, note_groups_q, note_groups_ans, note_chi, note_rab):
            m.set_opacity(0)

        notes = VGroup(note_legs, note_groups_q, note_groups_ans, note_chi, note_rab)
        note_legs.next_to(legs_block, DOWN, buff=0.18)
        note_groups_q.next_to(note_legs, DOWN, buff=0.10)
        note_groups_ans.move_to(note_groups_q)
        note_chi.next_to(note_groups_ans, DOWN, buff=0.10)
        note_rab.next_to(note_chi, DOWN, buff=0.10)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "组数＝总腿数÷每组腿数之和",
                font_size=15, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(
            packs_row, unit_note, legs_block, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        first_pack = pack_dicts[0]["pack"]
        other_packs = VGroup(
            *[d["pack"] for d in pack_dicts[1:]],
            dots,
        )

        return {
            "diagram": diagram,
            "packs_row": packs_row,
            "packs_left": packs_left,
            "first_pack": first_pack,
            "other_packs": other_packs,
            "dots": dots,
            "last_pack": last_d["pack"],
            "unit_note": unit_note,
            "legs_block": legs_block,
            "notes": notes,
            "note_legs": note_legs,
            "note_groups_q": note_groups_q,
            "note_groups_ans": note_groups_ans,
            "note_chi": note_chi,
            "note_rab": note_rab,
            "hint": hint,
            "rabbit_mult": rabbit_mult,
            "total_legs": total_legs,
            "legs_per": legs_per,
            "groups": groups,
            "chickens": chickens,
            "rabbits": rabbits,
            "chicken_legs": chicken_legs,
            "rabbit_legs": rabbit_legs,
        }
