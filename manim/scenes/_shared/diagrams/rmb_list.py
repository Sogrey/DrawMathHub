"""
人民币列表法（付款组合表）— 第4讲及同类题型。

约定：仅本模块维护列表法表格相关逻辑。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class RmbListDiagramMixin:
    """人民币付款枚举：表格式列表，逐行填入组合方案。"""

    def _table_cell(
        self,
        text: str,
        width: float,
        height: float,
        *,
        font_size: int = 20,
        color=WHITE,
        fill_color=None,
        fill_opacity: float = 0.30,
    ) -> dict[str, Any]:
        rect = Rectangle(
            width=width, height=height,
            stroke_color=GREY_B, stroke_width=1.5,
        )
        if fill_color is not None:
            rect.set_fill(fill_color, opacity=fill_opacity)
        label = self.safe_text(text, font_size=font_size, color=color)
        label.move_to(rect.get_center())
        pad = 0.14
        if label.width > width - pad:
            label.scale((width - pad) / label.width)
            label.move_to(rect.get_center())
        return {"cell": VGroup(rect, label), "rect": rect, "label": label}

    def make_rmb_payment_table(
        self,
        column_headers: list[str],
        methods: list[dict[str, Any]],
        draw_y: float,
        *,
        row_label_width: float = 1.15,
        col_width: float = 1.15,
        total_col_width: float = 2.40,
        row_height: float = 0.46,
        header_fill=YELLOW_E,
        row_fill=GREY_E,
    ) -> dict[str, Any]:
        """
        构建付款列表表格。

        methods 每项:
          name: str          — 行名，如「方法一」
          counts: list[int]  — 各面值张数
          sum_text: str      — 合计列，如「20+10=30」
        """
        col_widths = [row_label_width, *([col_width] * len(column_headers)), total_col_width]
        n_cols = len(col_widths)
        n_rows = len(methods) + 1

        grid_w = sum(col_widths)
        grid_h = row_height * n_rows
        origin = np.array([-grid_w / 2, grid_h / 2, 0])

        def cell_center(row: int, col: int) -> np.ndarray:
            x = origin[0] + sum(col_widths[:col]) + col_widths[col] / 2
            y = origin[1] - row * row_height - row_height / 2
            return np.array([x, y, 0])

        header_cells: list[dict[str, Any]] = []
        header_labels = ["", *column_headers, "合计/元"]
        for col, (text, w) in enumerate(zip(header_labels, col_widths)):
            info = self._table_cell(
                text, w, row_height,
                font_size=18, color=YELLOW if col > 0 else WHITE,
                fill_color=header_fill, fill_opacity=0.35,
            )
            info["cell"].move_to(cell_center(0, col))
            header_cells.append(info)

        header_row = VGroup(*[c["cell"] for c in header_cells])

        data_rows: list[dict[str, Any]] = []
        for row_idx, method in enumerate(methods, start=1):
            row_cells: list[dict[str, Any]] = []
            texts = [
                method["name"],
                *[str(n) for n in method["counts"]],
                method["sum_text"],
            ]
            for col, (text, w) in enumerate(zip(texts, col_widths)):
                is_total_col = col == n_cols - 1
                info = self._table_cell(
                    text, w, row_height,
                    font_size=18 if is_total_col else 20,
                    color=YELLOW if col == 0 else (TEAL_D if is_total_col else WHITE),
                    fill_color=row_fill if row_idx % 2 == 1 else None,
                    fill_opacity=0.18,
                )
                info["cell"].move_to(cell_center(row_idx, col))
                row_cells.append(info)
            data_rows.append({
                "name": method["name"],
                "counts": method["counts"],
                "sum_text": method["sum_text"],
                "cells": row_cells,
                "row": VGroup(*[c["cell"] for c in row_cells]),
                "total_cell": row_cells[-1],
            })

        table = VGroup(header_row, *[r["row"] for r in data_rows])
        table.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(table)

        wallet_hint = self.safe_text(
            "现有：1张20元　3张10元　2张5元　→　目标：付30元（不找零）",
            font_size=20, color=GREY_B,
        )
        wallet_hint.next_to(table, UP, buff=0.22)
        self.clamp_content(wallet_hint)

        return {
            "table": table,
            "wallet_hint": wallet_hint,
            "header_row": header_row,
            "header_cells": header_cells,
            "data_rows": data_rows,
            "diagram": VGroup(wallet_hint, table),
        }
