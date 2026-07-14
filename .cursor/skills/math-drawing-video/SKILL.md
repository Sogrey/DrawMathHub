---
name: math-drawing-video
description: |
  DrawMathHub 小学数学画图解题法 Manim 教学视频制作规范。基于 SafeScene 框架，覆盖 60 讲题型演示视频的结构、四区域布局、18 种图解方法、分步动画与列式作答规则。
  Trigger when: (1) 制作 DrawMathHub 解题演示视频, (2) 用户提及小学数学画图法/manim 教学视频, (3) 在 manim/ 目录编写或渲染 Scene 脚本, (4) 为某讲题型生成例题动画 MP4, (5) 用户 @math-drawing-video
---

# 小学数学画图法教学视频（DrawMathHub）

本项目专用 skill：在 **manim-video-safe** 通用底座之上，约束 DrawMathHub 60 讲演示视频的内容结构与教学节奏。

## 依赖底座（必须先读）

制作任何视频前，先阅读并遵循 **个人级** 通用 skill `manim-video-safe`（全局可用，不在本仓库内）：

| 资源 | 路径 |
|------|------|
| 通用 Manim skill | `~/.cursor/skills/manim-video-safe/SKILL.md` |
| SafeScene 模块 | `~/.cursor/skills/manim-video-safe/assets/safe_video.py` |
| 环境检测 | `~/.cursor/skills/manim-video-safe/scripts/check_env.py` |
| 依赖安装 | `~/.cursor/skills/manim-video-safe/scripts/install_deps.py` |

Windows 等价路径：`%USERPROFILE%\.cursor\skills\manim-video-safe\`

**工作流**：环境检测 → 继承 `MathLessonScene` → 按本 skill 领域规则编写 → 渲染 → `post_render.py` 归档。

**人类可读文档**：`doc/manim/`（环境、脚本、流程）；**经验踩坑**： [references/lessons-learned.md](references/lessons-learned.md)。

**新开对话制作新讲**：先读 [references/new-lesson-workflow.md](references/new-lesson-workflow.md) + [references/lessons-catalog.md](references/lessons-catalog.md)。

## 领域规则（详细）

| 文档 | 内容 |
|------|------|
| [references/new-lesson-workflow.md](references/new-lesson-workflow.md) | **新讲次制作流程**（规划→实现→渲染） |
| [references/lessons-catalog.md](references/lessons-catalog.md) | 已做讲次 1～10 索引与 API 速查 |
| [references/prompt.md](references/prompt.md) | 视频结构、四区域布局、18 种图解方法、列式作答 |
| [references/lessons-learned.md](references/lessons-learned.md) | **实战踩坑与经验**（布局、图解、点拨、前后端） |
| [references/manifest.example.json](references/manifest.example.json) | manifest 示例 |

## 快速检查清单

编写或审查脚本时确认：

- [ ] 题型讲解段：片头 + 概念 + 特征同屏上下分栏（`layout_numbered_features`）
- [ ] 片头副标题 `画图解题法 · {methodType}`，与 JSON 一致
- [ ] `show_title` 后 `init_layout_after_title()`；段内标题 `place_section_title()` + 正文 `place_below_section_title()`
- [ ] 题目框从 `title_bottom` 动态定位，保留至片尾前（点拨段可复用缩小图）
- [ ] 步骤在 `step_y`，画图在 `draw_y`，底部字幕不挡图解
- [ ] **之间问题**：`make_between_diagram`，待求区（边圈+横省略号）第四步全标红
- [ ] 作答段：列式前加文字说明（适用时），缩小图勿淡出
- [ ] 点拨段：`play_keypoints_only(..., diagram=..., from_scale=0.55~0.62)`
- [ ] 复杂图解：布局后检查 y 刻度对齐，辅助图全程 `self.add` 保留
- [ ] `keyPoints` 过长用 `\n` 或依赖 `safe_wrapped_text` 自动折行
- [ ] 脚本 `manim/scenes/{methodType}/problem_{lessonNumber}.py`，类名 `Problem{N}Scene`
- [ ] 成片在 `public/videos/{problemUuid}/{exampleUuid}/`，含 `full.mp4` + `manifest.json` + `segments/`

## 文件与目录规范

### 目录对照

```
manim/scenes/{methodType}/problem_{lessonNumber}.py   →  源码
public/data/problems/{lessonNumber}.json              →  题目元数据（含 uuid）
public/videos/{problemUuid}/{exampleUuid}/
  ├── full.mp4
  ├── manifest.json
  └── segments/01.mp4 … end.mp4
```

- 路由/进度用 `lessonNumber`（1–60）
- 视频路径用 JSON 的 `id`（problemUuid）和 `mainProblem.id`（exampleUuid）

### methodType 子目录（18 种）

图示法、列表法、画线法、连线法、线段图法、竖式法、树状图法、倒推法、逆推法、年龄轴法、假设法、打包法、流程图法、移多补少法、插旗法、十字交叉法、天平法、韦恩图法

### 脚本命名

| 规则 | 示例 |
|------|------|
| 文件名 | `problem_1.py` |
| 路径 | `manim/scenes/图示法/problem_1.py` |
| Scene 类名 | `Problem1Scene` |
| 讲次号 | 基类从文件名自动解析 |

### 分步交互

**manifest.json 由 Scene 自动生成**（禁止手写）。

| 模块 | 路径 |
|------|------|
| `MathLessonScene` | `manim/scenes/_shared/lesson_base.py` |
| `SegmentRecorder` | `manim/scenes/_shared/video_export.py` |
| 参考实现 | `manim/scenes/图示法/problem_1.py` |

**推荐分段**：题型讲解（含片头）→ 题目 → 图解 1…n → 作答 → 点拨 → 结尾

**`label` 规则**：
- 非画图段：2～4 字（题型讲解、题目、作答、点拨、结尾）
- 画图段：仅数字 `1`…`n`

完整版段间 `wait(3)`（`FULL_VIDEO_SEGMENT_GAP`），不计入分段 mp4。

### 渲染与归档

```bash
cd manim/scenes/图示法
python -m manim problem_1.py Problem1Scene -ql   # 预览
python -m manim problem_1.py Problem1Scene -qh   # 成片

python ../_shared/post_render.py --lesson 1 \
  --rendered media/videos/problem_1/1080p60/Problem1Scene.mp4
```

Windows：

```powershell
python ..\_shared\post_render.py --lesson 1 `
  --rendered media\videos\problem_1\480p15\Problem1Scene.mp4
```

## 与 Vue 前端对接

- 播放器：`src/components/SolutionVideoPlayer.vue`
- 路径：`src/data/videoAssets.ts` → `publicUrl('videos/...')` 拼接 base（GitHub Pages 子路径部署见 lessons-learned §5.5）
- 分步模式切换后须 `nextTick` 再加载第一段（已实现于 `useSegmentedVideoPlayer.ts`）

## 共享模块

项目在 `manim/scenes/_shared/` 维护 `safe_video.py`（与 skill 同步更新），脚本通过 `sys.path` 引用。

渲染中断后删除 `partial_movie_files` 再重渲；Python 3.8 共享模块需 `from __future__ import annotations`。
