"""
第37讲 逻辑推理问题（二）— 画图解题法（列表法）

母题：红红、丽丽、莹莹帽子颜色（红/黄/蓝）推理。
答案：红红蓝、丽丽红、莹莹黄

用法:
  cd manim/scenes/列表法
  python -m manim problem_37.py Problem37Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem37Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=30, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.32, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "根据几句“是/不是”的条件，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用表格逐步排除，推出谁对应什么——这就是列表推理！",
                font_size=26, color=WHITE,
            )
            concept_body = VGroup(s1_body, s1_body2).arrange(
                DOWN, buff=0.20, aligned_edge=LEFT,
            )
            concept_body.next_to(concept_title, DOWN, buff=0.38)
            concept_body.move_to(np.array([0, concept_body.get_center()[1], 0]))
            self.clamp_content(concept_body)
            concept_block = VGroup(concept_title, concept_body)

            divider_y = concept_block.get_bottom()[1] - 0.38
            divider = Line(
                np.array([self.safe_left + 0.5, divider_y, 0]),
                np.array([self.safe_right - 0.5, divider_y, 0]),
                stroke_width=1.5, color=GREY_B, stroke_opacity=0.25,
            )

            feature_title = self.safe_text("列表推理的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先建人×属性表", "每格表示一种对应可能"),
                ("2", "把不可能的画×", "条件说“不是”就先排除"),
                ("3", "只剩一种就画√", "再连锁排除其他人"),
            ]
            feature_groups = self.layout_numbered_features(
                features,
                top_y=feature_title.get_bottom()[1] - 0.42,
                row_step=1.08,
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：帽子颜色"):
            prob_all = self.make_problem_box(
                "题目：红黄蓝三顶帽子，红红说不是黄；丽丽说不是黄也不是蓝。",
                "三人分别戴什么颜色的帽子？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_logic_hat_table(draw_y, show_hint=True)
        mx = diag["mark_cross"]
        mk = diag["mark_check"]
        h, li, y = diag["hong"], diag["lili"], diag["ying"]
        r, ye, b = diag["red"], diag["yellow"], diag["blue"]

        # ── 图解1：建表 + 红红排除黄 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "建表并排除"):
            s1 = self.step_label("第一步：列出人与颜色表格，先记红红不是黄")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["table"]), run_time=0.7)
            self.play(mx(h, ye).animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle("红红：不是黄色帽子 → 黄色打×", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：丽丽只剩红 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "丽丽确定红色"):
            self.add(prob_all, diag["hint"], diag["table"], diag["notes"])
            s2 = self.step_label("第二步：丽丽不是黄也不是蓝，只剩红色")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                mx(li, ye).animate.set_opacity(1),
                mx(li, b).animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(mk(li, r).animate.set_opacity(1), run_time=0.45)
            self.play(
                mx(h, r).animate.set_opacity(1),
                mx(y, r).animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(diag["note_lili"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle("丽丽戴红色 → 红红、莹莹的红色打×", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：红红只剩蓝 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "红红确定蓝色"):
            self.add(prob_all, diag["hint"], diag["table"], diag["notes"])
            s3 = self.step_label("第三步：红红红、黄都排除，只剩蓝色")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(mk(h, b).animate.set_opacity(1), run_time=0.5)
            self.play(mx(y, b).animate.set_opacity(1), run_time=0.4)
            self.play(diag["note_hong"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle("红红戴蓝色 → 莹莹的蓝色打×", wait=4)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：莹莹只剩黄 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "莹莹确定黄色"):
            self.add(prob_all, diag["hint"], diag["table"], diag["notes"])
            s4 = self.step_label("第四步：莹莹只剩黄色，三人全部确定")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(mk(y, ye).animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_ying"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle(
                "莹莹戴黄色帽子，推理完成",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(diag["table"], diag["notes"])

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                self.safe_text("红红：蓝色帽子", font_size=24, color=TEAL_D),
                self.safe_text("丽丽：红色帽子", font_size=24, color=ORANGE),
                self.safe_text("莹莹：黄色帽子", font_size=24, color=YELLOW),
            ]
            formula_rows = VGroup(*lines).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in lines:
                self.play(FadeIn(row), run_time=0.45)
                self.wait(0.9)

            answer_text = self.safe_text(
                "答：红红蓝、丽丽红、莹莹黄。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("逐一排除不可能的结果", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula_rows), FadeOut(answer_text),
                FadeOut(highlight_box), FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
