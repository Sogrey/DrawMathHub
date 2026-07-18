"""
第14讲 错中求解问题 — 画图解题法（倒推法）

母题：被减数十位2→5，减数个位7→1，错得392，求正确结果
答案：（5-2）×10=30，7-1=6，392-30-6=356

用法:
  cd manim/scenes/倒推法
  python -m manim problem_14.py Problem14Scene -ql

渲染后:
  python ..\\_shared\\post_render.py --lesson 14 \\
    --rendered media\\videos\\problem_14\\480p15\\Problem14Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem14Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    MINUEND_TENS_CORRECT = 2
    MINUEND_TENS_WRONG = 5
    SUB_UNITS_CORRECT = 7
    SUB_UNITS_WRONG = 1
    WRONG_RESULT = 392

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        d_min = (self.MINUEND_TENS_WRONG - self.MINUEND_TENS_CORRECT) * 10
        d_sub = self.SUB_UNITS_CORRECT - self.SUB_UNITS_WRONG
        correct = self.WRONG_RESULT - d_min - d_sub

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
                "某道题按错误数字算了，给出错误结果，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "要倒推出正确结果——这就是错中求解！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("倒推法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "列出正确与错误算式", "把看对、看错的数位标清楚"),
                ("2", "分析差的变化", "被减数、减数变化会让差怎么变"),
                ("3", "从错误结果倒推", "把多算或少算的部分补回来"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：看错数位与错误结果"):
            prob_all = self.make_problem_box(
                "题目：小王做减法题，被减数十位上的2错看成5，",
                "减数个位上的7错看成1，得到392。正确结果是多少？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_wrong_subtract_diagram(
            draw_y,
            minuend_tens_correct=self.MINUEND_TENS_CORRECT,
            minuend_tens_wrong=self.MINUEND_TENS_WRONG,
            subtrahend_units_correct=self.SUB_UNITS_CORRECT,
            subtrahend_units_wrong=self.SUB_UNITS_WRONG,
            wrong_result=self.WRONG_RESULT,
            show_hint=True,
        )

        # ── 图解1：正确行 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "列正确算式"):
            s1 = self.step_label("第一步：列出正确的被减数、减数")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            self.play(FadeIn(diag["headers"]), run_time=0.5)
            self.play(FadeIn(diag["correct_row"], shift=DOWN * 0.1), run_time=0.65)
            self.safe_subtitle("正确：被减数是□2□，减数是□□7", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：错误行 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "列错误算式"):
            self.add(prob_all, diag["hint"], diag["headers"], diag["correct_row"])
            s2 = self.step_label("第二步：列出小王看错的数位")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["wrong_row"], shift=UP * 0.1), run_time=0.65)
            self.safe_subtitle("错误：十位看成5→□5□，个位看成1→□□1，差得392", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：数位差异 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标数位变化"):
            self.add(
                prob_all, diag["hint"], diag["headers"],
                diag["correct_row"], diag["wrong_row"],
            )
            s3 = self.step_label("第三步：标看错位置对差的影响")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["digit_arrows"]), run_time=0.55)
            self.play(FadeIn(diag["digit_deltas"]), run_time=0.55)
            self.safe_subtitle(
                "被减数多30，差也多30；减数少6，差多6",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：结果倒推 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "从错误结果倒推"):
            self.add(
                prob_all, diag["table_core"],
                diag["digit_arrows"], diag["digit_deltas"],
            )
            s4 = self.step_label("第四步：从392倒推正确结果")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["result_arrow"]), run_time=0.5)
            self.play(FadeIn(diag["result_notes"]), run_time=0.55)
            self.play(FadeIn(diag["fix_note"]), run_time=0.55)
            self.safe_subtitle(f"392 减去多算的 {d_min + d_sub}，得 {correct}", wait=4)
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = diag["annotated_table"]

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式倒推"):
            written_diagram = VGroup(diagram_all, diag["fix_note"])
            self.add(prob_all, written_diagram)
            written_diagram_scale = self.place_diagram_for_written(written_diagram)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"（{self.MINUEND_TENS_WRONG}−{self.MINUEND_TENS_CORRECT}）×10={d_min}",
                font_size=26, color=WHITE,
            )
            step2 = self.safe_text(
                f"{self.SUB_UNITS_CORRECT}−{self.SUB_UNITS_WRONG}={d_sub}",
                font_size=26, color=WHITE,
            )
            explain = self.safe_text(
                "错误结果里多加了这两部分，要减回去：",
                font_size=24, color=GREY_B,
            )
            step3 = self.safe_text(
                f"{self.WRONG_RESULT}−{d_min}−{d_sub}={correct}",
                font_size=26, color=WHITE,
            )

            formula_rows = VGroup(step1, step2, explain, step3).arrange(
                DOWN, buff=0.26, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1, step2]:
                self.play(FadeIn(row), run_time=0.5)
                self.wait(1.2)
            self.play(FadeIn(explain), run_time=0.45)
            self.wait(1)
            self.play(FadeIn(step3), run_time=0.5)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：这道减法题的正确结果是{correct}。",
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
            self.safe_subtitle("错中求解：先看错在哪，再从错误结果倒推", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula_rows), FadeOut(answer_text),
                FadeOut(highlight_box), FadeOut(prob_all), run_time=0.5,
            )

        diagram_for_keypoints = VGroup(diagram_all, diag["fix_note"])
        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=diagram_for_keypoints, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
