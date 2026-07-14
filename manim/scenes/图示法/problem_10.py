"""
第10讲 等量代换问题 — 画图解题法（图示法）

母题：乐乐用2个橘子可以换明明的1个苹果，换3个苹果要用几个橘子？
答案：3×2=6（个）

用法:
  cd manim/scenes/图示法
  python -m manim problem_10.py Problem10Scene -ql

渲染后:
  python ..\_shared\post_render.py --lesson 10 \\
    --rendered media\videos\problem_10\480p15\Problem10Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem10Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    GIVE_PER_RECEIVE = 2
    TARGET_RECEIVE = 3
    GIVE_LABEL = "橘子"
    RECEIVE_LABEL = "苹果"

    def _play_unit(self, unit: Mobject) -> None:
        parts = list(unit)
        self.play(FadeIn(parts[0], scale=0.9), run_time=0.45)
        self.play(Create(parts[1]), run_time=0.35)
        self.play(FadeIn(parts[2], shift=UP * 0.08), run_time=0.4)

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

            concept_title = self.safe_text("什么是等量代换问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "题里的一种量可以用与它相等的另一种量来代替，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先找等量关系，再按目标数量计算——这就是等量代换！", font_size=28, color=WHITE,
            )
            concept_body = VGroup(s1_body, s1_body2).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
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

            feature_title = self.safe_text("等量代换问题的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "两种量可以互相代替", "比如：2个橘子 = 1个苹果"),
                ("2", "先明确等量关系", "画图标出「几个换几个」"),
                ("3", "按目标数量代换", "每个苹果要2个橘子，3个就要3×2"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：橘子换苹果"):
            prob_all = self.make_problem_box(
                "题目：乐乐用2个橘子可以换明明的1个苹果，",
                "如果乐乐想用橘子换明明的3个苹果，要用几个橘子？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_substitution_diagram(
            self.GIVE_PER_RECEIVE,
            self.TARGET_RECEIVE,
            draw_y,
            give_label=self.GIVE_LABEL,
            receive_label=self.RECEIVE_LABEL,
        )
        total_give = diag["total_give"]

        # ── 图解1：符号图例 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "用图形表示苹果和橘子"):
            s1 = self.step_label("第一步：用图形表示两种物品")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            self.play(FadeIn(diag["legend_block"], shift=DOWN * 0.12), run_time=0.65)
            self.safe_subtitle(
                f"1个圆圈表示1个{self.RECEIVE_LABEL}，1个三角形表示1个{self.GIVE_LABEL}",
                wait=4,
            )
            self.play(FadeOut(s1), FadeOut(diag["hint"]), run_time=0.3)

        # ── 图解2：第一组等量关系 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "1个苹果连2个橘子"):
            self.add(prob_all, diag["legend_block"])
            s2 = self.step_label("第二步：画出一组等量关系")
            self.play(FadeIn(s2), run_time=0.5)
            self._play_unit(diag["single_unit"])
            self.play(FadeIn(diag["rule_text"], shift=DOWN * 0.08), run_time=0.5)
            self.safe_subtitle(
                f"{self.GIVE_PER_RECEIVE}个{self.GIVE_LABEL}可以换1个{self.RECEIVE_LABEL}",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：三组共3个苹果 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "画3组表示3个苹果"):
            self.add(
                prob_all, diag["legend_block"],
                diag["single_unit"],
            )
            s3 = self.step_label("第三步：再画两组，表示3个苹果")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeOut(diag["rule_text"]), run_time=0.3)
            for unit_info in diag["units"][1:]:
                self._play_unit(unit_info["unit"])
            self.play(FadeIn(diag["top_note"], shift=UP * 0.08), run_time=0.55)
            self.safe_subtitle(
                f"换1个{self.RECEIVE_LABEL}需要{self.GIVE_PER_RECEIVE}个{self.GIVE_LABEL}，"
                f"共 {self.TARGET_RECEIVE} 个{self.RECEIVE_LABEL}",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：数橘子、列式 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "共需6个橘子"):
            self.add(
                prob_all, diag["legend_block"],
                diag["units_row"], diag["top_note"],
            )
            s4 = self.step_label("第四步：数下方橘子，列式计算")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(FadeIn(diag["bottom_note_q"], shift=DOWN * 0.08), run_time=0.5)
            self.play(
                diag["all_triangles"].animate.set_color(YELLOW),
                run_time=0.45,
            )
            self.safe_subtitle(
                f"下方共 ? 个{self.GIVE_LABEL}，每个{self.RECEIVE_LABEL}对应"
                f"{self.GIVE_PER_RECEIVE}个{self.GIVE_LABEL}",
                wait=3,
            )
            self.play(
                ReplacementTransform(diag["bottom_note_q"], diag["bottom_note_a"]),
                FadeIn(diag["formula_label"], shift=DOWN * 0.08),
                run_time=0.75,
            )
            self.safe_subtitle(
                f"换{self.TARGET_RECEIVE}个{self.RECEIVE_LABEL}就要 "
                f"{self.TARGET_RECEIVE}×{self.GIVE_PER_RECEIVE}={total_give}（个）{self.GIVE_LABEL}",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), FadeOut(diag["formula_label"]), run_time=0.3)

        diagram_all = diag["layout_row"]

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            explain = self.safe_text(
                f"换1个{self.RECEIVE_LABEL}需要{self.GIVE_PER_RECEIVE}个{self.GIVE_LABEL}，"
                f"换{self.TARGET_RECEIVE}个{self.RECEIVE_LABEL}就要：",
                font_size=24, color=GREY_B,
            )
            formula = self.safe_text(
                f"{self.TARGET_RECEIVE}×{self.GIVE_PER_RECEIVE}={total_give}（个）",
                font_size=28, color=WHITE,
            )
            formula_rows = VGroup(explain, formula).arrange(
                DOWN, buff=0.35, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.45), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)
            self.play(FadeIn(explain, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(2)
            self.play(FadeIn(formula, shift=RIGHT * 0.2), run_time=0.5)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：要用{total_give}个{self.GIVE_LABEL}。",
                font_size=32, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.65)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("明确等量关系，再按目标数量相乘", wait=5)
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
