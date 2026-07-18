"""
第55讲 发车问题 — 画图解题法（线段图法）

母题：乐乐 2 米/秒骑行，迎面公交 10 米/秒、每 5 分钟发一辆。求相遇间隔。
答案：300×10=3000，3000÷(10+2)=250（秒）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_55.py Problem55Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem55Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    PERSON_SPEED = 2
    BUS_SPEED = 10
    DISPATCH_MIN = 5

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        ps = self.PERSON_SPEED
        bs = self.BUS_SPEED
        dm = self.DISPATCH_MIN

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
                "路上不断迎面遇到按固定间隔发出的车，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先求相邻车距，再当成相遇问题来算！",
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
                ("1", "统一时间单位", "分钟先换成秒，再算车距"),
                ("2", "求出相邻车距", "发车间隔 × 车速"),
                ("3", "转化成相遇", "车距 ÷ (人速＋车速)"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求人车相遇间隔"):
            prob_all = self.make_problem_box(
                f"题目：乐乐{ps}米/秒，迎面公交{bs}米/秒，每{dm}分钟发一辆。",
                "乐乐每隔多少秒与公交车相遇一次？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.12
        diag = self.make_bus_dispatch_diagram(
            draw_y,
            person_speed=ps,
            bus_speed=bs,
            dispatch_min=dm,
            show_hint=False,
        )
        dispatch_sec = diag["dispatch_sec"]
        spacing = diag["spacing"]
        meet_sec = diag["meet_sec"]

        # ── 图解1：画出等距公交车 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出等距公交车"):
            s1 = self.step_label("第一步：画出路上等距行驶的公交车")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(Create(diag["road"]), run_time=0.4)
            self.play(
                FadeIn(diag["bus_icons"]),
                diag["bus_labs"].animate.set_opacity(1),
                run_time=0.6,
            )
            self.play(
                diag["gap1_block"].animate.set_opacity(1),
                diag["gap2_block"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                "相遇路程就是公交车1到公交车2这一段",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：转化为相遇模型 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "转化为相遇模型"):
            self.add(
                prob_all, diag["road"], diag["bus_icons"], diag["bus_labs"],
                diag["gap1_block"], diag["gap2_block"],
            )
            s2 = self.step_label("第二步：乐乐与下一辆车相向而行")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["guides"].animate.set_opacity(1), run_time=0.45)
            self.play(
                Create(diag["meet_line"]), FadeIn(diag["meet_ticks"]),
                run_time=0.45,
            )
            self.play(
                GrowArrow(diag["arrow_person"]),
                GrowArrow(diag["arrow_bus"]),
                diag["person_lab"].animate.set_opacity(1),
                diag["bus2_lab"].animate.set_opacity(1),
                run_time=0.6,
            )
            self.play(diag["meet_tag"].animate.set_opacity(1), run_time=0.35)
            self.safe_subtitle(
                "从遇公交车1到遇公交车2，就是一次相遇",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：求出车距 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出相邻车距"):
            self.add(
                prob_all, diag["road"], diag["bus_icons"], diag["bus_labs"],
                diag["gap1_block"], diag["gap2_block"], diag["guides"],
                diag["meet_line"], diag["meet_ticks"],
                diag["arrow_person"], diag["arrow_bus"],
                diag["person_lab"], diag["bus2_lab"], diag["meet_tag"],
            )
            s3 = self.step_label("第三步：发车间隔×车速，求出相邻车距")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_time"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.4)
            self.play(diag["note_space"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                "发车间隔×车速＝相邻车距",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出相遇间隔 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出相遇时间间隔"):
            self.add(
                prob_all, diag["road"], diag["bus_icons"], diag["bus_labs"],
                diag["gap1_block"], diag["gap2_block"], diag["guides"],
                diag["meet_line"], diag["meet_ticks"],
                diag["arrow_person"], diag["arrow_bus"],
                diag["person_lab"], diag["bus2_lab"], diag["meet_tag"],
                diag["note_time"], diag["note_space"],
            )
            s4 = self.step_label("第四步：车距÷速度和，求出相遇间隔")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_meet"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                "每隔250秒相遇一次",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        # 含 PNG 图标，须用 Group；算式逐条加入，避免 notes 空壳重影
        diagram_all = Group(
            diag["road"], diag["bus_icons"], diag["bus_labs"],
            diag["gap1_block"], diag["gap2_block"], diag["guides"],
            diag["meet_line"], diag["meet_ticks"],
            diag["arrow_person"], diag["arrow_bus"],
            diag["person_lab"], diag["bus2_lab"], diag["meet_tag"],
            diag["note_time"], diag["note_space"], diag["note_meet"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"{dm}分钟={dispatch_sec}秒",
                font_size=24, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.75), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = self.safe_text(
                f"{dispatch_sec}×{bs}={spacing}（米）",
                font_size=24, color=WHITE,
            )
            f2.next_to(f1, DOWN, buff=0.26)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            f3 = self.safe_text(
                f"{spacing}÷({bs}+{ps})={meet_sec}（秒）",
                font_size=24, color=WHITE,
            )
            f3.next_to(f2, DOWN, buff=0.26)
            f3.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f3)

            answer_text = self.safe_text(
                f"答：乐乐每隔{meet_sec}秒会和公交车相遇一次。",
                font_size=18, color=YELLOW,
            )
            answer_text.next_to(f3, DOWN, buff=0.32)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.45)
            self.wait(0.5)
            self.play(FadeIn(f2), run_time=0.45)
            self.wait(0.5)
            self.play(FadeIn(f3), run_time=0.45)
            self.wait(0.6)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("迎面走 → 相遇问题", wait=5)
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
