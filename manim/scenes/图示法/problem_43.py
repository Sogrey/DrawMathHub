"""
第43讲 牛吃草问题 — 画图解题法（图示法）

母题：20头10天或24头6天；可供18头吃多少天？
答案：生长14份/天，原有60份，可吃15天。

用法:
  cd manim/scenes/图示法
  python -m manim problem_43.py Problem43Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem43Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    COWS_A, DAYS_A = 20, 10
    COWS_B, DAYS_B = 24, 6
    COWS_Q = 18

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        ca, da = self.COWS_A, self.DAYS_A
        cb, db = self.COWS_B, self.DAYS_B
        cq = self.COWS_Q
        eat_a, eat_b = ca * da, cb * db
        grow = (eat_a - eat_b) // (da - db)
        original = eat_a - grow * da
        days_q = original // (cq - grow)

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
                "草一边被吃、一边匀速生长，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "根据两次吃完的情况，求出原有草和每天生长量！",
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

            feature_title = self.safe_text("牛吃草问题的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "吃掉＝原有＋新长", "每头牛每天吃1份来统一单位"),
                ("2", "份数差÷天数差", "求出草每天生长多少份"),
                ("3", "原有÷每天净减", "得到这群牛可吃的天数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：两次吃完"):
            prob_all = self.make_problem_box(
                f"题目：可供{ca}头吃{da}天，或{cb}头吃{db}天。",
                f"可供{cq}头牛吃多少天？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_cow_grass_diagram(
            draw_y,
            cows_a=ca, days_a=da,
            cows_b=cb, days_b=db,
            cows_q=cq,
            show_hint=True,
        )

        # ── 图解1：画出两次吃草总量条 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出两次总量"):
            s1 = self.step_label("第一步：用长条表示两次「原有＋新长」的总量")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["align"]), run_time=0.3)
            self.play(
                FadeIn(diag["name_a"]),
                FadeIn(diag["orig_top"]),
                FadeIn(diag["brace_orig"]),
                run_time=0.55,
            )
            self.play(
                FadeIn(diag["grow_top"]),
                FadeIn(diag["brace_ga"]),
                run_time=0.5,
            )
            self.play(
                FadeIn(diag["name_b"]),
                FadeIn(diag["orig_bot"]),
                FadeIn(diag["grow_bot"]),
                FadeIn(diag["brace_gb"]),
                run_time=0.6,
            )
            self.safe_subtitle(
                f"{ca}×{da}={eat_a}份，{cb}×{db}={eat_b}份",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：求每天生长 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "求每天生长"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_row"], diag["bot_row"], diag["diff_g"], diag["notes"],
            )
            s2 = self.step_label("第二步：份数差÷天数差，求出每天新长多少份")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["diff_g"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_grow"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"({eat_a}－{eat_b})÷({da}－{db})={grow}（份/天）",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：求原有草 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求原有草"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_row"], diag["bot_row"], diag["diff_g"], diag["notes"],
            )
            s3 = self.step_label("第三步：总吃掉减去生长期间新长的，得原有草")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_orig"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{eat_a}－{grow}×{da}={original}（份）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求18头可吃天数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求可吃天数"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_row"], diag["bot_row"], diag["diff_g"], diag["notes"],
            )
            s4 = self.step_label(f"第四步：{cq}头每天净减，求可吃天数")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_days_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.5)
            self.play(
                diag["note_days_q"].animate.set_opacity(0),
                diag["note_days_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{original}÷({cq}－{grow})={days_q}（天）",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["align"], diag["top_row"], diag["bot_row"],
            diag["diff_g"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"({ca}×{da}－{cb}×{db})÷({da}－{db})={grow}",
                font_size=20, color=WHITE,
            )
            step2 = self.safe_text(
                f"{ca}×{da}－{grow}×{da}={original}",
                font_size=22, color=WHITE,
            )
            step3 = self.safe_text(
                f"{original}÷({cq}－{grow})={days_q}（天）",
                font_size=22, color=WHITE,
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
                f"答：可供{cq}头牛吃{days_q}天。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.34)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("抓住生长量与净减少量", wait=5)
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
