#!/usr/bin/env python3
"""从完整 MP4 按 manifest.json 中记录的时间切分各分段视频。"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
FULL_VIDEO_FILENAME = "full.mp4"


def _segment_range(seg: dict) -> tuple[float, float | None]:
    start = seg.get("startTime", seg.get("start_time", 0))
    end = seg.get("endTime", seg.get("end_time"))
    return float(start), float(end) if end is not None else None


def export_with_ffmpeg(full_mp4: Path, out_dir: Path, segments: list[dict]) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("错误: 未找到 ffmpeg", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    for seg in segments:
        start, end = _segment_range(seg)
        if end is None or end <= start:
            print(f"跳过无效分段: {seg.get('role') or seg.get('id')}")
            continue
        out = out_dir / seg["file"]
        out.parent.mkdir(parents=True, exist_ok=True)
        duration = end - start
        cmd = [
            ffmpeg, "-y", "-ss", str(start), "-i", str(full_mp4),
            "-t", str(duration), "-c", "copy", str(out),
        ]
        subprocess.run(cmd, check=True)
        print(f"导出: {out.name} ({duration:.1f}s)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem-id", type=str, required=True)
    parser.add_argument("--example-id", type=str, required=True)
    args = parser.parse_args()

    base = PROJECT_ROOT / "public" / "videos" / args.problem_id / args.example_id
    full_mp4 = base / FULL_VIDEO_FILENAME
    manifest_file = base / "manifest.json"

    if not manifest_file.is_file():
        print(f"缺少 manifest: {manifest_file}", file=sys.stderr)
        sys.exit(1)

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    export_with_ffmpeg(full_mp4, base, manifest["segments"])
    print("分段导出完成")


if __name__ == "__main__":
    main()
