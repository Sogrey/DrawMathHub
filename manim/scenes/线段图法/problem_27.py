"""
第27讲 相遇问题 — 画图解题法（线段图法）

母题：小星 60 米/分，小明 64 米/分，相向 5 分钟相遇，两家相距？
答案：60×5+64×5=620，或 (60+64)×5=620

用法:
  cd manim/scenes/线段图法
  python -m manim problem_27.py Problem27Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem27Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    LEFT_SPEED = 60
    RIGHT_SPEED = 64
    MEET_TIME = 5

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        v1 = self.LEFT_SPEED
        v2 = self.RIGHT_SPEED
        t = self.MEET_TIME
        d1 = v1 * t
        d2 = v2 * t
        total = d1 + d2

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
                "两人（或两车）从两地同时相向而行，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "经过一段时间后相遇——这就是相遇问题！",
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

            feature_title = self.safe_text("相遇问题的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "相向而行", "两人走的方向相对，越走越近"),
                ("2", "路程相加", "两家距离 = 两人各自路程之和"),
                ("3", "速度和 × 时间", "也可先加速度，再乘相遇时间"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：相向相遇"):
            prob_all = self.make_problem_box(
                f"题目：小星每分钟走{v1}米，小明每分钟走{v2}米。两人同时从家出发，",
                f"相向而行，经过{t}分钟相遇。两家相距多少米？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_meeting_diagram(
            draw_y,
            left_speed=v1,
            right_speed=v2,
            meet_time=t,
            show_hint=True,
        )

        # ── 图解1：画两家与线段 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出两家连线"):
            s1 = self.step_label("第一步：画出两家之间的线段")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(Create(diag["main"]), FadeIn(diag["ticks"]), run_time=0.6)
            self.play(FadeIn(diag["homes"]), run_time=0.5)
            self.play(FadeIn(diag["total_block"]), run_time=0.5)
            self.safe_subtitle("整条线段表示两家之间的距离", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标相遇点与两边行程 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标相向而行"):
            self.add(
                prob_all, diag["hint"], diag["line_core"],
                diag["homes"], diag["total_block"],
            )
            s2 = self.step_label("第二步：标出相遇点和两人相向而行")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["meet_block"]), run_time=0.5)
            self.play(
                GrowArrow(diag["left_arrows"][0]),
                GrowArrow(diag["left_arrows"][1]),
                run_time=0.55,
            )
            self.play(FadeIn(diag["left_info"]), run_time=0.4)
            self.play(
                GrowArrow(diag["right_arrows"][0]),
                GrowArrow(diag["right_arrows"][1]),
                run_time=0.55,
            )
            self.play(FadeIn(diag["right_info"]), run_time=0.4)
            self.safe_subtitle(
                f"小星向右走，小明向左走，{t} 分钟后在广场相遇",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：方法一分别求路程再加 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "方法一：路程相加"):
            self.add(
                prob_all, diag["hint"], diag["line_core"],
                diag["homes"], diag["total_block"],
                diag["meet_block"], diag["travel"], diag["notes"],
            )
            s3 = self.step_label("第三步：方法一 — 先求各自路程再相加")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_m1"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"小星 {v1}×{t}={d1} 米，小明 {v2}×{t}={d2} 米，和为 {total} 米",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：方法二速度和×时间 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "方法二：速度和×时间"):
            self.add(
                prob_all, diag["hint"], diag["line_core"],
                diag["homes"], diag["total_block"],
                diag["meet_block"], diag["travel"], diag["notes"],
            )
            s4 = self.step_label("第四步：方法二 — 速度和乘相遇时间")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(diag["note_m2"].animate.set_opacity(1), run_time=0.55)
            self.play(
                diag["total_q"].animate.set_opacity(0),
                diag["total_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"({v1}+{v2})×{t}={total}（米）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["line_core"], diag["homes"], diag["meet_block"],
            diag["travel"], diag["total_block"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"方法一：{v1}×{t}+{v2}×{t}={total}（米）",
                font_size=24, color=WHITE,
            )
            step2 = self.safe_text(
                f"方法二：({v1}+{v2})×{t}={total}（米）",
                font_size=24, color=WHITE,
            )
            formula_rows = VGroup(step1, step2).arrange(
                DOWN, buff=0.32, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1, step2]:
                self.play(FadeIn(row), run_time=0.5)
                self.wait(1.2)

            answer_text = self.safe_text(
                f"答：小星家和小明家相距{total}米。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.42)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("路程和 = 速度和 × 相遇时间", wait=5)
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
