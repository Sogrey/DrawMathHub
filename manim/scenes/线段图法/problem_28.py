"""
第28讲 追及问题 — 画图解题法（线段图法）

母题：乐乐在前方 150 米，方方 80 米/分，乐乐 50 米/分，几分钟追上？
答案：150÷(80−50)=5（分）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_28.py Problem28Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem28Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    CHASER_SPEED = 80
    AHEAD_SPEED = 50
    GAP = 150

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        v1 = self.CHASER_SPEED
        v2 = self.AHEAD_SPEED
        gap = self.GAP
        diff = v1 - v2
        t = gap // diff

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "两人同向而行，后面的人速度更快，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "经过一段时间追上前面的人——这就是追及问题！",
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

            feature_title = self.safe_text("追及问题的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "同向而行", "后追前，方向相同"),
                ("2", "先看路程差", "一开始两人相差多远"),
                ("3", "再看速度差", "路程差÷速度差 = 追及时间"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：同向追及"):
            prob_all = self.make_problem_box(
                f"题目：乐乐在方方前面{gap}米，方方每分钟{v1}米，乐乐每分钟{v2}米。",
                "方方几分钟能追上乐乐？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_catchup_diagram(
            draw_y,
            chaser_speed=v1,
            ahead_speed=v2,
            gap=gap,
            show_hint=True,
        )

        # ── 图解1：画出两条线段与路程差 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出追及线段图"):
            s1 = self.step_label("第一步：画出两人同向而行的线段图")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(
                FadeIn(diag["dash_start"]),
                FadeIn(diag["dash_ahead"]),
                FadeIn(diag["dash_catch"]),
                run_time=0.45,
            )
            self.play(
                Create(diag["ahead_line"]),
                FadeIn(diag["ahead_ticks"]),
                FadeIn(diag["ahead_name_lab"]),
                run_time=0.55,
            )
            self.play(
                Create(diag["chaser_line"]),
                FadeIn(diag["chaser_ticks"]),
                FadeIn(diag["chaser_name_lab"]),
                run_time=0.55,
            )
            self.play(FadeIn(diag["gap_block"]), FadeIn(diag["catch_tag"]), run_time=0.5)
            self.safe_subtitle(
                f"乐乐在前面 {gap} 米，两人都向右走，终点是追上的地方",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标速度与方向箭头 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标速度与方向"):
            self.add(
                prob_all, diag["hint"], diag["guides"],
                diag["ahead_line"], diag["ahead_ticks"], diag["ahead_name_lab"],
                diag["chaser_line"], diag["chaser_ticks"], diag["chaser_name_lab"],
                diag["gap_block"], diag["catch_tag"],
            )
            s2 = self.step_label("第二步：标出两人的速度")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                GrowArrow(diag["ahead_arrow"]),
                FadeIn(diag["ahead_speed_lab"]),
                run_time=0.55,
            )
            self.play(
                GrowArrow(diag["chaser_arrow"]),
                FadeIn(diag["chaser_speed_lab"]),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"方方每分钟 {v1} 米，乐乐每分钟 {v2} 米，同向前进",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：算速度差 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出速度差"):
            self.add(
                prob_all, diag["hint"], diag["guides"],
                diag["ahead_row"], diag["chaser_row"],
                diag["gap_block"], diag["catch_tag"], diag["notes"],
            )
            s3 = self.step_label("第三步：算出方方每分钟比乐乐多走多少")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_diff"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"速度差 {v1}−{v2}={diff} 米，也就是每分钟缩短 {diff} 米",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：路程差÷速度差 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求追及时间"):
            self.add(
                prob_all, diag["hint"], diag["guides"],
                diag["ahead_row"], diag["chaser_row"],
                diag["gap_block"], diag["catch_tag"], diag["notes"],
            )
            s4 = self.step_label("第四步：路程差÷速度差，求出追及时间")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(diag["note_time_q"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.6)
            self.play(
                diag["note_time_q"].animate.set_opacity(0),
                diag["note_time_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{gap}÷{diff}={t}（分）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["guides"], diag["ahead_row"], diag["chaser_row"],
            diag["gap_block"], diag["catch_tag"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step = self.safe_text(
                f"{gap}÷({v1}−{v2})={t}（分）",
                font_size=28, color=WHITE,
            )
            step_note = self.safe_text(
                "（路程差÷速度差）",
                font_size=20, color=GREY_B,
            )
            formula_rows = VGroup(step, step_note).arrange(
                DOWN, buff=0.28, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            self.play(FadeIn(step), run_time=0.55)
            self.wait(1.2)
            self.play(FadeIn(step_note), run_time=0.45)
            self.wait(1.0)

            answer_text = self.safe_text(
                f"答：方方{t}分钟能追上乐乐。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.42)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("追及时间 = 路程差 ÷ 速度差", wait=5)
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
