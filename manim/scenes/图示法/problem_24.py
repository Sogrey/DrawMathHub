"""
第24讲 方阵问题 — 画图解题法（图示法）

母题：单层空心方阵每边 9 人，共多少人？
答案：方法一 9×4−4=32；方法二 (9−1)×4=32

用法:
  cd manim/scenes/图示法
  python -m manim problem_24.py Problem24Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem24Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    SIDE_N = 9

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        side_n = self.SIDE_N
        total = (side_n - 1) * 4

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是方阵问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "把人排成空心或实心的正方形队伍，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "根据每边人数求总人数——这就是方阵问题！",
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

            feature_title = self.safe_text("单层空心方阵的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "只有最外圈有人", "中间是空的，只算外框"),
                ("2", "四个角易重复计", "每边×4 后要减掉 4 个角"),
                ("3", "也可每边少算 1 人", "(每边人数−1)×4，角不重复"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：单层空心方阵"):
            prob_all = self.make_problem_box(
                f"题目：学生们排成单层空心方阵，每条边有{side_n}人。",
                "这个空心方阵一共有多少人？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_hollow_square_diagram(
            draw_y,
            side_n=side_n,
            show_hint=True,
        )

        # ── 图解1：画出空心方阵 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出空心方阵"):
            s1 = self.step_label("第一步：用圆画出单层空心方阵")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.35)
            # 按边依次淡入，节奏更清晰
            n = side_n
            i_right0 = n
            i_bottom0 = n + (n - 2)
            i_left0 = i_bottom0 + n
            edges = [
                diag["circles"][0:n],
                diag["circles"][i_right0:i_bottom0],
                diag["circles"][i_bottom0:i_left0],
                diag["circles"][i_left0:],
            ]
            for edge in edges:
                self.play(FadeIn(edge, lag_ratio=0.05), run_time=0.55)
            self.play(FadeIn(diag["side_label"]), run_time=0.4)
            self.safe_subtitle(f"每条边 {side_n} 人，四个角上的人属于两条边", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：方法一（四角重复减 4）──
        with self.segment("draw-2", "2", "segments/04.mp4", "方法一：四角减重复"):
            self.add(prob_all, diag["hint"], diag["circles"], diag["side_label"])
            s2 = self.step_label("第二步：方法一 — 每边×4 再减去 4 个角")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                diag["edge_circles"].animate.set_color(ORANGE).set_fill(ORANGE, opacity=0.25),
                run_time=0.6,
            )
            self.play(
                diag["corner_circles"].animate.set_color(BLUE_C).set_fill(BLUE_C, opacity=0.45),
                run_time=0.7,
            )
            self.play(diag["m1_note"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"按 {side_n}×4 算，四个角各多算 1 次，要再减去 4",
                wait=5,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：方法二（每边 n−1）──
        with self.segment("draw-3", "3", "segments/05.mp4", "方法二：每边少算1人"):
            self.add(
                prob_all, diag["hint"], diag["circles"], diag["side_label"],
                diag["m1_note"], diag["side_brackets"],
            )
            s3 = self.step_label("第三步：方法二 — 每边看成 (人数−1)")
            self.play(FadeIn(s3), run_time=0.5)
            # 复位颜色后按边上色
            self.play(
                diag["circles"].animate.set_color(WHITE).set_fill(WHITE, opacity=0.08),
                run_time=0.45,
            )
            self.play(diag["side_label"].animate.set_opacity(0.35), run_time=0.3)
            anims = []
            for grp, color in zip(diag["side_groups"], diag["side_colors"]):
                anims.append(grp.animate.set_color(color).set_fill(color, opacity=0.28))
            self.play(*anims, run_time=0.8)
            self.play(diag["side_brackets"].animate.set_opacity(1), run_time=0.55)
            self.play(diag["m2_note"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"每边取 {side_n}−1={side_n - 1} 人，再×4，角上的人就不会重复",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：两种结果对照 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "两种算法得同解"):
            self.add(
                prob_all, diag["hint"], diag["circles"],
                diag["side_label"], diag["side_brackets"],
                diag["m1_note"], diag["m2_note"],
            )
            s4 = self.step_label("第四步：两种算法结果相同")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            total_label = self.safe_text(
                f"一共 {total} 人",
                font_size=28, color=YELLOW,
            )
            total_label.next_to(diag["m2_note"], DOWN, buff=0.22)
            # 并入 diagram 组，避免后续平移错位
            diag["layout_row"].add(total_label)
            diag["total_label"] = total_label
            self.play(FadeIn(total_label, shift=UP * 0.1), run_time=0.55)
            self.safe_subtitle(
                f"{side_n}×4−4 = ({side_n}−1)×4 = {total}（人）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["circles"], diag["side_brackets"],
            diag["side_label"], diag["m1_note"], diag["m2_note"],
            diag["total_label"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"方法一：{side_n}×4−4={total}（人）",
                font_size=26, color=WHITE,
            )
            step2 = self.safe_text(
                f"方法二：({side_n}−1)×4={total}（人）",
                font_size=26, color=WHITE,
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
                self.wait(1.3)

            answer_text = self.safe_text(
                f"答：这个空心方阵一共有{total}人。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.48)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("每边×4−4，或 (每边−1)×4，两种算法殊途同归", wait=5)
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
