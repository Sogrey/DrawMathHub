"""
连线法（搭配/匹配）— 第6讲及同类题型。

上下两行节点，红线两两相连，表示搭配组合。
"""

from __future__ import annotations

from typing import Any

import numpy as np

from diagrams.icon_assets import load_icon_png  # noqa: E402
from manim import *  # noqa: F403


class MatchLinkDiagramMixin:
    """搭配问题：上排与下排节点 + 连线。"""

    def _match_node(
        self,
        label: str,
        *,
        label_on_top: bool = True,
        icon_path: str | None = None,
        icon_height: float = 0.48,
        box_w: float = 0.52,
        box_h: float = 0.38,
        fill_color=TEAL_D,
        fill_opacity: float = 0.35,
        stroke_color=TEAL_D,
    ) -> dict[str, Any]:
        if icon_path:
            body = load_icon_png(icon_path, height=icon_height)
            anchor = body
        else:
            body = RoundedRectangle(
                width=box_w, height=box_h, corner_radius=0.08,
                color=stroke_color, stroke_width=2,
            )
            body.set_fill(fill_color, opacity=fill_opacity)
            anchor = body
        tag = self.safe_text(label, font_size=24, color=YELLOW)
        if label_on_top:
            tag.next_to(body, UP, buff=0.10)
            unit = Group(tag, body)
        else:
            tag.next_to(body, DOWN, buff=0.10)
            unit = Group(body, tag)
        return {"label": label, "box": anchor, "body": body, "tag": tag, "node": unit}

    def make_match_link_diagram(
        self,
        top_items: list[dict[str, Any]],
        bottom_items: list[dict[str, Any]],
        draw_y: float,
        *,
        top_buff: float = 0.72,
        bottom_buff: float = 1.15,
        row_gap: float = 1.75,
        top_y: float = 0.85,
        link_color=RED,
        link_stroke: float = 2.2,
        top_fill=TEAL_D,
        bottom_fill=PURPLE_A,
    ) -> dict[str, Any]:
        """
        构建上下连线搭配图。

        top_items / bottom_items 每项: {"label": "A", "icon": "dishes/pizza.png"} 等
        """
        top_nodes: list[dict[str, Any]] = []
        for item in top_items:
            info = self._match_node(
                item["label"],
                label_on_top=True,
                fill_color=top_fill,
                icon_path=item.get("icon"),
                icon_height=item.get("icon_height", 0.48),
            )
            top_nodes.append(info)

        bottom_nodes: list[dict[str, Any]] = []
        for item in bottom_items:
            info = self._match_node(
                item["label"],
                label_on_top=False,
                fill_color=bottom_fill,
                icon_path=item.get("icon"),
                icon_height=item.get("icon_height", 0.46),
            )
            bottom_nodes.append(info)

        top_row = Group(*[n["node"] for n in top_nodes]).arrange(RIGHT, buff=top_buff)
        bottom_row = Group(*[n["node"] for n in bottom_nodes]).arrange(RIGHT, buff=bottom_buff)
        bottom_row.next_to(top_row, DOWN, buff=row_gap)
        bottom_row.move_to(np.array([top_row.get_center()[0], bottom_row.get_center()[1], 0]))

        links: list[Line] = []
        links_by_top: dict[str, list[Line]] = {}
        for t in top_nodes:
            group: list[Line] = []
            for b in bottom_nodes:
                line = Line(
                    t["box"].get_bottom() + DOWN * 0.02,
                    b["box"].get_top() + UP * 0.02,
                    color=link_color, stroke_width=link_stroke,
                )
                links.append(line)
                group.append(line)
            links_by_top[t["label"]] = group

        nodes_block = Group(top_row, bottom_row)
        links_block = VGroup(*links)

        hint = self.safe_text(
            "每菜连每种饮料，不重不漏", font_size=20, color=GREY_B,
        )
        hint.next_to(top_row, UP, buff=0.22)

        diagram = Group(hint, nodes_block)
        full = Group(diagram, links_block)
        full.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(full)

        by_top = {n["label"]: n for n in top_nodes}
        by_bottom = {n["label"]: n for n in bottom_nodes}
        return {
            "diagram": full,
            "hint": hint,
            "nodes_block": nodes_block,
            "top_row": top_row,
            "bottom_row": bottom_row,
            "top_nodes": top_nodes,
            "bottom_nodes": bottom_nodes,
            "by_top": by_top,
            "by_bottom": by_bottom,
            "links": links,
            "links_by_top": links_by_top,
            "links_block": links_block,
            "link_count": len(links),
        }
