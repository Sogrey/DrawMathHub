#!/usr/bin/env python3
"""渲染后处理：复制完整 mp4 到 public，并按 manifest.json 切分分段。"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

_SHARED = Path(__file__).resolve().parent
sys.path.insert(0, str(_SHARED))

from video_export import SegmentRecorder, load_example_uuids  # noqa: E402
from export_segments import export_with_ffmpeg  # noqa: E402


def resolve_recorder(args: argparse.Namespace) -> SegmentRecorder:
    if args.problem_id and args.example_id:
        return SegmentRecorder(args.problem_id, args.example_id)
    if args.lesson is not None:
        problem_uuid, example_uuid, _ = load_example_uuids(args.lesson, args.example_index)
        return SegmentRecorder(problem_uuid, example_uuid)
    raise SystemExit("请指定 --lesson 或同时指定 --problem-id 与 --example-id")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lesson", type=int, help="讲次序号（从 JSON 解析 uuid）")
    parser.add_argument("--example-index", type=int, default=0, help="0=母题，1+=举一反三序号")
    parser.add_argument("--problem-id", type=str, help="题目 uuid")
    parser.add_argument("--example-id", type=str, help="例题视频 uuid")
    parser.add_argument("--rendered", type=Path, required=True, help="Manim 输出的完整 mp4")
    parser.add_argument("--skip-split", action="store_true")
    args = parser.parse_args()

    recorder = resolve_recorder(args)
    dest_full = recorder.copy_full_video_to_public(args.rendered.resolve())
    print(f"完整版 → {dest_full}")

    # 渲染产物旁若有 cover.png，拷到与 full.mp4 同目录
    rendered = args.rendered.resolve()
    sibling_cover = rendered.parent / "cover.png"
    if sibling_cover.is_file():
        dest_v = recorder.output_dir / "cover.png"
        dest_v.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sibling_cover, dest_v)
        print(f"大厅封面（media 旁路）→ {dest_v}")

    cover = recorder.archive_hall_cover()
    if cover is not None:
        print(f"大厅封面 → {cover}")
    else:
        print("提示: 未找到封面（需 Scene 在 keypoints 段导出 cover.png）")

    manifest_file = recorder.output_dir / "manifest.json"
    if not manifest_file.is_file():
        print(f"警告: 未找到 {manifest_file}，请先成功运行 Scene（finalize_lesson）")
        return

    if args.skip_split:
        return

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    export_with_ffmpeg(dest_full, recorder.output_dir, manifest["segments"])
    print("分段 mp4 导出完成")


if __name__ == "__main__":
    main()
