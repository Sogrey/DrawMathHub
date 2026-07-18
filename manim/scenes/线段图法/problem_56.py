"""
第56讲 工程问题（一）— 画图解题法（线段图法）

母题：甲乙合作30天完工；合作6天后乙再做40天完成。求甲单独几天。
答案：(1−1/30×6)÷40=1/50；1÷(1/30−1/50)=75（天）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_56.py Problem56Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem56Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    TOGETHER_DAYS = 30
    JOINTLY_DAYS = 6
    B_ALONE_DAYS = 40

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        td = self.TOGETHER_DAYS
        jd = self.JOINTLY_DAYS
        bd = self.B_ALONE_DAYS

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
                "工作总量、工作效率、工作时间三者互相联系，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "把总量看作1，用线段把合作段和单独段画清楚！",
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
                ("1", "总量看作1", "合作几天能完工→合作效率"),
                ("2", "画出分段工作量", "合作段 + 单独段"),
                ("3", "先求乙效再求甲", "甲效＝合作效−乙效"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求甲单独天数"):
            prob_all = self.make_problem_box(
                f"题目：甲乙合作{td}天完工；合作{jd}天后乙再做{bd}天完成。",
                "甲单独做需要多少天？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.22
        diag = self.make_work_project_diagram(
            draw_y,
            together_days=td,
            jointly_days=jd,
            b_alone_days=bd,
            show_hint=False,
        )
        b_den = diag["b_rate_den"]
        a_days = diag["a_alone_days"]

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

        # ── 图解2：标出合作段 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出甲乙合作段"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["total_brace"], diag["total_lab"],
            )
            s2 = self.step_label(f"第二步：标出甲乙合作{jd}天的工作量")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["joint_bar"].animate.set_opacity(1), run_time=0.45)
            diag["joint_bar"].set_fill(TEAL_D, opacity=0.30)
            self.play(
                FadeIn(diag["joint_brace"]),
                diag["joint_lab"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.play(diag["note_coop"].animate.set_opacity(1), run_time=0.45)
            self.safe_subtitle(
                f"合作效率1/{td}，合作{jd}天做了1/{td}×{jd}",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标出乙单独段并求乙效 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出乙单独段求乙效"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["total_brace"], diag["total_lab"],
                diag["joint_bar"], diag["joint_brace"], diag["joint_lab"],
                diag["note_coop"],
            )
            s3 = self.step_label("第三步：剩下的是乙单独做的，求出乙效")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["alone_bar"].animate.set_opacity(1), run_time=0.45)
            diag["alone_bar"].set_fill(ORANGE, opacity=0.30)
            self.play(diag["alone_lab"].animate.set_opacity(1), run_time=0.4)
            self.play(diag["note_b"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"乙的效率是1/{b_den}",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求甲单独天数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出甲单独天数"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["total_brace"], diag["total_lab"],
                diag["joint_bar"], diag["alone_bar"],
                diag["joint_brace"], diag["joint_lab"], diag["alone_lab"],
                diag["note_coop"], diag["note_b"],
            )
            s4 = self.step_label("第四步：甲效＝合作效−乙效，再求甲单独天数")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_a"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"甲单独需要{a_days}天",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["main"], diag["ticks"],
            diag["joint_bar"], diag["alone_bar"],
            diag["total_brace"], diag["total_lab"],
            diag["joint_brace"], diag["joint_lab"], diag["alone_lab"],
            diag["note_coop"], diag["note_b"], diag["note_a"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"(1−1/{td}×{jd})÷{bd}=1/{b_den}",
                font_size=22, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.70), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = self.safe_text(
                f"1÷(1/{td}−1/{b_den})={a_days}（天）",
                font_size=22, color=WHITE,
            )
            f2.next_to(f1, DOWN, buff=0.28)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            answer_text = self.safe_text(
                f"答：需要{a_days}天完成。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f2, DOWN, buff=0.34)
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
            self.safe_subtitle("关键：先求乙单独做的工作量", wait=5)
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
