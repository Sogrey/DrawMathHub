"""
画线法（轻重/大小比较）— 第5讲及同类题型。

用水平线段长度表示大小关系：越长越大（越重），越短越小（越轻）。
线段左端对齐，两端加竖线标记。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class LineCompareDiagramMixin:
    """逻辑推理比较：标签 + 左对齐线段。"""

    def _weight_line(
        self,
        length: float,
        *,
        color=WHITE,
        stroke_width: float = 4,
        cap_h: float = 0.10,
    ) -> VGroup:
        base = Line(ORIGIN, RIGHT * length, color=color, stroke_width=stroke_width)
        cap_l = Line(UP * cap_h, DOWN * cap_h, color=color, stroke_width=stroke_width)
        cap_r = cap_l.copy()
        cap_l.move_to(base.get_start())
        cap_r.move_to(base.get_end())
        return VGroup(cap_l, base, cap_r)

    def make_line_compare_diagram(
        self,
        items: list[dict[str, Any]],
        draw_y: float,
        *,
        line_left_x: float | None = None,
        row_buff: float = 0.62,
        label_gap: float = 0.22,
        line_color=WHITE,
    ) -> dict[str, Any]:
        """
        构建比较线段图。

        items 每项:
          name: str       — 名称，如「苹果」
          length: float   — 线段长度（越大表示越重/越大）
        按 items 顺序自上而下排列。
        """
        label_right_x = -0.40
        line_left_x = 0.18

        hint = self.safe_text(
            "线越长越重，线越短越轻", font_size=20, color=GREY_B,
        )

        rows: list[dict[str, Any]] = []
        row_groups: list[VGroup] = []

        for idx, item in enumerate(items):
            y = -idx * row_buff
            label = self.safe_text(f"{item['name']}：", font_size=26, color=YELLOW)
            label.move_to(np.array([label_right_x, y, 0]))
            label.align_to(np.array([label_right_x, 0, 0]), RIGHT)

            line = self._weight_line(item["length"], color=line_color)
            line.move_to(np.array([line_left_x, y, 0]))
            line.align_to(np.array([line_left_x, 0, 0]), LEFT)

            row = VGroup(label, line)
            rows.append({
                "name": item["name"],
                "length": item["length"],
                "label": label,
                "line": line,
                "row": row,
            })
            row_groups.append(row)

        diagram = VGroup(*row_groups)
        hint.next_to(diagram, UP, buff=0.28)
        full = VGroup(hint, diagram)
        full.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(full)

        by_name = {r["name"]: r for r in rows}
        return {
            "diagram": full,
            "hint": hint,
            "rows": rows,
            "by_name": by_name,
            "row_groups": row_groups,
        }
