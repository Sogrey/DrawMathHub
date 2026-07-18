# Manim 视频制作

DrawMathHub 解题演示视频使用 Manim + SafeScene 预渲染为 MP4。

**完整文档** → [doc/manim/README.md](../doc/manim/README.md)

| 文档 | 说明 |
|------|------|
| [环境搭建](../doc/manim/环境搭建.md) | Python、Manim CE、FFmpeg |
| [脚本编写](../doc/manim/脚本编写.md) | 基类 API、分段、布局 |
| [制作流程](../doc/manim/制作流程.md) | 渲染 → post_render 归档 |
| [踩坑记录](../.cursor/skills/math-drawing-video/references/lessons-learned.md) | 实战经验 |

## Skill

| Skill | 位置 | 作用 |
|-------|------|------|
| `manim-video-safe` | `~/.cursor/skills/` | SafeScene、环境检测 |
| `math-drawing-video` | `.cursor/skills/` | 垂域规范、分段、manifest |

## 快速命令（第 1 讲）

```bash
cd manim/scenes/图示法
python -m manim problem_1.py Problem1Scene -ql
python ../_shared/post_render.py --lesson 1 \
  --rendered media/videos/problem_1/480p15/Problem1Scene.mp4
```

产出：`public/videos/{problemUuid}/{exampleUuid}/`（含 `full.mp4`、`cover.png`、`manifest.json`、`segments/`）。

批量渲染默认自动出封面，见 [批量渲染.md](../doc/manim/批量渲染.md)。

详见 [scenes/_shared/README.md](scenes/_shared/README.md)。
