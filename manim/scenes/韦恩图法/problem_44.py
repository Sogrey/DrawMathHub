"""
第44讲 容斥问题 — 画图解题法（韦恩图法）

母题：全班36人，第一题对21、第二题对18，每人至少对一题。两题都对几人？
答案：21+18−36=3

用法:
  cd manim/scenes/韦恩图法
  python -m manim problem_44.py Problem44Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem44Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    SET_A = 21
    SET_B = 18
    TOTAL = 36

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        a, b, tot = self.SET_A, self.SET_B, self.TOTAL
        both = a + b - tot

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
                "整体里有几个集合互相重叠，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "直接相加会重复计数——用韦恩图找出重叠部分！",
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

            feature_title = self.safe_text("韦恩图法的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "画出两个重叠圈", "重叠部分就是同时属于两个集合的"),
                ("2", "发现相加会重复", "两题都对的人被算了两次"),
                ("3", "和减总人数", "交集＝两集之和－全集"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：两题都对"):
            prob_all = self.make_problem_box(
                f"题目：全班{tot}人，第一题对{a}人，第二题对{b}人，每人至少对一题。",
                "两题都做对的有多少人？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_venn_sets_diagram(
            draw_y, set_a=a, set_b=b, total=tot, show_hint=True,
        )

        # ── 图解1：画出两个重叠圆 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出韦恩图"):
            s1 = self.step_label("第一步：用两个重叠的圆表示做对两题的人")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(Create(diag["oval_a"]), FadeIn(diag["lab_a"]), run_time=0.55)
            self.play(Create(diag["oval_b"]), FadeIn(diag["lab_b"]), run_time=0.55)
            self.play(FadeIn(diag["both_q"]), run_time=0.4)
            self.safe_subtitle(
                "重叠部分就是两题都做对的人",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出全集 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出总人数"):
            self.add(
                prob_all, diag["hint"], diag["venn"], diag["notes"],
            )
            s2 = self.step_label("第二步：用括号标出全班总人数")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["total_block"]), run_time=0.55)
            self.safe_subtitle(
                f"每人至少做对一题，所以全集就是全班 {tot} 人",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：说明重复计算 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "发现重复"):
            self.add(
                prob_all, diag["hint"], diag["venn"],
                diag["total_block"], diag["notes"],
            )
            s3 = self.step_label("第三步：两集人数相加，发现比总人数多")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_sum"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_why"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"{a}+{b}={a + b}，多出来的就是被算了两次的重叠人数",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出交集 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出重叠"):
            self.add(
                prob_all, diag["hint"], diag["venn"],
                diag["total_block"], diag["notes"],
            )
            s4 = self.step_label("第四步：用两集之和减去总人数，求出重叠人数")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_calc_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.5)
            self.play(
                diag["note_calc_q"].animate.set_opacity(0),
                diag["note_calc_ans"].animate.set_opacity(1),
                diag["both_q"].animate.set_opacity(0),
                diag["both_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{a}+{b}－{tot}={both}（人）",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["venn"], diag["total_block"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            formula = self.safe_text(
                f"{a}+{b}－{tot}={both}（人）",
                font_size=28, color=WHITE,
            )
            formula.move_to(np.array([
                left_x + formula.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula)

            self.play(FadeIn(formula), run_time=0.5)
            self.wait(1.5)

            answer_text = self.safe_text(
                f"答：两题都做对的有{both}人。",
                font_size=24, color=YELLOW,
            )
            answer_text.next_to(formula, DOWN, buff=0.40)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("交集＝两集之和－全集", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula), FadeOut(answer_text),
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
