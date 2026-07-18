"""
第18讲 和差问题 — 画图解题法（线段图法）

母题：合唱团共12人，女比男多6人，男女各多少？
答案：方法一 (12+6)÷2=9，12-9=3；方法二 (12-6)÷2=3，12-3=9

两种解法分别各画一幅图，作答段上下同时保留。

用法:
  cd manim/scenes/线段图法
  python -m manim problem_18.py Problem18Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem18Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    TOTAL = 12
    DIFFERENCE = 6
    LARGE_NAME = "女"
    SMALL_NAME = "男"

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        total = self.TOTAL
        diff = self.DIFFERENCE
        large = (total + diff) // 2
        small = (total - diff) // 2

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
                "已知两个量的「和」与「差」，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求这两个量分别是多少——这就是和差问题！",
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

            feature_title = self.safe_text("线段图法解和差的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "画出长短两条线段", "长的是较大数，短的是较小数"),
                ("2", "标出「和」与「差」", "右侧标和，多出的一段是差"),
                ("3", "补差、去差两种图画法", "两法图都保留，结果相同"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：找「和」与「差」"):
            prob_all = self.make_problem_box(
                f"题目：合唱团共有{total}人，{self.LARGE_NAME}队员比{self.SMALL_NAME}队员多{diff}人。",
                f"{self.SMALL_NAME}、{self.LARGE_NAME}队员各有多少人？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(5)

        draw_y = self.layout["draw_y"]
        y1 = draw_y + 0.95
        y2 = draw_y - 1.05
        common = dict(
            total=total,
            difference=diff,
            large_name=self.LARGE_NAME,
            small_name=self.SMALL_NAME,
            show_hint=False,
            scale=0.78,
        )
        d1 = self.make_sum_diff_diagram(y1, **common)
        d2 = self.make_sum_diff_diagram(y2, **common)

        # ── 图解1：方法一底图 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "方法一：画长短线段"):
            s1 = self.step_label("第一步：方法一——先画男、女两条线段")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(d1["m1_tag"]), run_time=0.4)
            self.play(FadeIn(d1["align_l"]), run_time=0.3)
            self.play(
                Create(d1["large_base"]),
                Create(d1["large_extra_solid"]),
                FadeIn(d1["large_name"]),
                run_time=0.7,
            )
            self.play(
                Create(d1["small_line"]), FadeIn(d1["small_name"]),
                run_time=0.65,
            )
            self.play(FadeIn(d1["align_mid"]), run_time=0.35)
            self.safe_subtitle(
                f"{self.LARGE_NAME}比{self.SMALL_NAME}多，上面画得长一些",
                wait=5,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：方法一标和差 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "方法一：标和与差"):
            self.add(
                prob_all, d1["m1_tag"], d1["align"],
                d1["large_block"], d1["small_block"],
            )
            s2 = self.step_label("第二步：标出「和」与「差」")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(d1["diff_block"]), run_time=0.6)
            self.wait(0.6)
            self.play(FadeIn(d1["sum_block"]), run_time=0.6)
            self.safe_subtitle(
                f"一共 {total} 人是「和」，多出的 {diff} 人是「差」",
                wait=5,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：方法一补差（保留）──
        with self.segment("draw-3", "3", "segments/05.mp4", "方法一：补差凑平"):
            self.add(
                prob_all, d1["m1_tag"], d1["align"],
                d1["large_block"], d1["small_block"],
                d1["diff_block"], d1["sum_block"],
            )
            s3 = self.step_label(f"第三步：假设{self.SMALL_NAME}队员增加{diff}人")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(Create(d1["add_seg"]), FadeIn(d1["add_note"]), run_time=0.85)
            self.wait(0.8)
            self.play(
                FadeOut(d1["sum_label"]),
                FadeIn(d1["m1_sum_label"]),
                run_time=0.55,
            )
            self.play(FadeIn(d1["equal_note"]), run_time=0.5)
            self.safe_subtitle(
                f"补差后两量相等，总人数变成 {total}+{diff}={total + diff}；"
                f"（{total}+{diff}）÷2={large}",
                wait=6,
            )
            self.wait(1.5)
            self.play(FadeOut(s3), run_time=0.3)

        panel1 = d1["panel_m1"]

        # ── 图解4：方法二另起一图画底图 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "方法二：另画一幅底图"):
            self.add(prob_all, panel1)
            s4 = self.step_label("第四步：方法二——下面再画一幅同样的底图")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(FadeIn(d2["m2_tag"]), run_time=0.45)
            self.wait(0.4)
            self.play(FadeIn(d2["align_l"]), run_time=0.3)
            self.play(
                Create(d2["large_base"]),
                Create(d2["large_extra_solid"]),
                FadeIn(d2["large_name"]),
                run_time=0.7,
            )
            self.play(
                Create(d2["small_line"]), FadeIn(d2["small_name"]),
                run_time=0.65,
            )
            self.play(FadeIn(d2["align_mid"]), run_time=0.35)
            self.play(FadeIn(d2["diff_block"]), run_time=0.55)
            self.play(FadeIn(d2["sum_block"]), run_time=0.55)
            self.safe_subtitle(
                "方法二的图画在下面，和与差跟上面一样",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        # ── 图解5：方法二去差（与方法一并排保留）──
        with self.segment("draw-5", "5", "segments/07.mp4", "方法二：去差凑平"):
            self.add(
                prob_all, panel1,
                d2["m2_tag"], d2["align"],
                d2["large_block"], d2["small_block"],
                d2["diff_block"], d2["sum_block"],
            )
            s5 = self.step_label(f"第五步：假设{self.LARGE_NAME}队员减少{diff}人")
            self.play(FadeIn(s5), run_time=0.5)
            self.play(
                FadeOut(d2["large_extra_solid"]),
                FadeIn(d2["large_extra_dashed"]),
                FadeIn(d2["rem_extra_note"]),
                run_time=0.8,
            )
            self.wait(0.6)
            self.play(
                FadeOut(d2["sum_block"]),
                FadeIn(d2["rem_sum_block"]),
                run_time=0.55,
            )
            self.play(FadeIn(d2["equal_note"]), run_time=0.5)
            self.safe_subtitle(
                f"去差后两量相等，总人数变成 {total}−{diff}={total - diff}；"
                f"（{total}−{diff}）÷2={small}",
                wait=6,
            )
            self.wait(1.5)
            self.play(FadeOut(s5), run_time=0.3)

        panel2 = d2["panel_m2"]
        diagram_all = VGroup(panel1, panel2)

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/08.mp4", "书面答题：两种方法"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(
                diagram_all, right_fraction=0.62,
            )

            left_x = self.written_left_x()
            m1_title = self.safe_text("方法一（补差）：", font_size=22, color=ORANGE)
            m1_a = self.safe_text(
                f"{self.LARGE_NAME}队员：({total}+{diff})÷2={large}（人）",
                font_size=22, color=WHITE,
            )
            m1_b = self.safe_text(
                f"{self.SMALL_NAME}队员：{total}-{large}={small}（人）",
                font_size=22, color=WHITE,
            )
            m2_title = self.safe_text("方法二（去差）：", font_size=22, color=TEAL_D)
            m2_a = self.safe_text(
                f"{self.SMALL_NAME}队员：({total}-{diff})÷2={small}（人）",
                font_size=22, color=WHITE,
            )
            m2_b = self.safe_text(
                f"{self.LARGE_NAME}队员：{total}-{small}={large}（人）",
                font_size=22, color=WHITE,
            )

            formula_rows = VGroup(
                m1_title, m1_a, m1_b, m2_title, m2_a, m2_b,
            ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.75), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [m1_title, m1_a, m1_b]:
                self.play(FadeIn(row), run_time=0.4)
                self.wait(1.0)
            for row in [m2_title, m2_a, m2_b]:
                self.play(FadeIn(row), run_time=0.4)
                self.wait(1.0)

            answer_text = self.safe_text(
                f"答：{self.SMALL_NAME}队员有{small}人，{self.LARGE_NAME}队员有{large}人。",
                font_size=24, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.35)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("（和+差）÷2=较大数，（和−差）÷2=较小数", wait=6)
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
