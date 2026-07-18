---
name: math-drawing-video
description: |
  DrawMathHub 小学数学画图解题法 Manim 教学视频制作规范。基于 SafeScene，覆盖 60 讲结构、四区域布局、18 种图解、分步动画与列式规则。
  Trigger when: (1) 制作 DrawMathHub 解题演示视频, (2) 提及小学数学画图法/manim 教学视频, (3) 在 manim/ 编写或渲染 Scene, (4) 为某讲生成例题 MP4, (5) @math-drawing-video
---

# 小学数学画图法教学视频（DrawMathHub）

在 **manim-video-safe** 通用底座之上，约束本仓库 60 讲演示视频的内容结构与教学节奏。

## 依赖底座（必须先读）

| 资源 | 路径 |
|------|------|
| 通用 Manim skill | `~/.cursor/skills/manim-video-safe/SKILL.md` |
| SafeScene | `~/.cursor/skills/manim-video-safe/assets/safe_video.py` |
| 环境检测 / 安装 | `scripts/check_env.py`、`scripts/install_deps.py`（同目录） |

Windows：`%USERPROFILE%\.cursor\skills\manim-video-safe\`

**工作流**：环境检测 → `MathLessonScene` → 本 skill 规则 → 渲染 → `post_render.py`。

## references 三件套（勿整文件合并）

| 文件 | 作用 | Agent 何时读 |
|------|------|----------------|
| [references/new-lesson-workflow.md](references/new-lesson-workflow.md) | **怎么做**：规划→实现→检查清单 | 新开一讲 / 改流程 |
| [references/lessons-catalog.md](references/lessons-catalog.md) | **有什么**：1～60 索引 + 图解 API | 查复用、注册模块 |
| [references/lessons-learned.md](references/lessons-learned.md) | **别踩坑**：布局/FadeIn/图标/前端 | 写图解、修叠字、修不可见 |

**为何不合并成一个 md？**

- catalog 每讲更新，需短而可扫
- workflow 偏流程，极少改表
- learned 持续变长，整份塞进 workflow 会浪费上下文

**允许的去重**：workflow **不再复制** 60 行总表，只链到 catalog。人类摘要：[`doc/manim/技巧与踩坑.md`](../../../doc/manim/技巧与踩坑.md)。

另见：[prompt.md](references/prompt.md)（四区域、18 种方法）、[manifest.example.json](references/manifest.example.json)。

**新开对话**：先读 workflow + catalog；踩坑时再读 learned 对应节。

## 快速检查清单

- [ ] intro：`concept_title` = **「题型识别」** + 要点 `layout_numbered_features`（上下分栏、链式定位）
- [ ] 片头副标题 `画图解题法 · {methodType}`，与 JSON 一致
- [ ] `show_title` 后 `init_layout_after_title()`；题目框保留至 written 结束
- [ ] 步骤在 `step_y`，画图在 `draw_y`，字幕不挡图
- [ ] **图形勿** `set_opacity(0)` 再 `FadeIn`；文字可用 `animate.set_opacity(1)`（learned §十五）
- [ ] PNG 用 `Group` + `load_icon_png`；含图标的 `diagram_all` 用 `Group`
- [ ] 标签上下/左右错开，防叠字
- [ ] 作答：缩小图勿淡出；点拨 `play_keypoints_only(..., diagram=..., from_scale=...)`
- [ ] 路径 `manim/scenes/{methodType}/problem_{N}.py`，类名 `Problem{N}Scene`
- [ ] 成片 `public/videos/{problemUuid}/{exampleUuid}/` + manifest（禁止手写）

## 文件与目录

```
manim/scenes/{methodType}/problem_{N}.py
public/data/problems/{N}.json
public/videos/{problemUuid}/{exampleUuid}/full.mp4 + cover.png + manifest + segments/
manim/scenes/_shared/diagrams/   # 按题型，非按讲次
manim/assets/icons/              # PNG
```

18 种 methodType 子目录名与 JSON 一致（含中文）。

## 分段与渲染

推荐：`intro` → `question` → `draw-1…n` → `written` → `keypoints` → `end`。

```powershell
python scripts/render_all_videos.py --quality ql --lessons N
# 区间：--lessons 1-60；默认自动出封面（EXPORT_HALL_COVER=0 可关）
```

keypoints 中图解放大后 `export_hall_cover` 裁切 diagram → 视频目录 `cover.png`（与 full.mp4 同目录）。完整版段间 `wait(3)`（`FULL_VIDEO_SEGMENT_GAP`）不计入分段 mp4。

## 与 Vue 对接

- `SolutionVideoPlayer.vue`；路径 `videoAssets.ts` + `publicUrl`（Pages 子路径见 learned §5.5）
- `GridCard.vue`：`getCoverUrl`（与 full.mp4 同目录），失败回退 SVG；悬浮 tip 用 `problemIdentification`
- 分步切换后 `nextTick` 再播第一段

## 共享模块

`manim/scenes/_shared/`：`lesson_base.py`、`safe_video.py`、`video_export.py`、`diagrams/`。  
渲染中断删 `partial_movie_files`；Python 3.8 需 `from __future__ import annotations`。
