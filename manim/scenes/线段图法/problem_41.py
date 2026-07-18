"""
第41讲 分段计费问题 — 画图解题法（线段图法）

母题：阶梯水费，总费用 88.75 元，求用水量。
答案：21 立方米

用法:
  cd manim/scenes/线段图法
  python -m manim problem_41.py Problem41Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem41Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    T1_CAP, T1_PRICE = 10, 2.5
    T2_CAP, T2_PRICE = 15, 3.75
    T3_PRICE = 7.5
    TOTAL_FEE = 88.75

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        t1c, t1p = self.T1_CAP, self.T1_PRICE
        t2c, t2p = self.T2_CAP, self.T2_PRICE
        t3p = self.T3_PRICE
        fee = self.TOTAL_FEE
        fee12 = t1c * t1p + (t2c - t1c) * t2p
        total_vol = (fee - fee12) / t3p + t2c

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=32, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.32, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "按用量分成几个区间，每段单价不同，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用线段图判断落在哪一阶，再列式求数量！",
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

            feature_title = self.safe_text("阶梯计费的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先算满阶费用", "算最后一个阶梯之前的满额钱数"),
                ("2", "与总费用比较", "判断用水量到了哪一阶"),
                ("3", "再算超出部分", "超出费用÷单价＋已满用量"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：阶梯水费"):
            prob_all = self.make_problem_box(
                f"题目：水费阶梯 {t1p}/{t2p}/{t3p} 元，小红家水费 {fee:g} 元。",
                "3月份用了多少立方米水？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_tiered_billing_diagram(
            draw_y,
            t1_cap=t1c, t1_price=t1p,
            t2_cap=t2c, t2_price=t2p,
            t3_price=t3p, total_fee=fee,
            show_hint=True,
        )

        # ── 图解1：画出三段阶梯 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出三段用量"):
            s1 = self.step_label("第一步：把用水量画成三段，对应三个阶梯")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(Create(diag["s1"]), FadeIn(diag["brace1"]), run_time=0.55)
            self.play(Create(diag["s2"]), FadeIn(diag["brace2"]), run_time=0.5)
            self.play(Create(diag["s3"]), FadeIn(diag["brace3"]), run_time=0.5)
            self.safe_subtitle(
                f"不超过{t1c}、{t1c}到{t2c}、超过{t2c}，第三段先标问号",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：算前两阶费用并比较 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "前两阶费用比较"):
            self.add(
                prob_all, diag["hint"], diag["line_g"],
                diag["brace1"], diag["brace2"], diag["brace3"],
                diag["fee1_lab"], diag["fee2_lab"], diag["cmp_g"], diag["notes"],
            )
            s2 = self.step_label("第二步：求出前两个阶梯满额费用，与总费用比较")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["fee1_lab"].animate.set_opacity(1), run_time=0.4)
            self.play(diag["fee2_lab"].animate.set_opacity(1), run_time=0.4)
            self.play(diag["cmp_g"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{fee12:g} ＜ {fee:g}，说明超过了 {t2c:g} 立方米",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：判断落在第三阶 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "判断所在阶梯"):
            self.add(
                prob_all, diag["hint"], diag["line_g"],
                diag["brace1"], diag["brace2"], diag["brace3"],
                diag["fee1_lab"], diag["fee2_lab"], diag["cmp_g"], diag["notes"],
            )
            s3 = self.step_label("第三步：判断用水量达到了第三阶梯")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_over"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                "前两阶满额仍小于总费用，一定进入第三阶",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出总量 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出用水量"):
            self.add(
                prob_all, diag["hint"], diag["line_g"],
                diag["brace1"], diag["brace2"], diag["brace3"],
                diag["fee1_lab"], diag["fee2_lab"], diag["cmp_g"], diag["notes"],
            )
            s4 = self.step_label("第四步：先求第三阶用量，再加上 15 立方米")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_calc_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.5)
            self.play(
                diag["note_calc_q"].animate.set_opacity(0),
                diag["note_calc_ans"].animate.set_opacity(1),
                diag["l3_q"].animate.set_opacity(0),
                diag["l3_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"一共用了 {total_vol:g} 立方米",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["line_g"], diag["brace1"], diag["brace2"], diag["brace3"],
            diag["fee1_lab"], diag["fee2_lab"], diag["cmp_g"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{t1c:g}×{t1p:g}+({t2c:g}－{t1c:g})×{t2p:g}={fee12:g}",
                font_size=20, color=WHITE,
            )
            step2 = self.safe_text(
                f"{fee12:g}＜{fee:g}，超过{t2c:g}立方米",
                font_size=18, color=GREY_B,
            )
            step3 = self.safe_text(
                f"({fee:g}－{fee12:g})÷{t3p:g}+{t2c:g}={total_vol:g}",
                font_size=20, color=WHITE,
            )
            formula_rows = VGroup(step1, step2, step3).arrange(
                DOWN, buff=0.26, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1, step2, step3]:
                self.play(FadeIn(row), run_time=0.45)
                self.wait(0.9)

            answer_text = self.safe_text(
                f"答：她家3月份用了{total_vol:g}立方米水。",
                font_size=20, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.34)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("先算满阶费用，再判断所在阶梯", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula_rows), FadeOut(answer_text),
                FadeOut(highlight_box), FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=7,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
