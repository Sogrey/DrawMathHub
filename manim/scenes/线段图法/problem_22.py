"""
第22讲 归一问题 — 画图解题法（线段图法）

母题：3盆花15元，买7盆同样的花要多少元？
答案：15÷3×7=35（元）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_22.py Problem22Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem22Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    KNOWN_PARTS = 3
    KNOWN_TOTAL = 15
    NEW_PARTS = 7

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        k_parts = self.KNOWN_PARTS
        k_total = self.KNOWN_TOTAL
        n_parts = self.NEW_PARTS
        unit = k_total // k_parts
        new_total = unit * n_parts

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是归一问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "题目里有一个不变的「单一量」，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先求出它，再求新的总量或份数——这就是归一问题！",
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

            feature_title = self.safe_text("线段图法解归一的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "按新的份数画线段", "先把要求的份数均分成若干段"),
                ("2", "标出已知份数与总量", "对应其中几段及总价"),
                ("3", "先归一再求新总量", "总量÷份数 = 单一量，再×新份数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：份数与总量"):
            prob_all = self.make_problem_box(
                f"题目：爸爸买{k_parts}盆花一共花了{k_total}元，",
                f"如果买{n_parts}盆同样的花，需要多少元？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_unitary_line_diagram(
            draw_y,
            known_parts=k_parts,
            known_total=k_total,
            new_parts=n_parts,
            known_label=f"{k_parts}盆花 {k_total}元",
            new_label=f"{n_parts}盆花 ?元",
            answer_label=f"{n_parts}盆花 {new_total}元",
            show_hint=True,
        )

        # ── 图解1：画 7 等分线段 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画等分线段"):
            s1 = self.step_label(f"第一步：画一条线段，平均分成 {n_parts} 份")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.35)
            self.play(Create(diag["main"]), run_time=0.5)
            self.play(FadeIn(diag["ticks"]), run_time=0.55)
            self.safe_subtitle(
                f"{n_parts} 份表示买 {n_parts} 盆花要花的钱",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标 3 盆 15 元 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标已知份数"):
            self.add(prob_all, diag["hint"], diag["main"], diag["ticks"])
            s2 = self.step_label(f"第二步：标出 {k_parts} 盆花花了 {k_total} 元")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["known_bar"]), run_time=0.45)
            self.play(FadeIn(diag["known_block"]), run_time=0.55)
            self.safe_subtitle(
                f"前 {k_parts} 份对应 {k_total} 元",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标 7 盆待求 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标新的总量"):
            self.add(
                prob_all, diag["hint"], diag["main"], diag["ticks"],
                diag["known_bar"], diag["known_block"],
            )
            s3 = self.step_label(f"第三步：整条线段表示 {n_parts} 盆花的总价")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["new_block"]), run_time=0.55)
            self.safe_subtitle(
                f"要求的就是这 {n_parts} 份一共多少元",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：先归一 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "先求单一量"):
            self.add(
                prob_all, diag["hint"], diag["line_core"],
                diag["known_block"], diag["new_block"],
            )
            s4 = self.step_label("第四步：先求每盆多少钱（单一量）")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["unit_note"]), run_time=0.55)
            # 与括号同组内切换透明度，避免 FadeIn 孤儿对象落在旧坐标
            self.play(
                diag["new_lab_q"].animate.set_opacity(0),
                diag["new_lab_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{k_total}÷{k_parts}={unit}（元），再×{n_parts}={new_total}（元）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["line_core"], diag["known_block"],
            diag["new_block"], diag["unit_note"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            explain = self.safe_text(
                "先求每盆单价（单一量），再乘盆数：",
                font_size=22, color=GREY_B,
            )
            step = self.safe_text(
                f"{k_total}÷{k_parts}×{n_parts}={new_total}（元）",
                font_size=28, color=WHITE,
            )
            formula_rows = VGroup(explain, step).arrange(
                DOWN, buff=0.32, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            self.play(FadeIn(explain), run_time=0.45)
            self.wait(1.2)
            self.play(FadeIn(step), run_time=0.55)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：需要{new_total}元。",
                font_size=30, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.50)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("单一量不变：总量÷份数，再×新份数", wait=5)
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
