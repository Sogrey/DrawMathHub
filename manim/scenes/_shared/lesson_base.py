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
from diagrams.between import BetweenDiagramMixin  # noqa: E402
from diagrams.common import DiagramCommonMixin  # noqa: E402
from diagrams.line_compare import LineCompareDiagramMixin  # noqa: E402
from diagrams.match_link import MatchLinkDiagramMixin  # noqa: E402
from diagrams.period import PeriodDiagramMixin  # noqa: E402
from diagrams.queue import QueueDiagramMixin  # noqa: E402
from diagrams.rmb_list import RmbListDiagramMixin  # noqa: E402
from diagrams.transfer import TransferDiagramMixin  # noqa: E402
from diagrams.boat_rental import BoatRentalDiagramMixin  # noqa: E402
from diagrams.interval import IntervalDiagramMixin  # noqa: E402
from diagrams.well_climb import WellClimbDiagramMixin  # noqa: E402
from diagrams.substitution import SubstitutionDiagramMixin  # noqa: E402
from diagrams.time_vertical import TimeVerticalDiagramMixin  # noqa: E402
from diagrams.tree_digit import TreeDigitDiagramMixin  # noqa: E402
from diagrams.multiple_times import MultipleTimesDiagramMixin  # noqa: E402
from diagrams.wrong_subtract import WrongSubtractDiagramMixin  # noqa: E402
from diagrams.average import AverageDiagramMixin  # noqa: E402
from diagrams.sum_times import SumTimesDiagramMixin  # noqa: E402
from diagrams.diff_times import DiffTimesDiagramMixin  # noqa: E402
from diagrams.sum_diff import SumDiffDiagramMixin  # noqa: E402
from diagrams.overlap import OverlapDiagramMixin  # noqa: E402
from diagrams.unitary import UnitaryDiagramMixin  # noqa: E402
from diagrams.aggregate import AggregateDiagramMixin  # noqa: E402
from diagrams.hollow_square import HollowSquareDiagramMixin  # noqa: E402
from diagrams.restore_flow import RestoreFlowDiagramMixin  # noqa: E402

from manim import *  # noqa: F403


def lesson_number_from_script(path: Path) -> int:
    """从脚本文件名 problem_{lessonNumber}.py 解析讲次，与 public/data/problems/{n}.json 一致。"""
    m = re.fullmatch(r"problem_(\d+)", path.stem)
    if not m:
        raise ValueError(f"脚本须命名为 problem_{{lessonNumber}}.py，当前: {path.name}")
    return int(m.group(1))


class MathLessonScene(
    SafeScene,
    DiagramCommonMixin,
    BetweenDiagramMixin,
    QueueDiagramMixin,
    TransferDiagramMixin,
    PeriodDiagramMixin,
    RmbListDiagramMixin,
    LineCompareDiagramMixin,
    MatchLinkDiagramMixin,
    WellClimbDiagramMixin,
    IntervalDiagramMixin,
    BoatRentalDiagramMixin,
    SubstitutionDiagramMixin,
    TimeVerticalDiagramMixin,
    TreeDigitDiagramMixin,
    MultipleTimesDiagramMixin,
    WrongSubtractDiagramMixin,
    AverageDiagramMixin,
    SumTimesDiagramMixin,
    DiffTimesDiagramMixin,
    SumDiffDiagramMixin,
    OverlapDiagramMixin,
    UnitaryDiagramMixin,
    AggregateDiagramMixin,
    HollowSquareDiagramMixin,
    RestoreFlowDiagramMixin,
):
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

        title_bottom = hint_title.get_bottom()[1]
        body_reserve = 1.55
        zone_top = title_bottom - 0.28
        zone_bottom = self.safe_bottom + body_reserve
        zone_center_y = (zone_top + zone_bottom) / 2

        diagram.generate_target()
        diagram.target.scale(1 / from_scale)
        diagram.target.move_to(np.array([0, zone_center_y, 0]))
        zone_h = zone_top - zone_bottom
        if diagram.target.height > zone_h * 0.90:
            diagram.target.scale(zone_h * 0.90 / diagram.target.height)
        self.clamp_content(diagram.target)
        self.play(MoveToTarget(diagram), run_time=1.0)

        body = self.safe_wrapped_text(key_points, font_size=24, color=WHITE)
        body.next_to(diagram, DOWN, buff=0.28)
        body.move_to(np.array([0, body.get_center()[1], 0]))
        self.clamp_content(body)

        self.play(FadeIn(body, shift=UP * 0.15), run_time=0.5)
        self.wait(wait)
        self.play(FadeOut(Group(hint_title, diagram, body)), run_time=0.3)

    def written_left_x(self) -> float:
        """作答段左侧列式区 x。"""
        return self.layout.get("left_x", self.safe_left + 0.8)

    def written_left_y(self, offset: float = 0.0) -> float:
        """作答段左侧列式区基准 y（与图解 draw_y 对齐）。"""
        base = self.layout.get("draw_y", self.content_center[1])
        return base + offset

    def place_diagram_for_written(
        self,
        diagram: Mobject,
        *,
        run_time: float = 1.0,
        scale_run_time: float = 0.5,
        right_fraction: float = 0.58,
        right_margin: float = 0.35,
        y: float | None = None,
    ) -> float:
        """
        作答段：图解平移至右半区，仅在超出右半宽时缩小。
        返回 written_diagram_scale（供 play_keypoints_only 使用）。
        """
        mid_x = (self.safe_left + self.safe_right) / 2
        right_col_x = mid_x + (self.safe_right - mid_x) * right_fraction
        draw_y = y if y is not None else self.layout.get("draw_y", self.content_center[1])
        target = np.array([right_col_x, draw_y, 0])
        self.play(diagram.animate.move_to(target), run_time=run_time)

        right_half_width = self.safe_right - mid_x - right_margin
        scale = 1.0
        if diagram.width > right_half_width:
            scale = right_half_width / diagram.width
            self.play(diagram.animate.scale(scale), run_time=scale_run_time)
        self.clamp_content(diagram)
        return scale

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
