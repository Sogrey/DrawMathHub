"""
第1讲 之间问题 — 画图解题法（图示法）

本题演示（母题）：
  操场排队，从左边数起，玲玲是第6个，丽丽是第16个。玲玲和丽丽之间有几人？
  答案：16-1-6=9（人），玲玲和丽丽之间有9人。

用法:
  cd manim/scenes/图示法
  python -m manim problem_1.py Problem1Scene -qh

渲染后:
  python ../_shared/post_render.py --lesson 1 \\
    --rendered media/videos/problem_1/1080p60/Problem1Scene.mp4

脚本命名: problem_{lessonNumber}.py，与 public/data/problems/{lessonNumber}.json 一致
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem1Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            # ── 上板块：概念定义 ──
            concept_title = self.safe_text("题型识别", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "排队的时候，如果告诉你两个人分别排第几，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "问你他们之间有几个人——这就是之间问题！", font_size=28, color=WHITE,
            )
            concept_body = VGroup(s1_body, s1_body2).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            concept_body.next_to(concept_title, DOWN, buff=0.45)
            concept_body.move_to(np.array([0, concept_body.get_center()[1], 0]))
            self.clamp_content(concept_body)
            concept_block = VGroup(concept_title, concept_body)

            # 分隔线紧贴概念块下方，下板块整体再下移
            divider_y = concept_block.get_bottom()[1] - 0.45
            divider = Line(
                np.array([self.safe_left + 0.5, divider_y, 0]),
                np.array([self.safe_right - 0.5, divider_y, 0]),
                stroke_width=1.5,
                color=GREY_B,
                stroke_opacity=0.25,
            )

            # ── 下板块：特征（≤3 单列，≥4 左右两列）──
            feature_title = self.safe_text("之间问题的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "已知两人各排第几", "比如：小明排第3，小红排第8"),
                ("2", "问的是\"之间\"有几人", "\"之间\"不包括这两个人自己"),
                ("3", "用画图的方法最直观", "画圈圈表示人，一目了然！"),
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

        # ── 2：题目展示（全程保留至书面答题结束）──
        prob_all = None
        with self.segment("question", "题目", "segments/02.mp4", "读题：找出关键信息"):
            prob_all = self.make_problem_box(
                "题目：操场排队，从左边数起，玲玲是第6个，丽丽是第16个。",
                "玲玲和丽丽之间有几人？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)


        draw_y = self.layout["draw_y"]
        lingling_rank, lili_rank = 6, 16
        diag = self.make_between_diagram(lingling_rank, lili_rank, draw_y)
        diagram_row = diag["row"]

        # ── 3~6：图解步骤 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "用圆圈表示每个站位"):
            s4 = self.step_label("第一步：用圆圈表示每个人的站位")
            self.add(prob_all)
            self.play(FadeIn(s4), run_time=0.5)
            for part in diag["draw_order"]:
                if isinstance(part, Circle):
                    self.play(Create(part), run_time=0.4)
                elif isinstance(part, VGroup) and len(part) > 0 and isinstance(part[0], Dot):
                    self.play(FadeIn(part, scale=0.8), run_time=0.4)
                else:
                    self.play(Create(part), run_time=0.8)
            self.safe_subtitle(
                "1个圆圈代表1人；之间未知人数可以用省略号表示",
                wait=3,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        circle_r = diag["circle_r"]
        left_person = diag["left_person"]
        right_person = diag["right_person"]
        rank_left = diag["rank_left_anchor"]
        between_ellipsis = diag["between_ellipsis"]
        between_zone = diag["between_zone_circles"]

        # ── 5：图解步骤2 ──
        lingling_fill = lingling_name = brace_6 = six_label = None
        with self.segment("draw-2", "2", "segments/04.mp4", "标出玲玲的位置"):
            self.add(prob_all, diagram_row)
            s5 = self.step_label("第二步：标出玲玲的位置")
            self.play(FadeIn(s5), run_time=0.5)
            lingling_fill = Circle(
                radius=circle_r + 0.02, fill_opacity=0.5, fill_color=YELLOW,
                stroke_width=3, stroke_color=YELLOW,
            )
            lingling_fill.move_to(left_person.get_center())
            lingling_name = self.safe_text("玲玲", font_size=22, color=YELLOW)
            lingling_name.next_to(lingling_fill, DOWN, buff=0.15)
            brace_6 = BraceBetweenPoints(
                rank_left.get_top() + UP * 0.12,
                left_person.get_top() + UP * 0.12,
                direction=UP,
            ).set_color(TEAL_D)
            six_label = self.safe_text(f"{lingling_rank}人", font_size=22, color=TEAL_D)
            six_label.next_to(brace_6, UP, buff=0.1)
            self.play(
                FadeIn(lingling_fill), FadeIn(lingling_name),
                FadeIn(brace_6), FadeIn(six_label), run_time=0.8,
            )
            self.safe_subtitle(f"从左边数，第1到第{lingling_rank}个，共{lingling_rank}人", wait=4)
            self.play(FadeOut(s5), run_time=0.3)

        # ── 6：图解步骤3 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出丽丽与之间区域"):
            self.add(prob_all, diagram_row, lingling_fill, lingling_name, brace_6, six_label)
            s6 = self.step_label("第三步：标出丽丽的位置")
            self.play(FadeIn(s6), run_time=0.5)
            lili_fill = Circle(
                radius=circle_r + 0.02, fill_opacity=0.5, fill_color=PURPLE_A,
                stroke_width=3, stroke_color=PURPLE_A,
            )
            lili_fill.move_to(right_person.get_center())
            lili_name = self.safe_text("丽丽", font_size=22, color=PURPLE_A)
            lili_name.next_to(lili_fill, DOWN, buff=0.15)
            brace_16 = BraceBetweenPoints(
                rank_left.get_top() + UP * 0.77,
                right_person.get_top() + UP * 0.77,
                direction=UP,
            ).set_color(PURPLE_A)
            sixteen_label = self.safe_text(f"{lili_rank}人", font_size=22, color=PURPLE_A)
            sixteen_label.next_to(brace_16, UP, buff=0.1)
            self.play(FadeIn(lili_fill), FadeIn(lili_name), run_time=0.5)
            if between_ellipsis is not None:
                self.play(between_ellipsis.animate.set_color(YELLOW), run_time=0.5)
            self.play(FadeIn(brace_16), FadeIn(sixteen_label), run_time=0.5)
            self.safe_subtitle(f"丽丽排第{lili_rank}，玲玲和丽丽之间的人数正是要求的", wait=4)
            self.play(FadeOut(s6), run_time=0.3)
            lili_fill_ref, lili_name_ref = lili_fill, lili_name
            brace_16_ref, sixteen_label_ref = brace_16, sixteen_label

        # ── 7：图解步骤4 ──
        brace_between = q_label = None
        with self.segment("draw-4", "4", "segments/06.mp4", "标出「之间」的范围"):
            self.add(
                prob_all, diagram_row,
                lingling_fill, lingling_name, brace_6, six_label,
                lili_fill_ref, lili_name_ref, brace_16_ref, sixteen_label_ref,
            )
            s7 = self.step_label("第四步：标出\"之间\"的范围")
            self.play(FadeIn(s7), run_time=0.5)
            brace_between = BraceBetweenPoints(
                diag["between_brace_start"].get_bottom() + DOWN * 0.55,
                diag["between_brace_end"].get_bottom() + DOWN * 0.55,
                direction=DOWN,
            ).set_color(RED)
            q_label = self.safe_text("之间 = ?人", font_size=24, color=RED)
            q_label.next_to(brace_between, DOWN, buff=0.1)
            anims = [FadeIn(brace_between), FadeIn(q_label)]
            for c in between_zone:
                anims.insert(0, c.animate.set_color(RED).set_fill(RED, opacity=0.25).set_stroke(RED, width=3))
            if between_ellipsis is not None:
                anims.insert(len(between_zone), between_ellipsis.animate.set_color(RED))
            self.play(*anims, run_time=0.6)
            self.safe_subtitle("玲玲和丽丽之间有几人？", wait=4)
            self.wait(2)
            self.play(FadeOut(s7), run_time=0.3)

        diagram_all = VGroup(
            diagram_row,
            lingling_fill, lingling_name, brace_6, six_label,
            lili_fill_ref, lili_name_ref, brace_16_ref, sixteen_label_ref,
            brace_between, q_label,
        )

        # ── 7：书面答题（分析 + 列式 + 作答）──
        left_x = self.written_left_x()
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：分析、列式与规范作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)
            ana1 = self.safe_text("从左边第1个小朋友到玲玲，一共有6人", font_size=24, color=WHITE)
            ana2 = self.safe_text("丽丽排第16，她前面有几人呢？", font_size=24, color=WHITE)
            ana3 = self.safe_text("丽丽前面有 16 - 1 = 15（人）", font_size=24, color=TEAL_D)
            ana4 = self.safe_text("用15减去6，就是之间的人数！", font_size=24, color=WHITE)
            ana_group = VGroup(ana1, ana2, ana3, ana4).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            ana_group.move_to(np.array([
                left_x + ana_group.width / 2,
                self.written_left_y(0.95), 0,
            ]))
            ana_group.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(ana_group)
            for ana in [ana1, ana2, ana3, ana4]:
                self.play(FadeIn(ana, shift=RIGHT * 0.3), run_time=0.5)
                self.wait(2)
            self.wait(2)
            self.play(FadeOut(ana_group), run_time=0.5)

            step1_text = self.safe_text("丽丽前面的人数：", font_size=26, color=GREY_B)
            step1_formula = self.safe_mathtex(r"16 - 1 = 15", font_size=36, color=WHITE)
            step1_unit = self.safe_text("（人）", font_size=22, color=GREY_B)
            step1_row = VGroup(step1_text, step1_formula, step1_unit).arrange(RIGHT, buff=0.15)
            step1_row.move_to(np.array([left_x + step1_row.width / 2, self.written_left_y(0.85), 0]))
            step1_row.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(step1_row)
            self.play(FadeIn(step1_row), run_time=0.6)
            self.wait(2)
            step2_text = self.safe_text("之间的人数：", font_size=26, color=GREY_B)
            step2_formula = self.safe_mathtex(r"15 - 6 = 9", font_size=36, color=WHITE)
            step2_unit = self.safe_text("（人）", font_size=22, color=GREY_B)
            step2_row = VGroup(step2_text, step2_formula, step2_unit).arrange(RIGHT, buff=0.15)
            step2_row.move_to(np.array([left_x + step2_row.width / 2, self.written_left_y(0.0), 0]))
            step2_row.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(step2_row)
            self.play(FadeIn(step2_row), run_time=0.6)
            self.wait(2)
            combined_text = self.safe_text("合并算式：", font_size=26, color=GREY_B)
            combined_formula = self.safe_mathtex(r"16 - 1 - 6 = 9", font_size=42, color=YELLOW)
            combined_unit = self.safe_text("（人）", font_size=26, color=YELLOW)
            combined_row = VGroup(combined_text, combined_formula, combined_unit).arrange(RIGHT, buff=0.2)
            combined_row.move_to(np.array([left_x + combined_row.width / 2, self.written_left_y(-0.85), 0]))
            combined_row.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(combined_row)
            highlight_box = SurroundingRectangle(
                VGroup(combined_formula, combined_unit), color=RED, buff=0.15, corner_radius=0.1,
            )
            self.play(FadeIn(combined_row), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("用大数减1，再减小数，就是之间的人数", wait=5)
            self.wait(2)

            answer_text = self.safe_text("答：玲玲和丽丽之间有9人。", font_size=34, color=YELLOW)
            answer_text.move_to(np.array([
                left_x + answer_text.width / 2,
                highlight_box.get_bottom()[1] - 0.7, 0,
            ]))
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            self.play(FadeIn(answer_text, shift=UP * 0.2), run_time=0.8)
            self.wait(5)
            self.play(
                FadeOut(step1_row), FadeOut(step2_row),
                FadeOut(combined_row), FadeOut(highlight_box),
                FadeOut(answer_text), FadeOut(prob_all), run_time=0.5,
            )

        # ── 点拨：关键点拨（图解放大 + 点拨在下方）──
        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=6,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        # ── 结尾：片尾 ──
        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
