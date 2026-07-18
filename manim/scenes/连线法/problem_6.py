"""
第6讲 搭配问题 — 画图解题法（连线法）

母题：4 道菜 × 2 种饮料各选一个，几种搭配？
答案：4×2=8（种）

用法:
  cd manim/scenes/连线法
  python -m manim problem_6.py Problem6Scene -qh

渲染后:
  python ..\_shared\post_render.py --lesson 6 \\
    --rendered media\videos\problem_6\1080p60\Problem6Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem6Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    TOP_ITEMS = [
        {"label": "A", "icon": "dishes/pizza.png"},
        {"label": "B", "icon": "dishes/burger.png"},
        {"label": "C", "icon": "dishes/skewer.png"},
        {"label": "D", "icon": "dishes/noodles.png"},
    ]
    BOTTOM_ITEMS = [
        {"label": "①", "icon": "drinks/drink_cup.png"},
        {"label": "②", "icon": "drinks/soda.png"},
    ]
    TOP_COUNT = 4
    BOTTOM_COUNT = 2

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
                "从两类物品中各选一个组成一对，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求一共有几种不同搭配——这就是搭配问题！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("连线法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "上下（或左右）两类物品", "比如：菜和饮料各选一个"),
                ("2", "连线表示一种搭配", "每个菜连每个饮料，画清楚"),
                ("3", "不重不漏有序连线", "数线条或乘法得总数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：菜和饮料各选一个"):
            prob_all = self.make_problem_box(
                "题目：林林在食堂吃饭，菜和饮料各选一个，",
                "一共有几种不同的搭配方法？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_match_link_diagram(self.TOP_ITEMS, self.BOTTOM_ITEMS, draw_y)
        total_methods = self.TOP_COUNT * self.BOTTOM_COUNT

        # ── 图解1：画节点 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "标号并排列菜和饮料"):
            s1 = self.step_label("第一步：给菜和饮料编号，画上下两排")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            self.play(FadeIn(diag["top_row"], shift=DOWN * 0.12), run_time=0.65)
            self.play(FadeIn(diag["bottom_row"], shift=UP * 0.12), run_time=0.55)
            self.safe_subtitle("上排 A~D 是四道菜，下排 ①② 是两种饮料", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：A 的连线 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "从 A 开始连线"):
            self.add(prob_all, diag["hint"], diag["top_row"], diag["bottom_row"])
            s2 = self.step_label("第二步：从 A 菜开始，连每种饮料")
            self.play(FadeIn(s2), run_time=0.5)
            a_links = diag["links_by_top"]["A"]
            self.play(*[Create(line) for line in a_links], run_time=0.75)
            self.safe_subtitle("A 菜连 ① 和 ②，有 2 种搭配", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：B、C、D 连线 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "其余菜依次连线"):
            self.add(prob_all, diag["hint"], diag["nodes_block"], *a_links)
            s3 = self.step_label("第三步：B、C、D 菜也分别连线")
            self.play(FadeIn(s3), run_time=0.5)
            rest_anims = []
            for label in ("B", "C", "D"):
                rest_anims.append(
                AnimationGroup(*[Create(line) for line in diag["links_by_top"][label]]),
                )
            self.play(LaggedStart(*rest_anims, lag_ratio=0.25), run_time=1.4)
            self.safe_subtitle("每道菜都能连 2 种饮料，4 道菜共 4×2 条线", wait=4)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：统计 ──
        count_label = formula_label = None
        with self.segment("draw-4", "4", "segments/06.mp4", "数线条得搭配种数"):
            self.add(prob_all, diag["diagram"])
            s4 = self.step_label("第四步：数连线，得出搭配种数")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(
                diag["links_block"].animate.set_stroke(width=3.2, opacity=1.0),
                run_time=0.5,
            )
            count_label = self.safe_text(
                f"共 {diag['link_count']} 条线 → {total_methods} 种搭配",
                font_size=22, color=YELLOW,
            )
            count_label.next_to(diag["nodes_block"], DOWN, buff=0.28)
            self.clamp_content(count_label)
            formula_label = self.safe_text(
                f"{self.BOTTOM_COUNT}×{self.TOP_COUNT}={total_methods}（种）",
                font_size=22, color=TEAL_D,
            )
            formula_label.next_to(count_label, DOWN, buff=0.14)
            self.clamp_content(formula_label)
            self.play(FadeIn(count_label), FadeIn(formula_label), run_time=0.6)
            self.safe_subtitle("每条线是一种搭配，共 8 种不同的搭配方法", wait=4)
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = Group(diag["diagram"])
        if count_label is not None:
            diagram_all.add(count_label, formula_label)

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            formula = self.safe_text(
                f"{self.BOTTOM_COUNT}×{self.TOP_COUNT}={total_methods}（种）"
                f"　或　{self.TOP_COUNT}×{self.BOTTOM_COUNT}={total_methods}（种）",
                font_size=26, color=WHITE,
            )
            formula.move_to(np.array([
                left_x + formula.width / 2,
                self.written_left_y(0.35), 0,
            ]))
            formula.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula)
            self.play(FadeIn(formula), run_time=0.6)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：一共有{total_methods}种不同的搭配方法。",
                font_size=32, color=YELLOW,
            )
            answer_text.next_to(formula, DOWN, buff=0.65)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(answer_text, color=RED, buff=0.12, corner_radius=0.1)
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("连线法：有序连线，不重不漏", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula), FadeOut(answer_text),
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
