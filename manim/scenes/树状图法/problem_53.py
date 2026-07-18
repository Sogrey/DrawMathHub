"""
第53讲 概率问题 — 画图解题法（树状图法）

母题：三辆车经路口，各可左/直/右且等可能，求全部直行的概率。
答案：3×3×3=27，1÷27=1/27

用法:
  cd manim/scenes/树状图法
  python -m manim problem_53.py Problem53Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem53Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    CHOICES = ("左", "直", "右")
    FAVOR = "直"

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
                "几种结果出现的可能性相同，要求某一事件的概率，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "就用树状图把全部可能画出来，再算有利结果占比！",
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

            feature_title = self.safe_text("求概率的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "确认等可能性", "每种结果出现的机会一样大"),
                ("2", "树状图枚举", "按步骤画出全部可能结果"),
                ("3", "有利÷全部", "概率＝有利结果种数÷总种数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求全部直行的概率"):
            prob_all = self.make_problem_box(
                "题目：三辆车经路口，各可左/直/右且等可能。",
                "全部直行的概率是多少？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.15
        diag = self.make_probability_tree_diagram(
            draw_y,
            choices=self.CHOICES,
            favor=self.FAVOR,
            show_hint=False,
        )
        total = diag["total"]
        favor = diag["favor"]
        n = diag["n"]

        # ── 图解1：第一辆车 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出第一辆车的三种可能"):
            s1 = self.step_label("第一步：第一辆车——左、直、右")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(
                diag["root_dot"].animate.set_opacity(1),
                diag["lab1"].animate.set_opacity(1),
                run_time=0.35,
            )
            self.play(diag["layer1"].animate.set_opacity(1), run_time=0.7)
            self.safe_subtitle(
                f"第一辆车有 {n} 种可能：左、直、右",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：第二辆车 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画出第二辆车的分支"):
            self.add(prob_all, diag["root_dot"], diag["lab1"], diag["layer1"])
            s2 = self.step_label("第二步：第二辆车——每支再分左、直、右")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["lab2"].animate.set_opacity(1), run_time=0.3)
            self.play(diag["layer2"].animate.set_opacity(1), run_time=0.8)
            self.safe_subtitle(
                f"第二辆同样 {n} 种，已有 {n}×{n}={n * n} 种组合",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：第三辆车并数清总数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "画出第三辆并统计总数"):
            self.add(
                prob_all, diag["root_dot"],
                diag["lab1"], diag["lab2"],
                diag["layer1"], diag["layer2"],
            )
            s3 = self.step_label("第三步：第三辆车分支，数出全部可能")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["lab3"].animate.set_opacity(1), run_time=0.3)
            self.play(diag["layer3"].animate.set_opacity(1), run_time=0.9)
            self.play(diag["note_total"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"{n}×{n}×{n}={total}（种）等可能结果",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：有利结果与概率 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "标出全部直行并求概率"):
            self.add(
                prob_all, diag["root_dot"], diag["row_labs"],
                diag["layer1"], diag["layer2"], diag["layer3"],
                diag["note_total"],
            )
            s4 = self.step_label(f"第四步：全部{favor}行只有1种，求出概率")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_favor"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.5)
            self.play(diag["note_prob"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"概率＝1÷{total}＝1/{total}",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["root_dot"], diag["row_labs"],
            diag["layer1"], diag["layer2"], diag["layer3"],
            diag["notes"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"{n}×{n}×{n}={total}（种）",
                font_size=26, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.65), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = self.safe_text(
                f"1÷{total}=1/{total}",
                font_size=26, color=WHITE,
            )
            f2.next_to(f1, DOWN, buff=0.30)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            answer_text = self.safe_text(
                f"答：全部{favor}行的概率是1/{total}。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f2, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.5)
            self.wait(0.7)
            self.play(FadeIn(f2), run_time=0.5)
            self.wait(0.7)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("概率＝有利结果÷全部结果", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(f2),
                FadeOut(answer_text), FadeOut(highlight_box),
                FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
