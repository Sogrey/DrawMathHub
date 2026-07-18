"""
第45讲 逻辑推理问题（三）— 画图解题法（连线法）

母题：小明/小华/小强得金/银/铜；胡老师三句猜测只对一句。
答案：小明铜牌，小华金牌，小强银牌

用法:
  cd manim/scenes/连线法
  python -m manim problem_45.py Problem45Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem45Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

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
                "题目里混有对错不一的猜测，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "只知道「猜对了几句」——用连线逐一假设排除！",
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

            feature_title = self.safe_text("连线法的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "假设其中一句为真", "其余猜测一律当作假话来推"),
                ("2", "人与奖牌连线", "每人一牌，每牌一人，不能重复"),
                ("3", "矛盾就排除", "只留下没有矛盾的那一种假设"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：三猜只对一句"):
            prob_all = self.make_problem_box(
                "题目：小明、小华、小强一人金、一人银、一人铜。",
                "胡老师猜：①明金；②华不得金；③强不得铜。只对一句。各得什么牌？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_medal_logic_diagram(draw_y, show_hint=True)
        c1, c2, c3 = diag["case1"], diag["case2"], diag["case3"]

        def reveal_case(case, *, show_conflict: bool, show_ok: bool):
            self.play(
                FadeIn(case["title"]),
                FadeIn(case["top"]),
                FadeIn(case["bot"]),
                run_time=0.6,
            )
            case["lines"].set_opacity(1)
            self.play(*[Create(ln) for ln in case["lines"]], run_time=0.9)
            if show_conflict and len(case["conflict"]) > 0:
                case["conflict"].set_opacity(1)
                self.play(FadeIn(case["conflict"]), run_time=0.5)
            if show_ok:
                case["ok_tag"].set_opacity(1)
                self.play(FadeIn(case["ok_tag"]), run_time=0.4)

        # ── 图解1：假设①对 → 矛盾 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "假设①对，出现矛盾"):
            s1 = self.step_label("第一步：假设「小明得金牌」对 → 连线")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.4)

            reveal_case(c1, show_conflict=True, show_ok=False)
            self.safe_subtitle(
                "假话推得：小华也得金、小强得铜 → 两人金牌，矛盾！",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：假设②对 → 矛盾 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "假设②对，出现矛盾"):
            self.add(prob_all, diag["hint"], c1["panel"])
            s2 = self.step_label("第二步：假设「小华不得金牌」对 → 连线")
            self.play(FadeIn(s2), run_time=0.5)
            reveal_case(c2, show_conflict=True, show_ok=False)
            self.safe_subtitle(
                "推得小明、小华都只能得银牌 → 矛盾！",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：假设③对 → 成立 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "假设③对，成立"):
            self.add(prob_all, diag["hint"], c1["panel"], c2["panel"])
            s3 = self.step_label("第三步：假设「小强不得铜牌」对 → 连线")
            self.play(FadeIn(s3), run_time=0.5)
            reveal_case(c3, show_conflict=False, show_ok=True)
            self.play(diag["note_ans"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                "小明铜牌，小华金牌，小强银牌",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)

        diagram_all = VGroup(diag["cases"], diag["note_ans"])

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/06.mp4", "书面答题：写出答案"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            line1 = self.safe_text(
                "假设③正确时无矛盾，",
                font_size=24, color=WHITE,
            )
            line1.move_to(np.array([
                left_x + line1.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            line1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(line1)

            answer_text = self.safe_text(
                "答：小明铜牌，小华金牌，小强银牌。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(line1, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )

            self.play(FadeIn(line1), run_time=0.5)
            self.wait(1.0)
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("逐一假设，连线排除矛盾", wait=5)
            self.wait(2)
            self.play(
                FadeOut(line1), FadeOut(answer_text),
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
