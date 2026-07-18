"""
策略问题 — 第35讲：列表法（田忌赛马式对阵表）。

已知对方出场顺序与双方成绩，用表格排出己方出场与胜负。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class RaceStrategyDiagramMixin:
    """对阵列表：逐场填入己方出场与本场胜者。"""

    def _race_cell(
        self,
        text: str,
        width: float,
        height: float,
        *,
        font_size: int = 18,
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
        pad = 0.12
        if label.width > width - pad:
            label.scale((width - pad) / label.width)
            label.move_to(rect.get_center())
        if label.height > height - 0.08:
            label.scale((height - 0.08) / label.height)
            label.move_to(rect.get_center())
        return {"cell": VGroup(rect, label), "rect": rect, "label": label}

    def make_race_strategy_table(
        self,
        draw_y: float,
        *,
        class1_rows: list[str] | None = None,
        class2_fills: list[str] | None = None,
        winners: list[str] | None = None,
        match_labels: list[str] | None = None,
        show_hint: bool = True,
        x_shift: float = 0.0,
        col_widths: list[float] | None = None,
        row_height: float = 0.52,
        header_fill=YELLOW_E,
    ) -> dict[str, Any]:
        """
        class1_rows: 对方已定出场，如「1号 14秒2」
        class2_fills: 己方策略出场（初始可透明）
        winners: 本场胜者
        """
        if class1_rows is None:
            class1_rows = ["1号 14秒2", "2号 14秒7", "3号 15秒1"]
        if class2_fills is None:
            class2_fills = ["3号 15秒6", "1号 14秒5", "2号 14秒8"]
        if winners is None:
            winners = ["四(1)班", "四(2)班", "四(2)班"]
        if match_labels is None:
            match_labels = ["第一场", "第二场", "第三场"]
        n = len(class1_rows)
        if not (len(class2_fills) == len(winners) == len(match_labels) == n):
            raise ValueError("行数须一致")

        if col_widths is None:
            col_widths = [1.15, 2.0, 2.0, 1.55]
        headers = ["场次", "四(1)班", "四(2)班", "本场胜者"]

        n_rows = n + 1
        grid_w = sum(col_widths)
        grid_h = row_height * n_rows
        origin = np.array([-grid_w / 2, grid_h / 2, 0])

        def cell_center(row: int, col: int) -> np.ndarray:
            x = origin[0] + sum(col_widths[:col]) + col_widths[col] / 2
            y = origin[1] - row * row_height - row_height / 2
            return np.array([x, y, 0])

        header_g = VGroup()
        for col, (text, w) in enumerate(zip(headers, col_widths)):
            d = self._race_cell(
                text, w, row_height,
                font_size=18, color=YELLOW,
                fill_color=header_fill, fill_opacity=0.45,
            )
            d["cell"].move_to(cell_center(0, col))
            header_g.add(d["cell"])

        match_cells = VGroup()
        class1_cells = VGroup()
        class2_cells = VGroup()
        class2_labels = []
        winner_cells = VGroup()
        winner_labels = []

        for i in range(n):
            row = i + 1
            m = self._race_cell(match_labels[i], col_widths[0], row_height, font_size=17)
            m["cell"].move_to(cell_center(row, 0))
            match_cells.add(m["cell"])

            c1 = self._race_cell(class1_rows[i], col_widths[1], row_height, font_size=17)
            c1["cell"].move_to(cell_center(row, 1))
            class1_cells.add(c1["cell"])

            c2 = self._race_cell(
                class2_fills[i], col_widths[2], row_height,
                font_size=17, color=TEAL_D,
            )
            c2["label"].set_opacity(0)
            c2["cell"].move_to(cell_center(row, 2))
            class2_cells.add(c2["cell"])
            class2_labels.append(c2["label"])

            win_color = ORANGE if "2" in winners[i] else GREY_B
            w = self._race_cell(
                winners[i], col_widths[3], row_height,
                font_size=16, color=win_color,
            )
            w["label"].set_opacity(0)
            w["cell"].move_to(cell_center(row, 3))
            winner_cells.add(w["cell"])
            winner_labels.append(w["label"])

        table = VGroup(
            header_g, match_cells, class1_cells, class2_cells, winner_cells,
        )

        # 策略批注
        note_idea = self.safe_text(
            "策略：最弱对最强，再依次应对",
            font_size=16, color=ORANGE,
        )
        note_score_q = self.safe_text(
            "比分：?",
            font_size=16, color=YELLOW,
        )
        note_score_ans = self.safe_text(
            "比分：四(2)班 2 : 1 获胜",
            font_size=16, color=YELLOW,
        )
        for m in (note_idea, note_score_q, note_score_ans):
            m.set_opacity(0)

        notes = VGroup(note_idea, note_score_q, note_score_ans)
        note_idea.next_to(table, DOWN, buff=0.28)
        note_score_q.next_to(note_idea, DOWN, buff=0.12)
        note_score_ans.move_to(note_score_q)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "先以最弱的对最强的，然后依次应对",
                font_size=15, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.14)

        diagram = VGroup(table, notes, hint)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        diagram.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "table": table,
            "header": header_g,
            "match_cells": match_cells,
            "class1_cells": class1_cells,
            "class2_cells": class2_cells,
            "class2_labels": class2_labels,
            "winner_cells": winner_cells,
            "winner_labels": winner_labels,
            "notes": notes,
            "note_idea": note_idea,
            "note_score_q": note_score_q,
            "note_score_ans": note_score_ans,
            "hint": hint,
            "class1_rows": class1_rows,
            "class2_fills": class2_fills,
            "winners": winners,
            "n_matches": n,
        }
