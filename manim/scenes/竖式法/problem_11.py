"""
第11讲 时间问题 — 画图解题法（竖式法）

母题：8时38分始发，10时21分到达，求经过多长时间？
答案：1时43分

用法:
  cd manim/scenes/竖式法
  python -m manim problem_11.py Problem11Scene -ql

渲染后:
  python ..\_shared\post_render.py --lesson 11 \\
    --rendered media\videos\problem_11\480p15\Problem11Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem11Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    START_H, START_M = 8, 38
    END_H, END_M = 10, 21
    BORROW_H_MARK = 9
    BORROW_M_MARK = 81
    RESULT_H, RESULT_M = 1, 43

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

            concept_title = self.safe_text("什么是时间问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "求经过多长时间、开始或结束时刻——", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "与时、分、秒有关的计算，就是时间问题！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("竖式法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "时、分、秒有关", "求经过时间或开始/结束时刻"),
                ("2", "竖式对齐计算", "终止时间在上，起始时间在下"),
                ("3", "进率是 60", "分不够减，从「时」退 1 当 60 分"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：始发与到达时间"):
            prob_all = self.make_problem_box(
                "题目：某列车在8时38分始发，10时21分到达沈阳站。",
                "列车从出发到沈阳站共经过了多长时间？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_time_subtract_vertical(
            self.END_H, self.END_M,
            self.START_H, self.START_M,
            draw_y,
            result_h=self.RESULT_H,
            result_m=self.RESULT_M,
            borrow_h_mark=self.BORROW_H_MARK,
            borrow_m_mark=self.BORROW_M_MARK,
        )

        # ── 图解1：列竖式 + 填入时间（说明文字在竖式上方）──
        with self.segment("draw-1", "1", "segments/03.mp4", "列竖式并填入时间"):
            s1 = self.step_label("第一步：列竖式，终止在上、起始在下")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            self.wait(1.5)
            self.play(FadeIn(diag["end_row"], shift=DOWN * 0.08), run_time=0.55)
            self.play(
                FadeIn(diag["minus_sign"]),
                FadeIn(diag["start_row"], shift=DOWN * 0.08),
                run_time=0.55,
            )
            self.play(Create(diag["hline"]), run_time=0.45)
            self.play(FadeIn(diag["need_borrow_note"], shift=RIGHT * 0.1), run_time=0.45)
            self.safe_subtitle(
                f"分位 {self.END_M} 减 {self.START_M} 不够减，需要借位",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：借位 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "从「时」退1，分变成81"):
            self.add(
                prob_all, diag["hint"], diag["end_row"],
                diag["minus_sign"], diag["start_row"], diag["hline"],
                diag["need_borrow_note"],
            )
            s2 = self.step_label("第二步：从「时」退 1，加到「分」")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                diag["min_col"].animate.set_color(YELLOW),
                run_time=0.45,
            )
            self.play(FadeIn(diag["borrow_marks"], shift=UP * 0.12), run_time=0.65)
            self.safe_subtitle("1时=60分，21+60=81（分）；10退1后「时」上是9", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：得结果 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "得1时43分"):
            self.add(
                prob_all, diag["hint"], diag["borrow_marks"],
                diag["end_row"], diag["minus_sign"], diag["start_row"],
                diag["hline"],
            )
            s3 = self.step_label("第三步：计算得经过的时间")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeOut(diag["need_borrow_note"]), run_time=0.3)
            self.play(FadeIn(diag["result_row"], shift=UP * 0.1), run_time=0.65)
            self.play(
                diag["result_hour_t"].animate.set_color(TEAL_D),
                diag["result_min_t"].animate.set_color(TEAL_D),
                run_time=0.45,
            )
            self.safe_subtitle(
                f"81−{self.START_M}={self.RESULT_M}（分），"
                f"9−{self.START_H}={self.RESULT_H}（时）→ {self.RESULT_H}小时{self.RESULT_M}分钟",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s3), FadeOut(diag["hint"]), run_time=0.3)

        diagram_all = diag["layout_row"]

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/06.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            explain = self.safe_text(
                "1时=60分，分不够减时从「时」退1当60：",
                font_size=24, color=GREY_B,
            )
            step1 = self.safe_text(
                f"60+{self.END_M}={self.BORROW_M_MARK}（分）",
                font_size=28, color=WHITE,
            )
            step2 = self.safe_text(
                f"{self.BORROW_M_MARK}−{self.START_M}={self.RESULT_M}（分）  "
                f"10−1−{self.START_H}={self.RESULT_H}（时）",
                font_size=26, color=WHITE,
            )
            formula_rows = VGroup(explain, step1, step2).arrange(
                DOWN, buff=0.30, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.45), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)
            self.play(FadeIn(explain, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(1.5)
            self.play(FadeIn(step1, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(1.5)
            self.play(FadeIn(step2, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(2)

            answer_text = self.safe_text(
                "答：列车从出发到沈阳站共经过了1小时43分钟。",
                font_size=30, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.55)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("时分秒进率是60，竖式借位仿照减法", wait=5)
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
