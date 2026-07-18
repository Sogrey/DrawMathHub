"""
第58讲 鸽巢问题 — 画图解题法（图示法）

母题：4只鸽子飞进3个鸽巢，总有1个鸽巢里至少几只？
答案：4÷3=1……1；1+1=2（只）

用法:
  cd manim/scenes/图示法
  python -m manim problem_58.py Problem58Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem58Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    PIGEONS = 4
    NESTS = 3

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        m = self.PIGEONS
        n = self.NESTS

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
                "m 只鸽子飞进 n 个鸽巢，求总有一个巢里",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "至少有几只——用除法的商和余数来判断！",
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

            feature_title = self.safe_text("解题的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "认清 m 和 n", "鸽子数 m，鸽巢数 n"),
                ("2", "先每巢放1只", "看还剩几只"),
                ("3", "余数进任一巢", "至少＝商＋1"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：至少几只"):
            prob_all = self.make_problem_box(
                f"题目：{m}只鸽子飞进{n}个鸽巢里，",
                "总有1个鸽巢里至少飞进了几只鸽子？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.15
        diag = self.make_pigeonhole_diagram(
            draw_y, pigeons=m, nests=n, show_hint=False,
        )
        q = diag["quotient"]
        r = diag["remainder"]
        ans = diag["at_least"]

        # ── 图解1：画出鸽巢，每巢先放1只 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "每巢先飞进1只"):
            s1 = self.step_label(f"第一步：画出{n}个鸽巢，每巢先飞进1只")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["nests"]), run_time=0.55)
            self.play(FadeIn(diag["base_pigeons"]), run_time=0.55)
            self.play(diag["lab_one"].animate.set_opacity(1), run_time=0.4)
            self.safe_subtitle(
                f"{n}个鸽巢先飞进{n}只，还剩{r}只",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出剩下的鸽子 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出剩下的鸽子"):
            self.add(
                prob_all, diag["nests"], diag["base_pigeons"], diag["lab_one"],
            )
            s2 = self.step_label("第二步：标出剩下的鸽子")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["extra_pigeons"]), run_time=0.5)
            self.play(diag["lab_extra"].animate.set_opacity(1), run_time=0.4)
            self.safe_subtitle("剩下的鸽子无论飞进哪一个巢", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：余鸽飞进一巢，至少＝商+1 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出至少几只"):
            self.add(
                prob_all, diag["nests"], diag["base_pigeons"],
                diag["extra_pigeons"], diag["lab_one"], diag["lab_extra"],
            )
            s3 = self.step_label("第三步：剩下的飞进任一巢，至少＝商＋1")
            self.play(FadeIn(s3), run_time=0.5)

            moves = [
                diag["base_pigeons"][0].animate.move_to(diag["base_shift_in_first"]),
            ]
            for bird, target in zip(diag["extra_pigeons"], diag["stacked_targets"]):
                moves.append(bird.animate.move_to(target))
            self.play(*moves, run_time=0.85)

            # 强调第一个巢有 2 只
            ring = SurroundingRectangle(
                diag["nests"][0],
                color=YELLOW, buff=0.08, corner_radius=0.12, stroke_width=2.5,
            )
            self.play(Create(ring), run_time=0.45)
            self.play(diag["note_div"].animate.set_opacity(1), run_time=0.45)
            self.play(diag["note_add"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle(
                f"总有1个鸽巢里至少飞进了{ans}只",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s3), FadeOut(ring), run_time=0.35)

        diagram_all = Group(
            diag["nests"], diag["base_pigeons"], diag["extra_pigeons"],
            diag["lab_one"], diag["lab_extra"],
            diag["note_div"], diag["note_add"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/06.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"{m}÷{n}={q}（只）……{r}（只）",
                font_size=22, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.70), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = self.safe_text(
                f"{q}+1={ans}（只）",
                font_size=22, color=WHITE,
            )
            f2.next_to(f1, DOWN, buff=0.28)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            answer_text = self.safe_text(
                f"答：总有1个鸽巢里至少飞进了{ans}只鸽子。",
                font_size=20, color=YELLOW,
            )
            answer_text.next_to(f2, DOWN, buff=0.34)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.5)
            self.wait(0.7)
            self.play(FadeIn(f2), run_time=0.5)
            self.wait(0.7)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("关键：用 m÷n 的商与余数判断", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(f2),
                FadeOut(answer_text), FadeOut(highlight_box),
                FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=7,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
