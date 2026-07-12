"""
MathLessonScene — DrawMathHub 讲题 Scene 基类
"""

from __future__ import annotations

import inspect
import json
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import numpy as np

_SHARED_DIR = Path(__file__).resolve().parent
if str(_SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_DIR))

from safe_video import SafeScene  # noqa: E402
from video_export import FULL_VIDEO_SEGMENT_GAP, PROJECT_ROOT, SegmentRecorder  # noqa: E402

from manim import *  # noqa: F403


def lesson_number_from_script(path: Path) -> int:
    """从脚本文件名 problem_{lessonNumber}.py 解析讲次，与 public/data/problems/{n}.json 一致。"""
    m = re.fullmatch(r"problem_(\d+)", path.stem)
    if not m:
        raise ValueError(f"脚本须命名为 problem_{{lessonNumber}}.py，当前: {path.name}")
    return int(m.group(1))


class MathLessonScene(SafeScene):
    """小学数学画图解题法 — 可分段导出的讲题基类。"""

    LESSON_NUMBER: int = 0
    EXAMPLE_INDEX: int = 0

    def setup(self):
        super().setup()
        if self.LESSON_NUMBER == 0:
            script = Path(inspect.getfile(type(self)))
            self.LESSON_NUMBER = lesson_number_from_script(script)
        self.segment_recorder: SegmentRecorder | None = None
        self.problem_data: dict[str, Any] = {}
        self.layout: dict[str, float] = {}

    def load_problem(self) -> dict[str, Any]:
        path = PROJECT_ROOT / "public" / "data" / "problems" / f"{self.LESSON_NUMBER}.json"
        self.problem_data = json.loads(path.read_text(encoding="utf-8"))
        return self.problem_data

    def init_video_recorder(self) -> SegmentRecorder:
        data = self.problem_data or self.load_problem()
        problem_uuid = data["id"]
        if self.EXAMPLE_INDEX == 0:
            example_uuid = data["mainProblem"]["id"]
        else:
            example_uuid = data["extensionProblems"][self.EXAMPLE_INDEX - 1]["id"]
        self.segment_recorder = SegmentRecorder(problem_uuid, example_uuid)
        return self.segment_recorder

    @property
    def main_problem(self) -> dict[str, str]:
        return self.problem_data["mainProblem"]

    @property
    def method_type(self) -> str:
        return self.problem_data["methodType"]

    @property
    def title_text(self) -> str:
        return self.problem_data["title"]

    PROB_TOP_GAP = 0.35

    def init_layout_after_title(self, prob_h: float = 1.0) -> None:
        title_bottom = self._title_group.get_bottom()[1]
        prob_top = title_bottom - self.PROB_TOP_GAP
        prob_bottom = prob_top - prob_h
        draw_area_top = prob_bottom - 0.5
        draw_area_bottom = self.safe_bottom + 0.3
        self.layout = {
            "prob_top": prob_top,
            "prob_h": prob_h,
            "prob_bottom": prob_bottom,
            "step_y": prob_bottom - 0.25,
            "draw_y": (draw_area_top + draw_area_bottom) / 2,
            "draw_area_top": draw_area_top,
            "draw_area_bottom": draw_area_bottom,
            "left_x": self.safe_left + 0.8,
        }

    def make_problem_box(self, line1: str, line2: str | None = None) -> VGroup:
        prob_h = self.layout["prob_h"]
        prob_top = self.layout["prob_top"]
        prob_y_center = prob_top - prob_h / 2

        prob_bg = RoundedRectangle(
            corner_radius=0.15,
            width=self.safe_right - self.safe_left - 0.6,
            height=prob_h,
            color=TEAL_D,
            fill_opacity=0.12,
            fill_color=TEAL_D,
        )
        prob_bg.move_to(np.array([0, prob_y_center, 0]))
        self.clamp_content(prob_bg)

        prob_line1 = self.safe_text(line1, font_size=24, color=WHITE)
        lines = [prob_line1]
        if line2:
            prob_line2 = self.safe_text(line2, font_size=26, color=YELLOW)
            prob_line2.shift(RIGHT * 0.7)
            lines.append(prob_line2)

        prob_text = VGroup(*lines).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        prob_text.move_to(prob_bg.get_center())
        prob_text.align_to(prob_bg.get_left() + RIGHT * 0.25, LEFT)
        self.clamp_content(prob_text)
        return VGroup(prob_bg, prob_text)

    def step_label(self, text: str) -> Mobject:
        label = self.safe_text(text, font_size=26, color=ORANGE)
        label.move_to(np.array([0, self.layout["step_y"], 0]))
        self.clamp_content(label)
        return label

    def _person_circle(self, radius: float = 0.18, *, color=WHITE, stroke_width: int = 2) -> Circle:
        return Circle(radius=radius, color=color, stroke_width=stroke_width)

    def _horizontal_ellipsis(
        self, *, color=GREY_B, dot_r: float = 0.08, count: int = 4, buff: float = 0.1,
    ) -> VGroup:
        """横向省略号，与圆圈同行垂直居中。"""
        return VGroup(*[
            Dot(radius=dot_r, color=color, fill_opacity=1) for _ in range(count)
        ]).arrange(RIGHT, buff=buff)

    def make_between_diagram(
        self,
        left_rank: int,
        right_rank: int,
        draw_y: float,
        *,
        circle_r: float = 0.18,
        gap: float = 0.42,
        prefix_show_max: int = 5,
        prefix_tail: int = 2,
        between_edge: int = 1,
        suffix_extra: int = 2,
    ) -> dict[str, Any]:
        """
        之间问题示意图：前缀圈/省略号 + 左关键人 + 之间(边圈+横省略号+边圈)
        + 右关键人 + 后缀冗余圈。人数再大也不画满，仅示意起止。
        """
        parts: list[Mobject] = []
        draw_order: list[Mobject] = []

        prefix_circles = VGroup()
        prefix_ellipsis = None
        before_count = left_rank - 1
        if before_count > 0:
            if before_count <= prefix_show_max:
                prefix_circles = VGroup(*[
                    self._person_circle(circle_r) for _ in range(before_count)
                ]).arrange(RIGHT, buff=gap)
                parts.append(prefix_circles)
                draw_order.append(prefix_circles)
            else:
                prefix_ellipsis = self._horizontal_ellipsis()
                prefix_circles = VGroup(*[
                    self._person_circle(circle_r) for _ in range(prefix_tail)
                ]).arrange(RIGHT, buff=gap)
                parts.extend([prefix_ellipsis, prefix_circles])
                draw_order.extend([prefix_ellipsis, prefix_circles])

        left_person = self._person_circle(circle_r)
        parts.append(left_person)
        draw_order.append(left_person)

        between_count = right_rank - left_rank - 1
        between_start = VGroup()
        between_ellipsis = None
        between_end = VGroup()
        between_all = VGroup()

        if between_count > 0:
            if between_count <= between_edge * 2:
                between_all = VGroup(*[
                    self._person_circle(circle_r) for _ in range(between_count)
                ]).arrange(RIGHT, buff=gap)
                parts.append(between_all)
                draw_order.append(between_all)
            else:
                between_start = VGroup(*[
                    self._person_circle(circle_r) for _ in range(between_edge)
                ]).arrange(RIGHT, buff=gap)
                between_ellipsis = self._horizontal_ellipsis()
                between_end = VGroup(*[
                    self._person_circle(circle_r) for _ in range(between_edge)
                ]).arrange(RIGHT, buff=gap)
                parts.extend([between_start, between_ellipsis, between_end])
                draw_order.extend([between_start, between_ellipsis, between_end])

        right_person = self._person_circle(circle_r)
        parts.append(right_person)
        draw_order.append(right_person)

        suffix_circles = VGroup()
        if suffix_extra > 0:
            suffix_circles = VGroup(*[
                self._person_circle(circle_r) for _ in range(suffix_extra)
            ]).arrange(RIGHT, buff=gap)
            parts.append(suffix_circles)
            draw_order.append(suffix_circles)

        row = VGroup(*parts).arrange(RIGHT, buff=gap)
        row.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(row)

        rank_left_anchor = (
            prefix_circles[0] if len(prefix_circles) > 0 else left_person
        )
        if between_ellipsis is not None:
            between_region = VGroup(between_start, between_ellipsis, between_end)
            between_brace_start = between_start[0]
            between_brace_end = between_end[-1]
        elif len(between_all) > 0:
            between_region = between_all
            between_brace_start = between_all[0]
            between_brace_end = between_all[-1]
        else:
            between_region = VGroup()
            between_brace_start = left_person
            between_brace_end = right_person

        between_zone_circles = VGroup()
        if between_ellipsis is not None:
            if len(between_start) > 0:
                between_zone_circles.add(*between_start)
            if len(between_end) > 0:
                between_zone_circles.add(*between_end)
        elif len(between_all) > 0:
            between_zone_circles.add(*between_all)

        return {
            "row": row,
            "draw_order": draw_order,
            "prefix_circles": prefix_circles,
            "prefix_ellipsis": prefix_ellipsis,
            "left_person": left_person,
            "between_start": between_start,
            "between_ellipsis": between_ellipsis,
            "between_end": between_end,
            "between_all": between_all,
            "between_region": between_region,
            "between_zone_circles": between_zone_circles,
            "right_person": right_person,
            "suffix_circles": suffix_circles,
            "rank_left_anchor": rank_left_anchor,
            "between_brace_start": between_brace_start,
            "between_brace_end": between_brace_end,
            "circle_r": circle_r,
        }

    def make_queue_total_diagram(
        self,
        front_count: int,
        back_count: int,
        draw_y: float,
        *,
        circle_r: float = 0.18,
        gap: float = 0.42,
        zone_show_max: int = 5,
        zone_head: int = 2,
        zone_tail: int = 2,
    ) -> dict[str, Any]:
        """
        排队问题（求全队总人数）示意图：
        前区圈/省略号 + 中间关键人 + 后区圈/省略号。人数再大也不画满。
        front_count / back_count 均不含中间关键人。
        """
        parts: list[Mobject] = []
        draw_order: list[Mobject] = []
        front_ellipsis: VGroup | None = None
        back_ellipsis: VGroup | None = None
        front_zone_circles = VGroup()
        back_zone_circles = VGroup()
        front_brace_start: Mobject | None = None
        front_brace_end: Mobject | None = None
        back_brace_start: Mobject | None = None
        back_brace_end: Mobject | None = None

        if front_count > 0:
            if front_count <= zone_show_max:
                front_zone = VGroup(*[
                    self._person_circle(circle_r) for _ in range(front_count)
                ]).arrange(RIGHT, buff=gap)
                front_zone_circles = front_zone
                parts.append(front_zone)
                draw_order.append(front_zone)
                front_brace_start = front_zone[0]
                front_brace_end = front_zone[-1]
            else:
                front_head = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_head)
                ]).arrange(RIGHT, buff=gap)
                front_ellipsis = self._horizontal_ellipsis()
                front_tail = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_tail)
                ]).arrange(RIGHT, buff=gap)
                front_zone = VGroup(front_head, front_ellipsis, front_tail)
                front_zone_circles.add(*front_head, *front_tail)
                parts.extend([front_head, front_ellipsis, front_tail])
                draw_order.extend([front_head, front_ellipsis, front_tail])
                front_brace_start = front_head[0]
                front_brace_end = front_tail[-1]
        else:
            front_zone = VGroup()

        center_person = self._person_circle(circle_r)
        parts.append(center_person)
        draw_order.append(center_person)

        if back_count > 0:
            if back_count <= zone_show_max:
                back_zone = VGroup(*[
                    self._person_circle(circle_r) for _ in range(back_count)
                ]).arrange(RIGHT, buff=gap)
                back_zone_circles = back_zone
                parts.append(back_zone)
                draw_order.append(back_zone)
                back_brace_start = back_zone[0]
                back_brace_end = back_zone[-1]
            else:
                back_head = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_head)
                ]).arrange(RIGHT, buff=gap)
                back_ellipsis = self._horizontal_ellipsis()
                back_tail = VGroup(*[
                    self._person_circle(circle_r) for _ in range(zone_tail)
                ]).arrange(RIGHT, buff=gap)
                back_zone = VGroup(back_head, back_ellipsis, back_tail)
                back_zone_circles.add(*back_head, *back_tail)
                parts.extend([back_head, back_ellipsis, back_tail])
                draw_order.extend([back_head, back_ellipsis, back_tail])
                back_brace_start = back_head[0]
                back_brace_end = back_tail[-1]
        else:
            back_zone = VGroup()

        row = VGroup(*parts).arrange(RIGHT, buff=gap)
        row.move_to(np.array([0, draw_y, 0]))
        self.clamp_content(row)

        if front_brace_start is None:
            front_brace_start = center_person
            front_brace_end = center_person
        if back_brace_start is None:
            back_brace_start = center_person
            back_brace_end = center_person

        total_brace_start = front_brace_start
        total_brace_end = back_brace_end

        return {
            "row": row,
            "draw_order": draw_order,
            "front_zone": front_zone,
            "front_ellipsis": front_ellipsis,
            "front_zone_circles": front_zone_circles,
            "center_person": center_person,
            "back_zone": back_zone,
            "back_ellipsis": back_ellipsis,
            "back_zone_circles": back_zone_circles,
            "front_brace_start": front_brace_start,
            "front_brace_end": front_brace_end,
            "back_brace_start": back_brace_start,
            "back_brace_end": back_brace_end,
            "total_brace_start": total_brace_start,
            "total_brace_end": total_brace_end,
            "circle_r": circle_r,
        }

    def make_numbered_feature_row(
        self,
        num: str,
        main_text: str,
        sub_text: str,
        *,
        circle_r: float = 0.30,
        main_size: int = 28,
        sub_size: int = 22,
        max_text_width: float | None = None,
    ) -> VGroup:
        """序号圆 + 主句/副句 特征行。"""
        num_circle = Circle(
            radius=circle_r, color=TEAL_D, fill_opacity=0.8, fill_color=TEAL_D,
        )
        num_label = Text(num, font_size=26, color=WHITE, font=self.DEFAULT_FONT)
        num_label.move_to(num_circle.get_center())
        num_group = VGroup(num_circle, num_label)
        main_t = self.safe_text(main_text, font_size=main_size, color=WHITE)
        sub_t = self.safe_text(sub_text, font_size=sub_size, color=GREY_B)
        right_group = VGroup(main_t, sub_t).arrange(DOWN, buff=0.10, aligned_edge=LEFT)
        if max_text_width is not None:
            self.fit_to_width(right_group, max_text_width)
        return VGroup(num_group, right_group).arrange(RIGHT, buff=0.35, aligned_edge=UP)

    def layout_numbered_features(
        self,
        items: list[tuple[str, str, str]],
        *,
        top_y: float,
        row_step: float = 1.08,
        two_column_min: int = 4,
        left_margin: float = 0.8,
        col_inner_gap: float = 0.45,
    ) -> list[VGroup]:
        """
        特征列表：≤3 条单列左对齐；≥4 条左右两列（左列 ceil(n/2)）。
        top_y 为第一条特征行的中心纵坐标。
        """
        use_two_cols = len(items) >= two_column_min
        col_text_w = (self.safe_right - self.safe_left) / 2 - 1.1 if use_two_cols else None
        rows = [
            self.make_numbered_feature_row(
                num, main, sub, max_text_width=col_text_w,
            )
            for num, main, sub in items
        ]

        left_x = self.safe_left + left_margin
        if not use_two_cols:
            for i, row in enumerate(rows):
                row.move_to(np.array([0, top_y - i * row_step, 0]))
                row.align_to(np.array([left_x, 0, 0]), LEFT)
                self.clamp_content(row)
            return rows

        mid = (len(items) + 1) // 2
        col_center = (self.safe_left + self.safe_right) / 2
        right_x = col_center + col_inner_gap

        for i in range(mid):
            rows[i].move_to(np.array([0, top_y - i * row_step, 0]))
            rows[i].align_to(np.array([left_x, 0, 0]), LEFT)
            self.clamp_content(rows[i])
        for j, idx in enumerate(range(mid, len(items))):
            rows[idx].move_to(np.array([0, top_y - j * row_step, 0]))
            rows[idx].align_to(np.array([right_x, 0, 0]), LEFT)
            self.clamp_content(rows[idx])
        return rows

    def play_keypoints_only(
        self,
        key_points: str,
        wait: float = 6.0,
        *,
        diagram: Mobject | None = None,
        from_scale: float = 0.55,
    ) -> None:
        """关键点拨：无图解时正文居中；有图解时放大居中，点拨文字在图解下方。"""
        if diagram is None:
            self.clear()
            if self._title_group is not None:
                self.add(self._title_group)

            hint_title = self.place_section_title("关键点拨", font_size=32)
            body = self.safe_wrapped_text(key_points, font_size=28, color=WHITE)
            body.move_to(self.content_center)
            self.fit_content(body)

            self.play(FadeIn(hint_title), run_time=0.5)
            self.play(FadeIn(body, shift=UP * 0.2), run_time=0.5)
            self.wait(wait)
            self.play(FadeOut(VGroup(hint_title, body)), run_time=0.3)
            return

        if self._title_group is not None:
            self.add(self._title_group)

        hint_title = self.place_section_title("关键点拨", font_size=32)
        self.play(FadeIn(hint_title), run_time=0.5)

        draw_y = self.layout.get("draw_y", self.content_center[1])
        diagram.generate_target()
        diagram.target.scale(1 / from_scale)
        diagram.target.move_to(np.array([0, draw_y + 0.2, 0]))
        self.clamp_content(diagram.target)
        self.play(MoveToTarget(diagram), run_time=1.0)

        body = self.safe_wrapped_text(key_points, font_size=26, color=WHITE)
        body.next_to(diagram, DOWN, buff=0.45)
        body.move_to(np.array([0, body.get_center()[1], 0]))
        self.clamp_content(body)

        self.play(FadeIn(body, shift=UP * 0.15), run_time=0.5)
        self.wait(wait)
        self.play(FadeOut(VGroup(hint_title, diagram, body)), run_time=0.3)

    @contextmanager
    def segment(
        self,
        role: str,
        label: str,
        file: str,
        hint: str = "",
        *,
        gap_after: bool = True,
    ) -> Generator[None, None, None]:
        if self.segment_recorder is None:
            raise RuntimeError("请先调用 init_video_recorder()")
        self.segment_recorder.begin(role, label, file, hint, scene=self)
        try:
            yield
        finally:
            self.segment_recorder.end(self)
            if gap_after:
                self.wait(FULL_VIDEO_SEGMENT_GAP)

    def finalize_lesson(self, *, write_manifest: bool = True) -> Path | None:
        if self.segment_recorder is None:
            raise RuntimeError("请先调用 init_video_recorder()")
        if write_manifest:
            return self.segment_recorder.write_manifest()
        return None
