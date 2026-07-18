"""
第59讲 扶梯问题 — 画图解题法（线段图法）

母题：哥哥2级/秒用20秒，妹妹1级/秒用30秒，求扶梯静止可见台阶数。
答案：20×(2+x)=30×(1+x) → x=1 → 60级

用法:
  cd manim/scenes/线段图法
  python -m manim problem_59.py Problem59Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem59Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    BRO_WALK = 2
    SIS_WALK = 1
    BRO_TIME = 20
    SIS_TIME = 30

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        bw, sw = self.BRO_WALK, self.SIS_WALK
        bt, st = self.BRO_TIME, self.SIS_TIME

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
                "人和扶梯同向运动，实际速度＝人速＋扶梯速，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用速度线段对齐，再按同程列方程！",
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
                ("1", "速度可相加", "顺向：人速＋扶梯速"),
                ("2", "画出速度段", "扶梯段相同，行走段不同"),
                ("3", "同程列方程", "实际速度×时间相等"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求可见台阶数"):
            prob_all = self.make_problem_box(
                f"题目：哥哥{bw}级/秒用{bt}秒，妹妹{sw}级/秒用{st}秒上楼。",
                "扶梯静止时可见台阶有多少级？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.20
        diag = self.make_escalator_diagram(
            draw_y,
            bro_walk=bw, sis_walk=sw, bro_time=bt, sis_time=st,
            show_hint=False,
        )
        bro, sis = diag["bro"], diag["sis"]
        x_val = diag["esc_speed"]
        steps = diag["steps"]

        # ── 图解1：画出两人上行速度条 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出兄妹上行速度"):
            s1 = self.step_label("第一步：画出哥哥、妹妹的上行速度")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(
                FadeIn(bro["name_lab"]), FadeIn(bro["outline"]),
                FadeIn(bro["esc_bar"]), FadeIn(bro["walk_bar"]),
                run_time=0.55,
            )
            self.play(
                FadeIn(sis["name_lab"]), FadeIn(sis["outline"]),
                FadeIn(sis["esc_bar"]), FadeIn(sis["walk_bar"]),
                run_time=0.55,
            )
            self.play(
                FadeIn(diag["divider"]),
                FadeIn(diag["esc_brace"]),
                diag["esc_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle("左段是扶梯速度，右段是行走速度", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出行走速度与上行速度 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出行走与上行速度"):
            self.add(
                prob_all,
                bro["name_lab"], bro["outline"], bro["esc_bar"], bro["walk_bar"],
                sis["name_lab"], sis["outline"], sis["esc_bar"], sis["walk_bar"],
                diag["divider"], diag["esc_brace"], diag["esc_lab"],
            )
            s2 = self.step_label("第二步：标出各自的行走速度和上行速度")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                diag["bro_walk_lab"].animate.set_opacity(1),
                diag["sis_walk_lab"].animate.set_opacity(1),
                run_time=0.45,
            )
            self.play(
                FadeIn(bro["brace"]), bro["speed_lab"].animate.set_opacity(1),
                FadeIn(sis["brace"]), sis["speed_lab"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"实际速度＝扶梯速＋行走速",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：同程列方程求台阶数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "同程列方程求台阶数"):
            self.add(
                prob_all,
                bro["name_lab"], bro["outline"], bro["esc_bar"], bro["walk_bar"],
                bro["brace"], bro["speed_lab"],
                sis["name_lab"], sis["outline"], sis["esc_bar"], sis["walk_bar"],
                sis["brace"], sis["speed_lab"],
                diag["divider"], diag["esc_brace"], diag["esc_lab"],
                diag["bro_walk_lab"], diag["sis_walk_lab"],
            )
            s3 = self.step_label("第三步：两人上升台阶数相同，列出方程")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_eq"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_x"].animate.set_opacity(1), run_time=0.45)
            self.play(diag["note_ans"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"扶梯静止时可见台阶有{steps}级",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s3), run_time=0.3)

        diagram_all = VGroup(
            bro["name_lab"], bro["outline"], bro["esc_bar"], bro["walk_bar"],
            bro["brace"], bro["speed_lab"],
            sis["name_lab"], sis["outline"], sis["esc_bar"], sis["walk_bar"],
            sis["brace"], sis["speed_lab"],
            diag["divider"], diag["esc_brace"], diag["esc_lab"],
            diag["bro_walk_lab"], diag["sis_walk_lab"],
            diag["note_eq"], diag["note_x"], diag["note_ans"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/06.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            lines = [
                self.safe_text("解：设扶梯的运行速度为x级/秒。", font_size=18, color=WHITE),
                self.safe_text(f"{bt}×({bw}+x)={st}×({sw}+x)", font_size=20, color=WHITE),
                self.safe_text(f"x={x_val}", font_size=20, color=WHITE),
                self.safe_text(
                    f"{bt}×({bw}+{x_val})={steps}（级）",
                    font_size=20, color=WHITE,
                ),
            ]
            prev = None
            for i, line in enumerate(lines):
                if i == 0:
                    line.move_to(np.array([
                        left_x + line.width / 2,
                        self.written_left_y(0.85), 0,
                    ]))
                else:
                    line.next_to(prev, DOWN, buff=0.22)
                line.align_to(np.array([left_x, 0, 0]), LEFT)
                self.clamp_content(line)
                prev = line

            answer_text = self.safe_text(
                f"答：当扶梯静止时，扶梯的可见台阶有{steps}级。",
                font_size=18, color=YELLOW,
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
                self.wait(0.35)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.55)
            self.play(Create(highlight_box), run_time=0.4)
            self.safe_subtitle("关键：台阶数＝时间×（人速＋扶梯速）", wait=5)
            self.wait(2)
            self.play(
                *[FadeOut(line) for line in lines],
                FadeOut(answer_text), FadeOut(highlight_box),
                FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=7,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
