"""
第17讲 差倍问题 — 画图解题法（线段图法）

母题：鸭比鸡多24只，鸭是鸡的3倍，各有多少只？
答案：24÷(3-1)=12（只），12×3=36（只）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_17.py Problem17Scene -ql

渲染后:
  python ..\\_shared\\post_render.py --lesson 17 \\
    --rendered media\\videos\\problem_17\\480p15\\Problem17Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem17Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    DIFFERENCE = 24
    MULTIPLE = 3
    TOP_NAME = "鸡"
    BOTTOM_NAME = "鸭"

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        diff = self.DIFFERENCE
        mult = self.MULTIPLE
        parts = mult - 1
        unit = diff // parts
        bottom = unit * mult

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
                "已知两个量的「差」，又知道它们的倍数关系，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求这两个量分别是多少——这就是差倍问题！",
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

            feature_title = self.safe_text("线段图法解差倍的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "找清 1 倍量", "把较小数画成 1 段"),
                ("2", "按倍数画另一条", "几倍就画几段，左端对齐"),
                ("3", "差 ÷（倍数−1）", "多出的段数就是（倍数−1）"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：找「差」与倍数"):
            prob_all = self.make_problem_box(
                f"题目：{self.BOTTOM_NAME}比{self.TOP_NAME}多{diff}只，",
                f"{self.BOTTOM_NAME}的数量是{self.TOP_NAME}的{mult}倍。各有多少只？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_diff_times_diagram(
            draw_y,
            difference=diff,
            multiple=mult,
            top_name=self.TOP_NAME,
            bottom_name=self.BOTTOM_NAME,
            show_hint=True,
        )

        # ── 图解1：画鸡 1 倍 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画1倍量"):
            s1 = self.step_label(f"第一步：把{self.TOP_NAME}当作 1 倍量")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.35)
            self.play(FadeIn(diag["align_l"]), run_time=0.35)
            self.play(Create(diag["top_line"]), FadeIn(diag["top_name"]), run_time=0.55)
            self.play(FadeIn(diag["top_brace"]), FadeIn(diag["top_mult"]), run_time=0.45)
            self.safe_subtitle(f"{self.TOP_NAME}的数量较少，画成 1 段，当作 1 倍", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：画鸭 3 倍 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画多倍量"):
            self.add(
                prob_all, diag["hint"], diag["align_l"],
                diag["top_block"],
            )
            s2 = self.step_label(f"第二步：{self.BOTTOM_NAME}画成 {mult} 倍")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(Create(diag["bot_line"]), FadeIn(diag["bot_name"]), run_time=0.55)
            if len(diag["bot_ticks"]) > 0:
                self.play(FadeIn(diag["bot_ticks"]), run_time=0.4)
            self.play(FadeIn(diag["bot_brace"]), FadeIn(diag["bot_mult"]), run_time=0.45)
            self.play(FadeIn(diag["align_mid"]), run_time=0.4)
            self.safe_subtitle(
                f"{self.BOTTOM_NAME}是{self.TOP_NAME}的 {mult} 倍，画成 {mult} 段",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标出差 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出差额"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_block"], diag["bot_block"],
            )
            s3 = self.step_label("第三步：标出多出来的部分")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["diff_block"]), run_time=0.6)
            self.safe_subtitle(
                f"{self.BOTTOM_NAME}比{self.TOP_NAME}多的 {diff} 只，就是「差」",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：差是几个 1 倍 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "看成若干个1倍"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_block"], diag["bot_block"], diag["diff_block"],
            )
            s4 = self.step_label("第四步：把「差」看成几个 1 倍量")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["parts_note"]), run_time=0.55)
            self.safe_subtitle(
                f"差相当于 {parts} 个 1 倍量，"
                f"1 倍量 = {diff}÷{parts}={unit}（只）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["align"], diag["top_block"], diag["bot_block"],
            diag["diff_block"], diag["parts_note"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            explain = self.safe_text(
                f"差相当于（{mult}−1）个 1 倍量：",
                font_size=22, color=GREY_B,
            )
            step1 = self.safe_text(
                f"{diff}÷（{mult}−1）={unit}（只）",
                font_size=26, color=WHITE,
            )
            step1_note = self.safe_text(
                f"（{self.TOP_NAME}）",
                font_size=22, color=TEAL_D,
            )
            step1_row = VGroup(step1, step1_note).arrange(RIGHT, buff=0.18)
            step2 = self.safe_text(
                f"{unit}×{mult}={bottom}（只）",
                font_size=26, color=WHITE,
            )
            step2_note = self.safe_text(
                f"（{self.BOTTOM_NAME}）",
                font_size=22, color=PURPLE_A,
            )
            step2_row = VGroup(step2, step2_note).arrange(RIGHT, buff=0.18)
            alt = self.safe_text(
                f"或 {unit}+{diff}={bottom}（只）",
                font_size=22, color=GREY_B,
            )

            formula_rows = VGroup(explain, step1_row, step2_row, alt).arrange(
                DOWN, buff=0.24, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            self.play(FadeIn(explain), run_time=0.45)
            self.wait(1)
            self.play(FadeIn(step1_row), run_time=0.5)
            self.wait(1.4)
            self.play(FadeIn(step2_row), run_time=0.5)
            self.wait(1)
            self.play(FadeIn(alt), run_time=0.4)
            self.wait(1.2)

            answer_text = self.safe_text(
                f"答：{self.TOP_NAME}有{unit}只，{self.BOTTOM_NAME}有{bottom}只。",
                font_size=28, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.45)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("差÷（倍数−1）=1 倍量，再乘倍数求另一量", wait=5)
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
