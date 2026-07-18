"""
第49讲 利润问题 — 画图解题法（线段图法）

母题：200 个本，进价 5 元，按 40% 利润定价；先卖 160 个，余下按定价 60% 卖。
答案：利润 288 元

用法:
  cd manim/scenes/线段图法
  python -m manim problem_49.py Problem49Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem49Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    TOTAL_N = 200
    SOLD_N = 160
    COST = 5
    PROFIT_RATE = 0.40
    DISCOUNT = 0.60

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        tot = self.TOTAL_N
        sold = self.SOLD_N
        cost = self.COST
        rate_pct = int(self.PROFIT_RATE * 100)
        disc_pct = int(self.DISCOUNT * 100)

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
                "利润＝卖出的总钱数－进货总成本，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "分段卖时，先按销量把线段拆开，再分别算售出额！",
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

            feature_title = self.safe_text("分段销售的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先求定价", "进价×(1＋利润率)"),
                ("2", "按销量分段", "正价卖多少、促销卖多少"),
                ("3", "售出额减成本", "两段收入相加再减总成本"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：分段售出求利润"):
            prob_all = self.make_problem_box(
                f"题目：进{tot}个，进价{cost}元，按{rate_pct}%利润定价；先卖{sold}个，",
                f"余下按定价的{disc_pct}%卖。总利润多少元？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.25
        diag = self.make_profit_sale_diagram(
            draw_y,
            total_n=tot,
            sold_n=sold,
            cost=cost,
            profit_rate=self.PROFIT_RATE,
            discount=self.DISCOUNT,
            show_hint=False,
        )
        price = diag["price"]
        remain = diag["remain_n"]
        profit = diag["profit"]

        # ── 图解1：画出总量线段并分段 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出销量分段"):
            s1 = self.step_label("第一步：按销量把全部笔记本分成两段")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(Create(diag["main"]), FadeIn(diag["ticks"]), run_time=0.6)
            self.play(
                diag["sold_bar"].animate.set_opacity(1),
                diag["remain_bar"].animate.set_opacity(1),
                run_time=0.5,
            )
            diag["sold_bar"].set_fill(TEAL_D, opacity=0.30)
            diag["remain_bar"].set_fill(ORANGE, opacity=0.30)
            self.play(
                diag["sold_n_lab"].animate.set_opacity(1),
                diag["remain_n_lab"].animate.set_opacity(1),
                diag["total_n_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"正价卖{sold}个，余下{remain}个促销",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：求出定价 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "求出定价"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["sold_bar"], diag["remain_bar"],
                diag["sold_n_lab"], diag["remain_n_lab"], diag["total_n_lab"],
            )
            s2 = self.step_label("第二步：用进价和利润率求出定价")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["note_price"].animate.set_opacity(1), run_time=0.55)
            self.play(diag["sold_p_lab"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle(
                f"定价 {cost}×(1+{rate_pct}%)={price}（元）",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标促销单价 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出促销单价"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["sold_bar"], diag["remain_bar"],
                diag["sold_n_lab"], diag["remain_n_lab"], diag["total_n_lab"],
                diag["sold_p_lab"], diag["note_price"],
            )
            s3 = self.step_label("第三步：余下部分按定价的折扣标出单价")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["remain_p_lab"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"促销价 = {price}×{disc_pct}%",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求总利润 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出总利润"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["sold_bar"], diag["remain_bar"],
                diag["sold_n_lab"], diag["remain_n_lab"], diag["total_n_lab"],
                diag["sold_p_lab"], diag["remain_p_lab"], diag["note_price"],
            )
            s4 = self.step_label("第四步：两段售出额减去总成本，求出利润")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_profit_q"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.7)
            self.play(
                diag["note_profit_q"].animate.set_opacity(0),
                diag["note_profit_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"总利润是{profit}元",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["main"], diag["ticks"],
            diag["sold_bar"], diag["remain_bar"],
            diag["sold_n_lab"], diag["remain_n_lab"], diag["total_n_lab"],
            diag["sold_p_lab"], diag["remain_p_lab"], diag["notes"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = VGroup(
                self.safe_mathtex(
                    rf"{cost}\times(1+{rate_pct}\%)={price}",
                    font_size=26, color=WHITE,
                ),
                self.safe_text("（元）", font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.08)
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = VGroup(
                self.safe_mathtex(
                    rf"{sold}\times{price}+({tot}-{sold})"
                    rf"\times({price}\times{disc_pct}\%)"
                    rf"-{tot}\times{cost}={profit}",
                    font_size=18, color=WHITE,
                ),
                self.safe_text("（元）", font_size=16, color=WHITE),
            ).arrange(RIGHT, buff=0.08)
            f2.next_to(f1, DOWN, buff=0.32)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            answer_text = self.safe_text(
                f"答：可以获得利润{profit}元。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f2, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.5)
            self.wait(0.8)
            self.play(FadeIn(f2), run_time=0.55)
            self.wait(0.8)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("分段售出额 − 总成本 = 总利润", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(f2), FadeOut(answer_text),
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
