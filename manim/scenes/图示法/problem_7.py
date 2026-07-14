"""
第7讲 爬井问题 — 画图解题法（图示法）

母题：7米深井，白天上爬3米，晚上下滑2米，第几天到井口？
答案：7-3=4，3-2=1，4÷1=4，4+1=5（天）

用法:
  cd manim/scenes/图示法
  python -m manim problem_7.py Problem7Scene -qh

渲染后:
  python ..\_shared\post_render.py --lesson 7 \\
    --rendered media\videos\problem_7\1080p60\Problem7Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem7Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    DEPTH = 7
    CLIMB = 3
    SLIDE = 2

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

            concept_title = self.safe_text("什么是爬井问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "蜗牛从井底往井口爬，白天向上、晚上向下滑，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求几天能爬到井口——这就是爬井问题！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("图示法的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "白天向上爬、晚上向下滑", "一天一循环，有上有下"),
                ("2", "完整一天净爬 = 上爬 − 下滑", "比如：3−2=1，每天净向上1米"),
                ("3", "最后一天到井口不再下滑", "这是爬井问题最容易忽略的点"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：7米深井蜗牛爬井"):
            prob_all = self.make_problem_box(
                "题目：一只蜗牛从7米深的井底向上爬，白天向上爬3米，",
                "晚上向下滑2米。它会在第几天爬到井口？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_well_climb_diagram(
            self.DEPTH, self.CLIMB, self.SLIDE, draw_y,
        )
        total_days = diag["total_days"]

        # ── 图解1：画井 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画井并标深度，蜗牛在井底"):
            s1 = self.step_label("第一步：画出井，标出井深，蜗牛从井底出发")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            self.play(FadeIn(diag["well_block"]), run_time=0.9)
            self.safe_subtitle("先画出7米深的井，蜗牛从井底出发", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：一天循环（左侧，全程保留）──
        with self.segment("draw-2", "2", "segments/04.mp4", "示范一天上爬与下滑"):
            self.add(prob_all, diag["hint"], diag["well_block"])
            s2 = self.step_label("第二步：看一天——白天上爬，晚上下滑")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["cycle_block"], shift=RIGHT * 0.12), run_time=0.75)
            self.safe_subtitle(
                f"白天上爬{self.CLIMB}米，晚上滑{self.SLIDE}米，实际每天净向上{diag['net_per_day']}米",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：第1~4天（共用左侧竖轴）──
        with self.segment("draw-3", "3", "segments/05.mp4", "前4天每天净爬1米"):
            self.add(prob_all, diag["hint"], diag["well_block"], diag["cycle_block"])
            s3 = self.step_label("第三步：前4天，每天净向上爬1米")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["days_title"]), run_time=0.35)
            for mark in diag["day_marks"]:
                end_m = mark["end_m"]
                climb_top_m = mark["climb_top_m"]
                self.play(
                    FadeIn(mark["day_title"]),
                    FadeIn(mark["guide_start"]),
                    FadeIn(mark["start_tick"]), FadeIn(mark["start_label"]),
                    run_time=0.25,
                )
                self.play(FadeIn(mark["axis_line"]), FadeIn(mark["guide_climb"]), run_time=0.15)
                self.play(
                    FadeIn(mark["climb_arrow"]),
                    FadeIn(mark["climb_tick"]), FadeIn(mark["climb_label"]),
                    diag["snail"].animate.move_to(self._snail_at_height(diag, climb_top_m)),
                    run_time=0.35,
                )
                self.play(
                    FadeIn(mark["slide_arrow"]),
                    FadeIn(mark["guide_net"]),
                    diag["snail"].animate.move_to(self._snail_at_height(diag, end_m)),
                    run_time=0.35,
                )
                self.play(FadeIn(mark["net_tick"]), FadeIn(mark["label"]), run_time=0.25)
            self.safe_subtitle(
                f"前{diag['pre_days']}天每天净爬{diag['net_per_day']}米，第{diag['pre_days']}天末在{diag['pre_height']}米处",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：第5天到顶 ──
        fc = diag["final_climb"]
        with self.segment("draw-4", "4", "segments/06.mp4", "第5天到井口不再下滑"):
            self.add(
                prob_all, diag["hint"], diag["well_block"],
                diag["cycle_block"], diag["days_title"],
                diag["days_block"],
            )
            s4 = self.step_label("第四步：第5天再爬3米到井口，不再下滑")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(FadeIn(fc["graphics"]), run_time=0.55)
            self.play(
                diag["snail"].animate.move_to(self._snail_at_height(diag, self.DEPTH)),
                run_time=0.85,
            )
            self.play(FadeIn(fc["notes"], shift=RIGHT * 0.1), run_time=0.6)
            self.safe_subtitle("第5天再爬3米就到井口，到顶后不会再下滑", wait=4)
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = Group(diag["layout_row"], diag["hint"])

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                f"{self.DEPTH}-{self.CLIMB}={diag['pre_height']}（米）",
                f"{self.CLIMB}-{self.SLIDE}={diag['net_per_day']}（米）",
                f"{diag['pre_height']}÷{diag['net_per_day']}={diag['pre_days']}（天）",
                f"{diag['pre_days']}+1={total_days}（天）",
            ]
            formula_rows = VGroup(*[
                self.safe_text(line, font_size=26, color=WHITE) for line in lines
            ]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)
            self.play(FadeIn(formula_rows), run_time=0.6)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：它会在第{total_days}天爬到井口。",
                font_size=32, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.55)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(answer_text, color=RED, buff=0.12, corner_radius=0.1)
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("爬井问题：最后一天到井口后不再下滑", wait=5)
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

    def _well_y(self, meters: float, unit_h: float) -> float:
        return meters * unit_h

    def _snail_at_height(self, diag: dict, meters: float) -> np.ndarray:
        """共用竖轴上的蜗牛位置。"""
        floor = diag["well_line"].get_bottom()
        return np.array([
            floor[0] + diag["snail_offset_x"],
            floor[1] + self._well_y(meters, diag["unit_h"]) + 0.05,
            0,
        ])
