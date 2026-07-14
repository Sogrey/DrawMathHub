# Manim 演示视频文档

DrawMathHub 例题讲解视频使用 **Manim Community Edition + SafeScene** 预渲染为 MP4，供 Vue 前端完整播放或分步学习。

## 文档索引

| 文档 | 内容 |
|------|------|
| [环境搭建.md](./环境搭建.md) | Python、Manim CE、字体、环境检测 |
| [脚本编写.md](./脚本编写.md) | 目录结构、基类 API、分段写法、布局与图解规范 |
| [制作流程.md](./制作流程.md) | 从渲染到归档的完整命令与产出说明 |
| [批量渲染.md](./批量渲染.md) | **一键渲染所有例题视频** |

## 规范与经验（Cursor Skill）

| 资源 | 路径 |
|------|------|
| 垂域规范 | `.cursor/skills/math-drawing-video/SKILL.md` |
| **新讲次快速上手** | `.cursor/skills/math-drawing-video/references/new-lesson-workflow.md` |
| **已做讲次目录 1～10** | `.cursor/skills/math-drawing-video/references/lessons-catalog.md` |
| 详细 Prompt | `.cursor/skills/math-drawing-video/references/prompt.md` |
| **经验与踩坑** | `.cursor/skills/math-drawing-video/references/lessons-learned.md` |
| 参考脚本 | `manim/scenes/图示法/problem_1.py`（通用）；第 7～9 讲见 lessons-catalog |

基于通用 Manim 底座（个人级）：`~/.cursor/skills/manim-video-safe/`

## 一分钟上手（任意讲次 N）

```powershell
# 1. 项目根目录 — 预览第 N 讲（自动 manim + post_render）
python scripts/render_all_videos.py --quality ql --lessons N

# 2. 或手动（注意 methodType 子目录，如 线段图法）
cd manim/scenes/图示法
python -m manim problem_1.py Problem1Scene -ql
python ..\_shared\post_render.py --lesson 1 `
  --rendered media\videos\problem_1\480p15\Problem1Scene.mp4
```

产出目录：`public/videos/{problemUuid}/{exampleUuid}/`

**第 10 讲起**：先读 `new-lesson-workflow.md`，查 `lessons-catalog.md` 能否复用图解模块。

## 与前端的关系

- 题目数据：`public/data/problems/{lessonNumber}.json`（与 `datas/draw_math_all_lessons.json` 保持同步）
- 视频播放：`src/components/SolutionVideoPlayer.vue`
- 路径解析：`src/data/videoAssets.ts`（子路径部署须 `publicUrl` 补 base，见经验文档 §5.5）

## 经验归档（近期）

| 主题 | 文档章节 |
|------|----------|
| 新讲次全流程 | [new-lesson-workflow.md](../../.cursor/skills/math-drawing-video/references/new-lesson-workflow.md) |
| 1～9 讲索引 | [lessons-catalog.md](../../.cursor/skills/math-drawing-video/references/lessons-catalog.md) |
| intro 一屏上下布局 | [lessons-learned §六](../../.cursor/skills/math-drawing-video/references/lessons-learned.md) |
| 图解坐标/Brace/数据 | [lessons-learned §十一～十四](../../.cursor/skills/math-drawing-video/references/lessons-learned.md) |
| manifest 路径、GitHub Pages | [lessons-learned §5.5–5.7](../../.cursor/skills/math-drawing-video/references/lessons-learned.md) |
