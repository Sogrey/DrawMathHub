"""
第57讲 工程问题（二）— 画图解题法（线段图法）

母题：甲10天、乙15天、丙20天；三队同做，甲中途撤走，共6天完工。求甲实际几天。
答案：[1−(1/15+1/20)×6]÷1/10=3（天）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_57.py Problem57Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem57Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    A_DAYS = 10
    B_DAYS = 15
    C_DAYS = 20
    TOTAL_DAYS = 6

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        ad = self.A_DAYS
        bd = self.B_DAYS
        cd = self.C_DAYS
        td = self.TOTAL_DAYS

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
                "有人中途撤出时，先找谁从头干到了尾，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用总量1减去全程队的工作量，就是撤出队做的！",
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
                ("1", "总量看作1", "各队效率＝1÷单独天数"),
                ("2", "谁全程谁先算", "乙丙干满总天数"),
                ("3", "余量÷甲效", "求出甲实际工作天数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求甲实际天数"):
            prob_all = self.make_problem_box(
                f"题目：甲{ad}天、乙{bd}天、丙{cd}天；三队同做，甲中途撤走，共{td}天完工。",
                "甲队实际工作了多少天？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.28
        diag = self.make_work_leave_diagram(
            draw_y,
            a_days=ad, b_days=bd, c_days=cd, total_days=td,
            show_hint=False,
        )
        a_worked = diag["a_worked"]

        # ── 图解1：画出总量1 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出工作总量1"):
            s1 = self.step_label("第一步：设工作总量为1，画出全程")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(Create(diag["main"]), FadeIn(diag["ticks"]), run_time=0.55)
            self.play(
                FadeIn(diag["total_brace"]),
                diag["total_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle("工作总量看作单位1", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出乙丙全程段 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出乙丙全程工作量"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["total_brace"], diag["total_lab"],
            )
            s2 = self.step_label(f"第二步：乙、丙从头干到尾，共{td}天")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["bc_bar"].animate.set_opacity(1), run_time=0.45)
            diag["bc_bar"].set_fill(TEAL_D, opacity=0.30)
            self.play(
                FadeIn(diag["bc_brace"]),
                diag["bc_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(diag["note_bc"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle(
                f"乙丙完成：(1/{bd}+1/{cd})×{td}",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标出甲的工作量并求天数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出甲实际工作天数"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["total_brace"], diag["total_lab"],
                diag["bc_bar"], diag["bc_brace"], diag["bc_lab"],
                diag["note_bc"],
            )
            s3 = self.step_label("第三步：余下是甲做的，÷甲效得天数")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["a_bar"].animate.set_opacity(1), run_time=0.45)
            diag["a_bar"].set_fill(ORANGE, opacity=0.30)
            self.play(
                FadeIn(diag["a_brace"]),
                diag["a_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(diag["note_a"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"甲队实际工作了{a_worked}天",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s3), run_time=0.3)

        diagram_all = VGroup(
            diag["main"], diag["ticks"],
            diag["bc_bar"], diag["a_bar"],
            diag["total_brace"], diag["total_lab"],
            diag["bc_brace"], diag["bc_lab"],
            diag["a_brace"], diag["a_lab"],
            diag["note_bc"], diag["note_a"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/06.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"[1−(1/{bd}+1/{cd})×{td}]÷1/{ad}={a_worked}（天）",
                font_size=22, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.70), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            answer_text = self.safe_text(
                f"答：甲队实际工作了{a_worked}天。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f1, DOWN, buff=0.34)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.5)
            self.wait(0.8)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("关键：乙、丙从头干到了尾", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1),
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
