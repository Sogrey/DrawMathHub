"""
第21讲 周期问题 — 画图解题法（图示法）

母题：两种颜色的珠子依次排列，第32颗珠子是什么颜色的？
规律：灰、灰、灰、蓝、蓝（周期5）；32÷5=6组……2颗 → 灰色。

用法:
  cd manim/scenes/图示法
  python -m manim problem_21.py Problem21Scene -qh

渲染后:
  python ../_shared/post_render.py --lesson 21 \\
    --rendered media/videos/problem_21/1080p60/Problem21Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem21Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    PATTERN_COLORS = [GREY_B, GREY_B, GREY_B, BLUE_D, BLUE_D]
    PATTERN_NAMES = ["灰", "灰", "灰", "蓝", "蓝"]
    TOTAL_INDEX = 32

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem
        period = len(self.PATTERN_COLORS)
        full_groups = self.TOTAL_INDEX // period

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
                "物体或数字按固定规律重复排列，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求第几个是什么——这就是周期问题！", font_size=28, color=WHITE,
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
                stroke_width=1.5, color=GREY_B, stroke_opacity=0.25,
            )

            feature_title = self.safe_text("周期问题的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "排列有规律", "比如：灰灰灰蓝蓝，重复出现"),
                ("2", "先找出一个周期", "每几个为一组循环"),
                ("3", "总数÷周期看余数", "余数是几，就是组内第几个"),
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
                "题目：两种颜色的珠子依次排列如下图，",
                "第32颗珠子是什么颜色的？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_period_bead_diagram(
            self.PATTERN_COLORS, self.PATTERN_NAMES, self.TOTAL_INDEX, draw_y,
            draw_area_top=self.layout["draw_area_top"],
            draw_area_bottom=self.layout["draw_area_bottom"],
            step_y=self.layout["step_y"],
            tail_group_label=f"第{full_groups}组",
        )
        diagram = diag["diagram"]

        # ── 图解1：画珠子找规律 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "观察珠子排列规律"):
            s1 = self.step_label("第一步：观察珠子的排列规律")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(Create(diag["preview_line"]), run_time=0.4)
            self.play(*[Create(b) for b in diag["preview_beads"]], run_time=0.9)
            self.play(FadeIn(diag["pattern_hint"], shift=UP * 0.1), run_time=0.5)
            self.safe_subtitle("珠子的排列存在规律，灰灰灰蓝蓝重复出现", wait=3)
            self.wait(1)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：分组 ──
        period_label = None
        with self.segment("draw-2", "2", "segments/04.mp4", "每5颗为一组"):
            self.add(prob_all, diag["header"])
            s2 = self.step_label("第二步：每5颗珠子为一组")
            self.play(FadeIn(s2), run_time=0.5)
            for info in diag["group_infos"][:2]:
                self.play(FadeIn(info["unit"]), run_time=0.55)
            period_label = self.safe_text(f"每 {diag['period']} 颗为一组", font_size=22, color=TEAL_D)
            period_label.next_to(diag["grouped_row"], DOWN, buff=0.28)
            self.clamp_content(period_label)
            self.play(FadeIn(period_label), run_time=0.5)
            self.safe_subtitle("找出一个周期：5颗珠子为一组循环", wait=4)
            self.play(FadeOut(s2), FadeOut(period_label), run_time=0.3)

        # ── 图解3：分组示意与除法 ──
        div_label = None
        with self.segment("draw-3", "3", "segments/05.mp4", "分组计算组数与余数"):
            self.add(prob_all, diag["header"])
            for info in diag["group_infos"][:2]:
                self.add(info["unit"])
            s3 = self.step_label("第三步：分组计算组数和余数")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(
                FadeIn(diag["ellipsis"]),
                FadeIn(diag["group_infos"][2]["unit"]),
                run_time=0.7,
            )
            if diag["rem_unit"] is not None:
                self.play(FadeIn(diag["rem_unit"]), run_time=0.6)
            div_label = self.safe_text(
                f"{self.TOTAL_INDEX}÷{diag['period']}={diag['full_groups']}（组）……{diag['remainder']}（颗）",
                font_size=22, color=YELLOW,
            )
            mid_y = (diag["pattern_hint"].get_bottom()[1] + diag["grouped_row"].get_top()[1]) / 2
            div_label.move_to(np.array([0, mid_y, 0]))
            self.clamp_content(div_label)
            self.play(FadeIn(div_label), run_time=0.7)
            self.safe_subtitle(
                f"{self.TOTAL_INDEX}÷{diag['period']}={diag['full_groups']}组余{diag['remainder']}颗",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：标出第32颗 ──
        target_marker = target_arrow = target_label = color_hint = None
        with self.segment("draw-4", "4", "segments/06.mp4", "余数对应组内第几颗"):
            extras = [prob_all, diag["header"], diag["grouped_row"], div_label]
            self.add(*extras)
            s4 = self.step_label("第四步：余数是几，就是组内第几颗")
            self.play(FadeIn(s4), run_time=0.5)
            target_marker = SurroundingRectangle(
                diag["target_bead"], color=RED, buff=0.06, corner_radius=0.05,
            )
            target_arrow = Arrow(
                diag["target_bead"].get_bottom() + DOWN * 0.04,
                diag["target_bead"].get_bottom() + DOWN * 0.42,
                buff=0.04, color=RED, stroke_width=3,
            )
            target_label = self.safe_text(
                f"第{self.TOTAL_INDEX}颗", font_size=20, color=RED,
            )
            target_label.next_to(target_arrow, DOWN, buff=0.05)
            self.play(
                diag["target_bead"].animate.set_stroke(RED, width=4),
                Create(target_marker),
                GrowArrow(target_arrow),
                FadeIn(target_label),
                run_time=0.8,
            )
            color_hint = self.safe_text(
                f"余数{diag['remainder']} → 组内第{diag['target_pos']}颗 → {diag['target_color_name']}色",
                font_size=22, color=YELLOW,
            )
            color_hint.next_to(target_label, DOWN, buff=0.10)
            self.clamp_content(color_hint)
            self.play(FadeIn(color_hint), run_time=0.5)
            self.safe_subtitle(
                f"余数是{diag['remainder']}，第{diag['target_pos']}颗是{diag['target_color_name']}色珠子",
                wait=4,
            )
            self.wait(2)
            if target_marker is not None:
                diag["grouped_row"].add(target_marker, target_arrow, target_label)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = self.pack_period_diagram(
            diag, draw_y,
            div_label=div_label,
            color_hint=color_hint,
            draw_area_top=self.layout["draw_area_top"],
        )

        # ── 书面答题 ──
        left_x = self.written_left_x()
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式与规范作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            formula_line1 = self.safe_text(
                f"{self.TOTAL_INDEX} ÷ {diag['period']} = {diag['full_groups']}（组）……{diag['remainder']}（颗）",
                font_size=30, color=WHITE,
            )
            formula_line1.move_to(np.array([left_x + formula_line1.width / 2, self.written_left_y(0.5), 0]))
            formula_line1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_line1)
            self.play(FadeIn(formula_line1), run_time=0.6)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：第{self.TOTAL_INDEX}颗珠子是{diag['target_color_name']}色的。",
                font_size=32, color=YELLOW,
            )
            answer_text.move_to(np.array([
                left_x + answer_text.width / 2,
                formula_line1.get_bottom()[1] - 0.8, 0,
            ]))
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(answer_text, color=RED, buff=0.12, corner_radius=0.1)
            self.play(FadeIn(answer_text, shift=UP * 0.2), run_time=0.8)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("有余数看组内第几颗，无余数看组内最后一颗", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula_line1), FadeOut(answer_text),
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
