"""
第36讲 盈亏问题 — 画图解题法（线段图法）

母题：每人分12多出5；每人分14缺5。求人数与苹果数。
答案：（5+5）÷（14−12）=5；12×5+5=65

用法:
  cd manim/scenes/线段图法
  python -m manim problem_36.py Problem36Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem36Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    RATE_A = 12
    SURPLUS = 5
    RATE_B = 14
    DEFICIT = 5

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        ra = self.RATE_A
        sur = self.SURPLUS
        rb = self.RATE_B
        defi = self.DEFICIT
        gap = sur + defi
        diff = rb - ra
        people = gap // diff
        apples = ra * people + sur

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
                "同样多的物品，按两种标准平均分：",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "一种有剩余（盈），一种不够分（亏）——用线段图对比解决！",
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

            feature_title = self.safe_text("盈亏问题的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "一种盈、一种亏", "多出来的与不够的合起来比较"),
                ("2", "差来自分得量不同", "每人多分数＝分配差"),
                ("3", "（盈＋亏）÷差＝份数", "再代回求物品总数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：盈与亏"):
            prob_all = self.make_problem_box(
                f"题目：每人分{ra}个多出{sur}个；每人分{rb}个就缺{defi}个。",
                "一共有多少个小朋友？多少个苹果？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_surplus_deficit_diagram(
            draw_y,
            rate_a=ra, surplus=sur,
            rate_b=rb, deficit=defi,
            show_hint=True,
        )

        # ── 图解1：第一种（盈）──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出第一种分法"):
            s1 = self.step_label(f"第一步：画出每人分{ra}个，还多出{sur}个")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["align"]), run_time=0.35)
            self.play(
                FadeIn(diag["name_a"]),
                Create(diag["line_a"]),
                FadeIn(diag["brace_a"]),
                run_time=0.6,
            )
            self.play(
                Create(diag["line_sur"]),
                FadeIn(diag["brace_sur"]),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"第一种分法有剩余（盈）{sur}个",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：第二种（亏）──
        with self.segment("draw-2", "2", "segments/04.mp4", "画出第二种分法"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_row"], diag["notes"], diag["apples_tag"],
            )
            s2 = self.step_label(f"第二步：画出每人分{rb}个，缺的{defi}个用虚线表示")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                FadeIn(diag["name_b"]),
                Create(diag["line_b_solid"]),
                FadeIn(diag["brace_b"]),
                run_time=0.6,
            )
            self.play(
                Create(diag["line_b_def"]),
                FadeIn(diag["brace_def"]),
                FadeIn(diag["apples_tag"]),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"第二种分法不够分（亏）{defi}个",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：求出人数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出人数"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_row"], diag["bot_row"], diag["apples_tag"], diag["notes"],
            )
            s3 = self.step_label("第三步：（盈＋亏）÷分配差，求出小朋友人数")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_gap"].animate.set_opacity(1), run_time=0.45)
            self.play(diag["note_diff"].animate.set_opacity(1), run_time=0.45)
            self.play(diag["note_people_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.5)
            self.play(
                diag["note_people_q"].animate.set_opacity(0),
                diag["note_people_ans"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"（{sur}+{defi}）÷（{rb}－{ra}）={people}（人）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出苹果数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出苹果数"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_row"], diag["bot_row"], diag["apples_tag"], diag["notes"],
            )
            s4 = self.step_label("第四步：用人数求出苹果总数")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_apples"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{ra}×{people}+{sur}={apples}（个），或 {rb}×{people}－{defi}={apples}",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["align"], diag["top_row"], diag["bot_row"],
            diag["apples_tag"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"（{sur}+{defi}）÷（{rb}－{ra}）={people}（个）",
                font_size=22, color=WHITE,
            )
            step2 = self.safe_text(
                f"{ra}×{people}+{sur}={apples}（个）",
                font_size=24, color=WHITE,
            )
            formula_rows = VGroup(step1, step2).arrange(
                DOWN, buff=0.30, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1, step2]:
                self.play(FadeIn(row), run_time=0.5)
                self.wait(1.1)

            answer_text = self.safe_text(
                f"答：一共有{people}个小朋友，{apples}个苹果。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.38)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("（盈＋亏）÷分配差＝份数", wait=5)
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
