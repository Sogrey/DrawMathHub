"""
第12讲 组数问题 — 画图解题法（树状图法）

母题：用数字 2、4、6、8 能组成多少个不同的无重复数字的四位数？
答案：6×4=24（个）

用法:
  cd manim/scenes/树状图法
  python -m manim problem_12.py Problem12Scene -ql

渲染后:
  python ..\\_shared\\post_render.py --lesson 12 \\
    --rendered media\\videos\\problem_12\\480p15\\Problem12Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem12Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    DIGITS = [2, 4, 6, 8]
    FIXED_FIRST = 2

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        count_per = 6  # 3!
        first_choices = 4
        total = count_per * first_choices

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是组数问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "用给出的数字，按要求组成多位数，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求一共有多少种不同组法——这就是组数问题！", font_size=28, color=WHITE,
            )
            concept_body = VGroup(s1_body, s1_body2).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            concept_body.next_to(concept_title, DOWN, buff=0.45)
            concept_body.move_to(np.array([0, concept_body.get_center()[1], 0]))
            self.clamp_content(concept_body)
            concept_block = VGroup(concept_title, concept_body)

            divider_y = concept_block.get_bottom()[1] - 0.45
            divider = Line(
                np.array([self.safe_left + 0.5, divider_y, 0]),
                np.array([self.safe_right - 0.5, divider_y, 0]),
                stroke_width=1.5, color=GREY_B, stroke_opacity=0.25,
            )

            feature_title = self.safe_text("树状图法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先定首位，再定后续数位", "比如：先定千位，再定百、十、个位"),
                ("2", "画树状图分支表示选法", "每个分支代表一种数字选择"),
                ("3", "数分支再乘以首位选法", "首位固定时的组数 × 首位有几种"),
            ]
            feature_groups = self.layout_numbered_features(
                features,
                top_y=feature_title.get_bottom()[1] - 0.50,
                row_step=1.12,
            )
            intro_all = VGroup(concept_block, divider, feature_title, *feature_groups)

            self.play(FadeIn(concept_block, shift=DOWN * 0.15), run_time=0.8)
            self.wait(2)
            self.play(FadeIn(divider), FadeIn(feature_title, shift=DOWN * 0.15), run_time=0.6)
            for row in feature_groups:
                self.play(FadeIn(row, shift=RIGHT * 0.25), run_time=0.5)
                self.wait(1)
            self.wait(2)
            self.play(FadeOut(intro_all), run_time=0.5)

        # ── 题目展示 ──
        prob_all = None
        with self.segment("question", "题目", "segments/02.mp4", "读题：用给定数字组四位数"):
            prob_all = self.make_problem_box(
                "题目：用数字2、4、6、8能组成多少个",
                "不同的无重复数字的四位数？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_digit_tree_diagram(
            self.DIGITS, self.FIXED_FIRST, draw_y,
            y_step=0.36,
            x_step=0.88,
            node_r=0.17,
            show_hint=False,
            x_shift=1.15,
            scale=0.90,
        )
        tree_core = Group(diag["headers"], diag["tree_nodes"], diag["edges"])
        if len(diag["results"]) > 0:
            tree_core.add(diag["results"])

        # ── 图解1：列标题 + 千位根节点 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "先确定千位上的数字"):
            s1 = self.step_label("第一步：先确定千位上的数字")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["headers"]), run_time=0.5)
            self.play(FadeIn(diag["root"], scale=0.85), run_time=0.6)
            self.safe_subtitle(
                f"以{self.FIXED_FIRST}在千位为例，从左到右依次确定各数位",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：百位分支 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "确定百位上的数字"):
            self.add(prob_all, diag["headers"], diag["root"])
            s2 = self.step_label("第二步：确定百位上的数字")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["level1_nodes"], scale=0.85), run_time=0.55)
            if len(diag["edges_l1"]) > 0:
                self.play(*[Create(e) for e in diag["edges_l1"]], run_time=0.75)
            self.safe_subtitle("百位可从剩余数字中选，这里分出 3 条分支", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：十位、个位 + 结果数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "确定十位和个位"):
            self.add(
                prob_all, diag["headers"], diag["root"],
                diag["level1_nodes"], diag["edges_l1"],
            )
            s3 = self.step_label("第三步：依次确定十位和个位上的数字")
            self.play(FadeIn(s3), run_time=0.5)
            if len(diag["level2_nodes"]) > 0:
                self.play(FadeIn(diag["level2_nodes"], scale=0.85), run_time=0.55)
            if len(diag["edges_l2"]) > 0:
                self.play(*[Create(e) for e in diag["edges_l2"]], run_time=0.65)
            if len(diag["level3_nodes"]) > 0:
                self.play(FadeIn(diag["level3_nodes"], scale=0.85), run_time=0.55)
            if len(diag["edges_l3"]) > 0:
                self.play(*[Create(e) for e in diag["edges_l3"]], run_time=0.65)
            if len(diag["results"]) > 0:
                self.play(FadeIn(diag["results"], shift=RIGHT * 0.15), run_time=0.6)
            self.safe_subtitle(
                f"每条完整分支对应一个四位数，以{self.FIXED_FIRST}为千位共 {count_per} 个",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：统计总数 ──
        count_label = formula_label = stats_block = None
        with self.segment("draw-4", "4", "segments/06.mp4", "统计组数"):
            self.add(prob_all, tree_core)
            s4 = self.step_label("第四步：统计组数，求总数")
            self.play(FadeIn(s4), run_time=0.5)

            count_label = self.safe_text(
                f"以{self.FIXED_FIRST}为千位有 {count_per} 个；"
                f"同理以4、6、8为千位也各有 {count_per} 个",
                font_size=20, color=YELLOW,
            )
            formula_label = self.safe_text(
                f"千位有 {first_choices} 种选法 → {count_per}×{first_choices}={total}（个）",
                font_size=22, color=TEAL_D,
            )
            stats_block = VGroup(count_label, formula_label).arrange(
                DOWN, buff=0.14, aligned_edge=LEFT,
            )
            stats_bottom = self.safe_bottom + 0.38
            stats_block.move_to(np.array([
                0,
                stats_bottom + stats_block.height / 2,
                0,
            ]))
            self.clamp_content(stats_block)
            self.play(FadeIn(stats_block), run_time=0.6)
            self.wait(5)
            self.play(FadeOut(s4), run_time=0.3)

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, tree_core)
            if stats_block is not None:
                self.remove(stats_block)
            written_diagram_scale = self.place_diagram_for_written(tree_core)

            left_x = self.written_left_x()
            left_col_center_y = self.written_left_y()
            explain = self.safe_text(
                f"以{self.FIXED_FIRST}为千位有 {count_per} 个，千位有 {first_choices} 种选法",
                font_size=24, color=GREY_B,
            )
            explain.move_to(np.array([
                left_x + explain.width / 2,
                left_col_center_y + 0.75, 0,
            ]))
            explain.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(explain)
            self.play(FadeIn(explain), run_time=0.5)
            self.wait(1.5)

            formula = self.safe_text(
                f"{count_per}×{first_choices}={total}（个）",
                font_size=32, color=WHITE,
            )
            formula.next_to(explain, DOWN, buff=0.45)
            formula.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula)
            self.play(FadeIn(formula), run_time=0.6)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：用数字2、4、6、8能组成{total}个\n不同的无重复数字的四位数。",
                font_size=30, color=YELLOW,
            )
            answer_text.next_to(formula, DOWN, buff=0.55)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("树状图法：先分析首位固定时的组数，再乘首位选法", wait=5)
            self.wait(2)
            self.play(
                FadeOut(explain), FadeOut(formula), FadeOut(answer_text),
                FadeOut(highlight_box), FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=tree_core, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
