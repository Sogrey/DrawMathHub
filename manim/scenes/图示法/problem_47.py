"""
第47讲 比例问题（一）— 画图解题法（图示法）

母题：红∶新=3∶4，新∶明=6∶5，共62枚，小明多少枚？
答案：连比 9∶12∶10；62×10/(9+12+10)=20（分数线形式）

用法:
  cd manim/scenes/图示法
  python -m manim problem_47.py Problem47Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem47Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    RATIO_AB = (3, 4)
    RATIO_BC = (6, 5)
    TOTAL = 62
    NAMES = ["小红", "小新", "小明"]

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        ab, bc = self.RATIO_AB, self.RATIO_BC
        tot = self.TOTAL
        names = self.NAMES

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=32, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.32, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "已知总量，又给出两组部分量的比，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先化成连比，再按份数从总量里取出所求部分！",
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

            feature_title = self.safe_text("化连比的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "找出公共项", "两组比里都出现的那个人"),
                ("2", "对齐份数", "取公共项两个份数的最小公倍数"),
                ("3", "写出连比求值", "总量×所求份数÷总份数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：两组比求部分"):
            prob_all = self.make_problem_box(
                f"题目：{names[0]}∶{names[1]}={ab[0]}∶{ab[1]}，"
                f"{names[1]}∶{names[2]}={bc[0]}∶{bc[1]}，共{tot}枚。",
                f"{names[2]}有多少枚邮票？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_continuous_ratio_diagram(
            draw_y,
            names=names,
            ratio_ab=ab,
            ratio_bc=bc,
            total=tot,
            ask_index=2,
            show_hint=True,
        )
        linked = diag["linked"]
        ask_val = diag["ask_val"]

        # ── 图解1：列出两组比 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "列出两组比"):
            s1 = self.step_label("第一步：按三人分列，写出两组比")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["headers"]), run_time=0.5)
            self.play(FadeIn(diag["row1"]), run_time=0.55)
            self.play(FadeIn(diag["row2"]), run_time=0.55)
            self.safe_subtitle(
                f"{names[0]}∶{names[1]}={ab[0]}∶{ab[1]}，"
                f"{names[1]}∶{names[2]}={bc[0]}∶{bc[1]}",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：对齐公共项 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "对齐公共项份数"):
            self.add(
                prob_all, diag["hint"], diag["headers"],
                diag["row1"], diag["row2"],
            )
            s2 = self.step_label(f"第二步：对齐「{names[1]}」的份数")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["mid_box"].animate.set_stroke(opacity=1), run_time=0.45)
            self.play(diag["lcm_note"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["scale_note"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"{ab[1]} 与 {bc[0]} 的最小公倍数是 {diag['mid_lcm']}，"
                f"第一组×{diag['mul1']}，第二组×{diag['mul2']}",
                wait=5,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：写出连比 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "写出三人连比"):
            self.add(
                prob_all, diag["hint"], diag["headers"],
                diag["row1"], diag["row2"], diag["mid_box"],
                diag["lcm_note"], diag["scale_note"],
            )
            s3 = self.step_label("第三步：写出三人邮票数的连比")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["sep"].animate.set_opacity(1), run_time=0.35)
            self.play(
                diag["link_label"].animate.set_opacity(1),
                diag["link_col1"].animate.set_opacity(1),
                diag["link_col2"].animate.set_opacity(1),
                *[n.animate.set_opacity(1) for n in diag["link_nums"]],
                run_time=0.7,
            )
            self.safe_subtitle(
                f"{names[0]}∶{names[1]}∶{names[2]}"
                f"={linked[0]}∶{linked[1]}∶{linked[2]}",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：按份数求值 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "按份数求小明"):
            self.add(
                prob_all, diag["hint"], diag["headers"],
                diag["row1"], diag["row2"], diag["mid_box"],
                diag["sep"], diag["link_row"],
                diag["lcm_note"], diag["scale_note"],
            )
            s4 = self.step_label(f"第四步：总量按连比取出{names[2]}的份数")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["calc_q"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.6)
            self.play(
                diag["calc_q"].animate.set_opacity(0),
                diag["calc_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{tot}×{diag['ask_parts']}/({linked[0]}+{linked[1]}+{linked[2]})={ask_val}（枚）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["headers"], diag["row1"], diag["row2"], diag["mid_box"],
            diag["sep"], diag["link_row"],
            diag["lcm_note"], diag["scale_note"], diag["calc_ans"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"{names[0]}∶{names[1]}∶{names[2]}"
                f"={linked[0]}∶{linked[1]}∶{linked[2]}",
                font_size=22, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2_math = self.safe_mathtex(
                rf"{tot} \times \dfrac{{{diag['ask_parts']}}}{{{linked[0]}+{linked[1]}+{linked[2]}}} = {ask_val}",
                font_size=28, color=WHITE,
            )
            f2_unit = self.safe_text("（枚）", font_size=22, color=WHITE)
            f2 = VGroup(f2_math, f2_unit).arrange(RIGHT, buff=0.12)
            f2.next_to(f1, DOWN, buff=0.32)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            answer_text = self.safe_text(
                f"答：{names[2]}有{ask_val}枚邮票。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f2, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )

            self.play(FadeIn(f1), run_time=0.5)
            self.wait(0.8)
            self.play(FadeIn(f2), run_time=0.5)
            self.wait(0.8)
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("两组比化连比，再按份数求部分量", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(f2), FadeOut(answer_text),
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
