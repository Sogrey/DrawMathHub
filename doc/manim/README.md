# Manim 演示视频文档

DrawMathHub 例题讲解视频使用 **Manim Community Edition + SafeScene** 预渲染为 MP4，供 Vue 前端完整播放或分步学习。

## 文档索引

| 文档 | 内容 |
|------|------|
| [环境搭建.md](./环境搭建.md) | Python、Manim CE、字体、环境检测 |
| [脚本编写.md](./脚本编写.md) | 目录结构、基类 API、分段写法、布局与图解规范 |
| [制作流程.md](./制作流程.md) | 从渲染到归档的完整命令与产出说明 |

## 规范与经验（Cursor Skill）

| 资源 | 路径 |
|------|------|
| 垂域规范 | `.cursor/skills/math-drawing-video/SKILL.md` |
| 详细 Prompt | `.cursor/skills/math-drawing-video/references/prompt.md` |
| **经验与踩坑** | `.cursor/skills/math-drawing-video/references/lessons-learned.md` |
| 参考脚本 | `manim/scenes/图示法/problem_1.py` |

基于通用 Manim 底座（个人级）：`~/.cursor/skills/manim-video-safe/`

## 一分钟上手

```bash
# 1. 进入脚本目录
cd manim/scenes/图示法

# 2. 快速预览（低画质）
python -m manim problem_1.py Problem1Scene -ql

# 3. 归档到 public（复制 full.mp4 + 切分 segments）
python ..\_shared\post_render.py --lesson 1 `
  --rendered media\videos\problem_1\480p15\Problem1Scene.mp4
```

产出目录：`public/videos/{problemUuid}/{exampleUuid}/`

## 与前端的关系

- 题目数据：`public/data/problems/{lessonNumber}.json`
- 视频播放：`src/components/SolutionVideoPlayer.vue`
- 路径解析：`src/data/videoAssets.ts`（子路径部署须 `publicUrl` 补 base，见经验文档 §5.5）

## 经验归档（近期）

| 主题 | 文档章节 |
|------|----------|
| intro 一屏上下布局、特征双列 | [lessons-learned §六](../../.cursor/skills/math-drawing-video/references/lessons-learned.md) |
| cover+intro 合并、manifest 路径 | [lessons-learned §5.5–5.6](../../.cursor/skills/math-drawing-video/references/lessons-learned.md) |
| GitHub Pages 部署 | [lessons-learned §七](../../.cursor/skills/math-drawing-video/references/lessons-learned.md) |
