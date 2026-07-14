"""
第23讲 归总问题 — 画图解题法（线段图法）

母题：每行12人排成4行；每行8人可排几行？
答案：12×4÷8=6（行）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_23.py Problem23Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem23Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    OLD_UNIT = 12
    OLD_PARTS = 4
    NEW_UNIT = 8

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        old_u = self.OLD_UNIT
        old_p = self.OLD_PARTS
        new_u = self.NEW_UNIT
        total = old_u * old_p
        new_p = total // new_u

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是归总问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "题目里有一个不变的「总量」，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先求出总量，再求新的份数或新的单一量——这就是归总问题！",
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

            feature_title = self.safe_text("线段图法解归总的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "两条等长线段", "表示两种排法总人数相同"),
                ("2", "按各自单一量分段", "上图原单一量，下图新单一量"),
                ("3", "先归总再除", "单一量×份数=总量，总量÷新单一量"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：总量不变"):
            prob_all = self.make_problem_box(
                f"题目：每行排{old_u}人，正好排成{old_p}行；",
                f"如果每行排{new_u}人，可以排成几行？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_aggregate_line_diagram(
            draw_y,
            old_unit=old_u,
            old_parts=old_p,
            new_unit=new_u,
            old_unit_label=f"{old_u}人",
            new_unit_label=f"{new_u}人",
            ask_label="?行",
            answer_label=f"{new_p}行",
            show_hint=True,
        )

        # ── 图解1：上图画原来的排法 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画原来的排法"):
            s1 = self.step_label(f"第一步：画出每行{old_u}人、共{old_p}行")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.35)
            self.play(Create(diag["top_line"]), run_time=0.6)
            self.play(FadeIn(diag["top_unit_block"]), run_time=0.5)
            self.play(FadeIn(diag["top_parts_lab"]), run_time=0.4)
            self.safe_subtitle(
                f"上面线段分成 {old_p} 段，每段表示 {old_u} 人",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：下图画新的排法 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画新的排法"):
            self.add(
                prob_all, diag["hint"], diag["top_block"],
            )
            s2 = self.step_label(f"第二步：下面画出每行{new_u}人的排法")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(Create(diag["bot_line"]), run_time=0.6)
            self.play(FadeIn(diag["bot_unit_block"]), run_time=0.5)
            self.safe_subtitle(
                "上下两条线段一样长，总人数不变",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标待求行数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标求出几行"):
            self.add(
                prob_all, diag["hint"],
                diag["top_block"], diag["bot_block"],
            )
            s3 = self.step_label("第三步：标出可以排成几行")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["ask_block"]), run_time=0.55)
            self.safe_subtitle(
                f"问的就是下面这条线段一共有几段（几行）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：先求总量再除 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "先求总量"):
            self.add(
                prob_all, diag["hint"],
                diag["top_block"], diag["bot_block"], diag["ask_block"],
            )
            s4 = self.step_label("第四步：总量不变，先乘后除")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["total_note"]), run_time=0.55)
            self.play(
                diag["ask_lab_q"].animate.set_opacity(0),
                diag["ask_lab_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{old_u}×{old_p}={total}（人），{total}÷{new_u}={new_p}（行）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["top_block"], diag["bot_block"],
            diag["ask_block"], diag["total_note"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            explain = self.safe_text(
                "总量不变：先求总人数，再÷新的每行人数：",
                font_size=22, color=GREY_B,
            )
            step = self.safe_text(
                f"{old_u}×{old_p}÷{new_u}={new_p}（行）",
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
                f"答：可以排成{new_p}行。",
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
            self.safe_subtitle("总量不变：单一量×份数，再÷新的单一量", wait=5)
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
