"""
第19讲 年龄问题（一） — 画图解题法（线段图法）

母题：小明今年12岁，爷爷今年66岁，几年后爷爷是小明的4倍？
答案：66−12=54，54÷(4−1)=18，18−12=6（年）

图解复用差倍线段：1 倍（小明）+ 4 倍（爷爷），差 54 岁不变。

用法:
  cd manim/scenes/线段图法
  python -m manim problem_19.py Problem19Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem19Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    YOUNG_AGE = 12
    OLD_AGE = 66
    MULTIPLE = 4
    YOUNG_NAME = "小明"
    OLD_NAME = "爷爷"

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        young = self.YOUNG_AGE
        old = self.OLD_AGE
        mult = self.MULTIPLE
        age_diff = old - young
        parts = mult - 1
        future_young = age_diff // parts
        years = future_young - young

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
                "已知两人今年的年龄，求几年前或几年后",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "他们的年龄满足某种倍数关系——这就是年龄问题！",
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

            feature_title = self.safe_text("年龄问题的三个关键", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "年龄差永远不变", "不论过几年，大的总比小的大那么多"),
                ("2", "按将来倍数画线段", "较小年龄当作 1 倍，较大年龄画成几倍"),
                ("3", "差 ÷（倍数−1）", "得到将来的 1 倍年龄，再减今年求年数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：今年年龄与将来倍数"):
            prob_all = self.make_problem_box(
                f"题目：{self.YOUNG_NAME}今年{young}岁，{self.OLD_NAME}今年{old}岁，",
                f"几年后{self.OLD_NAME}的年龄是{self.YOUNG_NAME}的{mult}倍？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_diff_times_diagram(
            draw_y,
            difference=age_diff,
            multiple=mult,
            top_name=self.YOUNG_NAME,
            bottom_name=self.OLD_NAME,
            unit_label="岁",
            show_hint=True,
            hint_text="不管过几年，年龄差始终不变",
            unit_w=0.70,
        )

        # ── 图解1：先求年龄差 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "先求年龄差"):
            s1 = self.step_label("第一步：先算出两人的年龄差")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.4)

            diff_eq = self.safe_text(
                f"{old}−{young}={age_diff}（岁）",
                font_size=32, color=YELLOW,
            )
            diff_note = self.safe_text(
                "这个差，过几年也不会变！",
                font_size=24, color=ORANGE,
            )
            diff_block = VGroup(diff_eq, diff_note).arrange(DOWN, buff=0.35)
            diff_block.move_to(np.array([0, draw_y + 0.15, 0]))
            self.clamp_content(diff_block)
            self.play(FadeIn(diff_eq), run_time=0.6)
            self.wait(1)
            self.play(FadeIn(diff_note), run_time=0.5)
            self.safe_subtitle(
                f"{self.OLD_NAME}总比{self.YOUNG_NAME}大 {age_diff} 岁",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(diff_block), FadeOut(s1), run_time=0.4)

        # ── 图解2：画小明 1 倍（若干年后）──
        with self.segment("draw-2", "2", "segments/04.mp4", "画1倍量"):
            self.add(prob_all, diag["hint"])
            s2 = self.step_label(
                f"第二步：把若干年后{self.YOUNG_NAME}的年龄当作 1 倍"
            )
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["align_l"]), run_time=0.35)
            self.play(Create(diag["top_line"]), FadeIn(diag["top_name"]), run_time=0.55)
            self.play(FadeIn(diag["top_brace"]), FadeIn(diag["top_mult"]), run_time=0.45)
            self.safe_subtitle(
                f"将来{self.YOUNG_NAME}的年龄画成 1 段",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：画爷爷 4 倍 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "画多倍量"):
            self.add(
                prob_all, diag["hint"], diag["align_l"],
                diag["top_block"],
            )
            s3 = self.step_label(
                f"第三步：{self.OLD_NAME}若干年后画成 {mult} 倍"
            )
            self.play(FadeIn(s3), run_time=0.5)
            self.play(Create(diag["bot_line"]), FadeIn(diag["bot_name"]), run_time=0.55)
            if len(diag["bot_ticks"]) > 0:
                self.play(FadeIn(diag["bot_ticks"]), run_time=0.4)
            self.play(FadeIn(diag["bot_brace"]), FadeIn(diag["bot_mult"]), run_time=0.45)
            self.play(FadeIn(diag["align_mid"]), run_time=0.4)
            self.safe_subtitle(
                f"那时{self.OLD_NAME}是{self.YOUNG_NAME}的 {mult} 倍，画成 {mult} 段",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：标出年龄差 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "标年龄差"):
            self.add(
                prob_all, diag["hint"], diag["align"],
                diag["top_block"], diag["bot_block"],
            )
            s4 = self.step_label("第四步：把不变的年龄差标在图上")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(FadeIn(diag["diff_block"]), run_time=0.6)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["parts_note"]), run_time=0.55)
            self.safe_subtitle(
                f"差 {age_diff} 岁相当于 {parts} 个 1 倍量 → "
                f"{age_diff}÷{parts}={future_young}（岁）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["align"], diag["top_block"], diag["bot_block"],
            diag["diff_block"], diag["parts_note"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式求年数"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{old}−{young}={age_diff}（岁）",
                font_size=26, color=WHITE,
            )
            step1_note = self.safe_text("（年龄差）", font_size=20, color=GREY_B)
            step1_row = VGroup(step1, step1_note).arrange(RIGHT, buff=0.16)

            step2 = self.safe_text(
                f"{age_diff}÷（{mult}−1）={future_young}（岁）",
                font_size=26, color=WHITE,
            )
            step2_note = self.safe_text(
                f"（将来{self.YOUNG_NAME}）",
                font_size=20, color=TEAL_D,
            )
            step2_row = VGroup(step2, step2_note).arrange(RIGHT, buff=0.16)

            step3 = self.safe_text(
                f"{future_young}−{young}={years}（年）",
                font_size=26, color=WHITE,
            )
            step3_note = self.safe_text("（过了几年）", font_size=20, color=ORANGE)
            step3_row = VGroup(step3, step3_note).arrange(RIGHT, buff=0.16)

            formula_rows = VGroup(step1_row, step2_row, step3_row).arrange(
                DOWN, buff=0.28, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1_row, step2_row, step3_row]:
                self.play(FadeIn(row), run_time=0.5)
                self.wait(1.3)

            answer_text = self.safe_text(
                f"答：{years}年后{self.OLD_NAME}的年龄是{self.YOUNG_NAME}的{mult}倍。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.48)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("年龄差永远不变，用差倍思路求将来 1 倍年龄", wait=5)
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
