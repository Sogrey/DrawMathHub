"""
第29讲 火车过桥问题 — 画图解题法（插旗法）

母题：车长 360 米，过树 8 秒；同样速度过桥 1260 米，需多久？
答案：(360+1260)÷(360÷8)=36（秒）

用法:
  cd manim/scenes/插旗法
  python -m manim problem_29.py Problem29Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem29Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    TRAIN_LEN = 360
    BRIDGE_LEN = 1260
    TREE_TIME = 8

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        L = self.TRAIN_LEN
        B = self.BRIDGE_LEN
        t_tree = self.TREE_TIME
        speed = L // t_tree
        t_bridge = (L + B) // speed

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
                "火车有长度，过桥时要从车头上桥一直到车尾离桥，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "求所用时间或桥长——这就是火车过桥问题！",
                font_size=26, color=WHITE,
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

            feature_title = self.safe_text("插旗法的三个要点", font_size=32, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.55, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "在车尾插旗", "标记开始过桥与完全过桥的位置"),
                ("2", "两旗距离是路程", "过桥路程 = 火车长 + 桥长"),
                ("3", "先求速度再求时间", "过树可得速度，再算过桥时间"),
            ]
            feature_groups = self.layout_numbered_features(
                features,
                top_y=feature_title.get_bottom()[1] - 0.45,
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：过树与过桥"):
            prob_all = self.make_problem_box(
                f"题目：长{L}米的火车用{t_tree}秒经过一棵树，",
                f"同样速度通过长{B}米的大桥，需要多长时间？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_train_bridge_diagram(
            draw_y,
            train_len=L,
            bridge_len=B,
            tree_time=t_tree,
            show_hint=True,
        )

        # ── 图解1：画出两次火车位置 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出开始与结束位置"):
            s1 = self.step_label("第一步：画出车头刚上桥与车尾刚离桥时的火车")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["train1"], shift=RIGHT * 0.1), run_time=0.55)
            self.play(FadeIn(diag["train2"], shift=RIGHT * 0.1), run_time=0.55)
            self.safe_subtitle("左边是开始过桥，右边是完全过桥", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：在车尾插旗 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "车尾插旗"):
            self.add(prob_all, diag["hint"], diag["trains"])
            s2 = self.step_label("第二步：在两次的车尾处各插一面旗")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["flag1"], shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(diag["flag2"], shift=UP * 0.15), run_time=0.5)
            self.safe_subtitle("看车尾：从这面旗到那面旗，就是火车行驶的路程", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标桥长与两旗路程 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出路程关系"):
            self.add(
                prob_all, diag["hint"], diag["trains"], diag["flags"],
            )
            s3 = self.step_label("第三步：标出桥长，看出两旗距离=车长+桥长")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(FadeIn(diag["bridge_block"]), run_time=0.55)
            self.play(FadeIn(diag["path_arrow"]), FadeIn(diag["path_block"]), run_time=0.6)
            self.play(
                diag["path_lab_q"].animate.set_opacity(0),
                diag["path_lab_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"过桥路程 = {L}+{B}={L + B}（米）",
                wait=5,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求速度与过桥时间 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求速度与时间"):
            self.add(
                prob_all, diag["hint"], diag["trains"], diag["flags"],
                diag["bridge_block"], diag["path_arrow"], diag["path_block"],
                diag["notes"],
            )
            s4 = self.step_label("第四步：用过树求速度，再求过桥时间")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.3)
            self.play(diag["note_speed"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.8)
            self.play(diag["note_time"].animate.set_opacity(1), run_time=0.5)
            self.safe_subtitle(
                f"（{L}+{B}）÷（{L}÷{t_tree}）={t_bridge}（秒）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["trains"], diag["flags"],
            diag["bridge_block"], diag["path_arrow"], diag["path_block"],
            diag["notes"],
        )

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step = self.safe_text(
                f"（{L}＋{B}）÷（{L}÷{t_tree}）={t_bridge}（秒）",
                font_size=24, color=WHITE,
            )
            step_note = self.safe_text(
                "（过桥路程 ÷ 过树所得速度）",
                font_size=18, color=GREY_B,
            )
            formula_rows = VGroup(step, step_note).arrange(
                DOWN, buff=0.28, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)

            self.play(FadeIn(step), run_time=0.55)
            self.wait(1.3)
            self.play(FadeIn(step_note), run_time=0.45)
            self.wait(1.0)

            answer_text = self.safe_text(
                f"答：需要{t_bridge}秒。",
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
            self.safe_subtitle("火车通过大桥的路程 = 火车长 + 桥长", wait=5)
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
