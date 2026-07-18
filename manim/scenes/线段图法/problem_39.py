"""
第39讲 方程问题 — 画图解题法（线段图法）

母题：甲 48、乙 72，甲先开 2 小时，几小时后乙追上？
答案：48×2+48x=72x → x=4

用法:
  cd manim/scenes/线段图法
  python -m manim problem_39.py Problem39Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem39Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    AHEAD_SPEED = 48
    CHASER_SPEED = 72
    HEAD_START = 2

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        va = self.AHEAD_SPEED
        vb = self.CHASER_SPEED
        t0 = self.HEAD_START
        lead = va * t0
        x_ans = lead // (vb - va)

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
                "题中隐藏着未知数的等量关系，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用线段图找出相等的量，再列方程求解！",
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

            feature_title = self.safe_text("用方程解追及的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "设未知数 x", "设乙开出 x 小时后追上"),
                ("2", "找等量关系", "追上时甲路程＝乙路程"),
                ("3", "按图列方程", "先行路程＋甲走 x＝乙走 x"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：同向追及"):
            prob_all = self.make_problem_box(
                f"题目：甲{va}千米/时，乙{vb}千米/时，甲先开{t0}小时。",
                "几小时后乙车追上甲车？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_equation_catchup_diagram(
            draw_y,
            ahead_speed=va,
            chaser_speed=vb,
            head_start=t0,
            show_hint=True,
        )

        # ── 图解1：画出甲的路程（先行＋共同）──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出甲车路程"):
            s1 = self.step_label("第一步：设 x 小时后追上，画出甲车两段路程")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["guides"]), run_time=0.4)
            self.play(
                FadeIn(diag["name_a"]),
                Create(diag["line_lead"]),
                FadeIn(diag["brace_lead"]),
                run_time=0.6,
            )
            self.play(
                Create(diag["line_ax"]),
                FadeIn(diag["brace_ax"]),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"甲先走{t0}小时，再与乙共同走 x 小时",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：画出乙的路程 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画出乙车路程"):
            self.add(
                prob_all, diag["hint"], diag["guides"],
                diag["top_row"], diag["notes"],
            )
            s2 = self.step_label("第二步：乙车只走 x 小时，路程与甲车总长相等")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                FadeIn(diag["name_b"]),
                Create(diag["line_b"]),
                FadeIn(diag["brace_b"]),
                run_time=0.65,
            )
            self.safe_subtitle("追上时，两车行驶的路程相同", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：写出等量关系与方程 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "列出方程"):
            self.add(
                prob_all, diag["hint"], diag["guides"],
                diag["top_row"], diag["bot_row"], diag["notes"],
            )
            s3 = self.step_label("第三步：根据等量关系列出方程")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_eq"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_form_q"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{va}×{t0}+{va}x={vb}x",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：解出 x ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出x"):
            self.add(
                prob_all, diag["hint"], diag["guides"],
                diag["top_row"], diag["bot_row"], diag["notes"],
            )
            s4 = self.step_label("第四步：解方程，求出追上时间")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_form_ans"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{lead}+{va}x={vb}x → x={x_ans}",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["guides"], diag["top_row"], diag["bot_row"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列方程作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                self.safe_text("解：设 x 小时后乙车追上甲车。", font_size=20, color=GREY_B),
                self.safe_text(f"{va}×{t0}+{va}x={vb}x", font_size=24, color=WHITE),
                self.safe_text(f"{lead}+{va}x={vb}x", font_size=24, color=WHITE),
                self.safe_text(f"{vb - va}x={lead}", font_size=24, color=WHITE),
                self.safe_text(f"x={x_ans}", font_size=26, color=ORANGE),
            ]
            formula_rows = VGroup(*lines).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in lines:
                self.play(FadeIn(row), run_time=0.4)
                self.wait(0.7)

            answer_text = self.safe_text(
                f"答：{x_ans}小时后乙车追上甲车。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.32)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("追上时两车路程相等", wait=5)
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
