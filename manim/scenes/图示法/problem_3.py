"""
第3讲 移多补少问题 — 画图解题法（图示法）

母题：芳芳有14朵花，晶晶有10朵花。芳芳给晶晶几朵花，两人的花就同样多？
答案：14-10=4，4的一半是2，芳芳给晶晶2朵花。

用法:
  cd manim/scenes/图示法
  python -m manim problem_3.py Problem3Scene -qh

渲染后:
  python ../_shared/post_render.py --lesson 3 \\
    --rendered media/videos/problem_3/1080p60/Problem3Scene.mp4
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCENES = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SCENES / "_shared"))

from lesson_base import MathLessonScene  # noqa: E402
from manim import *
import numpy as np


class Problem3Scene(MathLessonScene):
    EXAMPLE_INDEX = 0

    @staticmethod
    def _remove_from_tree(root: Mobject, target: Mobject) -> bool:
        """从 VGroup 树中摘掉子物体（FadeOut 后仍留在树中会导致缩放时复现）。"""
        if target in root.submobjects:
            root.remove(target)
            return True
        for child in list(root.submobjects):
            if Problem3Scene._remove_from_tree(child, target):
                return True
        return False

    def _play_draw_part(self, part: Mobject) -> None:
        if isinstance(part, Circle):
            self.play(Create(part), run_time=0.35)
        elif isinstance(part, VGroup) and len(part) > 0 and isinstance(part[0], Dot):
            self.play(FadeIn(part, scale=0.8), run_time=0.35)
        elif isinstance(part, (Text, VGroup)):
            self.play(FadeIn(part, shift=RIGHT * 0.15), run_time=0.4)
        else:
            self.play(Create(part), run_time=0.6)

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        more_count, less_count = 14, 10
        more_name, less_name = "芳芳", "晶晶"

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
                "两部分数量不一样，从多的那边拿出一些补给少的，", font_size=28, color=WHITE,
            )
            s1_body2 = self.safe_text(
                "让两边变得同样多——这就是移多补少问题！", font_size=28, color=WHITE,
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
                stroke_width=1.5,
                color=GREY_B,
                stroke_opacity=0.25,
            )

            feature_title = self.safe_text("移多补少问题的三个特征", font_size=34, color=YELLOW)
            feature_title.move_to(np.array([0, divider_y - 0.60, 0]))
            self.clamp_content(feature_title)

            features = [
                ("1", "两部分数量不相等", "比如：芳芳14朵，晶晶10朵"),
                ("2", "从多的移给少的", "不是全部给，只给「多出的一半」"),
                ("3", "移完后两边同样多", "给出的量 = 差量 ÷ 2"),
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
        with self.segment("question", "题目", "segments/02.mp4", "读题：找出关键信息"):
            prob_all = self.make_problem_box(
                "题目：芳芳有14朵花，晶晶有10朵花。",
                "芳芳给晶晶几朵花，两人的花就同样多？",
            )
            self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
            self.wait(4)

        draw_y = self.layout["draw_y"]
        diag = self.make_transfer_balance_diagram(
            more_count, less_count, draw_y,
            more_name=more_name, less_name=less_name,
        )
        diagram = diag["diagram"]

        # ── 图解1：画圆圈 ──
        with self.segment("draw-1", "1", "segments/03.mp4", "用圆圈表示两人的花"):
            s1 = self.step_label("第一步：用圆圈表示两人的花")
            self.add(prob_all)
            self.play(FadeIn(s1), run_time=0.5)
            for part in diag["draw_order"]:
                self._play_draw_part(part)
            self.safe_subtitle(
                "1个圆圈代表1朵花；数量较多时，可以用省略号表示",
                wait=3,
            )
            self.wait(1)
            self.play(FadeOut(s1), run_time=0.3)

        # ── 图解2：对齐相同部分 ──
        with self.segment("draw-2", "2", "segments/04.mp4", "标出同样多的部分"):
            self.add(prob_all, diagram)
            s2 = self.step_label("第二步：标出同样多的部分")
            self.play(FadeIn(s2), run_time=0.5)
            same_anims = []
            for c in diag["same_circles_more"]:
                same_anims.append(c.animate.set_color(TEAL_D).set_fill(TEAL_D, opacity=0.25))
            for c in diag["same_circles_less"]:
                same_anims.append(c.animate.set_color(TEAL_D).set_fill(TEAL_D, opacity=0.25))
            if diag["same_ellipsis_more"] is not None:
                same_anims.append(diag["same_ellipsis_more"].animate.set_color(TEAL_D))
            if diag["same_ellipsis_less"] is not None:
                same_anims.append(diag["same_ellipsis_less"].animate.set_color(TEAL_D))
            self.play(*same_anims, run_time=0.7)
            self.safe_subtitle("上下两行左对齐的部分，表示同样多的花", wait=4)
            self.play(FadeOut(s2), run_time=0.3)

        # ── 图解3：标出差量 ──
        brace_more = more_label = brace_less = less_label = None
        brace_extra_ref = extra_label_ref = None
        with self.segment("draw-3", "3", "segments/05.mp4", "标出多出的数量"):
            self.add(prob_all, diagram)
            s3 = self.step_label("第三步：标出多出的数量")
            self.play(FadeIn(s3), run_time=0.5)
            # 括号须覆盖整行（含省略号），不能用子组首尾圆圈当端点
            brace_more = Brace(diag["more_brace_span"], direction=UP, buff=0.10).set_color(YELLOW)
            more_label = self.safe_text(f"{more_count}朵", font_size=22, color=YELLOW)
            more_label.next_to(brace_more, UP, buff=0.08)
            brace_less = Brace(diag["less_brace_span"], direction=DOWN, buff=0.10).set_color(PURPLE_A)
            less_label = self.safe_text(f"{less_count}朵", font_size=22, color=PURPLE_A)
            less_label.next_to(brace_less, DOWN, buff=0.08)
            self.play(
                FadeIn(brace_more), FadeIn(more_label),
                FadeIn(brace_less), FadeIn(less_label),
                run_time=0.8,
            )
            if diag["extra_brace_span"] is not None:
                brace_extra = Brace(
                    diag["extra_brace_span"], direction=UP, buff=0.45,
                ).set_color(RED)
                extra_label = self.safe_text(f"多{diag['diff']}朵", font_size=22, color=RED)
                extra_label.next_to(brace_extra, UP, buff=0.08)
                extra_anims = [FadeIn(brace_extra), FadeIn(extra_label)]
                for c in diag["extra_circles"]:
                    extra_anims.insert(0, c.animate.set_color(RED).set_fill(RED, opacity=0.3))
                if diag["extra_ellipsis"] is not None:
                    extra_anims.append(diag["extra_ellipsis"].animate.set_color(RED))
                self.play(*extra_anims, run_time=0.6)
            self.safe_subtitle(
                f"{more_name}比{less_name}多 {more_count}-{less_count}={diag['diff']}（朵）",
                wait=4,
            )
            self.play(FadeOut(s3), run_time=0.3)
            if diag["extra_brace_span"] is not None:
                brace_extra_ref = brace_extra
                extra_label_ref = extra_label

        # ── 图解4：移出一半 ──
        transfer_arrow = transfer_hint = give_dashed = moving_copies = None
        with self.segment("draw-4", "4", "segments/06.mp4", "多出的一半补给少的"):
            extras = [prob_all, diagram, brace_more, more_label, brace_less, less_label]
            if diag["extra_brace_span"]:
                extras.extend([brace_extra_ref, extra_label_ref])
            self.add(*extras)
            s4 = self.step_label("第四步：把多出的一半补给少的")
            self.play(FadeIn(s4), run_time=0.5)

            circle_r = diag["circle_r"]
            give_circles = diag["give_circles"]
            received_targets = diag["received_circles"]

            if len(give_circles) > 0 and len(received_targets) > 0:
                give_dashed = VGroup()
                moving_copies = VGroup()
                for c in give_circles:
                    center = c.get_center()
                    dashed = DashedVMobject(
                        Circle(radius=circle_r, color=GREY_B, stroke_width=2),
                        num_dashes=10,
                    )
                    dashed.set_stroke(GREY_B, width=2, opacity=0.55)
                    dashed.move_to(center)
                    give_dashed.add(dashed)
                    copy = self._received_circle(circle_r)
                    copy.move_to(center)
                    moving_copies.add(copy)

                transfer_anims = []
                for i, c in enumerate(give_circles):
                    transfer_anims.append(
                        Succession(
                            TransformFromCopy(c, moving_copies[i]),
                            AnimationGroup(
                                FadeOut(c),
                                Create(give_dashed[i]),
                            ),
                            moving_copies[i].animate.move_to(
                                received_targets[i].get_center(),
                            ),
                        ),
                    )
                self.play(LaggedStart(*transfer_anims, lag_ratio=0.18), run_time=1.6)

                # 移走动画后从图解树中彻底移除实线圆，避免作答段缩放时复现
                for c in give_circles:
                    self._remove_from_tree(diagram, c)
                    c.set_opacity(0)

                arrow_start = give_dashed.get_center() + DOWN * 0.12
                arrow_end = moving_copies.get_center() + UP * 0.12
                transfer_arrow = Arrow(
                    arrow_start, arrow_end, buff=0.08, color=ORANGE, stroke_width=4,
                )
                transfer_hint = self.safe_text(
                    f"给{diag['transfer_half']}朵", font_size=22, color=ORANGE,
                )
                transfer_hint.next_to(transfer_arrow, RIGHT, buff=0.12)
                self.play(GrowArrow(transfer_arrow), FadeIn(transfer_hint), run_time=0.7)

            self.safe_subtitle(
                f"芳芳最后{diag['transfer_half']}朵虚线表示移走；"
                f"{less_name}补上{diag['transfer_half']}朵后，两人一样多",
                wait=4,
            )
            self.wait(2)
            self.play(FadeOut(s4), run_time=0.3)

        diagram_all = VGroup(
            diagram,
            brace_more, more_label, brace_less, less_label,
        )
        if diag["extra_brace_span"]:
            diagram_all.add(brace_extra_ref, extra_label_ref)
        if transfer_arrow is not None:
            diagram_all.add(transfer_arrow, transfer_hint)
        if give_dashed is not None:
            diagram_all.add(give_dashed)
        if moving_copies is not None and len(moving_copies) > 0:
            diagram_all.add(moving_copies)

        # ── 书面答题 ──
        left_x = self.written_left_x()
        with self.segment("written", "作答", "segments/07.mp4", "书面答题：分析、列式与规范作答"):
            self.add(prob_all, diagram_all)
            written_diagram_scale = self.place_diagram_for_written(diagram_all)

            ana1 = self.safe_text(
                f"{more_name}比{less_name}多 {more_count} - {less_count} = {diag['diff']}（朵）",
                font_size=24, color=WHITE,
            )
            ana2 = self.safe_text(
                f"{diag['diff']}朵的一半是 {diag['transfer_half']} 朵",
                font_size=24, color=TEAL_D,
            )
            ana_group = VGroup(ana1, ana2).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            ana_group.move_to(np.array([
                left_x + ana_group.width / 2,
                self.written_left_y(0.95), 0,
            ]))
            ana_group.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(ana_group)
            for ana in [ana1, ana2]:
                self.play(FadeIn(ana, shift=RIGHT * 0.3), run_time=0.5)
                self.wait(2)
            self.wait(1)
            self.play(FadeOut(ana_group), run_time=0.5)

            formula = self.safe_mathtex(
                rf"{more_count} - {less_count} = {diag['diff']}", font_size=36, color=WHITE,
            )
            half_text = self.safe_text(f"{diag['diff']}朵的一半是{diag['transfer_half']}朵", font_size=28, color=GREY_B)
            formula_row = VGroup(formula, half_text).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            formula_row.move_to(np.array([left_x + formula_row.width / 2, self.written_left_y(0.4), 0]))
            formula_row.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(formula_row)
            self.play(FadeIn(formula_row), run_time=0.6)
            self.wait(2)

            answer_text = self.safe_text(
                f"答：{more_name}给{less_name}{diag['transfer_half']}朵花，两人的花就同样多。",
                font_size=32, color=YELLOW,
            )
            answer_text.move_to(np.array([
                left_x + answer_text.width / 2,
                formula_row.get_bottom()[1] - 0.8, 0,
            ]))
            answer_text.align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(answer_text)
            highlight_box = SurroundingRectangle(answer_text, color=RED, buff=0.12, corner_radius=0.1)
            self.play(FadeIn(answer_text, shift=UP * 0.2), run_time=0.8)
            self.play(Create(highlight_box), run_time=0.5)
            self.safe_subtitle("差量的一半，就是要移过去的数量", wait=5)
            self.wait(2)
            self.play(
                FadeOut(formula_row), FadeOut(answer_text),
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
