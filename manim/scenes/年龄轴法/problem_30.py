"""
第30讲 年龄问题（二）— 画图解题法（年龄轴法）

母题：爷爷+爸爸=100岁；爷爷像爸爸现在这么大时，爸爸是爷爷一半。爷爷今年？
答案：100÷(2+3)=20，20×3=60

用法:
  cd manim/scenes/年龄轴法
  python -m manim problem_30.py Problem30Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem30Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    AGE_SUM = 100
    YOUNG_UNITS = 2
    OLD_UNITS = 3

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        s = self.AGE_SUM
        yu = self.YOUNG_UNITS
        ou = self.OLD_UNITS
        total_u = yu + ou
        diff = s // total_u
        old_age = diff * ou

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=34, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "两人年龄在几年前或几年后存在倍数关系，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用年龄轴把「年龄差」当作单位来分析——这就是年龄轴法！",
                font_size=26, color=WHITE,
            )
            concept_body = VGroup(s1_body, s1_body2).arrange(
                DOWN, buff=0.22, aligned_edge=LEFT,
            )
            concept_body.next_to(concept_title, DOWN, buff=0.40)
            concept_body.move_to(np.array([0, concept_body.get_center()[1], 0]))
            self.clamp_content(concept_body)
            concept_block = VGroup(concept_title, concept_body)

            divider_y = concept_block.get_bottom()[1] - 0.40
            divider = Line(
                np.array([self.safe_left + 0.5, divider_y, 0]),
                np.array([self.safe_right - 0.5, divider_y, 0]),
                stroke_width=1.5, color=GREY_B, stroke_opacity=0.25,
            )

            feature_title = self.safe_text("年龄轴法的三个要点", font_size=32, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.55, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "年龄差永远不变", "两人年龄同时增长，差不变"),
                ("2", "用年龄差作单位", "把今年年龄看成几个差"),
                ("3", "抓住倍数关系", "再由年龄和求出每一个差"),
            ]
            feature_groups = self.layout_numbered_features(
                features,
                top_y=feature_title.get_bottom()[1] - 0.45,
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：年龄与倍数"):
            prob_all = self.make_problem_box(
                f"题目：爷爷和爸爸年龄和是{s}岁。当爷爷像爸爸现在这样大时，",
                "爸爸正好是爷爷的一半。爷爷今年多少岁？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_age_axis_diagram(
            draw_y,
            age_sum=s,
            young_units=yu,
            old_units=ou,
            show_hint=True,
        )

        # ── 图解1：画出年龄轴 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出年龄轴"):
            s1 = self.step_label("第一步：画出年龄轴，标出年龄差单位")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(Create(diag["main"]), FadeIn(diag["axis_tip"]), run_time=0.5)
            self.play(FadeIn(diag["ticks"]), FadeIn(diag["tick_labels"]), run_time=0.45)
            self.play(FadeIn(diag["diff_block"]), run_time=0.5)
            self.safe_subtitle("把「1个年龄差」当作单位，在轴上往后数", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：推出份数关系 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "推出份数"):
            self.add(
                prob_all, diag["hint"], diag["axis"], diag["diff_block"],
                diag["notes"],
            )
            s2 = self.step_label("第二步：根据「一半」关系，推出今年的份数")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["past_note"].animate.set_opacity(1), run_time=0.55)
            self.play(FadeIn(diag["young_block"]), run_time=0.5)
            self.play(FadeIn(diag["old_block"]), run_time=0.5)
            self.safe_subtitle(
                f"爸爸今年占 {yu} 个差，爷爷今年占 {ou} 个差",
                wait=5,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：年龄和 = 5 个差 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "年龄和与差"):
            self.add(
                prob_all, diag["hint"], diag["axis"], diag["diff_block"],
                diag["young_block"], diag["old_block"], diag["notes"],
            )
            s3 = self.step_label("第三步：年龄和等于几个年龄差")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["sum_note"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{yu}+{ou}={total_u} 个年龄差，一共 {s} 岁",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出爷爷年龄 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出爷爷年龄"):
            self.add(
                prob_all, diag["hint"], diag["axis"], diag["diff_block"],
                diag["young_block"], diag["old_block"], diag["notes"],
            )
            s4 = self.step_label("第四步：先求一个年龄差，再求爷爷年龄")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(diag["calc_note"].animate.set_opacity(1), run_time=0.55)
            self.play(
                diag["young_lab_q"].animate.set_opacity(0),
                diag["young_lab_ans"].animate.set_opacity(1),
                diag["old_lab_q"].animate.set_opacity(0),
                diag["old_lab_ans"].animate.set_opacity(1),
                run_time=0.6,
            )
            self.safe_subtitle(
                f"{s}÷{total_u}={diff}（岁），爷爷={diff}×{ou}={old_age}岁",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["axis"], diag["diff_block"],
            diag["young_block"], diag["old_block"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{s}÷（{yu}＋{ou}）={diff}（岁）",
                font_size=26, color=WHITE,
            )
            step1_note = self.safe_text("（一个年龄差）", font_size=18, color=GREY_B)
            step1_row = VGroup(step1, step1_note).arrange(RIGHT, buff=0.16)

            step2 = self.safe_text(
                f"{diff}×{ou}={old_age}（岁）",
                font_size=26, color=WHITE,
            )
            step2_note = self.safe_text("（爷爷今年）", font_size=18, color=YELLOW)
            step2_row = VGroup(step2, step2_note).arrange(RIGHT, buff=0.16)

            formula_rows = VGroup(step1_row, step2_row).arrange(
                DOWN, buff=0.32, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1_row, step2_row]:
                self.play(FadeIn(row), run_time=0.5)
                self.wait(1.2)

            answer_text = self.safe_text(
                f"答：爷爷今年{old_age}岁。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.42)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("年龄差不变，抓住份数关系是关键", wait=5)
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
