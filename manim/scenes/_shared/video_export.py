"""
分段录制与 manifest 导出 — DrawMathHub Manim 公共模块
"""

from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from manim import Scene


def scene_time(scene: Scene) -> float:
    """Manim 0.18+ 当前时间（秒）。"""
    return float(scene.renderer.time)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

FULL_VIDEO_SEGMENT_GAP = 3.0
FULL_VIDEO_FILENAME = "full.mp4"
SEGMENTS_SUBDIR = "segments"

# 分段 id 由 problem/example/role 确定性生成，重渲染路径不变
SEGMENT_UUID_NAMESPACE = uuid.UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479")


def make_segment_id(problem_uuid: str, example_uuid: str, role: str) -> str:
    """manifest 分段 id（uuid），与视频文件名无关。"""
    return str(uuid.uuid5(SEGMENT_UUID_NAMESPACE, f"{problem_uuid}/{example_uuid}/{role}"))


@dataclass
class SegmentMeta:
    id: str
    role: str
    label: str
    file: str
    hint: str = ""
    start_time: float = 0.0
    end_time: float = 0.0

    def to_manifest_entry(self) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "id": self.id,
            "role": self.role,
            "label": self.label,
            "file": self.file,
            **({"hint": self.hint} if self.hint else {}),
        }
        if self.end_time > self.start_time:
            entry["startTime"] = round(self.start_time, 1)
            entry["endTime"] = round(self.end_time, 1)
        return entry


@dataclass
class SegmentRecorder:
    """记录 Scene 内各分段的时间范围，并写出 manifest / 切分 mp4。"""

    problem_uuid: str
    example_uuid: str
    segments: list[SegmentMeta] = field(default_factory=list)
    _open: SegmentMeta | None = field(default=None, repr=False)

    @property
    def output_dir(self) -> Path:
        return (
            PROJECT_ROOT
            / "public"
            / "videos"
            / self.problem_uuid
            / self.example_uuid
        )

    @property
    def full_video_public_path(self) -> str:
        return FULL_VIDEO_FILENAME

    @property
    def full_video_file(self) -> Path:
        return self.output_dir / FULL_VIDEO_FILENAME

    def begin(
        self,
        role: str,
        label: str,
        file: str,
        hint: str = "",
        scene: Scene | None = None,
    ) -> None:
        if self._open is not None:
            raise RuntimeError(f"分段 {self._open.role} 尚未 end，不能开始 {role}")
        seg_id = make_segment_id(self.problem_uuid, self.example_uuid, role)
        self._open = SegmentMeta(id=seg_id, role=role, label=label, file=file, hint=hint)
        if scene is not None:
            self._open.start_time = scene_time(scene)

    def end(self, scene: Scene) -> None:
        if self._open is None:
            return
        self._open.end_time = scene_time(scene)
        self.segments.append(self._open)
        self._open = None

    def write_manifest(self) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        manifest: dict[str, Any] = {
            "version": 2,
            "problemId": self.problem_uuid,
            "exampleId": self.example_uuid,
            "fullVideo": self.full_video_public_path,
            "segments": [s.to_manifest_entry() for s in self.segments],
        }
        path = self.output_dir / "manifest.json"
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def export_segment_videos(self, full_mp4: Path | None = None) -> list[Path]:
        src = full_mp4 or self.full_video_file
        if not src.is_file():
            raise FileNotFoundError(f"完整视频不存在: {src}")

        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            raise RuntimeError("未找到 ffmpeg，无法切分分段视频")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        exported: list[Path] = []

        for seg in self.segments:
            if seg.end_time <= seg.start_time:
                continue
            out = self.output_dir / seg.file
            out.parent.mkdir(parents=True, exist_ok=True)
            duration = seg.end_time - seg.start_time
            cmd = [
                ffmpeg,
                "-y",
                "-ss",
                str(seg.start_time),
                "-i",
                str(src),
                "-t",
                str(duration),
                "-c",
                "copy",
                str(out),
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            exported.append(out)

        return exported

    def copy_full_video_to_public(self, rendered_mp4: Path) -> Path:
        dest = self.full_video_file
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rendered_mp4, dest)
        return dest


def load_example_uuids(lesson_number: int, example_index: int = 0) -> tuple[str, str, str]:
    """从 public/data/problems/{lessonNumber}.json 读取 problem/example uuid。"""
    path = PROJECT_ROOT / "public" / "data" / "problems" / f"{lesson_number}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    problem_uuid = data["id"]
    if example_index == 0:
        example_uuid = data["mainProblem"]["id"]
    else:
        example_uuid = data["extensionProblems"][example_index - 1]["id"]
    return problem_uuid, example_uuid, str(path)


def standard_segment_plan() -> list[dict[str, str]]:
    return [
        {"role": "cover", "label": "封面", "desc": "片头标题 show_title"},
        {"role": "intro", "label": "题型讲解", "desc": "题型讲解与特征"},
        {"role": "question", "label": "题目", "desc": "题目展示与图解基础"},
        {"role": "draw", "label": "1…n", "desc": "图解解题分步（仅画图段用数字序号）"},
        {"role": "written", "label": "作答", "desc": "书面答题：分析、列式、规范作答"},
        {"role": "keypoints", "label": "点拨", "desc": "关键点拨（仅底部字幕区，无其他讲解）"},
        {"role": "end", "label": "结尾", "desc": "片尾 show_credits"},
    ]
