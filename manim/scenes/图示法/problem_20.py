"""
第20讲 重叠问题 — 画图解题法（图示法）

母题：三根 60 厘米木条绑成 140 厘米，每处重叠多长？
答案：60×3=180，180−140=40，40÷2=20（厘米）

用法:
  cd manim/scenes/图示法
  python -m manim problem_20.py Problem20Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem20Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    PIECE_LEN = 60
    COUNT = 3
    JOINED_LEN = 140

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        piece = self.PIECE_LEN
        n = self.COUNT
        joined = self.JOINED_LEN
        raw = piece * n
        ov_n = n - 1
        ov_total = raw - joined
        one_ov = ov_total // ov_n

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("什么是重叠问题？", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "几个物体连在一起时会有重叠，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "已知原长与拼成后的长，求每段重叠多长——这就是重叠问题！",
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

            feature_title = self.safe_text("图示法解重叠的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先画出物体搭接样子", "看清有几处重叠"),
                ("2", "重叠处会「少算」长度", "拼成长 = 原总长 − 重叠总长"),
                ("3", "n 个物体有 (n−1) 处重叠", "重叠总长再均分到每一处"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：原长与拼成长"):
            prob_all = self.make_problem_box(
                f"题目：把{n}根长{piece}厘米的木条绑起来，绑成一根长{joined}厘米的木条，",
                "每两根中间重叠多长？（各重叠长度相等）",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_overlap_bars_diagram(
            draw_y,
            piece_len=piece,
            count=n,
            joined_len=joined,
            show_hint=True,
        )

        # ── 图解1：画出三根搭接 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出搭接木条"):
            s1 = self.step_label(f"第一步：画出{n}根木条搭接的样子")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.35)
            for bar in diag["bars"]:
                self.play(FadeIn(bar, shift=RIGHT * 0.15), run_time=0.45)
            self.safe_subtitle("一根接一根，中间有重叠的部分", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标单根长与总长 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标原长与拼成长"):
            self.add(prob_all, diag["hint"], diag["bar_groups"])
            s2 = self.step_label("第二步：标出每根原长和绑好后的总长")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["piece_block"]), run_time=0.55)
            self.wait(0.5)
            self.play(FadeIn(diag["total_block"]), run_time=0.55)
            self.safe_subtitle(
                f"每根 {piece} 厘米，绑好后一共 {joined} 厘米",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标重叠处 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标重叠段"):
            self.add(
                prob_all, diag["hint"], diag["bar_groups"],
                diag["piece_block"], diag["total_block"],
            )
            s3 = self.step_label("第三步：标出重叠部分")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["ov_highlights"]), run_time=0.6)
            self.play(FadeIn(diag["ov_block"]), run_time=0.5)
            self.play(FadeIn(diag["count_note"]), run_time=0.45)
            self.safe_subtitle(
                f"{n} 根木条中间有 {ov_n} 处重叠，每处一样长",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：推出每段重叠 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "算出重叠长"):
            self.add(
                prob_all, diag["hint"], diag["bar_groups"],
                diag["piece_block"], diag["total_block"],
                diag["ov_highlights"], diag["ov_block"], diag["count_note"],
            )
            s4 = self.step_label("第四步：用「少掉的长度」求每处重叠")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(
                FadeOut(diag["ov_q"]),
                FadeIn(diag["ov_ans"]),
                run_time=0.55,
            )
            # 把答案并入 ov_block 便于后续平移
            diag["ov_block"].add(diag["ov_ans"])
            self.safe_subtitle(
                f"少掉 {raw}−{joined}={ov_total} 厘米，"
                f"再÷{ov_n} 处 → 每处 {one_ov} 厘米",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["bar_groups"], diag["ov_highlights"],
            diag["piece_block"], diag["ov_brace"], diag["ov_ans"],
            diag["total_block"], diag["count_note"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{piece}×{n}={raw}（厘米）",
                font_size=26, color=WHITE,
            )
            step1_note = self.safe_text("（原总长）", font_size=20, color=GREY_B)
            step1_row = VGroup(step1, step1_note).arrange(RIGHT, buff=0.16)

            step2 = self.safe_text(
                f"{raw}−{joined}={ov_total}（厘米）",
                font_size=26, color=WHITE,
            )
            step2_note = self.safe_text("（重叠总长）", font_size=20, color=ORANGE)
            step2_row = VGroup(step2, step2_note).arrange(RIGHT, buff=0.16)

            step3 = self.safe_text(
                f"{ov_total}÷{ov_n}={one_ov}（厘米）",
                font_size=26, color=WHITE,
            )
            step3_note = self.safe_text("（每处重叠）", font_size=20, color=TEAL_D)
            step3_row = VGroup(step3, step3_note).arrange(RIGHT, buff=0.16)

            formula_rows = VGroup(step1_row, step2_row, step3_row).arrange(
                DOWN, buff=0.28, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in [step1_row, step2_row, step3_row]:
                self.play(FadeIn(row), run_time=0.5)
                self.wait(1.3)

            answer_text = self.safe_text(
                f"答：每两根木条中间的重叠部分长{one_ov}厘米。",
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
            self.safe_subtitle("n 个物体有 (n−1) 处重叠，重叠总长再均分", wait=5)
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
