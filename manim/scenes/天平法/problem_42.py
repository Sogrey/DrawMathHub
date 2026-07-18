"""
第42讲 找次品问题 — 画图解题法（天平法）

母题：9 盒饼干，1 盒偏轻。至少称几次能保证找出？
答案：至少称 2 次

用法:
  cd manim/scenes/天平法
  python -m manim problem_42.py Problem42Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem42Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    N = 9
    ANSWER = 2

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        n = self.N
        ans = self.ANSWER

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=34, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.32, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "外观一样的物品里混进一件质量不同的次品，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用天平称，用最少次数保证找出来——这就是天平法！",
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

            feature_title = self.safe_text("天平法找次品的三个要点", font_size=28, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "平均分成 3 份", "天平一次有平衡、偏左、偏右三种结果"),
                ("2", "每次称其中 2 份", "根据结果判断次品在哪一份"),
                ("3", "逐次缩小范围", "直到只剩一件，保证找出"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：9盒找次品"):
            prob_all = self.make_problem_box(
                f"题目：{n}盒饼干外观相同，1盒偏轻是次品。",
                "用天平至少称几次能保证找出？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_balance_defect_diagram(draw_y, n=n, show_hint=True)

        # ── 图解1：编号并三等分 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "三等分"):
            s1 = self.step_label("第一步：把9盒编号，平均分成3组")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["all_circles"]), run_time=0.7)
            self.play(FadeIn(diag["group_braces"]), run_time=0.55)
            self.safe_subtitle(
                "每组3盒：①组1-3，②组4-6，③组7-9",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：第一次称 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "第一次称量"):
            self.add(
                prob_all, diag["hint"], diag["overview"],
                diag["weigh_row"], diag["note_ans"],
            )
            s2 = self.step_label("第二步：第一次称，①组与②组放上天平")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["weigh1"].animate.set_opacity(1), run_time=0.7)
            self.safe_subtitle(
                "若平衡，次品一定在剩下的③组里",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：第二次称 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "第二次称量"):
            self.add(
                prob_all, diag["hint"], diag["overview"],
                diag["weigh_row"], diag["note_ans"],
            )
            s3 = self.step_label("第三步：从含次品的3盒中取2盒再称一次")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["weigh2"].animate.set_opacity(1), run_time=0.7)
            self.safe_subtitle(
                "平衡则剩下那盒是次品；不平衡则偏轻那边是次品",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：结论 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "保证找出"):
            self.add(
                prob_all, diag["hint"], diag["overview"],
                diag["weigh_row"], diag["note_ans"],
            )
            s4 = self.step_label("第四步：两次称量就能保证找出次品")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_ans"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"至少称 {ans} 次能保证找出这盒饼干",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["overview"], diag["weigh_row"], diag["note_ans"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                self.safe_text("把9盒平均分成3组，每次称其中2组。", font_size=20, color=WHITE),
                self.safe_text("第1次：缩小到含次品的3盒；", font_size=20, color=WHITE),
                self.safe_text("第2次：再称出偏轻的那一盒。", font_size=20, color=WHITE),
            ]
            formula_rows = VGroup(*lines).arrange(DOWN, buff=0.26, aligned_edge=LEFT)
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
                f"答：至少称{ans}次能保证找出这盒饼干。",
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
            self.safe_subtitle("三等分，每次称两份，逐步缩小范围", wait=5)
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
