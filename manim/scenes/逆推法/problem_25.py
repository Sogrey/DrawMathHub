"""
第25讲 还原问题（一）— 画图解题法（逆推法）

母题：一个数×6、+6、÷6、−6后得6，求原数。
答案：6+6=12，12×6=72，72−6=66，66÷6=11

用法:
  cd manim/scenes/逆推法
  python -m manim problem_25.py Problem25Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem25Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    FORWARD_OPS = ["×6", "+6", "÷6", "−6"]
    RESULT = 6

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        ops = self.FORWARD_OPS
        result = self.RESULT

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
                "一个数经过多步运算后得到结果，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "要反过来求出最开始的数——这就是还原问题！",
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

            feature_title = self.safe_text("逆推法的三个要点", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先画出正向流程图", "按题目顺序标出每步运算"),
                ("2", "从结果往回推", "每一步用原来的逆运算"),
                ("3", "加减小数对调，乘除对数", "+↔−，×↔÷"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：多步运算还原"):
            prob_all = self.make_problem_box(
                "题目：一个数乘6，加上6，除以6，再减去6，",
                f"最后结果等于{result}。这个数是多少？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_restore_flow_diagram(
            draw_y,
            forward_ops=ops,
            result=result,
            show_hint=True,
        )
        vals = diag["box_values"]
        answer = vals[0]

        # ── 图解1：画出正向流程图 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出正向流程图"):
            s1 = self.step_label("第一步：按运算顺序画出流程图")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)

            self.play(FadeIn(diag["boxes"][0]), FadeIn(diag["start_tag"]), run_time=0.45)
            for i in range(len(ops)):
                self.play(
                    GrowArrow(diag["fwd_arrows"][i]),
                    FadeIn(diag["fwd_labels"][i]),
                    run_time=0.4,
                )
                if i < len(ops) - 1:
                    self.play(FadeIn(diag["boxes"][i + 1]), run_time=0.35)
                else:
                    self.play(
                        FadeIn(diag["result_node"]),
                        FadeIn(diag["result_tag"]),
                        run_time=0.4,
                    )
            self.safe_subtitle("从左到右：×6 → +6 → ÷6 → −6，最后得到结果", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出逆运算箭头 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出逆运算"):
            self.add(
                prob_all, diag["hint"], diag["flow"],
            )
            s2 = self.step_label("第二步：从结果出发，标出每步的逆运算")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(
                diag["rev_arrows"].animate.set_opacity(1),
                diag["rev_labels"].animate.set_opacity(1),
                run_time=0.7,
            )
            self.safe_subtitle("减法变加法，除法变乘法，加法变减法，乘法变除法", wait=5)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：逐步逆推填数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "逐步逆推填数"):
            self.add(prob_all, diag["hint"], diag["flow"])
            s3 = self.step_label("第三步：从右往左，一步步求出各方框的数")
            self.play(FadeIn(s3), run_time=0.5)

            # 从最后一个方框往左填
            # ops[-1] 的逆：从 result → vals[-1]
            n = len(ops)
            subtitles = [
                f"{result}+6={vals[n - 1]}（减去6的逆运算是加上6）",
                f"{vals[n - 1]}×6={vals[n - 2]}（除以6的逆运算是乘6）",
                f"{vals[n - 2]}−6={vals[n - 3]}（加上6的逆运算是减去6）",
                f"{vals[n - 3]}÷6={vals[n - 4]}（乘6的逆运算是除以6）",
            ]
            # 填框顺序：box index n-1, n-2, n-3, n-4
            for k, box_i in enumerate(range(n - 1, -1, -1)):
                self.play(
                    diag["rev_arrows"][box_i].animate.set_color(YELLOW),
                    diag["rev_labels"][box_i].animate.set_color(YELLOW),
                    run_time=0.35,
                )
                self.play(
                    diag["box_qs"][box_i].animate.set_opacity(0),
                    diag["box_ans"][box_i].animate.set_opacity(1),
                    diag["box_frames"][box_i].animate.set_color(YELLOW),
                    run_time=0.5,
                )
                self.safe_subtitle(subtitles[k], wait=3.2)
                self.play(
                    diag["rev_arrows"][box_i].animate.set_color(BLUE_C),
                    diag["rev_labels"][box_i].animate.set_color(BLUE_C),
                    run_time=0.25,
                )

            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：点明起始数 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "得出起始数"):
            self.add(prob_all, diag["hint"], diag["flow"])
            s4 = self.step_label("第四步：最左边方框里的数就是所求")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)

            ring = SurroundingRectangle(
                diag["boxes"][0], color=RED, buff=0.10, corner_radius=0.08,
            )
            # 并入 flow，避免后续平移错位
            diag["flow"].add(ring)
            diag["start_ring"] = ring
            ans_note = self.safe_text(
                f"起始数是 {answer}",
                font_size=26, color=YELLOW,
            )
            ans_note.next_to(diag["nodes"], DOWN, buff=0.55)
            diag["flow"].add(ans_note)
            diag["ans_note"] = ans_note

            self.play(Create(ring), run_time=0.5)
            self.play(FadeIn(ans_note, shift=UP * 0.1), run_time=0.45)
            self.safe_subtitle(f"逆推四步后得到：这个数是 {answer}", wait=4)
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["flow"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            steps = [
                (f"{result}+6={vals[3]}", "← 最后一步 −6 的逆"),
                (f"{vals[3]}×6={vals[2]}", "← ÷6 的逆"),
                (f"{vals[2]}−6={vals[1]}", "← +6 的逆"),
                (f"{vals[1]}÷6={vals[0]}", "← ×6 的逆"),
            ]
            rows = VGroup()
            for expr, note in steps:
                e = self.safe_text(expr, font_size=24, color=WHITE)
                n = self.safe_text(note, font_size=18, color=GREY_B)
                rows.add(VGroup(e, n).arrange(RIGHT, buff=0.18))
            formula_rows = rows.arrange(DOWN, buff=0.26, aligned_edge=LEFT)
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            for row in rows:
                self.play(FadeIn(row), run_time=0.45)
                self.wait(1.0)

            answer_text = self.safe_text(
                f"答：这个数是{answer}。",
                font_size=26, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.42)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("从结果出发，逐步用逆运算还原", wait=5)
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
