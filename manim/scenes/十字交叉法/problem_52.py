"""
第52讲 浓度问题 — 画图解题法（十字交叉法）

母题：20% 与 5% 盐水混合成 15% 盐水 600 克，求各需多少克。
答案：20% 需 400 克，5% 需 200 克。

用法:
  cd manim/scenes/十字交叉法
  python -m manim problem_52.py Problem52Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem52Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    HIGH = 0.20
    LOW = 0.05
    MIX = 0.15
    TOTAL = 600

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        high_pct = int(round(self.HIGH * 100))
        low_pct = int(round(self.LOW * 100))
        mix_pct = int(round(self.MIX * 100))
        total = self.TOTAL

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
                "两种不同浓度的溶液混合，配成新浓度的溶液，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用十字交叉找出两种溶液的质量比，再按总量分配！",
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

            feature_title = self.safe_text("十字交叉法的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "标出三种浓度", "两种原液 + 混合后的目标浓度"),
                ("2", "交叉求差值", "差值之比就是质量之比"),
                ("3", "按比分配总量", "求出两种溶液各需多少克"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求两种盐水用量"):
            prob_all = self.make_problem_box(
                f"题目：{high_pct}%与{low_pct}%盐水混合成{mix_pct}%盐水{total}克。",
                f"各需多少克？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.20
        diag = self.make_concentration_cross_diagram(
            draw_y,
            high=self.HIGH,
            low=self.LOW,
            mix=self.MIX,
            total=total,
            show_hint=False,
        )
        high_amt = diag["high_amt"]
        low_amt = diag["low_amt"]
        high_ratio = diag["high_ratio"]
        low_ratio = diag["low_ratio"]
        high_parts = diag["high_parts_pct"]
        low_parts = diag["low_parts_pct"]

        # ── 图解1：标出三种浓度 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "标出三种浓度"):
            s1 = self.step_label("第一步：标出两种原液浓度和混合浓度")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(
                diag["high_lab"].animate.set_opacity(1),
                diag["low_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(
                diag["mix_dot"].animate.set_opacity(1),
                diag["mix_lab"].animate.set_opacity(1),
                run_time=0.45,
            )
            self.safe_subtitle(
                f"左上{high_pct}%、左下{low_pct}%、中间混合{mix_pct}%",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：画出十字交叉 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "画出十字交叉"):
            self.add(
                prob_all,
                diag["high_lab"], diag["low_lab"],
                diag["mix_dot"], diag["mix_lab"],
            )
            s2 = self.step_label("第二步：画出十字交叉线，求出浓度差")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                diag["line_high"].animate.set_opacity(1),
                diag["line_low"].animate.set_opacity(1),
                run_time=0.7,
            )
            self.play(
                diag["diff_high"].animate.set_opacity(1),
                diag["diff_low"].animate.set_opacity(1),
                run_time=0.6,
            )
            self.safe_subtitle(
                f"交叉得 {high_parts}% 与 {low_parts}%",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：写出质量比 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "写出质量比"):
            self.add(
                prob_all,
                diag["high_lab"], diag["low_lab"],
                diag["mix_dot"], diag["mix_lab"],
                diag["line_high"], diag["line_low"],
                diag["diff_high"], diag["diff_low"],
            )
            s3 = self.step_label("第三步：浓度差之比就是质量之比")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_ratio_q"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.5)
            self.play(diag["note_ratio_ans"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle(
                f"{high_pct}%∶{low_pct}%＝{high_parts}%∶{low_parts}%＝{high_ratio}∶{low_ratio}",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：按比分配总量 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "按比分配总量"):
            self.add(
                prob_all,
                diag["high_lab"], diag["low_lab"],
                diag["mix_dot"], diag["mix_lab"],
                diag["line_high"], diag["line_low"],
                diag["diff_high"], diag["diff_low"],
                diag["note_ratio_q"], diag["note_ratio_ans"],
            )
            s4 = self.step_label(f"第四步：按 {high_ratio}∶{low_ratio} 分配 {total} 克")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_calc_high"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.4)
            self.play(diag["note_calc_low"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"{high_pct}%需{high_amt}克，{low_pct}%需{low_amt}克",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["line_high"], diag["line_low"],
            diag["mix_dot"], diag["mix_lab"],
            diag["high_lab"], diag["low_lab"],
            diag["diff_high"], diag["diff_low"],
            diag["notes"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"({mix_pct}%-{low_pct}%)/({high_pct}%-{mix_pct}%)={high_ratio}/{low_ratio}",
                font_size=22, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.75), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = self.safe_text(
                f"{total}×{high_ratio}/({high_ratio}+{low_ratio})={high_amt}（克）",
                font_size=22, color=TEAL_D,
            )
            f2.next_to(f1, DOWN, buff=0.28)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            f3 = self.safe_text(
                f"{total}×{low_ratio}/({high_ratio}+{low_ratio})={low_amt}（克）",
                font_size=22, color=ORANGE,
            )
            f3.next_to(f2, DOWN, buff=0.24)
            f3.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f3)

            answer_text = self.safe_text(
                f"答：需{high_pct}%盐水{high_amt}克，{low_pct}%盐水{low_amt}克。",
                font_size=20, color=YELLOW,
            )
            answer_text.next_to(f3, DOWN, buff=0.32)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.5)
            self.wait(0.6)
            self.play(FadeIn(f2), run_time=0.45)
            self.wait(0.5)
            self.play(FadeIn(f3), run_time=0.45)
            self.wait(0.6)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("交叉差之比＝质量比", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(f2), FadeOut(f3),
                FadeOut(answer_text), FadeOut(highlight_box),
                FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
