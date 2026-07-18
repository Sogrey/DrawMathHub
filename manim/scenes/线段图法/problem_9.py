"""
第9讲 租船问题 — 画图解题法（线段图法）

母题：34人去划船，每条船最多坐4人，至少需要租几条船？
答案：34÷4=8（条）……2（人），8+1=9（条）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_9.py Problem9Scene -qh

渲染后:
  python ..\_shared\post_render.py --lesson 9 \\
    --rendered media\videos\problem_9\1080p60\Problem9Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem9Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    TOTAL = 34
    CAPACITY = 4

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

            concept_title = self.safe_text("题型识别", font_size=36, color=YELLOW)
            concept_title.move_to(np.array([0, zone_top - 0.35, 0]))
            self.clamp_content(concept_title)

            s1_body = self.safe_text(
                "一批人分船坐，每条船有容量上限，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "问至少租几条——这就是租船问题！", font_size=28, color=WHITE,
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

            feature_title = self.safe_text("租船问题的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "用线段表示总人数", "按每条船容量切分线段"),
                ("2", "先算能坐满几条船", "34÷4=8，先租8条"),
                ("3", "有余数要进一", "剩2人也要1条船 → 8+1=9"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：34人每船4人"):
            prob_all = self.make_problem_box(
                "题目：二（1）班34人去公园划船，每条船最多坐4人，",
                "至少需要租几条船？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_boat_rental_diagram(self.TOTAL, self.CAPACITY, draw_y)
        quotient = diag["quotient"]
        remainder = diag["remainder"]
        boats = diag["boats"]

        # ── 图解1：画主线段 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画线段表示34人"):
            s1 = self.step_label("第一步：画一条线段表示34人")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(FadeIn(diag["hint"]), run_time=0.4)
            self.play(Create(diag["main_line"]), FadeIn(diag["line_block"][0]), FadeIn(diag["line_block"][2]), run_time=0.85)
            self.safe_subtitle("先画线段，代表全部34人", wait=4)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：8段每段4人 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "切8段每段4人"):
            self.add(prob_all, diag["hint"], diag["line_block"])
            s2 = self.step_label("第二步：每4人一条船，先租8条")
            self.play(FadeIn(s2), run_time=0.5)
            batch_size = 2
            segs = diag["full_segments"]
            for start in range(0, len(segs), batch_size):
                batch = segs[start:start + batch_size]
                self.play(*[FadeIn(m["parts"], shift=UP * 0.06) for m in batch], run_time=0.45)
            self.safe_subtitle(f"{self.TOTAL}里面有{quotient}个{self.CAPACITY}，先租{quotient}条船", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：余2人 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出余2人"):
            self.add(prob_all, diag["hint"], diag["line_block"], diag["full_block"])
            s3 = self.step_label("第三步：还剩2人没有船")
            self.play(FadeIn(s3), run_time=0.5)
            if diag["rem_parts"] is not None:
                self.play(FadeIn(diag["rem_parts"], shift=UP * 0.06), run_time=0.55)
            self.safe_subtitle(f"34÷4={quotient}……{remainder}，还剩{remainder}人", wait=4)
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：大括号 ──
        rem_on_screen = diag["rem_parts"] if diag["rem_parts"] is not None else VGroup()
        with self.segment("draw-4", "4", "segments/06.mp4", "标共34人与船数"):
            self.add(prob_all, diag["hint"], diag["line_block"], diag["full_block"], rem_on_screen)
            s4 = self.step_label("第四步：标总人数和需要的船数")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(GrowFromCenter(diag["people_brace"]), FadeIn(diag["people_label"]), run_time=0.55)
            self.play(GrowFromCenter(diag["boats_brace"]), FadeIn(diag["boats_label"]), run_time=0.55)
            self.safe_subtitle("上面标共34人，下面标需要几条船", wait=4)
            self.play(FadeOut(s4), run_time=0.3)

        # ── 图解5：进一法 ──
        with self.segment("draw-5", "5", "segments/07.mp4", "余2人再租1条"):
            self.add(
                prob_all, diag["hint"], diag["line_block"], diag["full_block"],
                rem_on_screen, diag["people_block"], diag["boats_block"],
            )
            s5 = self.step_label("第五步：剩余的人还要再租1条船")
            self.play(FadeIn(s5), run_time=0.5)
            self.play(FadeIn(diag["extra_boat_note"], shift=DOWN * 0.08), run_time=0.5)
            self.play(FadeIn(diag["final_boats_note"]), FadeIn(diag["rule_note"]), run_time=0.55)
            new_boats_label = self.safe_text(f"{boats} 条船", font_size=20, color=YELLOW)
            new_boats_label.move_to(diag["boats_label"].get_center())
            self.play(Transform(diag["boats_label"], new_boats_label), run_time=0.45)
            self.safe_subtitle("进一法：有余数时，商要加1", wait=4)
            self.play(FadeOut(s5), run_time=0.3)

        diagram_all = diag["layout_row"]

        # ── 书面答题 ──
        with self.segment("written", "作答", "segments/08.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            step1 = self.safe_text(
                f"{self.TOTAL}÷{self.CAPACITY}={quotient}（条）……{remainder}（人）",
                font_size=26, color=WHITE,
            )
            explain = self.safe_text(
                f"先租满{quotient}条船，还剩{remainder}人，",
                font_size=24, color=GREY_B,
            )
            explain2 = self.safe_text(
                "所有人都要有船坐，还要再租1条：",
                font_size=24, color=GREY_B,
            )
            step2 = self.safe_text(
                f"{quotient}+1={boats}（条）",
                font_size=28, color=WHITE,
            )
            formula_rows = VGroup(step1, explain, explain2, step2).arrange(
                DOWN, buff=0.22, aligned_edge=LEFT,
            )
            formula_rows.move_to(np.array([
                left_x + formula_rows.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            formula_rows.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_rows)
            self.play(FadeIn(step1), run_time=0.5)
            self.wait(0.8)
            self.play(FadeIn(explain), FadeIn(explain2), run_time=0.55)
            self.play(FadeIn(step2), run_time=0.5)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：至少需要租{boats}条船。",
                font_size=32, color=YELLOW,
            )
            answer_text.next_to(formula_rows, DOWN, buff=0.55)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
            )
            self.play(FadeIn(answer_text, shift=UP * 0.15), run_time=0.7)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("有余数用进一法：商加1", wait=5)
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
