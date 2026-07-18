"""
第48讲 比例问题（二）— 画图解题法（线段图法）

母题：男生的 3/4 = 女生的 5/6，共 38 人。求男女各几人？
答案：男:女=10:9；男20人，女18人

用法:
  cd manim/scenes/线段图法
  python -m manim problem_48.py Problem48Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem48Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    BOY_NUM, BOY_DEN = 3, 4
    GIRL_NUM, GIRL_DEN = 5, 6
    TOTAL = 38

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        bn, bd = self.BOY_NUM, self.BOY_DEN
        gn, gd = self.GIRL_NUM, self.GIRL_DEN
        tot = self.TOTAL

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
                "题里给出「甲的几分之几＝乙的几分之几」，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用线段对齐等量段，就能把等量关系化成比！",
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

            feature_title = self.safe_text("等量化比的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "画出两段并均分", "男生÷4，女生÷6，标出对应分数段"),
                ("2", "对齐相等的两段", "竖虚线对齐，看出等量关系"),
                ("3", "化成比再求人数", "甲:乙＝乙的分数:甲的分数"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：等量分数"):
            prob_all = self.make_problem_box(
                f"题目：共{tot}人，男生人数的{bn}/{bd}与女生人数的{gn}/{gd}相等。",
                "男生、女生各有多少人？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.42
        diag = self.make_equal_fraction_ratio_diagram(
            draw_y,
            boy_num=bn, boy_den=bd,
            girl_num=gn, girl_den=gd,
            total=tot,
            equal_w=3.3,
            row_gap=0.95,
            show_hint=False,
        )
        rb, rg = diag["ratio_boy"], diag["ratio_girl"]
        vb, vg = diag["boy_val"], diag["girl_val"]

        # ── 图解1：画出两段均分 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出男女线段"):
            s1 = self.step_label("第一步：画出男生、女生人数线段并均分")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(
                Create(diag["boy_line"]), FadeIn(diag["boy_ticks"]),
                FadeIn(diag["boy_lab"]),
                run_time=0.65,
            )
            self.play(
                Create(diag["girl_line"]), FadeIn(diag["girl_ticks"]),
                FadeIn(diag["girl_lab"]),
                run_time=0.65,
            )
            self.safe_subtitle(
                f"男生均分成{bd}份，女生均分成{gd}份",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出相等分数段 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "对齐相等分数段"):
            self.add(
                prob_all,
                diag["boy_line"], diag["boy_ticks"], diag["boy_lab"],
                diag["girl_line"], diag["girl_ticks"], diag["girl_lab"],
            )
            s2 = self.step_label("第二步：标出相等的两段，用竖线对齐")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                diag["boy_eq_bar"].animate.set_opacity(1),
                diag["girl_eq_bar"].animate.set_opacity(1),
                run_time=0.5,
            )
            # 保证填充可见、不整块盖住线：只恢复 fill
            diag["boy_eq_bar"].set_fill(YELLOW, opacity=0.28)
            diag["girl_eq_bar"].set_fill(YELLOW, opacity=0.28)
            self.play(
                FadeIn(diag["boy_frac"]), FadeIn(diag["girl_frac"]),
                run_time=0.45,
            )
            diag["boy_frac"].set_opacity(1)
            diag["girl_frac"].set_opacity(1)
            self.play(
                diag["dash_eq"].animate.set_opacity(1),
                diag["eq_tag"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"男生的{bn}/{bd}与女生的{gn}/{gd}一样长，表示人数相等",
                wait=5,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：化成比 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "等量关系化成比"):
            self.add(
                prob_all,
                diag["boy_row"], diag["girl_row"],
                diag["dash_eq"], diag["eq_tag"],
            )
            s3 = self.step_label("第三步：把等量关系化成男生:女生的比")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_eq"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_ratio_q"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.5)
            self.play(diag["note_ratio_ans"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"男生:女生 = {gn}/{gd} : {bn}/{bd} = {rb}:{rg}",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：按比求人数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "按比求出人数"):
            self.add(
                prob_all,
                diag["boy_row"], diag["girl_row"],
                diag["dash_eq"], diag["eq_tag"],
                diag["note_eq"], diag["note_ratio_q"], diag["note_ratio_ans"],
            )
            s4 = self.step_label("第四步：按连比从总人数中求出男女人数")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["calc_boy"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["calc_girl"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"男生{vb}人，女生{vg}人",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["boy_row"], diag["girl_row"],
            diag["dash_eq"], diag["eq_tag"],
            diag["notes"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"男生:女生={rb}:{rg}",
                font_size=24, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            f2 = VGroup(
                self.safe_text("男生：", font_size=20, color=WHITE),
                self.safe_mathtex(
                    rf"{tot}\times\dfrac{{{rb}}}{{{rb}+{rg}}}={vb}",
                    font_size=26, color=WHITE,
                ),
                self.safe_text("（人）", font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.08)
            f2.next_to(f1, DOWN, buff=0.28)
            f2.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f2)

            f3 = VGroup(
                self.safe_text("女生：", font_size=20, color=WHITE),
                self.safe_mathtex(
                    rf"{tot}\times\dfrac{{{rg}}}{{{rb}+{rg}}}={vg}",
                    font_size=26, color=WHITE,
                ),
                self.safe_text("（人）", font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.08)
            f3.next_to(f2, DOWN, buff=0.24)
            f3.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f3)

            answer_text = self.safe_text(
                f"答：男生有{vb}人，女生有{vg}人。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f3, DOWN, buff=0.32)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            # 描边高亮，避免填充挡住字
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.45)
            self.wait(0.6)
            self.play(FadeIn(f2), run_time=0.5)
            self.wait(0.5)
            self.play(FadeIn(f3), run_time=0.5)
            self.wait(0.6)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("甲×b/a=乙×d/c ⇒ 甲:乙=d/c:b/a", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(f2), FadeOut(f3),
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

