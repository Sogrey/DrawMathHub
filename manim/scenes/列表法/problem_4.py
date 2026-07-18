"""
第4讲 人民币问题 — 画图解题法（列表法）

母题：阳阳有1张20元、3张10元、2张5元，买30元足球不找零，有几种付钱方法？
答案：列表枚举共4种。

用法:
  cd manim/scenes/列表法
  python -m manim problem_4.py Problem4Scene -qh

渲染后:
  python ..\_shared\post_render.py --lesson 4 \\
    --rendered media\videos\problem_4\1080p60\Problem4Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem4Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    COLUMN_HEADERS = ["20元/张", "10元/张", "5元/张"]
    METHODS = [
        {"name": "方法一", "counts": [1, 1, 0], "sum_text": "20+10=30"},
        {"name": "方法二", "counts": [1, 0, 2], "sum_text": "20+5+5=30"},
        {"name": "方法三", "counts": [0, 3, 0], "sum_text": "10+10+10=30"},
        {"name": "方法四", "counts": [0, 2, 2], "sum_text": "10+10+5+5=30"},
    ]

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

            concept_title = self.safe_text("题型识别", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "用不同面值的人民币组合付款，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "在不找零的情况下有几种付法——这就是人民币问题！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("列表法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "看清有哪些面值", "比如：20元、10元、5元各几张"),
                ("2", "用表格有序列举", "从大面值开始，一行一种组合"),
                ("3", "合计等于目标金额", "不找零 = 付的钱正好等于30元"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：找出关键信息"):
            prob_all = self.make_problem_box(
                "题目：阳阳有1张20元的纸币，3张10元的纸币，2张5元的纸币。",
                "阳阳要买一个30元的足球，在不找钱的情况下，他有几种不同的付钱方法？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_rmb_payment_table(
            self.COLUMN_HEADERS, self.METHODS, draw_y,
        )

        # ── 图解1：画表格表头 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "列表格整理钱币信息"):
            s1 = self.step_label("第一步：画表格，列出各面值")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["wallet_hint"]), run_time=0.5)
            self.play(FadeIn(diag["header_row"], shift=DOWN * 0.12), run_time=0.7)
            self.safe_subtitle("表格列出每种面值用几张，最后一列写合计", wait=3)
            self.wait(1)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：方法一、二 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "从20元开始有序列举"):
            self.add(prob_all, diag["wallet_hint"], diag["header_row"])
            s2 = self.step_label("第二步：从面值大的开始列举")
            self.play(FadeIn(s2), run_time=0.5)
            for row_info in diag["data_rows"][:2]:
                self.play(FadeIn(row_info["row"], shift=RIGHT * 0.15), run_time=0.65)
            self.safe_subtitle("先从20元开始：1张20元时，再配10元或5元凑30元", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：方法三、四 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "继续列举其余组合"):
            self.add(prob_all, diag["wallet_hint"], diag["header_row"])
            for row_info in diag["data_rows"][:2]:
                self.add(row_info["row"])
            s3 = self.step_label("第三步：继续列举，不重不漏")
            self.play(FadeIn(s3), run_time=0.5)
            for row_info in diag["data_rows"][2:]:
                self.play(FadeIn(row_info["row"], shift=RIGHT * 0.15), run_time=0.65)
            self.safe_subtitle("不用20元时，用10元和5元凑30元", wait=4)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：统计几种 ──
        count_label = None
        with self.segment("draw-4", "4", "segments/06.mp4", "合计等于30元的有几种"):
            self.add(prob_all, diag["diagram"])
            s4 = self.step_label("第四步：合计等于30元的有几种")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(
                *[
                    row_info["total_cell"]["label"].animate.set_color(YELLOW)
                    for row_info in diag["data_rows"]
                ],
                run_time=0.6,
            )
            count_label = self.safe_text(
                f"共 {len(self.METHODS)} 种付钱方法", font_size=24, color=YELLOW,
            )
            count_label.next_to(diag["table"], DOWN, buff=0.22)
            self.clamp_content(count_label)
            self.play(FadeIn(count_label), run_time=0.5)
            self.safe_subtitle("合计正好30元的行，数一数共有几种", wait=4)
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(diag["diagram"])
        if count_label is not None:
            diagram_all.add(count_label)

        # ── 书面答题 ──
        left_x = self.written_left_x()
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列举四种方法"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            answer_lines = [
                "方法一：付1张20元和1张10元的纸币；",
                "方法二：付1张20元和2张5元的纸币；",
                "方法三：付3张10元的纸币；",
                "方法四：付2张10元和2张5元的纸币。",
            ]
            answer_group = VGroup(*[
                self.safe_text(line, font_size=24, color=WHITE) for line in answer_lines
            ]).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            answer_group.move_to(np.array([
                left_x + answer_group.width / 2,
                self.written_left_y(0.35), 0,
            ]))
            answer_group.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_group)

            for line in answer_group:
                self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.45)
                self.wait(1.2)

            final_answer = self.safe_text(
                "答：他有4种不同的付钱方法。", font_size=32, color=YELLOW,
            )
            final_answer.next_to(answer_group, DOWN, buff=0.55)
            final_answer.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(final_answer)
            highlight_box = SurroundingRectangle(final_answer, color=RED, buff=0.12, corner_radius=0.1)
            self.play(FadeIn(final_answer, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("列表法：从大面值开始有序列举，做到不重不漏", wait=5)
            self.wait(2)
            self.play(
                FadeOut(answer_group), FadeOut(final_answer),
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
