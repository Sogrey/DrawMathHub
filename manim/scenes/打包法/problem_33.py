"""
第33讲 鸡兔同笼问题（二）— 画图解题法（打包法）

母题：兔是鸡的3倍，共280条腿。鸡和兔各多少只？
答案：每组14条腿；280÷14=20组；鸡20，兔60

用法:
  cd manim/scenes/打包法
  python -m manim problem_33.py Problem33Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem33Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    RABBIT_MULT = 3
    TOTAL_LEGS = 280
    CHICKEN_LEGS = 2
    RABBIT_LEGS = 4

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        mult = self.RABBIT_MULT
        total = self.TOTAL_LEGS
        c_legs = self.CHICKEN_LEGS
        r_legs = self.RABBIT_LEGS
        legs_per = mult * r_legs + c_legs
        groups = total // legs_per
        chickens = groups
        rabbits = mult * groups

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
                "鸡、兔数量存在倍数关系，且已知总腿数，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "按倍数打成「一组」来求——这就是打包法！",
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

            feature_title = self.safe_text("打包法的三个要点", font_size=32, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "按倍数打成一组", "如兔是鸡的3倍→1鸡+3兔"),
                ("2", "先算每组腿数", "用总腿数÷每组腿数得组数"),
                ("3", "再按份数求只数", "鸡＝1×组数，兔＝倍数×组数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：倍数与总腿数"):
            prob_all = self.make_problem_box(
                f"题目：鸡兔同笼，兔的数量是鸡的{mult}倍，一共有{total}条腿。",
                "鸡和兔各有多少只？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_chicken_rabbit_pack_diagram(
            draw_y,
            rabbit_mult=mult,
            total_legs=total,
            chicken_legs=c_legs,
            rabbit_legs=r_legs,
            show_hint=True,
        )

        # ── 图解1：打出一组 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "打成一组"):
            s1 = self.step_label(f"第一步：按倍数，把1只鸡和{mult}只兔打成一组")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["first_pack"]), FadeIn(diag["unit_note"]), run_time=0.7)
            self.safe_subtitle(
                f"兔是鸡的{mult}倍，所以每组里有1鸡＋{mult}兔",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：重复打包，标总腿数 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "多组与总腿数"):
            self.add(
                prob_all, diag["hint"], diag["first_pack"], diag["unit_note"],
                diag["notes"],
            )
            s2 = self.step_label("第二步：同样的组可以重复出现，总腿数280条")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["other_packs"]), run_time=0.65)
            self.play(FadeIn(diag["legs_block"]), run_time=0.5)
            self.safe_subtitle(
                f"每一组腿数相同，一共有{total}条腿",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：每组腿数与组数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出组数"):
            self.add(
                prob_all, diag["hint"], diag["packs_row"], diag["unit_note"],
                diag["legs_block"], diag["notes"],
            )
            s3 = self.step_label("第三步：先算每组腿数，再求一共几组")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_legs"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{mult}×{r_legs}＋{c_legs}={legs_per}（条）",
                wait=3,
            )
            self.play(diag["note_groups_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.5)
            self.play(
                diag["note_groups_q"].animate.set_opacity(0),
                diag["note_groups_ans"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"{total}÷{legs_per}={groups}（组）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出鸡兔只数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出鸡和兔"):
            self.add(
                prob_all, diag["hint"], diag["packs_row"], diag["unit_note"],
                diag["legs_block"], diag["notes"],
            )
            s4 = self.step_label("第四步：按每组份数，求出鸡和兔各有多少只")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_chi"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_rab"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"鸡 {chickens} 只，兔 {rabbits} 只",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["packs_row"], diag["unit_note"], diag["legs_block"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{mult}×{r_legs}＋{c_legs}={legs_per}（条）",
                font_size=24, color=WHITE,
            )
            step2 = self.safe_text(
                f"{total}÷{legs_per}={groups}（组）",
                font_size=24, color=WHITE,
            )
            step3 = self.safe_text(
                f"鸡：1×{groups}={chickens}（只）",
                font_size=24, color=WHITE,
            )
            step4 = self.safe_text(
                f"兔：{mult}×{groups}={rabbits}（只）",
                font_size=24, color=WHITE,
            )
            formula_rows = VGroup(step1, step2, step3, step4).arrange(
                DOWN, buff=0.26, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1, step2, step3, step4]:
                self.play(FadeIn(row), run_time=0.45)
                self.wait(0.9)

            answer_text = self.safe_text(
                f"答：鸡有{chickens}只，兔有{rabbits}只。",
                font_size=24, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("组数＝总腿数÷每组腿数之和", wait=5)
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
