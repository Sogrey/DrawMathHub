"""
第32讲 鸡兔同笼问题（一）— 画图解题法（假设法）

母题：共14个头、38条腿。鸡和兔各多少只？
答案：兔 (38−14×2)÷(4−2)=5；鸡 14−5=9

用法:
  cd manim/scenes/假设法
  python -m manim problem_32.py Problem32Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem32Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    HEADS = 14
    LEGS = 38
    CHICKEN_LEGS = 2
    RABBIT_LEGS = 4

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        heads = self.HEADS
        legs = self.LEGS
        c_legs = self.CHICKEN_LEGS
        r_legs = self.RABBIT_LEGS
        assume = heads * c_legs
        short = legs - assume
        per = r_legs - c_legs
        rabbits = short // per
        chickens = heads - rabbits

        # ── 题型讲解（含片头）──
        with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)

            title_bottom = self._title_group.get_bottom()[1]
            zone_top = title_bottom - 0.45

            concept_title = self.safe_text("题型识别", font_size=34, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "已知鸡、兔的总头数和总腿数，",
                font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "先假设一种情形，再按腿数差修正——这就是假设法！",
                font_size=28, color=WHITE,
            )
            concept_body = VGroup(s1_body, s1_body2).arrange(
                DOWN, buff=0.22, aligned_edge=LEFT,
            )
            concept_body.next_to(concept_title, DOWN, buff=0.40)
            concept_body.move_to(np.array([0, concept_body.get_center()[1], 0]))
            self.clamp_content(concept_body)
            concept_block = VGroup(concept_title, concept_body)

            divider_y = concept_block.get_bottom()[1] - 0.40
            divider = Line(
                np.array([self.safe_left + 0.5, divider_y, 0]),
                np.array([self.safe_right - 0.5, divider_y, 0]),
                stroke_width=1.5, color=GREY_B, stroke_opacity=0.25,
            )

            feature_title = self.safe_text("假设法的三个要点", font_size=32, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.55, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "先假设一种极端", "比如先当全部都是鸡"),
                ("2", "算腿数差多少", "与实际总腿数比较"),
                ("3", "按每只相差修正", "差腿数÷每只多出腿数＝兔数"),
            ]
            feature_groups = self.layout_numbered_features(
                features,
                top_y=feature_title.get_bottom()[1] - 0.45,
                row_step=1.10,
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：头数与腿数"):
            prob_all = self.make_problem_box(
                f"题目：鸡兔同笼，共有{heads}个头，{legs}条腿。",
                "鸡和兔各有多少只？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_chicken_rabbit_diagram(
            draw_y,
            heads=heads,
            legs=legs,
            chicken_legs=c_legs,
            rabbit_legs=r_legs,
            show_hint=True,
        )

        # ── 图解1：画出 14 个头，假设全是鸡 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "假设全部是鸡"):
            s1 = self.step_label("第一步：用○表示头，假设全部是鸡，每只画2条腿")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["heads"]), run_time=0.7)
            self.play(FadeIn(diag["chicken_legs_g"]), run_time=0.6)
            self.play(FadeIn(diag["assume_top"]), FadeIn(diag["assume_bot"]), run_time=0.55)
            self.safe_subtitle(
                f"假设{heads}只全是鸡，一共{assume}条腿",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：比实际少多少腿 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "算出少的腿数"):
            self.add(
                prob_all, diag["hint"], diag["bodies"],
                diag["assume_top"], diag["assume_bot"], diag["notes"],
                diag["result_rabbit"], diag["result_chicken"],
            )
            s2 = self.step_label("第二步：和实际腿数比较，算出相差多少")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["note_short"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{legs}－{assume}={short}（条），假设把兔当成了鸡",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：每只相差 → 兔的只数 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "求出兔的只数"):
            self.add(
                prob_all, diag["hint"], diag["bodies"],
                diag["assume_top"], diag["assume_bot"], diag["notes"],
                diag["result_rabbit"], diag["result_chicken"],
            )
            s3 = self.step_label("第三步：每只兔比鸡多2条腿，求出兔有几只")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_diff"].animate.set_opacity(1), run_time=0.5)
            self.play(diag["note_rab_q"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.6)
            self.play(
                diag["note_rab_q"].animate.set_opacity(0),
                diag["note_rab_ans"].animate.set_opacity(1),
                run_time=0.5,
            )
            # 给前 rabbits 只加上兔腿
            self.play(
                *[extra.animate.set_opacity(1) for extra in diag["rabbit_extras"]],
                run_time=0.9,
            )
            self.safe_subtitle(
                f"{short}÷{per}={rabbits}（只兔）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：分组标注鸡与兔 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "标出鸡和兔"):
            self.add(
                prob_all, diag["hint"], diag["bodies"],
                diag["assume_top"], diag["assume_bot"], diag["notes"],
                diag["result_rabbit"], diag["result_chicken"],
            )
            s4 = self.step_label("第四步：把变成兔的部分标出来，再求鸡数")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(FadeOut(diag["assume_top"]), run_time=0.35)
            self.play(
                diag["result_rabbit"].animate.set_opacity(1),
                diag["result_chicken"].animate.set_opacity(1),
                run_time=0.6,
            )
            self.play(diag["note_chi_ans"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"鸡：{heads}－{rabbits}={chickens}（只）",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["bodies"], diag["assume_bot"],
            diag["result_rabbit"], diag["result_chicken"], diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"兔：（{legs}－{heads}×{c_legs}）÷（{r_legs}－{c_legs}）={rabbits}（只）",
                font_size=22, color=WHITE,
            )
            step2 = self.safe_text(
                f"鸡：{heads}－{rabbits}={chickens}（只）",
                font_size=24, color=WHITE,
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
                self.wait(1.1)

            answer_text = self.safe_text(
                f"答：鸡有{chickens}只，兔有{rabbits}只。",
                font_size=24, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.40)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("假设全是鸡，用相差腿数÷2得到兔数", wait=5)
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
