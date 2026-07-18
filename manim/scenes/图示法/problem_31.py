"""
第31讲 植树问题 — 画图解题法（图示法）

母题：公路长100米，每隔10米栽一棵，两端都栽。一共栽多少棵？
答案：100÷10＋1＝11（棵）

用法:
  cd manim/scenes/图示法
  python -m manim problem_31.py Problem31Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem31Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    DISTANCE = 100
    GAP = 10

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        dist = self.DISTANCE
        gap = self.GAP
        intervals = dist // gap
        trees = intervals + 1

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
                "在一条线段上按固定间隔栽树，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "根据两端栽不栽，由距离、间隔求出棵数——这就是植树问题！",
                font_size=28, color=WHITE,
            )
            concept_body = VGroup(s1_body, s1_body2).arrange(
                DOWN, buff=0.22, aligned_edge=LEFT,
            )
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

            feature_title = self.safe_text("植树问题的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先求间隔数", "间隔数＝距离÷间隔长度"),
                ("2", "看两端栽不栽", "两端都栽，棵数＝间隔数＋1"),
                ("3", "三种典型情形", "两端栽 / 一端栽 / 两端不栽"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：两端都栽"):
            prob_all = self.make_problem_box(
                f"题目：在一条长{dist}米的公路一侧植树，每隔{gap}米栽一棵，",
                "两端都栽。一共要栽多少棵树？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_plant_trees_diagram(
            draw_y,
            distance=dist,
            gap=gap,
            both_ends=True,
            show_hint=True,
        )

        # ── 图解1：画出公路与两端 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出公路与两端"):
            s1 = self.step_label("第一步：画出公路，标出总长，两端先栽上树")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(Create(diag["road"]), run_time=0.5)
            self.play(FadeIn(diag["dist_block"]), run_time=0.45)
            # 只先露出两端树：preview 第一棵 + end_tree
            first = diag["preview"][0]
            self.play(FadeIn(first), FadeIn(diag["end_tree"]), run_time=0.55)
            self.play(FadeIn(diag["end_note"]), run_time=0.4)
            self.safe_subtitle("两端都栽，是解题的关键", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：按间隔画树 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "按间隔画树"):
            self.add(
                prob_all, diag["hint"], diag["road"], diag["dist_block"],
                diag["preview"][0], diag["end_tree"], diag["end_note"],
                diag["notes"],
            )
            s2 = self.step_label(f"第二步：每隔{gap}米栽一棵，中间用省略号表示")
            self.play(FadeIn(s2), run_time=0.5)
            rest = VGroup(*diag["preview"][1:])
            self.play(FadeIn(rest), FadeIn(diag["gap_braces"]), run_time=0.6)
            self.play(FadeIn(diag["dots"]), run_time=0.4)
            self.safe_subtitle(
                f"相邻两棵之间是一个间隔，间隔长度是{gap}米",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：求出间隔数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出间隔数"):
            self.add(
                prob_all, diag["hint"], diag["road"], diag["dist_block"],
                diag["trees"], diag["gap_braces"], diag["end_note"],
                diag["notes"],
            )
            s3 = self.step_label("第三步：间隔数＝距离÷间隔长度")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_iv"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{dist}÷{gap}={intervals}（个间隔）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：棵数＝间隔数＋1 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出棵数"):
            self.add(
                prob_all, diag["hint"], diag["road"], diag["dist_block"],
                diag["trees"], diag["gap_braces"], diag["end_note"],
                diag["notes"],
            )
            s4 = self.step_label("第四步：两端都栽，棵数＝间隔数＋1")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(diag["note_tree_q"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.8)
            self.play(
                diag["note_tree_q"].animate.set_opacity(0),
                diag["note_tree_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{intervals}+1={trees}（棵）",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["road"], diag["trees"], diag["gap_braces"],
            diag["dist_block"], diag["end_note"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            formula = self.safe_text(
                f"{dist}÷{gap}＋1={trees}（棵）",
                font_size=28, color=WHITE,
            )
            formula.move_to(np.array([
                left_x + formula.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula)

            self.play(FadeIn(formula), run_time=0.5)
            self.wait(1.5)

            answer_text = self.safe_text(
                f"答：一共要栽{trees}棵树。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula, DOWN, buff=0.42)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("两端都栽，棵数比间隔数多1", wait=5)
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
