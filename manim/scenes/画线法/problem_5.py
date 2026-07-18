"""
第5讲 逻辑推理问题（一）— 画图解题法（画线法）

母题：苹果、香蕉、梨比轻重，哪个最重？哪个最轻？
答案：苹果最重，香蕉最轻。

用法:
  cd manim/scenes/画线法
  python -m manim problem_5.py Problem5Scene -qh

渲染后:
  python ..\_shared\post_render.py --lesson 5 \\
    --rendered media\videos\problem_5\1080p60\Problem5Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem5Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    # 苹果 > 梨 > 香蕉
    COMPARE_ITEMS = [
        {"name": "苹果", "length": 2.8},
        {"name": "香蕉", "length": 1.4},
        {"name": "梨", "length": 2.0},
    ]

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

            concept_title = self.safe_text("题型识别", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "根据已知的数量关系，推出谁大谁小、谁重谁轻——", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "这就是逻辑推理问题！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("画线法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "画线段表示大小", "线段越长，表示越重（越大）"),
                ("2", "左端对齐比较", "一眼看出谁长谁短"),
                ("3", "逐步补全关系", "根据条件逐条画线，推出结论"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：找出比较关系"):
            prob_all = self.make_problem_box(
                "题目：有苹果、香蕉和梨三个水果，苹果比香蕉重，梨比香蕉重，",
                "梨比苹果轻。请你想一想，哪个水果最重？哪个水果最轻？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_line_compare_diagram(self.COMPARE_ITEMS, draw_y)
        apple = diag["by_name"]["苹果"]
        banana = diag["by_name"]["香蕉"]
        pear = diag["by_name"]["梨"]

        # ── 图解1：苹果 vs 香蕉 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "苹果比香蕉重"):
            s1 = self.step_label("第一步：苹果比香蕉重，画长线和短线")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            for row in (apple, banana):
                self.play(FadeIn(row["label"], shift=RIGHT * 0.12), run_time=0.35)
                self.play(Create(row["line"]), run_time=0.55)
            self.safe_subtitle("苹果比香蕉重 → 苹果的线比香蕉的线长", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：补上梨 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "梨比香蕉重、比苹果轻"):
            self.add(prob_all, diag["hint"], apple["row"], banana["row"])
            s2 = self.step_label("第二步：根据梨的条件补画线段")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(pear["label"], shift=RIGHT * 0.12), run_time=0.35)
            self.play(Create(pear["line"]), run_time=0.6)
            self.safe_subtitle("梨比香蕉重、比苹果轻 → 梨的线在中间", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：得出结论 ──
        heaviest_tag = lightest_tag = None
        with self.segment("draw-3", "3", "segments/05.mp4", "比较线段得出结论"):
            self.add(prob_all, diag["diagram"])
            s3 = self.step_label("第三步：比较三条线段，得出结论")
            self.play(FadeIn(s3), run_time=0.5)
            heaviest_tag = self.safe_text("最重", font_size=22, color=RED)
            heaviest_tag.next_to(apple["line"], RIGHT, buff=0.15)
            lightest_tag = self.safe_text("最轻", font_size=22, color=TEAL_D)
            lightest_tag.next_to(banana["line"], RIGHT, buff=0.15)
            self.play(
                apple["line"].animate.set_color(YELLOW),
                FadeIn(heaviest_tag, shift=LEFT * 0.1),
                run_time=0.55,
            )
            self.play(
                banana["line"].animate.set_color(GREY_B),
                FadeIn(lightest_tag, shift=LEFT * 0.1),
                run_time=0.55,
            )
            self.safe_subtitle("苹果的线最长 → 最重；香蕉的线最短 → 最轻", wait=4)
            self.wait(1)
            self.play(FadeOut(s3), run_time=0.3)

        diagram_all = VGroup(diag["diagram"])
        if heaviest_tag is not None:
            diagram_all.add(heaviest_tag, lightest_tag)

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/06.mp4", "书面答题：规范作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            answer_text = self.safe_text(
                "答：苹果最重，香蕉最轻。", font_size=32, color=YELLOW,
            )
            answer_text.move_to(np.array([
                left_x + answer_text.width / 2,
                self.written_left_y(0.2), 0,
            ]))
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(answer_text, color=RED, buff=0.12, corner_radius=0.1)
            self.play(FadeIn(answer_text, shift=UP * 0.2), run_time=0.8)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("画线比较：越长越重，越短越轻", wait=5)
            self.wait(2)
            self.play(
                FadeOut(answer_text), FadeOut(highlight_box), FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
