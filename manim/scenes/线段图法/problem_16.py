"""
第16讲 和倍问题 — 画图解题法（线段图法）

母题：花花和美美一共24颗糖，美美是花花的3倍，各有多少？
答案：24÷（1+3）=6（颗），6×3=18（颗）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_16.py Problem16Scene -ql

渲染后:
  python ..\\_shared\\post_render.py --lesson 16 \\
    --rendered media\\videos\\problem_16\\480p15\\Problem16Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem16Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    TOTAL = 24
    MULTIPLE = 3
    TOP_NAME = "花花"
    BOTTOM_NAME = "美美"

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        total = self.TOTAL
        mult = self.MULTIPLE
        parts = 1 + mult
        unit = total // parts
        bottom = unit * mult

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是和倍问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "已知两个量的「和」，又知道它们的倍数关系，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求这两个量分别是多少——这就是和倍问题！",
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

            feature_title = self.safe_text("线段图法解和倍的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "找清 1 倍量", "把较小数画成 1 段"),
                ("2", "按倍数画另一条", "几倍就画几段，左端对齐"),
                ("3", "和 ÷（倍数+1）", "先求 1 倍量，再求多倍量"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：找「和」与倍数"):
            prob_all = self.make_problem_box(
                f"题目：{self.TOP_NAME}和{self.BOTTOM_NAME}一共有{total}颗糖果，",
                f"{self.BOTTOM_NAME}的糖果数量是{self.TOP_NAME}的{mult}倍，各有多少颗？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_sum_times_diagram(
            draw_y,
            total=total,
            multiple=mult,
            top_name=self.TOP_NAME,
            bottom_name=self.BOTTOM_NAME,
            show_hint=True,
        )

        # ── 图解1：画花花 1 倍 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画1倍量"):
            s1 = self.step_label(f"第一步：把{self.TOP_NAME}当作 1 倍量")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.35)
            self.play(FadeIn(diag["align"]), run_time=0.35)
            self.play(Create(diag["top_line"]), FadeIn(diag["top_name"]), run_time=0.55)
            self.play(FadeIn(diag["top_brace"]), FadeIn(diag["top_mult"]), run_time=0.45)
            self.safe_subtitle(f"{self.TOP_NAME}的糖果较少，画成 1 段，当作 1 倍", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：画美美 3 倍 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画多倍量"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_block"],
            )
            s2 = self.step_label(f"第二步：{self.BOTTOM_NAME}画成 {mult} 倍")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(Create(diag["bot_line"]), FadeIn(diag["bot_name"]), run_time=0.55)
            if len(diag["bot_ticks"]) > 0:
                self.play(FadeIn(diag["bot_ticks"]), run_time=0.4)
            self.play(FadeIn(diag["bot_brace"]), FadeIn(diag["bot_mult"]), run_time=0.45)
            self.safe_subtitle(
                f"{self.BOTTOM_NAME}是{self.TOP_NAME}的 {mult} 倍，画成 {mult} 段",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标出和 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出总和"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_block"], diag["bot_block"],
            )
            s3 = self.step_label("第三步：在右侧标出一共的颗数")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["sum_block"]), run_time=0.6)
            self.safe_subtitle(f"两边合起来一共 {total} 颗，就是「和」", wait=4)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：倍数量关系 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "看成若干个1倍"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_block"], diag["bot_block"], diag["sum_block"],
            )
            s4 = self.step_label("第四步：把「和」看成几个 1 倍量")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["parts_note"]), run_time=0.55)
            self.safe_subtitle(
                f"{total} 颗相当于 {parts} 个 1 倍量，"
                f"1 倍量 = {total}÷{parts}={unit}（颗）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["align"], diag["top_block"], diag["bot_block"],
            diag["sum_block"], diag["parts_note"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            explain = self.safe_text(
                f"和相当于（{mult}+1）个 1 倍量：",
                font_size=22, color=GREY_B,
            )
            step1 = self.safe_text(
                f"{total}÷（1+{mult}）={unit}（颗）",
                font_size=26, color=WHITE,
            )
            step1_note = self.safe_text(
                f"（{self.TOP_NAME}）",
                font_size=22, color=TEAL_D,
            )
            step1_row = VGroup(step1, step1_note).arrange(RIGHT, buff=0.18)
            step2 = self.safe_text(
                f"{unit}×{mult}={bottom}（颗）",
                font_size=26, color=WHITE,
            )
            step2_note = self.safe_text(
                f"（{self.BOTTOM_NAME}）",
                font_size=22, color=PURPLE_A,
            )
            step2_row = VGroup(step2, step2_note).arrange(RIGHT, buff=0.18)

            formula_rows = VGroup(explain, step1_row, step2_row).arrange(
                DOWN, buff=0.28, aligned_edge=LEFT,
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
            self.wait(1.5)

            answer_text = self.safe_text(
                f"答：{self.TOP_NAME}有{unit}颗糖果，{self.BOTTOM_NAME}有{bottom}颗糖果。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.50)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("和÷（倍数+1）=1 倍量，再乘倍数求另一量", wait=5)
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
