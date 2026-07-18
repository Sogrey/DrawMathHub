"""
鸽巢问题 — 第58讲：鸟图标 + ○ 鸽巢图示。

先每巢放 1 只，再把余下的鸽子放进任一巢，说明总有一巢至少 商+1 只。

注意：ImageMobject / VMobject 若先 set_opacity(0) 再 FadeIn，目标透明度仍是 0，
图会永久不可见；延迟出现的图元保持不透明，场景里再 FadeIn。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from diagrams.icon_assets import load_icon_png  # noqa: E402
from manim import *  # noqa: F403


class PigeonholeDiagramMixin:
    """鸽巢原理：n 个椭圆巢 + m 只鸟图标。"""

    BIRD_ICON = "animals/bird.png"
    BIRD_ICON_H = 0.42

    def make_pigeonhole_diagram(
        self,
        draw_y: float,
        *,
        pigeons: int = 4,
        nests: int = 3,
        nest_w: float = 1.70,
        nest_h: float = 1.10,
        gap: float = 0.38,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if pigeons <= 0 or nests <= 0:
            raise ValueError("鸽子数、鸽巢数须为正")
        if pigeons <= nests:
            raise ValueError("本题需鸽子数大于鸽巢数")

        quotient, remainder = divmod(pigeons, nests)
        # 2n > m > n 时，至少 = quotient + 1（商≥1 且有余）
        at_least = quotient + (1 if remainder > 0 else 0)

        nest_color = WHITE
        icon_h = self.BIRD_ICON_H

        total_row_w = nests * nest_w + (nests - 1) * gap
        left_x = -total_row_w / 2
        nest_y = 0.35

        nest_ellipses = VGroup()
        nest_centers: list[np.ndarray] = []
        for i in range(nests):
            cx = left_x + nest_w / 2 + i * (nest_w + gap)
            center = np.array([cx, nest_y, 0])
            nest_centers.append(center)
            e = Ellipse(
                width=nest_w, height=nest_h,
                color=nest_color, stroke_width=2.5,
            )
            e.set_fill(opacity=0)
            e.move_to(center)
            nest_ellipses.add(e)

        # 每巢先放 1 只 — ImageMobject 用 Group；勿预置 opacity=0
        base_pigeons = Group()
        for center in nest_centers:
            bird = load_icon_png(self.BIRD_ICON, height=icon_h)
            bird.move_to(center + DOWN * 0.06)
            base_pigeons.add(bird)

        # 余下的鸽子，先放在最右巢右侧
        extra_pigeons = Group()
        extra_start = nest_centers[-1] + RIGHT * (nest_w / 2 + 0.55)
        for j in range(remainder):
            bird = load_icon_png(self.BIRD_ICON, height=icon_h)
            bird.move_to(extra_start + RIGHT * j * (icon_h + 0.22))
            extra_pigeons.add(bird)

        # 余鸽飞进第 1 个巢后的叠放位置（示意：并排）
        stacked_targets: list[np.ndarray] = []
        for j in range(remainder):
            stacked_targets.append(
                nest_centers[0] + RIGHT * 0.28 + UP * (0.02 + j * 0.08)
            )
        base_shift_in_first = nest_centers[0] + LEFT * 0.28 + DOWN * 0.06

        lab_one = self.safe_text("每巢先飞进1只", font_size=15, color=GREY_B)
        lab_one.next_to(nest_ellipses[0], UP, buff=0.18)

        lab_extra = self.safe_text("剩下的鸽子", font_size=15, color=ORANGE)
        if len(extra_pigeons) > 0:
            lab_extra.next_to(extra_pigeons, UP, buff=0.14)
        else:
            lab_extra.set_opacity(0)

        note_div = self.safe_text(
            f"{pigeons}÷{nests}={quotient}（只）……{remainder}（只）",
            font_size=17, color=WHITE,
        )
        note_add = self.safe_text(
            f"{quotient}+1={at_least}（只）",
            font_size=18, color=YELLOW,
        )
        # 文字可用 set_opacity(0)+animate.set_opacity(1)；图元不要
        for mobj in (lab_one, lab_extra, note_div, note_add):
            mobj.set_opacity(0)

        notes = VGroup(note_div, note_add).arrange(
            DOWN, buff=0.14, aligned_edge=LEFT,
        )
        notes.next_to(nest_ellipses, DOWN, buff=0.45)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "利用 m÷n 的商与余数来判断",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.10)

        diagram = Group(
            nest_ellipses, base_pigeons, extra_pigeons,
            lab_one, lab_extra, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "nests": nest_ellipses,
            "nest_centers": nest_centers,
            "base_pigeons": base_pigeons,
            "extra_pigeons": extra_pigeons,
            "stacked_targets": stacked_targets,
            "base_shift_in_first": base_shift_in_first,
            "lab_one": lab_one,
            "lab_extra": lab_extra,
            "notes": notes,
            "note_div": note_div,
            "note_add": note_add,
            "hint": hint,
            "pigeons": pigeons,
            "nests_n": nests,
            "quotient": quotient,
            "remainder": remainder,
            "at_least": at_least,
            "answer": f"至少飞进了{at_least}只",
        }
