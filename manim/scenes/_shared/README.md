# Manim Scene 公共模块

## 目录

```
manim/scenes/
├── _shared/
│   ├── safe_video.py       # SafeScene 基类（可从 ~/.cursor/skills/manim-video-safe/assets/ 更新）
│   ├── lesson_base.py      # MathLessonScene：分段、布局、读 JSON
│   ├── video_export.py     # manifest.json（含分段时间轴）
│   ├── post_render.py      # 渲染后复制 mp4、切分分段
│   └── export_segments.py  # 单独切分工具
├── 图示法/
│   └── problem_1.py        # 第1讲 之间问题（参考实现，文件名 = problem_{lessonNumber}.py）
└── {methodType}/
    └── problem_{id}.py
```

## 推荐分段结构

| 分段 | 导航 label | 内容 |
|------|-----------|------|
| intro | 题型讲解 | `show_title` + 题型讲解与特征 |
| question | 题目 | 题目 + 图解基础 |
| draw-* | 1…n | 图解解题分步（仅画图段用数字） |
| written | 作答 | 书面答题（分析 + 列式 + 作答） |
| keypoints | 点拨 | 图解放大居中 + `safe_wrapped_text` 点拨在下方（可传 `diagram`） |
| end | 结尾 | `show_credits` |

Vue 分步导航直接读取 manifest 中各段的 `label`，与分段视频一一对应。

完整版各段之间自动 `wait(3)` 秒（`FULL_VIDEO_SEGMENT_GAP`），不计入分段切分时间。

## 工作流

```bash
# 1. 渲染
cd manim/scenes/图示法
python -m manim problem_1.py Problem1Scene -qh

# 2. 后处理（复制完整版 + 切分分段）
python ../_shared/post_render.py --lesson 1 \
  --rendered media/videos/problem_1/1080p60/Problem1Scene.mp4

# manifest.json 由 Scene 运行时 finalize_lesson() 写入 public/
```

产出：`public/videos/{problemUuid}/{exampleUuid}/`

## 新建一讲

1. 复制 `图示法/problem_1.py` → `{methodType}/problem_{lessonNumber}.py`
2. 文件名与 `lessonNumber` 一致，`LESSON_NUMBER` 由基类从文件名自动解析
3. 用 `with self.segment(...):` 包裹各环节
4. 末尾 `self.finalize_lesson()`
5. 踩坑见 [lessons-learned.md](../../../.cursor/skills/math-drawing-video/references/lessons-learned.md)
