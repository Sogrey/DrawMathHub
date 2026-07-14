"""
第2讲 排队问题 — 画图解题法（图示法）

本题演示（母题）：
  一（1）班学生排队测身高，聪聪前面有8人，后面有10人。聪聪这队一共有多少人？
  答案：8+10+1=19（人），聪聪这队一共有19人。

用法:
  cd manim/scenes/图示法
  python -m manim problem_2.py Problem2Scene -qh

渲染后:
  python ../_shared/post_render.py --lesson 2 \\
    --rendered media/videos/problem_2/1080p60/Problem2Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem2Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        front_count, back_count = 8, 10
        center_name = "聪聪"

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是排队问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "排队时以某人为参照，告诉你他前面、后面各有多少人，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "问全队一共几人——这就是排队问题！", font_size=28, color=WHITE,
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
                stroke_width=1.5,
                color=GREY_B,
                stroke_opacity=0.25,
            )

            feature_title = self.safe_text("排队问题的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "以一个人为参照", "比如：聪聪前面几人、后面几人"),
                ("2", "前面、后面的人数都不含自己", "「前面8人」不含聪聪"),
                ("3", "求全队用加法", "前面 + 后面 + 1（自己）"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：找出关键信息"):
            prob_all = self.make_problem_box(
                "题目：一（1）班学生排队测身高，聪聪前面有8人，后面有10人。",
                "聪聪这队一共有多少人？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_queue_total_diagram(front_count, back_count, draw_y)
        diagram_row = diag["row"]

        # ── 图解步骤1：画排队结构 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "用圆圈表示排队的人"):
            s1 = self.step_label("第一步：用圆圈表示排队的人")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            for part in diag["draw_order"]:
                if isinstance(part, Circle):
                    self.play(Create(part), run_time=0.4)
                elif isinstance(part, VGroup) and len(part) > 0 and isinstance(part[0], Dot):
                    self.play(FadeIn(part, scale=0.8), run_time=0.4)
                else:
                    self.play(Create(part), run_time=0.8)
            self.safe_subtitle(
                "1个圆圈代表1人；人数较多时，可以用省略号表示",
                wait=3,
            )
            self.wait(1)
            self.play(FadeOut(s1), run_time=0.3)

        circle_r = diag["circle_r"]
        center_person = diag["center_person"]
        front_ellipsis = diag["front_ellipsis"]
        back_ellipsis = diag["back_ellipsis"]
        front_zone = diag["front_zone_circles"]
        back_zone = diag["back_zone_circles"]

        # ── 图解步骤2：标出聪聪 ──
        center_fill = center_name_mob = None
        with self.segment("draw-2", "2", "segments/04.mp4", f"标出{center_name}的位置"):
            self.add(prob_all, diagram_row)
            s2 = self.step_label(f"第二步：标出{center_name}的位置")
            self.play(FadeIn(s2), run_time=0.5)
            center_fill = Circle(
                radius=circle_r + 0.02, fill_opacity=0.5, fill_color=YELLOW,
                stroke_width=3, stroke_color=YELLOW,
            )
            center_fill.move_to(center_person.get_center())
            center_name_mob = self.safe_text(center_name, font_size=22, color=YELLOW)
            center_name_mob.next_to(center_fill, DOWN, buff=0.15)
            self.play(FadeIn(center_fill), FadeIn(center_name_mob), run_time=0.8)
            self.safe_subtitle(f"{center_name}是我们要参照的那个人", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解步骤3：标出前8、后10 ──
        brace_front = front_label = brace_back = back_label = None
        with self.segment("draw-3", "3", "segments/05.mp4", f"标出前面{front_count}人、后面{back_count}人"):
            self.add(prob_all, diagram_row, center_fill, center_name_mob)
            s3 = self.step_label(f"第三步：标出前面{front_count}人、后面{back_count}人")
            self.play(FadeIn(s3), run_time=0.5)
            brace_front = BraceBetweenPoints(
                diag["front_brace_start"].get_top() + UP * 0.12,
                diag["front_brace_end"].get_top() + UP * 0.12,
                direction=UP,
            ).set_color(TEAL_D)
            front_label = self.safe_text(f"{front_count}人", font_size=22, color=TEAL_D)
            front_label.next_to(brace_front, UP, buff=0.1)
            brace_back = BraceBetweenPoints(
                diag["back_brace_start"].get_top() + UP * 0.12,
                diag["back_brace_end"].get_top() + UP * 0.12,
                direction=UP,
            ).set_color(PURPLE_A)
            back_label = self.safe_text(f"{back_count}人", font_size=22, color=PURPLE_A)
            back_label.next_to(brace_back, UP, buff=0.1)
            self.play(
                FadeIn(brace_front), FadeIn(front_label),
                FadeIn(brace_back), FadeIn(back_label),
                run_time=0.8,
            )
            self.safe_subtitle(
                f"前面{front_count}人、后面{back_count}人，都不含{center_name}自己",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解步骤4：标出全队 ──
        brace_total = total_label = None
        with self.segment("draw-4", "4", "segments/06.mp4", "标出全队总人数"):
            self.add(
                prob_all, diagram_row, center_fill, center_name_mob,
                brace_front, front_label, brace_back, back_label,
            )
            s4 = self.step_label("第四步：标出全队总人数")
            self.play(FadeIn(s4), run_time=0.5)
            brace_total = BraceBetweenPoints(
                diag["total_brace_start"].get_bottom() + DOWN * 0.55,
                diag["total_brace_end"].get_bottom() + DOWN * 0.55,
                direction=DOWN,
            ).set_color(RED)
            total_label = self.safe_text("全队 = ?人", font_size=24, color=RED)
            total_label.next_to(brace_total, DOWN, buff=0.1)
            anims: list = [FadeIn(brace_total), FadeIn(total_label)]
            for c in front_zone:
                anims.insert(0, c.animate.set_color(TEAL_D).set_fill(TEAL_D, opacity=0.2))
            for c in back_zone:
                anims.insert(len(front_zone), c.animate.set_color(PURPLE_A).set_fill(PURPLE_A, opacity=0.2))
            anims.insert(
                len(front_zone) + len(back_zone),
                center_fill.animate.set_fill(YELLOW, opacity=0.6),
            )
            if front_ellipsis is not None:
                anims.append(front_ellipsis.animate.set_color(TEAL_D))
            if back_ellipsis is not None:
                anims.append(back_ellipsis.animate.set_color(PURPLE_A))
            self.play(*anims, run_time=0.6)
            self.safe_subtitle(
                f"要把前面、后面，再加上{center_name}自己，才是全队人数",
                wait=4,
            )
            self.wait(2)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diagram_row,
            center_fill, center_name_mob,
            brace_front, front_label, brace_back, back_label,
            brace_total, total_label,
        )

        # ── 书面答题 ──
        left_x = self.written_left_x()
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：分析、列式与规范作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            ana1 = self.safe_text(f"{center_name}前面有 {front_count} 人", font_size=24, color=WHITE)
            ana2 = self.safe_text(f"{center_name}后面有 {back_count} 人", font_size=24, color=WHITE)
            ana3 = self.safe_text(
                f"还要加上{center_name}自己，才是全队人数", font_size=24, color=WHITE,
            )
            ana_group = VGroup(ana1, ana2, ana3).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            ana_group.move_to(np.array([
                left_x + ana_group.width / 2,
                self.written_left_y(0.95), 0,
            ]))
            ana_group.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(ana_group)
            for ana in [ana1, ana2, ana3]:
                self.play(FadeIn(ana, shift=RIGHT * 0.3), run_time=0.5)
                self.wait(2)
            self.wait(2)
            self.play(FadeOut(ana_group), run_time=0.5)

            formula_text = self.safe_text("全队人数：", font_size=26, color=GREY_B)
            formula = self.safe_mathtex(
                rf"{front_count} + {back_count} + 1 = 19", font_size=42, color=YELLOW,
            )
            formula_unit = self.safe_text("（人）", font_size=26, color=YELLOW)
            formula_row = VGroup(formula_text, formula, formula_unit).arrange(RIGHT, buff=0.2)
            formula_row.move_to(np.array([
                left_x + formula_row.width / 2, self.written_left_y(0.3), 0,
            ]))
            formula_row.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_row)
            highlight_box = SurroundingRectangle(
                VGroup(formula, formula_unit), color=RED, buff=0.15, corner_radius=0.1,
            )
            self.play(FadeIn(formula_row), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("前面 + 后面 + 1，中间的 1 就是参照人自己", wait=5)
            self.wait(2)

            answer_text = self.safe_text("答：聪聪这队一共有19人。", font_size=34, color=YELLOW)
            answer_text.move_to(np.array([
                left_x + answer_text.width / 2,
                highlight_box.get_bottom()[1] - 0.7, 0,
            ]))
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            self.play(FadeIn(answer_text, shift=UP * 0.2), run_time=0.8)
            self.wait(5)
            self.play(
                FadeOut(formula_row), FadeOut(highlight_box),
                FadeOut(answer_text), FadeOut(prob_all), run_time=0.5,
            )

        # ── 点拨 ──
        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        # ── 片尾 ──
        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
