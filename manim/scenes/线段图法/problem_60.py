"""
第60讲 行程综合问题（二）— 画图解题法（线段图法）

母题：甲乙速度比3:5，AB相距400km，往返，求第一、二次相遇点距离。
答案：150；50；400-150-50=200（千米）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_60.py Problem60Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem60Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    DISTANCE = 400
    SPEED_A = 3
    SPEED_B = 5

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        d = self.DISTANCE
        sa, sb = self.SPEED_A, self.SPEED_B

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=30, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.32, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "两车相向往返，会多次相遇，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先数清一共走了几个全程，再按速度比分路程！",
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

            feature_title = self.safe_text("解题的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "数清全程数", "第n次相遇共走n个全程（相向）"),
                ("2", "速度比＝路程比", "时间相同，按份数分路程"),
                ("3", "定位两次相遇", "再求两遇点之间的距离"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求两次相遇点距离"):
            prob_all = self.make_problem_box(
                f"题目：甲乙速度比{sa}:{sb}，AB相距{d}千米，相向往返。",
                "第一、二次相遇点相距多少千米？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.25
        diag = self.make_multi_meet_diagram(
            draw_y,
            distance=d, speed_a=sa, speed_b=sb,
            show_hint=False,
        )
        first = diag["first_from_a"]
        second_b = diag["second_from_b"]
        gap = diag["gap"]

        # ── 图解1：画出AB全程与往返路线 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出AB与往返路线"):
            s1 = self.step_label("第一步：画出A、B两地和两车往返路线")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(
                Create(diag["main"]), FadeIn(diag["ticks"]),
                FadeIn(diag["lab_a"]), FadeIn(diag["lab_b"]),
                run_time=0.6,
            )
            self.play(
                FadeIn(diag["total_brace"]), FadeIn(diag["total_lab"]),
                run_time=0.45,
            )
            self.play(
                Create(diag["path_a"]), Create(diag["path_b"]),
                FadeIn(diag["start_a"]), FadeIn(diag["start_b"]),
                diag["lab_jia"].animate.set_opacity(1),
                diag["lab_yi"].animate.set_opacity(1),
                run_time=0.7,
            )
            self.play(
                FadeIn(diag["arrows"]),
                diag["turn_a_lab"].animate.set_opacity(1),
                diag["turn_b_lab"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle("到达对方出发地后立即折返，箭头表示方向", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出第一次相遇 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出第一次相遇点"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["lab_a"], diag["lab_b"],
                diag["total_brace"], diag["total_lab"],
                diag["path_a"], diag["path_b"],
                diag["start_a"], diag["start_b"],
                diag["arrows"], diag["turn_labs"],
                diag["lab_jia"], diag["lab_yi"],
            )
            s2 = self.step_label("第二步：第一次相遇——共走1个全程")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(Create(diag["v1"]), run_time=0.4)
            self.play(diag["meet1_lab"].animate.set_opacity(1), run_time=0.4)
            self.play(diag["note1"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"甲从A走了{first}千米",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：第二次相遇并求间距 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出两次相遇点距离"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["lab_a"], diag["lab_b"],
                diag["total_brace"], diag["total_lab"],
                diag["path_a"], diag["path_b"],
                diag["start_a"], diag["start_b"],
                diag["arrows"], diag["turn_labs"],
                diag["lab_jia"], diag["lab_yi"],
                diag["v1"], diag["meet1_lab"], diag["note1"],
            )
            s3 = self.step_label("第三步：第二次相遇——共走3个全程，求间距")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(Create(diag["v2"]), run_time=0.4)
            self.play(diag["meet2_lab"].animate.set_opacity(1), run_time=0.4)
            self.play(diag["note2"].animate.set_opacity(1), run_time=0.5)
            self.play(
                FadeIn(diag["gap_brace"]),
                diag["gap_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(diag["note3"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"两次相遇点相距{gap}千米",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s3), run_time=0.3)

        diagram_all = VGroup(
            diag["main"], diag["ticks"],
            diag["lab_a"], diag["lab_b"],
            diag["total_brace"], diag["total_lab"],
            diag["path_a"], diag["path_b"],
            diag["start_a"], diag["start_b"],
            diag["arrows"], diag["turn_labs"],
            diag["lab_jia"], diag["lab_yi"],
            diag["v1"], diag["v2"],
            diag["meet1_lab"], diag["meet2_lab"],
            diag["gap_brace"], diag["gap_lab"],
            diag["note1"], diag["note2"], diag["note3"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/06.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                self.safe_text(
                    f"{d}×{sa}/({sa}+{sb})={first}（千米）",
                    font_size=18, color=WHITE,
                ),
                self.safe_text(
                    f"3×{d}×{sa}/({sa}+{sb})-{d}={second_b}（千米）",
                    font_size=17, color=WHITE,
                ),
                self.safe_text(
                    f"{d}-{first}-{second_b}={gap}（千米）",
                    font_size=18, color=WHITE,
                ),
            ]
            prev = None
            for i, line in enumerate(lines):
                if i == 0:
                    line.move_to(np.array([
                        left_x + line.width / 2,
                        self.written_left_y(0.75), 0,
                    ]))
                else:
                    line.next_to(prev, DOWN, buff=0.24)
                line.align_to(np.array([left_x, 0, 0]), LEFT)
                self.clamp_content(line)
                prev = line

            answer_text = self.safe_text(
                f"答：两车第一次与第二次相遇点相距{gap}千米。",
                font_size=17, color=YELLOW,
            )
            answer_text.next_to(lines[-1], DOWN, buff=0.30)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.10, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            for line in lines:
                self.play(FadeIn(line), run_time=0.4)
                self.wait(0.4)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.55)
            self.play(Create(highlight_box), run_time=0.4)
            self.safe_subtitle("关键：先确定一共走了几个全程", wait=5)
            self.wait(2)
            self.play(
                *[FadeOut(line) for line in lines],
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
