"""
第34讲 最优化问题 — 画图解题法（流程图法）

母题：洗衣30、晾衣3；扫地8、拖地10、擦桌子5。至少多久？
答案：30＋3＝33（分）

用法:
  cd manim/scenes/流程图法
  python -m manim problem_34.py Problem34Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem34Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    WASH = 30
    HANG = 3
    SWEEP = 8
    MOP = 10
    WIPE = 5

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        wash = self.WASH
        hang = self.HANG
        sweep = self.SWEEP
        mop = self.MOP
        wipe = self.WIPE
        manual = sweep + mop + wipe
        total = wash + hang

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
                "做几件事各需一定时间，求「至少」多久做完，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "用流程图理清先后与并行——这就是流程图法！",
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

            feature_title = self.safe_text("合理安排时间的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "分清先后顺序", "有的事必须等另一件做完"),
                ("2", "找出可同时做", "洗衣机工作时可干别的"),
                ("3", "取关键路径时长", "并行取最长，再加后续串行"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：家务时间"):
            prob_all = self.make_problem_box(
                f"题目：扫地{sweep}分、拖地{mop}分、擦桌子{wipe}分，"
                f"洗衣{wash}分、晾衣{hang}分。",
                "红红帮妈妈做家务至少需要多长时间？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_chores_flow_diagram(
            draw_y,
            wash=wash, hang=hang,
            sweep=sweep, mop=mop, wipe=wipe,
            show_hint=True,
        )

        # ── 图解1：洗衣与晾衣的先后 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "洗衣后再晾衣"):
            s1 = self.step_label("第一步：洗完衣服才能晾衣服，画出关键先后")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeIn(diag["hint"]), run_time=0.3)
            self.play(FadeIn(diag["wash_box"]), run_time=0.5)
            self.play(FadeIn(diag["top_arrow"]), FadeIn(diag["hang_box"]), run_time=0.55)
            self.safe_subtitle(
                f"洗衣机 {wash} 分钟结束之后，才能晾衣 {hang} 分钟",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：洗衣期间可同时做的事 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "并行家务"):
            self.add(
                prob_all, diag["hint"], diag["top_row"], diag["notes"],
            )
            s2 = self.step_label("第二步：洗衣的同时，可以扫地、拖地、擦桌子")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(FadeIn(diag["bottom_block"]), run_time=0.65)
            self.play(
                FadeIn(diag["parallel_link"]),
                FadeIn(diag["parallel_note"]),
                run_time=0.5,
            )
            self.safe_subtitle(
                "能同时做的事情尽量同时做",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：比较并行时长 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "比较并行时间"):
            self.add(
                prob_all, diag["hint"], diag["flow"], diag["notes"],
            )
            s3 = self.step_label("第三步：比较「手动三项」和「洗衣」谁更长")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(diag["note_fit"].animate.set_opacity(1), run_time=0.55)
            self.safe_subtitle(
                f"{sweep}+{mop}+{wipe}={manual}＜{wash}，洗衣更长",
                wait=4,
            )
            self.play(diag["note_path"].animate.set_opacity(1), run_time=0.5)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出最短时间 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出最少时间"):
            self.add(
                prob_all, diag["hint"], diag["flow"], diag["notes"],
            )
            s4 = self.step_label("第四步：最短时间＝洗衣＋晾衣")
            self.play(FadeIn(s4), run_time=0.5)
            if len(diag["hint"]) > 0:
                self.play(FadeOut(diag["hint"]), run_time=0.25)
            self.play(diag["note_calc_q"].animate.set_opacity(1), run_time=0.4)
            self.wait(0.6)
            self.play(
                diag["note_calc_q"].animate.set_opacity(0),
                diag["note_calc_ans"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"{wash}＋{hang}={total}（分）",
                wait=4,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(diag["flow"], diag["notes"])

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            formula = self.safe_text(
                f"{wash}＋{hang}={total}（分）",
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
                f"答：红红帮妈妈做家务至少需要{total}分钟。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(formula, DOWN, buff=0.40)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("分清先后与并行，取关键路径", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula), FadeOut(answer_text),
                FadeOut(highlight_box), FadeOut(prob_all), run_time=0.5,
            )

        with self.segment("keypoints", "点拨", "segments/keypoints.mp4", "该题型的解题关键"):
            self.play_keypoints_only(
                mp["keyPoints"], wait=7,
                diagram=diagram_all, from_scale=written_diagram_scale,
            )

        with self.segment("end", "结尾", "segments/end.mp4", "片尾", gap_after=False):
            self.show_credits("THE END")

        self.finalize_lesson()
