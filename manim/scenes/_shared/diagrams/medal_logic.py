"""
逻辑推理（三）— 第45讲：连线法（假设猜对 → 连线找矛盾）。

上排三人、下排金银铜；逐一假设某一猜测为真，连线后标出矛盾或成立。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class MedalLogicDiagramMixin:
    """奖牌猜测：三人×三牌连线，假设排除法。"""

    def _medal_chip(
        self,
        text: str,
        *,
        font_size: int = 16,
        color=WHITE,
        box_w: float = 0.72,
        box_h: float = 0.36,
        fill_opacity: float = 0.20,
    ) -> VGroup:
        box = RoundedRectangle(
            width=box_w, height=box_h, corner_radius=0.06,
            stroke_width=2.0, stroke_color=color,
            fill_color=color, fill_opacity=fill_opacity,
        )
        lab = self.safe_text(text, font_size=font_size, color=color)
        if lab.width > box_w - 0.12:
            lab.scale((box_w - 0.12) / lab.width)
        lab.move_to(box.get_center())
        return VGroup(box, lab)

    def _make_one_case(
        self,
        *,
        title: str,
        links: list[tuple[int, int]],
        conflict_pair: tuple[int, int] | None,
        ok: bool,
        people: list[str],
        medals: list[str],
        medal_colors: list,
        scale: float = 0.92,
    ) -> dict[str, Any]:
        """
        links: (人下标, 奖牌下标)
        conflict_pair: 两个冲突的人下标（指向同一奖牌时）
        """
        top = VGroup(*[
            self._medal_chip(p, font_size=15, color=WHITE, box_w=0.78)
            for p in people
        ]).arrange(RIGHT, buff=0.28)
        bot = VGroup(*[
            self._medal_chip(m, font_size=15, color=c, box_w=0.72, fill_opacity=0.28)
            for m, c in zip(medals, medal_colors)
        ]).arrange(RIGHT, buff=0.28)
        bot.next_to(top, DOWN, buff=0.95)

        lines = VGroup()
        for pi, mi in links:
            a = top[pi].get_bottom()
            b = bot[mi].get_top()
            ln = Line(a, b, color=TEAL_D if ok else GREY_B, stroke_width=2.4)
            lines.add(ln)

        conflict = VGroup()
        if conflict_pair is not None:
            i, j = conflict_pair
            # 冲突线标红，旁注「矛盾」（勿用 SurroundingRectangle，会盖成大红块）
            lines[i].set_color(RED)
            lines[j].set_color(RED)
            mid = (lines[i].get_center() + lines[j].get_center()) / 2
            tag = self.safe_text("矛盾", font_size=15, color=RED)
            tag.move_to(mid + RIGHT * 0.55)
            conflict = VGroup(tag)
            conflict.set_opacity(0)

        ok_tag = self.safe_text("成立", font_size=14, color=YELLOW)
        ok_tag.next_to(bot, DOWN, buff=0.14)
        ok_tag.set_opacity(0)

        title_m = self.safe_text(title, font_size=14, color=GREY_B)
        title_m.next_to(top, UP, buff=0.14)

        panel = VGroup(title_m, top, bot, lines, conflict, ok_tag)
        panel.scale(scale)

        return {
            "panel": panel,
            "top": top,
            "bot": bot,
            "lines": lines,
            "conflict": conflict,
            "ok_tag": ok_tag,
            "title": title_m,
            "ok": ok,
        }

    def make_medal_logic_diagram(
        self,
        draw_y: float,
        *,
        people: list[str] | None = None,
        medals: list[str] | None = None,
        show_hint: bool = True,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if people is None:
            people = ["小明", "小华", "小强"]
        if medals is None:
            medals = ["金", "银", "铜"]
        medal_colors = [YELLOW, GREY_B, ORANGE]

        # 图1：假设「小明得金」对 → 小华得金、小强得铜 → 两人金牌矛盾
        # 假话：小华不得金为假→小华得金；小强不得铜为假→小强得铜
        case1 = self._make_one_case(
            title="图1：假设①对",
            links=[(0, 0), (1, 0), (2, 2)],  # 明-金, 华-金, 强-铜
            conflict_pair=(0, 1),
            ok=False,
            people=people, medals=medals, medal_colors=medal_colors,
        )
        # 图2：假设「小华不得金」对 → 明不得金(假①)，强得铜(假③)
        # 明、华都只能银 → 矛盾
        case2 = self._make_one_case(
            title="图2：假设②对",
            links=[(0, 1), (1, 1), (2, 2)],  # 明-银, 华-银, 强-铜
            conflict_pair=(0, 1),
            ok=False,
            people=people, medals=medals, medal_colors=medal_colors,
        )
        # 图3：假设「小强不得铜」对 → 明不得金，华得金 → 明铜、强银 成立
        case3 = self._make_one_case(
            title="图3：假设③对",
            links=[(0, 2), (1, 0), (2, 1)],  # 明-铜, 华-金, 强-银
            conflict_pair=None,
            ok=True,
            people=people, medals=medals, medal_colors=medal_colors,
        )

        cases = VGroup(case1["panel"], case2["panel"], case3["panel"]).arrange(
            RIGHT, buff=0.28, aligned_edge=UP,
        )
        # 线条 / 矛盾 / 成立 初始隐藏，由场景分步显现
        for c in (case1, case2, case3):
            c["lines"].set_opacity(0)
            c["conflict"].set_opacity(0)
            c["ok_tag"].set_opacity(0)

        note_ans = self.safe_text(
            "小明铜牌，小华金牌，小强银牌",
            font_size=16, color=YELLOW,
        )
        note_ans.set_opacity(0)
        note_ans.next_to(cases, DOWN, buff=0.28)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "逐一假设猜对一句，连线排除矛盾",
                font_size=14, color=GREY_B,
            )
            hint.next_to(note_ans, DOWN, buff=0.10)

        diagram = VGroup(cases, note_ans, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "cases": cases,
            "case1": case1,
            "case2": case2,
            "case3": case3,
            "note_ans": note_ans,
            "hint": hint,
            "people": people,
            "medals": medals,
            "answer": "小明铜牌，小华金牌，小强银牌",
        }
