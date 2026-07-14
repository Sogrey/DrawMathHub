"""
树状图法（组数/排列）— 第12讲及同类题型。

从左到右按数位分支，展示无重复数字组数。
"""

from __future__ import annotations

from itertools import permutations
from typing import Any

import numpy as np

from manim import *  # noqa: F403


class _TrieNode:
    __slots__ = ("digit", "children", "x", "y", "path")

    def __init__(self, digit: int, path: tuple[int, ...]) -> None:
        self.digit = digit
        self.path = path
        self.children: list[_TrieNode] = []
        self.x = 0.0
        self.y = 0.0


class TreeDigitDiagramMixin:
    """组数问题：数位树状图（固定首位示例）。"""

    def _build_digit_trie(self, digits: list[int], fixed_first: int) -> _TrieNode:
        rest = [d for d in digits if d != fixed_first]
        root = _TrieNode(fixed_first, (fixed_first,))
        for perm in permutations(rest):
            path = (fixed_first,) + perm
            node = root
            for i in range(1, len(path)):
                child_digit = path[i]
                child_path = path[: i + 1]
                found = next(
                    (c for c in node.children if c.digit == child_digit),
                    None,
                )
                if found is None:
                    found = _TrieNode(child_digit, child_path)
                    node.children.append(found)
                node = found
        return root

    def _assign_trie_positions(
        self,
        root: _TrieNode,
        *,
        x_step: float,
        y_step: float,
    ) -> list[_TrieNode]:
        leaves: list[_TrieNode] = []

        def collect_leaves(node: _TrieNode) -> None:
            if not node.children:
                leaves.append(node)
            else:
                for child in node.children:
                    collect_leaves(child)

        collect_leaves(root)
        for i, leaf in enumerate(leaves):
            leaf.y = (len(leaves) - 1) / 2 * y_step - i * y_step

        all_nodes: list[_TrieNode] = []

        def assign(node: _TrieNode, depth: int) -> None:
            node.x = depth * x_step
            all_nodes.append(node)
            if node.children:
                for child in node.children:
                    assign(child, depth + 1)
                node.y = sum(c.y for c in node.children) / len(node.children)

        assign(root, 0)
        return all_nodes

    def _digit_tree_node(
        self,
        digit: int,
        *,
        radius: float = 0.20,
        color=TEAL_D,
    ) -> VGroup:
        circle = Circle(radius=radius, color=color, stroke_width=2)
        circle.set_fill(color, opacity=0.35)
        label = Text(str(digit), font_size=20, color=WHITE, font=self.DEFAULT_FONT)
        label.move_to(circle.get_center())
        return VGroup(circle, label)

    def make_digit_tree_diagram(
        self,
        digits: list[int],
        fixed_first: int,
        draw_y: float,
        *,
        place_labels: list[str] | None = None,
        x_step: float = 1.05,
        y_step: float = 0.48,
        node_r: float = 0.20,
        show_results: bool = True,
        show_hint: bool = True,
        x_shift: float = 0.0,
        scale: float = 1.0,
    ) -> dict[str, Any]:
        """
        构建固定首位的数位树状图。

        digits: 可用数字列表，如 [2, 4, 6, 8]
        fixed_first: 示范的首位数字，如 2
        """
        if place_labels is None:
            n = len(digits)
            defaults = ["千位", "百位", "十位", "个位", "万位", "十万位"]
            place_labels = defaults[:n]

        root_trie = self._build_digit_trie(digits, fixed_first)
        all_trie_nodes = self._assign_trie_positions(
            root_trie, x_step=x_step, y_step=y_step,
        )

        node_map: dict[tuple[int, ...], VGroup] = {}
        for tn in all_trie_nodes:
            mob = self._digit_tree_node(tn.digit, radius=node_r)
            mob.move_to(np.array([tn.x, tn.y, 0]))
            node_map[tn.path] = mob

        edges: list[Line] = []
        edges_l1: list[Line] = []
        edges_l2: list[Line] = []
        edges_l3: list[Line] = []

        def add_edges(node: _TrieNode) -> None:
            for child in node.children:
                p = node_map[node.path].get_center()
                c = node_map[child.path].get_center()
                edge = Line(p, c, color=GREY_B, stroke_width=1.8)
                edges.append(edge)
                depth = len(child.path) - 1
                if depth == 1:
                    edges_l1.append(edge)
                elif depth == 2:
                    edges_l2.append(edge)
                else:
                    edges_l3.append(edge)
                add_edges(child)

        add_edges(root_trie)

        headers: list[Mobject] = []
        for i, label in enumerate(place_labels[: len(digits)]):
            hdr = self.safe_text(label, font_size=18, color=YELLOW)
            hdr.move_to(np.array([i * x_step, 0, 0]))
            headers.append(hdr)

        root_mob = node_map[(fixed_first,)]
        level1_nodes = VGroup(*[
            node_map[child.path] for child in root_trie.children
        ])
        level2_nodes = VGroup(*[
            mob for path, mob in node_map.items()
            if len(path) == 3
        ])
        level3_nodes = VGroup(*[
            mob for path, mob in node_map.items()
            if len(path) == 4
        ])

        results_block = VGroup()
        result_numbers: list[str] = []
        if show_results and len(digits) == 4:
            rest = [d for d in digits if d != fixed_first]
            for perm in permutations(rest):
                num_str = "".join(str(d) for d in (fixed_first,) + perm)
                result_numbers.append(num_str)
            result_mobs: list[Mobject] = []
            for num_str in result_numbers:
                txt = self.safe_text(num_str, font_size=16, color=WHITE)
                result_mobs.append(txt)
            results_block = VGroup(*result_mobs).arrange(DOWN, buff=0.12)
            if level3_nodes:
                results_block.next_to(level3_nodes, RIGHT, buff=0.35)
                for i, leaf_tn in enumerate([
                    n for n in all_trie_nodes if len(n.path) == len(digits)
                ]):
                    if i < len(result_mobs):
                        result_mobs[i].move_to(np.array([
                            results_block.get_left()[0] + results_block.width / 2,
                            node_map[leaf_tn.path].get_center()[1],
                            0,
                        ]))

        count_per_first = len(list(permutations(
            [d for d in digits if d != fixed_first],
        )))
        first_choices = len(digits)

        hint = VGroup()
        if show_hint:
            hint = self.safe_text(
                f"以{fixed_first}为{place_labels[0]}，依次确定后续数位",
                font_size=20, color=GREY_B,
            )

        tree_nodes = VGroup(*node_map.values())
        edges_vg = VGroup(*edges)
        headers_vg = VGroup(*headers)

        content = Group(headers_vg, tree_nodes, edges_vg)
        if show_results and len(results_block) > 0:
            content.add(results_block)

        full = Group(content)
        full.move_to(np.array([0, draw_y, 0]))

        headers_vg.next_to(tree_nodes, UP, buff=0.55)
        headers_vg.shift(RIGHT * (headers_vg.get_center()[0] - tree_nodes.get_center()[0]))
        for i, hdr in enumerate(headers):
            hdr.move_to(np.array([
                i * x_step + tree_nodes.get_center()[0] - (len(digits) - 1) * x_step / 2,
                headers_vg.get_center()[1],
                0,
            ]))

        if show_hint:
            hint.next_to(full, DOWN, buff=0.22)
            diagram = Group(hint, content)
        else:
            diagram = Group(content)
        if scale != 1.0:
            diagram.scale(scale)
        if x_shift != 0.0:
            diagram.shift(RIGHT * x_shift)
        full_with_hint = Group(diagram)
        full_with_hint.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(full_with_hint)

        return {
            "diagram": diagram,
            "content": content,
            "full": full_with_hint,
            "hint": hint,
            "headers": headers_vg,
            "root": root_mob,
            "level1_nodes": level1_nodes,
            "level2_nodes": level2_nodes,
            "level3_nodes": level3_nodes,
            "edges_l1": VGroup(*edges_l1),
            "edges_l2": VGroup(*edges_l2),
            "edges_l3": VGroup(*edges_l3),
            "edges": edges_vg,
            "tree_nodes": tree_nodes,
            "results": results_block,
            "result_numbers": result_numbers,
            "count_per_first": count_per_first,
            "first_choices": first_choices,
            "fixed_first": fixed_first,
            "place_labels": place_labels,
        }
