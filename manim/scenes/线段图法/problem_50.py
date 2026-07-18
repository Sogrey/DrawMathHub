"""
第50讲 纳税问题 — 画图解题法（线段图法）

母题：工资 7200，免征额 5000，税率 3%。求个税。
答案：(7200−5000)×3%=66（元）

用法:
  cd manim/scenes/线段图法
  python -m manim problem_50.py Problem50Scene -ql
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem50Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    SALARY = 7200
    EXEMPTION = 5000
    RATE = 0.03

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        salary = self.SALARY
        exemption = self.EXEMPTION
        rate_pct = int(round(self.RATE * 100))

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
                "工资里先划出免征额，剩下的才是应纳税所得额，",
                font_size=26, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "再用「应纳税额＝应纳税所得额×税率」来算！",
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

            feature_title = self.safe_text("纳税计算的三个要点", font_size=30, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.52, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "画出工资全长", "用线段表示本月工资总额"),
                ("2", "分出免征额", "剩下的就是应纳税所得额"),
                ("3", "所得额×税率", "得到应缴纳的个人所得税"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：求个税"):
            prob_all = self.make_problem_box(
                f"题目：工资{salary}元，免征额{exemption}元，超出部分按{rate_pct}%纳税。",
                "这个月应缴纳个人所得税多少元？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"] - 0.28
        diag = self.make_tax_income_diagram(
            draw_y,
            salary=salary,
            exemption=exemption,
            rate=self.RATE,
            show_hint=False,
        )
        taxable = diag["taxable"]
        tax = diag["tax"]

        # ── 图解1：画出工资并分出免征额 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "画出工资线段"):
            s1 = self.step_label("第一步：画出工资全长，标出免征额")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            self.play(Create(diag["main"]), FadeIn(diag["ticks"]), run_time=0.55)
            self.play(diag["salary_lab"].animate.set_opacity(1), run_time=0.4)
            self.play(
                diag["exempt_bar"].animate.set_opacity(1),
                run_time=0.45,
            )
            diag["exempt_bar"].set_fill(TEAL_D, opacity=0.30)
            self.play(
                diag["exempt_lab"].animate.set_opacity(1),
                diag["exempt_tag"].animate.set_opacity(1),
                run_time=0.45,
            )
            self.safe_subtitle(
                f"左边 {exemption} 元是个税免征额，不用交税",
                wait=4,
            )
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：标出应纳税所得额 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出应纳税所得额"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["salary_lab"], diag["exempt_bar"],
                diag["exempt_lab"], diag["exempt_tag"],
            )
            s2 = self.step_label("第二步：余下部分就是应纳税所得额")
            self.play(FadeIn(s2), run_time=0.5)
            self.play(diag["tax_bar"].animate.set_opacity(1), run_time=0.45)
            diag["tax_bar"].set_fill(ORANGE, opacity=0.30)
            self.play(diag["tax_lab_q"].animate.set_opacity(1), run_time=0.45)
            self.play(diag["note_taxable"].animate.set_opacity(1), run_time=0.5)
            self.wait(0.5)
            self.play(
                diag["tax_lab_q"].animate.set_opacity(0),
                diag["tax_lab_ans"].animate.set_opacity(1),
                run_time=0.5,
            )
            self.safe_subtitle(
                f"{salary}−{exemption}={taxable}（元）",
                wait=4,
            )
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标出税率 ──
        with self.segment("draw-3", "3", "segments/05.mp4", "标出税率"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["salary_lab"], diag["exempt_bar"], diag["tax_bar"],
                diag["exempt_lab"], diag["exempt_tag"], diag["tax_lab_ans"],
                diag["note_taxable"],
            )
            s3 = self.step_label("第三步：在应纳税所得额下标出税率")
            self.play(FadeIn(s3), run_time=0.5)
            self.play(
                diag["rate_brace"].animate.set_opacity(1),
                diag["rate_note"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"这一段按 {rate_pct}% 的税率缴纳",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)

        # ── 图解4：求出税额 ──
        with self.segment("draw-4", "4", "segments/06.mp4", "求出应纳税额"):
            self.add(
                prob_all, diag["main"], diag["ticks"],
                diag["salary_lab"], diag["exempt_bar"], diag["tax_bar"],
                diag["exempt_lab"], diag["exempt_tag"], diag["tax_lab_ans"],
                diag["rate_brace"], diag["rate_note"], diag["note_taxable"],
            )
            s4 = self.step_label("第四步：应纳税所得额×税率，求出税额")
            self.play(FadeIn(s4), run_time=0.5)
            self.play(diag["note_tax_q"].animate.set_opacity(1), run_time=0.45)
            self.wait(0.6)
            self.play(
                diag["note_tax_q"].animate.set_opacity(0),
                diag["note_tax_ans"].animate.set_opacity(1),
                run_time=0.55,
            )
            self.safe_subtitle(
                f"{taxable}×{rate_pct}%={tax}（元）",
                wait=5,
            )
            self.wait(1)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diag["main"], diag["ticks"],
            diag["exempt_bar"], diag["tax_bar"],
            diag["salary_lab"], diag["exempt_lab"], diag["exempt_tag"],
            diag["tax_lab_ans"], diag["rate_brace"], diag["rate_note"],
            diag["notes"],
        )

        # ── 列式作答 ──
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：列式作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            left_x = self.written_left_x()
            f1 = self.safe_text(
                f"({salary}−{exemption})×{rate_pct}%={tax}（元）",
                font_size=26, color=WHITE,
            )
            f1.move_to(np.array([
                left_x + f1.width / 2,
                self.written_left_y(0.55), 0,
            ]))
            f1.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(f1)

            answer_text = self.safe_text(
                f"答：应缴纳个人所得税{tax}元。",
                font_size=22, color=YELLOW,
            )
            answer_text.next_to(f1, DOWN, buff=0.36)
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(
                answer_text, color=RED, buff=0.12, corner_radius=0.1,
                stroke_width=2.5,
            )
            highlight_box.set_fill(opacity=0)

            self.play(FadeIn(f1), run_time=0.55)
            self.wait(1.0)
            self.play(FadeIn(answer_text, shift=UP * 0.12), run_time=0.6)
            self.play(Create(highlight_box), run_time=0.45)
            self.safe_subtitle("应纳税额＝应纳税所得额×税率", wait=5)
            self.wait(2)
            self.play(
                FadeOut(f1), FadeOut(answer_text),
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
