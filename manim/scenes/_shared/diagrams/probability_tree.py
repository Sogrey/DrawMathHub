"""
概率问题 — 第53讲：三辆车路口选择的树状图。

每层（每辆车）分三支：左、直、右；共 3×3×3=27 种等可能结果。
高亮「直→直→直」这一条，对应有利结果 m=1。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from manim import *  # noqa: F403


class ProbabilityTreeDiagramMixin:
    """古典概率：树状图枚举等可能结果。"""

    def make_probability_tree_diagram(
        self,
        draw_y: float,
        *,
        choices: tuple[str, ...] = ("左", "直", "右"),
        favor: str = "直",
        cars: int = 3,
        tree_w: float = 8.6,
        level_gap: float = 0.78,
        show_hint: bool = False,
        x_shift: float = 0.0,
    ) -> dict[str, Any]:
        if cars != 3 or len(choices) != 3 or favor not in choices:
            raise ValueError("本图解固定为三车、三向，且 favor 须在 choices 中")

        n = len(choices)  # 3
        total = n ** cars  # 27
        favor_idx = choices.index(favor)
        # 有利结果：全部直行
        favor_count = 1

        # 局部坐标：顶层 y=1.05，向下展开
        y1, y2, y3 = 1.05, 1.05 - level_gap, 1.05 - 2 * level_gap
        left_x = -tree_w / 2
        # 第三层 27 个叶子均分
        leaf_xs = [left_x + (i + 0.5) * tree_w / total for i in range(total)]
        # 第二层：每组 3 叶取中点
        mid_xs = [
            sum(leaf_xs[i * n:(i + 1) * n]) / n
            for i in range(n * n)
        ]
        # 第一层：每组 9 叶取中点
        top_xs = [
            sum(leaf_xs[i * n * n:(i + 1) * n * n]) / (n * n)
            for i in range(n)
        ]
        root_x = 0.0
        root_y = y1 + 0.42

        favor_color = TEAL_B
        normal_color = GREY_B
        line_color = GREY_A

        # 行标签
        lab1 = self.safe_text("第一辆", font_size=16, color=YELLOW)
        lab2 = self.safe_text("第二辆", font_size=16, color=YELLOW)
        lab3 = self.safe_text("第三辆", font_size=16, color=YELLOW)
        for lab, y in ((lab1, y1), (lab2, y2), (lab3, y3)):
            lab.move_to(np.array([left_x - 0.72, y, 0]))

        # 根到第一层
        root_dot = Dot(np.array([root_x, root_y, 0]), radius=0.05, color=WHITE)

        edges1 = VGroup()
        nodes1 = VGroup()
        texts1 = VGroup()
        for i, ch in enumerate(choices):
            p = np.array([top_xs[i], y1, 0])
            is_f = i == favor_idx
            col = favor_color if is_f else WHITE
            e = Line(
                np.array([root_x, root_y, 0]), p,
                color=favor_color if is_f else line_color,
                stroke_width=2.8 if is_f else 1.8,
            )
            t = self.safe_text(ch, font_size=20, color=col)
            t.move_to(p + UP * 0.22)
            nodes1.add(Dot(p, radius=0.04, color=col))
            edges1.add(e)
            texts1.add(t)

        # 第一→第二
        edges2 = VGroup()
        nodes2 = VGroup()
        texts2 = VGroup()
        for i in range(n):  # 父：第一层
            for j, ch in enumerate(choices):
                mid_i = i * n + j
                p0 = np.array([top_xs[i], y1, 0])
                p1 = np.array([mid_xs[mid_i], y2, 0])
                is_f = i == favor_idx and j == favor_idx
                col = favor_color if is_f else WHITE
                e = Line(
                    p0, p1,
                    color=favor_color if is_f else line_color,
                    stroke_width=2.6 if is_f else 1.4,
                )
                t = self.safe_text(ch, font_size=15, color=col)
                t.move_to(p1 + UP * 0.18)
                nodes2.add(Dot(p1, radius=0.035, color=col))
                edges2.add(e)
                texts2.add(t)

        # 第二→第三（叶子）
        edges3 = VGroup()
        nodes3 = VGroup()
        texts3 = VGroup()
        favor_leaf_idx = favor_idx * n * n + favor_idx * n + favor_idx  # 直直直
        for mid_i in range(n * n):
            i = mid_i // n
            j = mid_i % n
            for k, ch in enumerate(choices):
                leaf_i = mid_i * n + k
                p0 = np.array([mid_xs[mid_i], y2, 0])
                p1 = np.array([leaf_xs[leaf_i], y3, 0])
                is_f = leaf_i == favor_leaf_idx
                col = favor_color if is_f else WHITE
                e = Line(
                    p0, p1,
                    color=favor_color if is_f else line_color,
                    stroke_width=2.4 if is_f else 1.0,
                )
                t = self.safe_text(ch, font_size=11, color=col)
                t.move_to(p1 + DOWN * 0.16)
                nodes3.add(Dot(p1, radius=0.025, color=col))
                edges3.add(e)
                texts3.add(t)

        # 分组：便于分步动画
        layer1 = VGroup(edges1, nodes1, texts1)
        layer2 = VGroup(edges2, nodes2, texts2)
        layer3 = VGroup(edges3, nodes3, texts3)
        row_labs = VGroup(lab1, lab2, lab3)

        for m in (root_dot, layer1, layer2, layer3, row_labs):
            m.set_opacity(0)

        # 底部说明
        note_total = self.safe_text(
            f"全部可能：{n}×{n}×{n}={total}（种）",
            font_size=18, color=WHITE,
        )
        note_favor = self.safe_text(
            f"全部{favor}行：只有 {favor_count} 种",
            font_size=18, color=favor_color,
        )
        note_prob = self.safe_text(
            f"概率＝{favor_count}÷{total}＝1/{total}",
            font_size=20, color=YELLOW,
        )
        for m in (note_total, note_favor, note_prob):
            m.set_opacity(0)

        notes = VGroup(note_total, note_favor, note_prob).arrange(
            DOWN, buff=0.12, aligned_edge=LEFT,
        )
        notes.next_to(layer3, DOWN, buff=0.42)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                "等可能结果：P＝有利÷全部",
                font_size=14, color=GREY_B,
            )
            hint.next_to(notes, DOWN, buff=0.10)

        diagram = VGroup(
            root_dot, row_labs, layer1, layer2, layer3, notes, hint,
        )
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        # 整体略右移，给左侧行标签留空
        diagram.shift(RIGHT * 0.35)
        diagram.move_to(np.array([0.2, draw_y, 0]))
        self.clamp_content(diagram)

        return {
            "diagram": diagram,
            "root_dot": root_dot,
            "row_labs": row_labs,
            "lab1": lab1,
            "lab2": lab2,
            "lab3": lab3,
            "layer1": layer1,
            "layer2": layer2,
            "layer3": layer3,
            "edges1": edges1,
            "edges2": edges2,
            "edges3": edges3,
            "texts1": texts1,
            "texts2": texts2,
            "texts3": texts3,
            "nodes1": nodes1,
            "nodes2": nodes2,
            "nodes3": nodes3,
            "notes": notes,
            "note_total": note_total,
            "note_favor": note_favor,
            "note_prob": note_prob,
            "hint": hint,
            "choices": choices,
            "favor": favor,
            "total": total,
            "favor_count": favor_count,
            "n": n,
            "answer": f"全部{favor}行的概率是1/{total}",
        }
