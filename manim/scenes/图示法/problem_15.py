"""
第15讲 平均数问题（一） — 画图解题法（图示法）

母题：五个数平均40，前三平均32，后三平均46，求中间数
答案：40×5=200，32×3=96，46×3=138，96+138-200=34

用法:
  cd manim/scenes/图示法
  python -m manim problem_15.py Problem15Scene -ql

渲染后:
  python ..\\_shared\\post_render.py --lesson 15 \\
    --rendered media\\videos\\problem_15\\480p15\\Problem15Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem15Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    COUNT = 5
    TOTAL_AVG = 40
    FRONT_AVG = 32
    BACK_AVG = 46
    FRONT_N = 3
    BACK_N = 3

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        total_sum = self.TOTAL_AVG * self.COUNT
        front_sum = self.FRONT_AVG * self.FRONT_N
        back_sum = self.BACK_AVG * self.BACK_N
        middle = front_sum + back_sum - total_sum

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是平均数问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "已知一组数的平均数，以及其中几段数的平均数，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求某个特定的数——这就是平均数问题！",
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

            feature_title = self.safe_text("图示法解平均数的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先画数的位置", "按从小到大画出每一个数"),
                ("2", "用和代替平均", "平均数×个数 = 这一段的和"),
                ("3", "重叠处多算了", "两段相加再减总和，得中间数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：总平均与前后平均"):
            prob_all = self.make_problem_box(
                "题目：五个数的平均数是40，前三个平均数是32，",
                "后三个平均数是46。最中间的那个数是多少？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_middle_average_diagram(
            draw_y,
            count=self.COUNT,
            total_avg=self.TOTAL_AVG,
            front_avg=self.FRONT_AVG,
            back_avg=self.BACK_AVG,
            front_n=self.FRONT_N,
            back_n=self.BACK_N,
            show_hint=True,
        )

        # ── 图解1：五个圆圈 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出五个数"):
            s1 = self.step_label("第一步：从小到大画出五个数")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.4)
            for c, lab in zip(diag["circles"], diag["labels_g"]):
                self.play(Create(c), FadeIn(lab), run_time=0.28)
            self.safe_subtitle("①②③④⑤表示五个数，③是最中间的数", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：五个数的和 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标五个数的和"):
            self.add(prob_all, diag["row"], diag["hint"])
            s2 = self.step_label("第二步：标出五个数的和")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["total_block"]), run_time=0.65)
            self.safe_subtitle(
                f"总数量=平均数×总份数，{self.TOTAL_AVG}×{self.COUNT}={total_sum}",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：前三、后三的和 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标前三与后三的和"):
            self.add(prob_all, diag["row"], diag["hint"], diag["total_block"])
            s3 = self.step_label("第三步：标出前三个、后三个的和")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["front_block"]), run_time=0.55)
            self.wait(0.4)
            self.play(FadeIn(diag["back_block"]), run_time=0.55)
            self.safe_subtitle(
                f"前三：{self.FRONT_AVG}×{self.FRONT_N}={front_sum}；"
                f"后三：{self.BACK_AVG}×{self.BACK_N}={back_sum}",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：重叠倒推中间数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "重叠处求中间数"):
            self.add(
                prob_all, diag["row"], diag["hint"],
                diag["total_block"], diag["front_block"], diag["back_block"],
            )
            s4 = self.step_label("第四步：中间数被算了两次")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(
                diag["mid_circle"].animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.25),
                FadeIn(diag["mid_ring"]),
                run_time=0.55,
            )
            self.play(FadeIn(diag["mid_note"]), run_time=0.45)
            self.safe_subtitle(
                f"前三+后三多算了中间一次，再减去总和：{front_sum}+{back_sum}-{total_sum}={middle}",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["row"],
            diag["front_block"], diag["back_block"], diag["total_block"],
            diag["mid_ring"], diag["mid_note"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式求中间数"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{self.TOTAL_AVG}×{self.COUNT}={total_sum}",
                font_size=26, color=WHITE,
            )
            step2 = self.safe_text(
                f"{self.FRONT_AVG}×{self.FRONT_N}={front_sum}",
                font_size=26, color=WHITE,
            )
            step3 = self.safe_text(
                f"{self.BACK_AVG}×{self.BACK_N}={back_sum}",
                font_size=26, color=WHITE,
            )
            explain = self.safe_text(
                "前三与后三相加，中间数多算一次，再减总和：",
                font_size=22, color=GREY_B,
            )
            step4 = self.safe_text(
                f"{front_sum}+{back_sum}-{total_sum}={middle}",
                font_size=26, color=WHITE,
            )
            formula_rows = VGroup(step1, step2, step3, explain, step4).arrange(
                DOWN, buff=0.22, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1, step2, step3]:
                self.play(FadeIn(row), run_time=0.45)
                self.wait(0.9)
            self.play(FadeIn(explain), run_time=0.4)
            self.wait(1)
            self.play(FadeIn(step4), run_time=0.5)
            self.wait(1.5)

            answer_text = self.safe_text(
                f"答：最中间的那个数是{middle}。",
                font_size=30, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.50)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("平均数先化成和，重叠相加再减总和", wait=5)
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
