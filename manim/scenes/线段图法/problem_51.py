"""
第51讲 储蓄问题 — 画图解题法（线段图法）

母题：本金 20000，五年定期，年利率 2.65%。求利息。
答案：20000×2.65%×5=2650（元）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_51.py Problem51Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem51Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    PRINCIPAL = 20000
    YEARS = 5
    RATE = 0.0265

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        p = self.PRINCIPAL
        years = self.YEARS
        rate_str = f"{self.RATE * 100:g}"

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
                "把钱存进银行，经过一段时间会得到利息，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "利息＝本金×利率×存期——用线段把本金和利息画清楚！",
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

            feature_title = self.safe_text("求利息的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "找准本金", "存入银行的钱是多少"),
                ("2", "看清利率和存期", "年利率、存了几年"),
                ("3", "套用公式", "利息＝本金×利率×存期"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求到期利息"):
            prob_all = self.make_problem_box(
                f"题目：本金{p}元，存期{years}年，年利率{rate_str}%。",
                "到期后有多少元利息？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.28
        diag = self.make_savings_interest_diagram(
            draw_y,
            principal=p,
            years=years,
            rate=self.RATE,
            show_hint=False,
        )
        interest = diag["interest"]

        # ── 图解1：画出本金 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出本金线段"):
            s1 = self.step_label("第一步：画出本金这一段")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(Create(diag["main"]), FadeIn(diag["ticks"]), run_time=0.55)
            self.play(diag["prin_bar"].animate.set_opacity(1), run_time=0.45)
            diag["prin_bar"].set_fill(TEAL_D, opacity=0.30)
            self.play(diag["prin_lab"].animate.set_opacity(1), run_time=0.4)
            self.safe_subtitle(
                f"左边是本金 {p} 元",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：画出利息并分年 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画出利息并分年"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["prin_bar"], diag["prin_lab"],
            )
            s2 = self.step_label(f"第二步：画出{years}年利息，并均分成{years}小段")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["int_bar"].animate.set_opacity(1), run_time=0.45)
            diag["int_bar"].set_fill(ORANGE, opacity=0.30)
            self.play(
                diag["int_lab"].animate.set_opacity(1),
                diag["year_ticks"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(diag["year_labs"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"右边是{years}年利息，每一小格表示一年的利息",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标出年利率含义 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出年利率"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["prin_bar"], diag["int_bar"], diag["year_ticks"],
                diag["prin_lab"], diag["int_lab"], diag["year_labs"],
            )
            s3 = self.step_label("第三步：说明每年利息与本金的关系")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["rate_note"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_formula"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"每年利息为本金的 {rate_str}%",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出利息 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出到期利息"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["prin_bar"], diag["int_bar"], diag["year_ticks"],
                diag["prin_lab"], diag["int_lab"], diag["year_labs"],
                diag["rate_note"], diag["note_formula"],
            )
            s4 = self.step_label("第四步：用公式求出到期利息")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_calc_q"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.6)
            self.play(
                diag["note_calc_q"].animate.set_opacity(0),
                diag["note_calc_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{p}×{rate_str}%×{years}={interest}（元）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["main"], diag["ticks"],
            diag["prin_bar"], diag["int_bar"], diag["year_ticks"],
            diag["prin_lab"], diag["int_lab"], diag["year_labs"],
            diag["rate_note"], diag["notes"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"{p}×{rate_str}%×{years}={interest}（元）",
                font_size=26, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            answer_text = self.safe_text(
                f"答：到期后有{interest}元利息。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f1, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.55)
            self.wait(1.0)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("利息＝本金×利率×存期", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(answer_text),
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
