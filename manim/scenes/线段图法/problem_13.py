"""
第13讲 倍数问题 — 画图解题法（线段图法）

母题：苹果8个，梨比苹果的5倍少4个，一共多少个？
答案：5×8-4=36，36+8=44（个）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_13.py Problem13Scene -ql

渲染后:
  python ..\\_shared\\post_render.py --lesson 13 \\
    --rendered media\\videos\\problem_13\\480p15\\Problem13Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem13Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    UNIT_VALUE = 8
    MULTIPLE = 5
    LESS_BY = 4

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        unit = self.UNIT_VALUE
        mult = self.MULTIPLE
        less = self.LESS_BY
        pear_qty = mult * unit - less
        total = pear_qty + unit

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是倍数问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "已知一个数是另一个数的几倍多（少）几，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求总数——这就是倍数问题！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("线段图法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先找 1 倍量", "通常较矮的那条线段代表 1 倍"),
                ("2", "画多倍量的线段", "按倍数切分，与 1 倍对齐"),
                ("3", "标「多几 / 少几」再列式", "先求多倍量，再求总和"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：苹果与梨的数量关系"):
            prob_all = self.make_problem_box(
                "题目：李老师给同学们购买了一些水果，其中苹果有8个，",
                "梨的数量比苹果的5倍少4个。一共购买了多少个苹果和梨？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_multiple_times_diagram(
            unit, mult, draw_y,
            less_by=less,
            top_name="苹果",
            bottom_name="梨",
            show_hint=True,
            x_shift=0.75,
        )

        # ── 图解1：苹果 1 倍量 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画苹果线段表示1倍量"):
            s1 = self.step_label("第一步：画线段表示苹果的 1 倍量")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            self.play(Create(diag["apple_line"]), run_time=0.7)
            self.play(
                FadeIn(diag["apple_block"][0]),
                FadeIn(diag["apple_labels"]),
                run_time=0.6,
            )
            self.safe_subtitle("苹果有 8 个，作为 1 倍量", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：梨 5 倍线段 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画梨的5倍线段"):
            self.add(prob_all, diag["hint"], diag["apple_block"])
            s2 = self.step_label("第二步：画梨的线段，表示 5 倍")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(Create(diag["pear_solid"]), run_time=0.65)
            self.play(FadeIn(diag["pear_block"][0]), run_time=0.4)
            self.play(FadeIn(diag["pear_ticks"]), run_time=0.55)
            self.play(FadeIn(diag["pear_mult_labels"]), run_time=0.55)
            self.safe_subtitle("梨比苹果多，按 1 倍长度切 5 段", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：少 4 个 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出少4个"):
            self.add(
                prob_all, diag["hint"], diag["apple_block"],
                diag["pear_solid"], diag["pear_block"][0], diag["pear_ticks"],
                diag["pear_mult_labels"],
            )
            s3 = self.step_label("第三步：标出「少 4 个」")
            self.play(FadeIn(s3), run_time=0.5)
            if len(diag["pear_dashed"]) > 0:
                self.play(Create(diag["pear_dashed"]), run_time=0.55)
            if len(diag["less_block"]) > 0:
                self.play(FadeIn(diag["less_block"]), run_time=0.55)
            self.safe_subtitle("5 倍满格还差 4 个，用虚线表示少的部分", wait=4)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：标梨的数量 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "标梨的数量"):
            self.add(prob_all, diag["core"])
            s4 = self.step_label("第四步：标出梨的数量")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["qty_block"]), run_time=0.6)
            self.safe_subtitle("先求梨：5×8−4=36（个）", wait=4)
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = diag["layout_row"]

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{mult}×{unit}−{less}={pear_qty}（个）",
                font_size=28, color=WHITE,
            )
            explain = self.safe_text(
                "先求梨的数量，再与苹果相加：",
                font_size=24, color=GREY_B,
            )
            step2 = self.safe_text(
                f"{pear_qty}+{unit}={total}（个）",
                font_size=28, color=WHITE,
            )
            formula_rows = VGroup(step1, explain, step2).arrange(
                DOWN, buff=0.28, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)
            self.play(FadeIn(step1), run_time=0.5)
            self.wait(1.5)
            self.play(FadeIn(explain), run_time=0.45)
            self.play(FadeIn(step2), run_time=0.5)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：李老师一共购买了{total}个苹果和梨。",
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
            self.safe_subtitle("线段图法：找清 1 倍量与多倍量的关系", wait=5)
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
