"""
第35讲 策略问题 — 画图解题法（列表法）

母题：四(1) vs 四(2) 百米对抗，四(2) 以 2:1 获胜的出场策略。
答案：3号对1号（弃一场），再1号对2号、2号对3号。

用法:
  cd manim/scenes/列表法
  python -m manim problem_35.py Problem35Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem35Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    CLASS1 = ["1号 14秒2", "2号 14秒7", "3号 15秒1"]
    CLASS2 = ["3号 15秒6", "1号 14秒5", "2号 14秒8"]
    WINNERS = ["四(1)班", "四(2)班", "四(2)班"]
    MATCHES = ["第一场", "第二场", "第三场"]

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

            concept_title = self.safe_text("题型识别", font_size=34, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.32, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "双方一对一对决，已知实力和一方出场顺序，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "要排出另一方怎样出场才能获胜——可用列表法！",
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

            feature_title = self.safe_text("策略安排的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先比较双方实力", "成绩好的选手实力更强"),
                ("2", "必要时弃掉一场", "最弱去对对方最强"),
                ("3", "再用强手依次应对", "保证多赢几场，总分获胜"),
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
        # 题目很长：拆两行写入题目框
        prob_all = None
        with self.segment("question", "题目", "segments/02.mp4", "读题：对抗赛策略"):
            prob_all = self.make_problem_box(
                "题目：四(1)班与四(2)班百米对抗，一对一计分。",
                "四(2)班以2比1获胜，如何安排出场？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_race_strategy_table(
            draw_y,
            class1_rows=self.CLASS1,
            class2_fills=self.CLASS2,
            winners=self.WINNERS,
            match_labels=self.MATCHES,
            show_hint=True,
        )

        # ── 图解1：列出已知出场表 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "列出对阵表"):
            s1 = self.step_label("第一步：列表，先写入四(1)班的出场顺序")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(
                FadeIn(diag["header"]),
                FadeIn(diag["match_cells"]),
                FadeIn(diag["class1_cells"]),
                FadeIn(diag["class2_cells"]),
                FadeIn(diag["winner_cells"]),
                run_time=0.8,
            )
            self.safe_subtitle(
                "四(1)班出场已定：1号、2号、3号依次上场",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：第一场弃子 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "最弱对最强"):
            self.add(
                prob_all, diag["hint"], diag["table"], diag["notes"],
            )
            s2 = self.step_label("第二步：第一场用最弱的3号，应对对方最强的1号")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["note_idea"].animate.set_opacity(1), run_time=0.45)
            self.play(diag["class2_labels"][0].animate.set_opacity(1), run_time=0.45)
            self.play(diag["winner_labels"][0].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle(
                "这一场故意输掉，保存实力",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：后两场取胜 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "强手依次应对"):
            self.add(
                prob_all, diag["hint"], diag["table"], diag["notes"],
            )
            s3 = self.step_label("第三步：用1号、2号依次应对对方剩下的队员")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["class2_labels"][1].animate.set_opacity(1), run_time=0.45)
            self.play(diag["winner_labels"][1].animate.set_opacity(1), run_time=0.4)
            self.safe_subtitle("14秒5 快于 14秒7，四(2)班得分", wait=3)
            self.play(diag["class2_labels"][2].animate.set_opacity(1), run_time=0.45)
            self.play(diag["winner_labels"][2].animate.set_opacity(1), run_time=0.4)
            self.safe_subtitle("14秒8 快于 15秒1，四(2)班再得1分", wait=3)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：总结比分 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "总结比分"):
            self.add(
                prob_all, diag["hint"], diag["table"], diag["notes"],
            )
            s4 = self.step_label("第四步：统计比分，确认以2比1获胜")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_score_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.5)
            self.play(
                diag["note_score_q"].animate.set_opacity(0),
                diag["note_score_ans"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle("四(2)班赢两场、输一场，总分2:1", wait=4)
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(diag["table"], diag["notes"])

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：补充完整"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                self.safe_text("第一场：3号15秒6 → 四(1)班胜", font_size=20, color=WHITE),
                self.safe_text("第二场：1号14秒5 → 四(2)班胜", font_size=20, color=WHITE),
                self.safe_text("第三场：2号14秒8 → 四(2)班胜", font_size=20, color=WHITE),
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
                "答：四(2)班按「弱→强→中」出场，以2:1获胜。",
                font_size=20, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("先以最弱的对最强的，然后依次应对", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula_rows), FadeOut(answer_text),
                FadeOut(highlight_box), FadeOut(prob_all), run_time=0.5,
            )

        keypoints_text = mp["keyPoints"]
        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                keypoints_text, wait=6,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
