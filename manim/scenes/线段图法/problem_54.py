"""
第54讲 流水行船问题 — 画图解题法（线段图法）

母题：甲乙河长 168 千米，顺水 6 小时，逆水 8 小时。求船速、水速。
答案：船速 24.5 千米/时，水速 3.5 千米/时。

用法:
  cd manim/scenes/线段图法
  python -m manim problem_54.py Problem54Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem54Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    DISTANCE = 168
    DOWN_HOURS = 6
    UP_HOURS = 8

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        dist = self.DISTANCE
        dh = self.DOWN_HOURS
        uh = self.UP_HOURS

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
                "船在有水流的河里行驶，顺水快、逆水慢，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先画出顺水、逆水路程，再求船速和水速！",
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
                ("1", "画出同程线段", "顺水、逆水路程相同，用时不同"),
                ("2", "先求顺逆水速", "路程÷时间＝速度"),
                ("3", "再求船速水速", "和差各除以2"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求船速和水速"):
            prob_all = self.make_problem_box(
                f"题目：甲乙相距{dist}千米，顺水{dh}小时，逆水{uh}小时。",
                "求船速和水速各是多少？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.22
        diag = self.make_boat_current_diagram(
            draw_y,
            distance=dist,
            down_hours=dh,
            up_hours=uh,
            show_hint=False,
        )
        down = diag["down"]
        up = diag["up"]
        down_s = diag["down_s"]
        up_s = diag["up_s"]
        boat_s = diag["boat_s"]
        water_s = diag["water_s"]

        # ── 图解1：画出顺水、逆水同程 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出顺水与逆水路程"):
            s1 = self.step_label("第一步：画出顺水、逆水两条同程线段")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(
                diag["title_down"].animate.set_opacity(1),
                Create(down["main"]), FadeIn(down["ticks"]),
                run_time=0.55,
            )
            self.play(
                down["bar"].animate.set_opacity(1),
                down["lab_a"].animate.set_opacity(1),
                down["lab_b"].animate.set_opacity(1),
                run_time=0.4,
            )
            down["bar"].set_fill(TEAL_D, opacity=0.28)
            self.play(
                FadeIn(down["brace"]),
                down["dist_lab"].animate.set_opacity(1),
                run_time=0.4,
            )
            self.play(
                diag["title_up"].animate.set_opacity(1),
                Create(up["main"]), FadeIn(up["ticks"]),
                run_time=0.55,
            )
            self.play(
                up["bar"].animate.set_opacity(1),
                up["lab_a"].animate.set_opacity(1),
                up["lab_b"].animate.set_opacity(1),
                run_time=0.4,
            )
            up["bar"].set_fill(ORANGE, opacity=0.28)
            self.play(
                FadeIn(up["brace"]),
                up["dist_lab"].animate.set_opacity(1),
                run_time=0.4,
            )
            self.safe_subtitle(
                f"甲乙都是 {dist} 千米，路程相同",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出用时 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出顺水逆水用时"):
            self.add(
                prob_all,
                diag["title_down"], down["main"], down["ticks"], down["bar"],
                down["lab_a"], down["lab_b"], down["brace"], down["dist_lab"],
                diag["title_up"], up["main"], up["ticks"], up["bar"],
                up["lab_a"], up["lab_b"], up["brace"], up["dist_lab"],
            )
            s2 = self.step_label(f"第二步：标出顺水{dh}小时、逆水{uh}小时")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                diag["time_down"].animate.set_opacity(1),
                diag["time_up"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                "同程不同时：顺水快、逆水慢",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：求顺水、逆水速度 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出顺水与逆水速度"):
            self.add(
                prob_all,
                diag["title_down"], down["main"], down["ticks"], down["bar"],
                down["lab_a"], down["lab_b"], down["brace"], down["dist_lab"],
                diag["time_down"],
                diag["title_up"], up["main"], up["ticks"], up["bar"],
                up["lab_a"], up["lab_b"], up["brace"], up["dist_lab"],
                diag["time_up"],
            )
            s3 = self.step_label("第三步：路程÷时间，求出顺水、逆水速度")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["speed_down"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.4)
            self.play(diag["speed_up"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"顺水{down_s}，逆水{up_s}（千米/时）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求船速与水速 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出船速与水速"):
            self.add(
                prob_all,
                diag["title_down"], down["main"], down["ticks"], down["bar"],
                down["lab_a"], down["lab_b"], down["brace"], down["dist_lab"],
                diag["time_down"], diag["speed_down"],
                diag["title_up"], up["main"], up["ticks"], up["bar"],
                up["lab_a"], up["lab_b"], up["brace"], up["dist_lab"],
                diag["time_up"], diag["speed_up"],
            )
            s4 = self.step_label("第四步：用和差公式求船速、水速")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_boat"].animate.set_opacity(1), run_time=0.55)
            self.wait(0.5)
            self.play(diag["note_water"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"船速{boat_s}千米/时，水速{water_s}千米/时",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["title_down"], down["main"], down["ticks"], down["bar"],
            down["lab_a"], down["lab_b"], down["brace"], down["dist_lab"],
            diag["time_down"], diag["speed_down"],
            diag["title_up"], up["main"], up["ticks"], up["bar"],
            up["lab_a"], up["lab_b"], up["brace"], up["dist_lab"],
            diag["time_up"], diag["speed_up"],
            diag["notes"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"({dist}÷{dh}+{dist}÷{uh})÷2={boat_s}（千米/时）",
                font_size=20, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.70), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = self.safe_text(
                f"({dist}÷{dh}−{dist}÷{uh})÷2={water_s}（千米/时）",
                font_size=20, color=WHITE,
            )
            f2.next_to(f1, DOWN, buff=0.28)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            answer_text = self.safe_text(
                f"答：船速{boat_s}千米/时，水速{water_s}千米/时。",
                font_size=18, color=YELLOW,
            )
            answer_text.next_to(f2, DOWN, buff=0.32)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.5)
            self.wait(0.7)
            self.play(FadeIn(f2), run_time=0.5)
            self.wait(0.7)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("船速取和、水速取差，再各÷2", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(f2),
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
