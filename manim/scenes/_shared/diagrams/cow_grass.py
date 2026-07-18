"""
牛吃草问题 — 第43讲：图示法。

原有草 + 若干天新长草 = 牛吃的总份数；用两次吃草差求日生长量。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class CowGrassDiagramMixin:
    """牛吃草：两条水平条对比「原有 + 新长」。"""

    def make_cow_grass_diagram(
        self,
        draw_y: float,
        *,
        cows_a: int = 20,
        days_a: int = 10,
        cows_b: int = 24,
        days_b: int = 6,
        cows_q: int = 18,
        row_gap: float = 1.15,
        bar_h: float = 0.42,
        show_hint: bool = True,
        x_shift: float = 0.0,
        unit_label: str = "份",
    ) -> dict[str, Any]:
        if days_a <= days_b:
            raise ValueError("需 days_a > days_b")
        eat_a = cows_a * days_a
        eat_b = cows_b * days_b
        day_diff = days_a - days_b
        grow_diff = eat_a - eat_b
        if grow_diff % day_diff != 0:
            raise ValueError("份数差须能被天数差整除")
        grow_per = grow_diff // day_diff
        original = eat_a - grow_per * days_a
        net_q = cows_q - grow_per
        if net_q <= 0 or original % net_q != 0:
            raise ValueError("无法整除求出天数")
        days_q = original // net_q

        # 宽度：以 eat_a 为总长
        total_w = 6.5
        orig_w = total_w * original / eat_a
        grow_a_w = total_w - orig_w
        grow_b_w = total_w * (grow_per * days_b) / eat_a
        # eat_b 总宽
        bar_b_w = orig_w + grow_b_w

        left_x = -total_w / 2
        top_y = row_gap / 2
        bot_y = -row_gap / 2

        def bar_seg(x0, x1, y, color, fill_opacity=0.55):
            rect = Rectangle(
                width=x1 - x0, height=bar_h,
                stroke_width=2.0, stroke_color=color,
                fill_color=color, fill_opacity=fill_opacity,
            )
            rect.move_to(np.array([(x0 + x1) / 2, y, 0]))
            return rect

        # 上行：原有 + 10天新长
        orig_top = bar_seg(left_x, left_x + orig_w, top_y, WHITE, 0.35)
        grow_top = bar_seg(
            left_x + orig_w, left_x + total_w, top_y, TEAL_D, 0.55,
        )
        name_a = self.safe_text(f"{cows_a}头×{days_a}天", font_size=14, color=GREY_B)
        name_a.next_to(np.array([left_x, top_y, 0]), LEFT, buff=0.18)

        brace_orig_t = Brace(
            Line(np.array([left_x, top_y, 0]), np.array([left_x + orig_w, top_y, 0])),
            UP, buff=0.10,
        )
        brace_orig_t.set_color(GREY_B)
        lab_orig = self.safe_text("原有的草", font_size=13, color=GREY_B)
        lab_orig.next_to(brace_orig_t, UP, buff=0.04)

        brace_ga = Brace(
            Line(
                np.array([left_x + orig_w, top_y, 0]),
                np.array([left_x + total_w, top_y, 0]),
            ),
            UP, buff=0.10,
        )
        brace_ga.set_color(TEAL_D)
        lab_ga = self.safe_text(f"{days_a}天新长", font_size=13, color=TEAL_D)
        lab_ga.next_to(brace_ga, UP, buff=0.04)

        top_row = VGroup(
            orig_top, grow_top, name_a,
            brace_orig_t, lab_orig, brace_ga, lab_ga,
        )

        # 下行：原有 + 6天新长
        orig_bot = bar_seg(left_x, left_x + orig_w, bot_y, WHITE, 0.35)
        grow_bot = bar_seg(
            left_x + orig_w, left_x + bar_b_w, bot_y, TEAL_D, 0.55,
        )
        name_b = self.safe_text(f"{cows_b}头×{days_b}天", font_size=14, color=GREY_B)
        name_b.next_to(np.array([left_x, bot_y, 0]), LEFT, buff=0.18)

        brace_gb = Brace(
            Line(
                np.array([left_x + orig_w, bot_y, 0]),
                np.array([left_x + bar_b_w, bot_y, 0]),
            ),
            DOWN, buff=0.10,
        )
        brace_gb.set_color(TEAL_D)
        lab_gb = self.safe_text(f"{days_b}天新长", font_size=13, color=TEAL_D)
        lab_gb.next_to(brace_gb, DOWN, buff=0.04)

        bot_row = VGroup(orig_bot, grow_bot, name_b, brace_gb, lab_gb)

        # 对齐虚线：原有右端
        align = DashedLine(
            np.array([left_x + orig_w, top_y + 0.35, 0]),
            np.array([left_x + orig_w, bot_y - 0.35, 0]),
            color=GREY_B, stroke_width=1.4, dash_length=0.08,
        )

        # 右侧差值：上方新长比下方多出的一段
        diff_span = Line(
            np.array([left_x + bar_b_w, top_y + bar_h / 2 + 0.02, 0]),
            np.array([left_x + total_w, top_y + bar_h / 2 + 0.02, 0]),
        )
        diff_br = Brace(diff_span, UP, buff=0.06)
        diff_br.set_color(ORANGE)
        diff_lab = self.safe_text(f"{day_diff}天新长差", font_size=13, color=ORANGE)
        diff_lab.next_to(diff_br, UP, buff=0.04)
        diff_g = VGroup(diff_br, diff_lab)
        diff_g.set_opacity(0)

        # 批注
        note_grow = self.safe_text(
            f"每天生长：({eat_a}－{eat_b})÷({days_a}－{days_b})={grow_per}",
            font_size=15, color=TEAL_D,
        )
        note_orig = self.safe_text(
            f"原有草：{eat_a}－{grow_per}×{days_a}={original}",
            font_size=15, color=GREY_B,
        )
        note_days_q = self.safe_text(
            f"{cows_q}头可吃：{original}÷({cows_q}－{grow_per})=?",
            font_size=15, color=YELLOW,
        )
        note_days_ans = self.safe_text(
            f"{cows_q}头可吃：{original}÷({cows_q}－{grow_per})={days_q}（天）",
            font_size=15, color=YELLOW,
        )
        for m in (note_grow, note_orig, note_days_q, note_days_ans):
            m.set_opacity(0)

        notes = VGroup(note_grow, note_orig, note_days_q, note_days_ans)
        note_grow.next_to(bot_row, DOWN, buff=0.55)
        note_orig.next_to(note_grow, DOWN, buff=0.12)
        note_days_q.next_to(note_orig, DOWN, buff=0.12)
        note_days_ans.move_to(note_days_q)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "份数差÷天数差＝每天生长；原有÷每天净减＝天数",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(
            align, top_row, bot_row, diff_g, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "align": align,
            "top_row": top_row,
            "bot_row": bot_row,
            "orig_top": orig_top,
            "grow_top": grow_top,
            "orig_bot": orig_bot,
            "grow_bot": grow_bot,
            "brace_orig": VGroup(brace_orig_t, lab_orig),
            "brace_ga": VGroup(brace_ga, lab_ga),
            "brace_gb": VGroup(brace_gb, lab_gb),
            "name_a": name_a,
            "name_b": name_b,
            "diff_g": diff_g,
            "notes": notes,
            "note_grow": note_grow,
            "note_orig": note_orig,
            "note_days_q": note_days_q,
            "note_days_ans": note_days_ans,
            "hint": hint,
            "cows_a": cows_a,
            "days_a": days_a,
            "cows_b": cows_b,
            "days_b": days_b,
            "cows_q": cows_q,
            "eat_a": eat_a,
            "eat_b": eat_b,
            "grow_per": grow_per,
            "original": original,
            "days_q": days_q,
            "unit_label": unit_label,
        }
