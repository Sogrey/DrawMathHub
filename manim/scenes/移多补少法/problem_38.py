"""
第38讲 平均数问题（二）— 画图解题法（移多补少法）

母题：甲乙丙丁 8.5/9.0/8.6/8.7，小艺比五人平均多 0.8。小艺多少分？
答案：五人平均 8.9；小艺 9.7

用法:
  cd manim/scenes/移多补少法
  python -m manim problem_38.py Problem38Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem38Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    SCORES = [8.5, 9.0, 8.6, 8.7]
    NAMES = ["甲", "乙", "丙", "丁"]
    EXTRA = 0.8
    NEW_NAME = "小艺"

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        scores = self.SCORES
        n = len(scores)
        extra = self.EXTRA
        four_avg = sum(scores) / n
        share = extra / n
        five_avg = four_avg + share
        new_score = five_avg + extra
        new_name = self.NEW_NAME

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
                "新加入一个人，只知道他比全员平均分多多少，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用移多补少求出全员平均，再求他的分数！",
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

            feature_title = self.safe_text("移多补少求平均的三个要点", font_size=28, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先算原有人的平均", "已知分数先求四人平均"),
                ("2", "多出的均摊补齐", "多出的0.8平均分给其他四人"),
                ("3", "再求新人分数", "五人平均＋多出的量"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：多出0.8分"):
            prob_all = self.make_problem_box(
                f"题目：甲乙丙丁得分{scores[0]}/{scores[1]}/{scores[2]}/{scores[3]}，"
                f"{new_name}比五人平均多{extra}分。",
                f"{new_name}得了多少分？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_average_shift_diagram(
            draw_y,
            scores=scores,
            names=self.NAMES,
            new_name=new_name,
            extra=extra,
            show_hint=True,
        )

        # ── 图解1：四人柱与四人平均 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出四人平均"):
            s1 = self.step_label("第一步：用柱形表示四人得分，标出四人平均分")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(
                FadeIn(diag["four_blues"]),
                FadeIn(diag["name_labs"][:n]),
                run_time=0.7,
            )
            self.play(FadeIn(diag["line4"]), run_time=0.5)
            self.add(diag["notes"])
            self.play(diag["note_four"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"四人平均分是 {four_avg:g} 分",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：小艺多出 0.8，均摊 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "移多补少"):
            self.add(
                prob_all, diag["hint"], diag["four_blues"], diag["name_labs"][:n],
                diag["line4"], diag["notes"], diag["tips_four"],
            )
            s2 = self.step_label(f"第二步：把{new_name}多出的{extra}分平均补给其他四人")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                FadeIn(diag["new_blue"]),
                FadeIn(diag["name_labs"][n]),
                run_time=0.5,
            )
            self.play(
                diag["new_extra"].animate.set_opacity(1),
                diag["extra_anno"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.play(
                *[a.animate.set_opacity(0.85) for a in diag["arrows"]],
                *[t.animate.set_opacity(1) for t in diag["tips_four"]],
                run_time=0.7,
            )
            self.safe_subtitle(
                f"{extra}÷{n}={share:g}，每人补 {share:g} 分",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：求出五人平均 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出五人平均"):
            self.add(
                prob_all, diag["hint"], diag["chart"], diag["notes"],
            )
            s3 = self.step_label("第三步：四人平均加上均摊量，得到五人平均分")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(
                diag["line5"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(diag["note_five_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.5)
            self.play(
                diag["note_five_q"].animate.set_opacity(0),
                diag["note_five_ans"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"{four_avg:g}+{share:g}={five_avg:g}（分）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出小艺分数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出小艺分数"):
            self.add(
                prob_all, diag["hint"], diag["chart"], diag["notes"],
            )
            s4 = self.step_label(f"第四步：五人平均再加上多出的{extra}分")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_new"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{five_avg:g}+{extra}={new_score:g}（分）",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(diag["chart"], diag["notes"])

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"({scores[0]}+{scores[1]}+{scores[2]}+{scores[3]})÷{n}"
                f"+({extra}÷{n})={five_avg:g}",
                font_size=18, color=WHITE,
            )
            step1_note = self.safe_text("（五人平均）", font_size=16, color=GREY_B)
            step1_row = VGroup(step1, step1_note).arrange(RIGHT, buff=0.12)

            step2 = self.safe_text(
                f"{five_avg:g}+{extra}={new_score:g}（分）",
                font_size=24, color=WHITE,
            )
            formula_rows = VGroup(step1_row, step2).arrange(
                DOWN, buff=0.30, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1_row, step2]:
                self.play(FadeIn(row), run_time=0.5)
                self.wait(1.1)

            answer_text = self.safe_text(
                f"答：{new_name}得了{new_score:g}分。",
                font_size=24, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.38)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("移多补少，先定五人平均再求个人", wait=5)
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
