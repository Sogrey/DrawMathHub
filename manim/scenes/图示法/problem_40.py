"""
第40讲 因数与倍数问题 — 画图解题法（图示法）

母题：两自然数 LCM=90，GCD=9。两数分别是多少？
答案：9 与 90，或 18 与 45

用法:
  cd manim/scenes/图示法
  python -m manim problem_40.py Problem40Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem40Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    GCD = 9
    LCM = 90

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        gcd = self.GCD
        lcm = self.LCM
        product = lcm // gcd

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
                "已知两数的最大公因数和最小公倍数，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用短除法求出原来的两个自然数！",
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

            feature_title = self.safe_text("短除分析的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "公因数作短除", "两数同时除以最大公因数"),
                ("2", "商必须互质", "否则公因数还可以再约"),
                ("3", "GCD×a×b＝LCM", "再把 a、b 乘回公因数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：GCD与LCM"):
            prob_all = self.make_problem_box(
                f"题目：两自然数的最小公倍数是{lcm}，最大公因数是{gcd}。",
                "这两个自然数分别是多少？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_gcd_lcm_short_diagram(
            draw_y, gcd=gcd, lcm=lcm, show_hint=True,
        )

        # ── 图解1：画出短除图式 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出短除"):
            s1 = self.step_label("第一步：用短除法，两数同时除以最大公因数9")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["short_div"]), run_time=0.75)
            self.safe_subtitle(
                "设两数为 A、B，短除后得到商 a、b",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：强调互质 + 关系式 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "互质与关系"):
            self.add(
                prob_all, diag["hint"], diag["short_div"], diag["notes"],
            )
            s2 = self.step_label("第二步：a 与 b 互质，且 9×a×b＝90")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["coprime_g"]), run_time=0.5)
            self.play(diag["note_rel"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{gcd}×a×b＝{lcm}，所以 a×b＝{product}",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：分解互质因数对 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "分解互质对"):
            self.add(
                prob_all, diag["hint"], diag["short_div"],
                diag["coprime_g"], diag["notes"],
            )
            s3 = self.step_label(f"第三步：把 {product} 写成互质的因数对")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_pairs"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                "1 与 10 互质，2 与 5 互质（注意：不是所有因数对都互质）",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：还原两数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "还原两数"):
            self.add(
                prob_all, diag["hint"], diag["short_div"],
                diag["coprime_g"], diag["notes"],
            )
            s4 = self.step_label("第四步：把 a、b 分别乘回 9，得到原来的两数")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_case1"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.8)
            self.play(diag["note_case2"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                "两组答案：9 和 90，或 18 和 45",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["short_div"], diag["coprime_g"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                self.safe_text(f"{lcm}÷{gcd}={product}", font_size=22, color=WHITE),
                self.safe_text(f"{product}=1×10=2×5", font_size=22, color=WHITE),
                self.safe_text("① 1×9=9，10×9=90", font_size=20, color=TEAL_D),
                self.safe_text("② 2×9=18，5×9=45", font_size=20, color=ORANGE),
            ]
            formula_rows = VGroup(*lines).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in lines:
                self.play(FadeIn(row), run_time=0.4)
                self.wait(0.8)

            answer_text = self.safe_text(
                "答：这两个自然数是9和90，或18和45。",
                font_size=20, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.32)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("借助短除法分析 GCD 与 LCM 的关系", wait=5)
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
