#!/usr/bin/env python3
"""
一键渲染所有 Manim 例题视频，并归档到 public/videos/。

自动扫描 manim/scenes/{methodType}/problem_*.py，依次执行：
  1. manim 渲染完整 mp4
  2. post_render.py 复制 full.mp4 并切分 segments
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCENES_ROOT = REPO_ROOT / "manim" / "scenes"
POST_RENDER = SCENES_ROOT / "_shared" / "post_render.py"
PROBLEMS_DIR = REPO_ROOT / "public" / "data" / "problems"

QUALITY_PRESETS: dict[str, tuple[str, str]] = {
    "ql": ("480p15", "-ql"),
    "qh": ("1080p60", "-qh"),
}


@dataclass(frozen=True)
class LessonJob:
    lesson: int
    method_type: str
    script: Path
    scene_class: str

    @property
    def workdir(self) -> Path:
        return self.script.parent

    def rendered_mp4(self, quality_dir: str) -> Path:
        return (
            self.workdir
            / "media"
            / "videos"
            / f"problem_{self.lesson}"
            / quality_dir
            / f"{self.scene_class}.mp4"
        )


def discover_lessons() -> list[LessonJob]:
    jobs: list[LessonJob] = []
    pattern = re.compile(r"^problem_(\d+)\.py$")
    for script in sorted(SCENES_ROOT.rglob("problem_*.py")):
        if "_shared" in script.parts:
            continue
        match = pattern.match(script.name)
        if not match:
            continue
        lesson = int(match.group(1))
        jobs.append(
            LessonJob(
                lesson=lesson,
                method_type=script.parent.name,
                script=script,
                scene_class=f"Problem{lesson}Scene",
            ),
        )
    return sorted(jobs, key=lambda job: job.lesson)


def filter_lessons(jobs: list[LessonJob], lesson_filter: str | None) -> list[LessonJob]:
    if not lesson_filter:
        return jobs
    wanted: set[int] = set()
    for part in lesson_filter.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", 1)
            start, end = int(start_s.strip()), int(end_s.strip())
            if end < start:
                start, end = end, start
            wanted.update(range(start, end + 1))
        else:
            wanted.add(int(token))
    return [job for job in jobs if job.lesson in wanted]


def run_step(label: str, cmd: list[str], *, cwd: Path, dry_run: bool) -> None:
    print(f"\n>> {label}")
    print("   ", " ".join(cmd))
    if dry_run:
        return
    subprocess.run(cmd, cwd=cwd, check=True)


def render_lesson(
    job: LessonJob,
    *,
    quality: str,
    example_index: int,
    dry_run: bool,
    skip_render: bool,
    skip_post: bool,
) -> None:
    quality_dir, manim_flag = QUALITY_PRESETS[quality]
    json_file = PROBLEMS_DIR / f"{job.lesson}.json"
    if not json_file.is_file():
        raise FileNotFoundError(f"缺少题目数据: {json_file}")

    print("=" * 60)
    print(f"第 {job.lesson} 讲 | {job.method_type} | {job.scene_class}")

    if not skip_render:
        run_step(
            "Manim 渲染",
            [
                sys.executable,
                "-m",
                "manim",
                job.script.name,
                job.scene_class,
                manim_flag,
            ],
            cwd=job.workdir,
            dry_run=dry_run,
        )

    rendered = job.rendered_mp4(quality_dir)
    if not dry_run and not skip_render and not rendered.is_file():
        raise FileNotFoundError(f"未找到渲染输出: {rendered}")

    if skip_post:
        return

    run_step(
        "后处理归档",
        [
            sys.executable,
            str(POST_RENDER),
            "--lesson",
            str(job.lesson),
            "--example-index",
            str(example_index),
            "--rendered",
            str(rendered),
        ],
        cwd=job.workdir,
        dry_run=dry_run,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="一键渲染所有 Manim 例题视频并归档")
    parser.add_argument(
        "--quality",
        choices=sorted(QUALITY_PRESETS),
        default="qh",
        help="画质：ql=480p15 预览，qh=1080p60 成片（默认）",
    )
    parser.add_argument(
        "--lessons",
        help="仅渲染指定讲次：逗号分隔或区间，如 1,3,21 或 1-60",
    )
    parser.add_argument(
        "--example-index",
        type=int,
        default=0,
        help="例题序号：0=母题，1+=举一反三（默认 0）",
    )
    parser.add_argument(
        "--skip-render",
        action="store_true",
        help="跳过 manim 渲染，仅执行 post_render",
    )
    parser.add_argument(
        "--skip-post",
        action="store_true",
        help="跳过 post_render，仅执行 manim 渲染",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="某一讲失败时继续下一讲",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印命令，不实际执行",
    )
    args = parser.parse_args()

    jobs = filter_lessons(discover_lessons(), args.lessons)
    if not jobs:
        print("未找到可渲染的 problem_*.py 脚本", file=sys.stderr)
        return 1

    print(f"共 {len(jobs)} 讲：{', '.join(str(job.lesson) for job in jobs)}")
    print(f"画质：{args.quality} ({QUALITY_PRESETS[args.quality][0]})")

    started = time.time()
    failed: list[int] = []

    for job in jobs:
        try:
            render_lesson(
                job,
                quality=args.quality,
                example_index=args.example_index,
                dry_run=args.dry_run,
                skip_render=args.skip_render,
                skip_post=args.skip_post,
            )
        except (subprocess.CalledProcessError, FileNotFoundError, OSError) as exc:
            print(f"\n!! 第 {job.lesson} 讲失败: {exc}", file=sys.stderr)
            failed.append(job.lesson)
            if not args.continue_on_error:
                return 1

    elapsed = time.time() - started
    if failed:
        print(f"\n完成（部分失败）：{len(jobs) - len(failed)}/{len(jobs)}，"
              f"失败讲次 {failed}，耗时 {elapsed:.0f}s")
        return 1

    print(f"\n全部完成：{len(jobs)} 讲，耗时 {elapsed:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
