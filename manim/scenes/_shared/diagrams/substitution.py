"""
等量代换问题图解 — 第10讲及同类题型。

教材结构：1 个圆圈在上、下方连若干三角形（1 换多），横向重复多组。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class SubstitutionDiagramMixin:
    """等量代换：圆圈/三角形符号 + 树状连接 + 横向多组。"""

    def _substitution_circle(
        self,
        radius: float = 0.18,
        *,
        color=RED,
        stroke_width: int = 2,
        fill_opacity: float = 0.22,
    ) -> Circle:
        c = Circle(radius=radius, color=color, stroke_width=stroke_width)
        c.set_fill(color, opacity=fill_opacity)
        return c

    def _substitution_triangle(
        self,
        side: float = 0.34,
        *,
        color=ORANGE,
        stroke_width: int = 2,
        fill_opacity: float = 0.22,
    ) -> RegularPolygon:
        t = RegularPolygon(n=3, color=color, stroke_width=stroke_width)
        t.scale(side)
        t.set_fill(color, opacity=fill_opacity)
        return t

    def _substitution_unit(
        self,
        give_per_receive: int,
        *,
        circle_r: float = 0.18,
        tri_side: float = 0.34,
        tri_buff: float = 0.14,
        vert_gap: float = 0.42,
    ) -> dict[str, Any]:
        """单组：1 个 receive 图形在上，give_per_receive 个 give 图形在下，斜线相连。"""
        circle = self._substitution_circle(circle_r)
        tris = VGroup(*[
            self._substitution_triangle(tri_side) for _ in range(give_per_receive)
        ])
        tris.arrange(RIGHT, buff=tri_buff)
        tri_center_y = circle.get_center()[1] - vert_gap
        tris.move_to(np.array([circle.get_center()[0], tri_center_y, 0]))

        lines = VGroup()
        for tri in tris:
            line = Line(
                circle.get_bottom() + DOWN * 0.02,
                tri.get_top() + UP * 0.02,
                color=GREY_B,
                stroke_width=1.8,
            )
            lines.add(line)

        unit = VGroup(circle, lines, tris)
        return {
            "unit": unit,
            "circle": circle,
            "triangles": tris,
            "lines": lines,
        }

    def make_substitution_diagram(
        self,
        give_per_receive: int,
        target_receive: int,
        draw_y: float,
        *,
        give_label: str = "橘子",
        receive_label: str = "苹果",
        circle_r: float = 0.18,
        tri_side: float = 0.34,
        unit_buff: float = 0.62,
        tri_buff: float = 0.14,
    ) -> dict[str, Any]:
        """
        构建等量代换树状图（与教材母题精讲一致）。

        give_per_receive: 换 1 个 receive 需要几个 give
        target_receive: 目标 receive 数量
        """
        total_give = target_receive * give_per_receive

        units: list[dict[str, Any]] = []
        for _ in range(target_receive):
            units.append(self._substitution_unit(
                give_per_receive,
                circle_r=circle_r,
                tri_side=tri_side,
                tri_buff=tri_buff,
            ))

        single_unit = units[0]["unit"]
        units_row = VGroup(*[u["unit"] for u in units]).arrange(RIGHT, buff=unit_buff)

        all_circles = VGroup(*[u["circle"] for u in units])
        all_triangles = VGroup(*[tri for u in units for tri in u["triangles"]])

        circle_legend = self._substitution_circle(circle_r)
        tri_legend = self._substitution_triangle(tri_side)
        circle_tag = self.safe_text(receive_label, font_size=20, color=RED)
        tri_tag = self.safe_text(give_label, font_size=20, color=ORANGE)
        legend_block = VGroup(
            VGroup(circle_legend, circle_tag).arrange(RIGHT, buff=0.10),
            VGroup(tri_legend, tri_tag).arrange(RIGHT, buff=0.10),
        ).arrange(RIGHT, buff=0.45)

        top_note = self.safe_text(
            f"→ {target_receive}个{receive_label}", font_size=22, color=YELLOW,
        )

        bottom_note_q = self.safe_text(
            f"→ ?个{give_label}", font_size=22, color=ORANGE,
        )
        bottom_note_a = self.safe_text(
            f"→ {total_give}个{give_label}", font_size=22, color=ORANGE,
        )
        bottom_note_a.move_to(bottom_note_q.get_center())

        formula_label = self.safe_text(
            f"{target_receive}×{give_per_receive}={total_give}（个）",
            font_size=24, color=YELLOW,
        )

        rule_text = self.safe_text(
            f"{give_per_receive}个{give_label} = 1个{receive_label}",
            font_size=22, color=RED,
        )

        hint = self.safe_text(
            "先找等量关系，再按目标数量代换",
            font_size=20, color=GREY_B,
        )

        # 以 units_row 为锚点链式定位（全部在同一坐标系，最后整体平移一次）
        units_row.move_to(ORIGIN)
        top_note.next_to(all_circles, UP, buff=0.52)
        legend_block.next_to(top_note, UP, buff=0.42)
        legend_block.shift(UP * 0.18)
        hint.next_to(legend_block, UP, buff=0.16)

        bottom_note_q.next_to(all_triangles, DOWN, buff=0.62)
        bottom_note_a.move_to(bottom_note_q.get_center())
        formula_label.next_to(bottom_note_q, DOWN, buff=0.42)
        rule_text.next_to(single_unit, DOWN, buff=0.48)

        # 整体平移一次，避免部分元素留在旧坐标导致重叠
        all_parts = VGroup(
            hint, legend_block, top_note, units_row,
            bottom_note_q, bottom_note_a, formula_label, rule_text,
        )
        all_parts.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(all_parts)

        layout_row = VGroup(legend_block, top_note, units_row, bottom_note_a)

        return {
            "diagram": all_parts,
            "hint": hint,
            "legend_block": legend_block,
            "single_unit": single_unit,
            "units": units,
            "units_row": units_row,
            "extra_units": VGroup(*[u["unit"] for u in units[1:]]),
            "all_circles": all_circles,
            "all_triangles": all_triangles,
            "rule_text": rule_text,
            "top_note": top_note,
            "bottom_note_q": bottom_note_q,
            "bottom_note_a": bottom_note_a,
            "formula_label": formula_label,
            "layout_row": layout_row,
            "total_give": total_give,
        }
