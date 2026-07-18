"""
逻辑推理（二）— 第37讲：列表法（帽子颜色排除表）。

人 × 颜色网格，用 × / √ 逐步排除不可能结果。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class LogicHatTableDiagramMixin:
    """帽子颜色逻辑表：逐格排除与确认。"""

    def _logic_cell(
        self,
        text: str,
        width: float,
        height: float,
        *,
        font_size: int = 20,
        color=WHITE,
        fill_color=None,
        fill_opacity: float = 0.35,
    ) -> dict[str, Any]:
        rect = Rectangle(
            width=width, height=height,
            stroke_color=GREY_B, stroke_width=1.5,
        )
        if fill_color is not None:
            rect.set_fill(fill_color, opacity=fill_opacity)
        label = self.safe_text(text, font_size=font_size, color=color)
        label.move_to(rect.get_center())
        pad = 0.10
        if label.width > width - pad:
            label.scale((width - pad) / label.width)
            label.move_to(rect.get_center())
        return {"cell": VGroup(rect, label), "rect": rect, "label": label}

    def make_logic_hat_table(
        self,
        draw_y: float,
        *,
        people: list[str] | None = None,
        colors: list[str] | None = None,
        show_hint: bool = True,
        x_shift: float = 0.0,
        cell_w: float = 1.35,
        name_w: float = 1.25,
        row_h: float = 0.58,
        header_fill=YELLOW_E,
        mark_font: int = 28,
    ) -> dict[str, Any]:
        if people is None:
            people = ["红红", "丽丽", "莹莹"]
        if colors is None:
            colors = ["红色", "黄色", "蓝色"]
        n = len(people)
        if len(colors) != n:
            raise ValueError("人数与颜色数须一致")

        col_ws = [name_w, *[cell_w] * n]
        n_rows = n + 1
        n_cols = n + 1
        grid_w = sum(col_ws)
        grid_h = row_h * n_rows
        origin = np.array([-grid_w / 2, grid_h / 2, 0])

        def cell_center(row: int, col: int) -> np.ndarray:
            x = origin[0] + sum(col_ws[:col]) + col_ws[col] / 2
            y = origin[1] - row * row_h - row_h / 2
            return np.array([x, y, 0])

        # 表头
        corner = self._logic_cell("", col_ws[0], row_h, fill_color=header_fill)
        corner["cell"].move_to(cell_center(0, 0))
        header_g = VGroup(corner["cell"])
        for j, cname in enumerate(colors):
            d = self._logic_cell(
                cname, col_ws[j + 1], row_h,
                font_size=18, color=YELLOW,
                fill_color=header_fill, fill_opacity=0.45,
            )
            d["cell"].move_to(cell_center(0, j + 1))
            header_g.add(d["cell"])

        name_cells = VGroup()
        grid_rects = []  # [row][col] rect
        marks: dict[tuple[int, int], Mobject] = {}

        for i, pname in enumerate(people):
            nd = self._logic_cell(pname, col_ws[0], row_h, font_size=18)
            nd["cell"].move_to(cell_center(i + 1, 0))
            name_cells.add(nd["cell"])
            row_rects = []
            for j in range(n):
                empty = self._logic_cell("", col_ws[j + 1], row_h)
                empty["cell"].move_to(cell_center(i + 1, j + 1))
                name_cells.add(empty["cell"])  # 一并加入便于 FadeIn 底表
                row_rects.append(empty["rect"])
                # 预建 × 与 √，透明
                pos = cell_center(i + 1, j + 1)
                cross = self.safe_text("×", font_size=mark_font, color=TEAL_D)
                cross.move_to(pos)
                cross.set_opacity(0)
                check = self.safe_text("√", font_size=mark_font, color=ORANGE)
                check.move_to(pos)
                check.set_opacity(0)
                marks[(i, j)] = VGroup(cross, check)
            grid_rects.append(row_rects)

        marks_g = VGroup(*[marks[k] for k in sorted(marks.keys())])
        table = VGroup(header_g, name_cells, marks_g)

        # 结果批注
        note_lili = self.safe_text(
            "丽丽只剩红色 → 戴红色帽子",
            font_size=15, color=ORANGE,
        )
        note_hong = self.safe_text(
            "红红只剩蓝色 → 戴蓝色帽子",
            font_size=15, color=TEAL_D,
        )
        note_ying = self.safe_text(
            "莹莹只剩黄色 → 戴黄色帽子",
            font_size=15, color=YELLOW,
        )
        for m in (note_lili, note_hong, note_ying):
            m.set_opacity(0)
        notes = VGroup(note_lili, note_hong, note_ying)
        note_lili.next_to(table, DOWN, buff=0.28)
        note_hong.next_to(note_lili, DOWN, buff=0.10)
        note_ying.next_to(note_hong, DOWN, buff=0.10)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "逐一排除不可能的结果",
                font_size=15, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(table, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        def mark_cross(pi: int, cj: int) -> Mobject:
            return marks[(pi, cj)][0]

        def mark_check(pi: int, cj: int) -> Mobject:
            return marks[(pi, cj)][1]

        # 索引约定：people[0]=红红, [1]=丽丽, [2]=莹莹；colors[0]=红,[1]=黄,[2]=蓝
        return {
            "diagram": diagram,
            "table": table,
            "header": header_g,
            "name_cells": name_cells,
            "marks": marks,
            "marks_g": marks_g,
            "mark_cross": mark_cross,
            "mark_check": mark_check,
            "notes": notes,
            "note_lili": note_lili,
            "note_hong": note_hong,
            "note_ying": note_ying,
            "hint": hint,
            "people": people,
            "colors": colors,
            # 语义别名便于场景引用
            "hong": 0,
            "lili": 1,
            "ying": 2,
            "red": 0,
            "yellow": 1,
            "blue": 2,
        }
