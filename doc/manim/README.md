# Manim 演示视频文档

DrawMathHub 例题讲解视频使用 **Manim Community Edition + SafeScene** 预渲染为 MP4，供 Vue 完整播放或分步学习。

## 文档索引

| 文档 | 内容 |
|------|------|
| [环境搭建.md](./环境搭建.md) | Python、Manim CE、字体、环境检测 |
| [脚本编写.md](./脚本编写.md) | 目录结构、基类 API、分段写法 |
| [制作流程.md](./制作流程.md) | 从选题到归档的命令与产出 |
| [批量渲染.md](./批量渲染.md) | 一键渲染多讲；**自动导出题型大厅封面** |
| [**技巧与踩坑.md**](./技巧与踩坑.md) | **画图解题技巧摘要 + 文档分工说明** |
| [单文件分步播放方案.md](./单文件分步播放方案.md) | **待开发**：只留 full.mp4 + seek；进度条切分标记 |

## Cursor Skill（规范 SSOT）

| 资源 | 路径 | 作用 |
|------|------|------|
| Skill 入口 | `.cursor/skills/math-drawing-video/SKILL.md` | Agent 总规范 |
| **制作流程** | `references/new-lesson-workflow.md` | 怎么做一讲 |
| **讲次目录 1～60** | `references/lessons-catalog.md` | 库存索引 / API |
| **踩坑全文** | `references/lessons-learned.md` | 技巧与踩坑 SSOT |
| Prompt | `references/prompt.md` | 四区域、18 种方法 |

三者**不要整份合并**（见 [技巧与踩坑.md](./技巧与踩坑.md)「文档怎么分」）：总表、流程、长文踩坑更新节奏不同；只去掉重复的总表复制。

通用底座：`~/.cursor/skills/manim-video-safe/`

## 一分钟上手

```powershell
python scripts/render_all_videos.py --quality ql --lessons N
# 或区间：--lessons 1-60
```

产出：

- `public/videos/{problemUuid}/{exampleUuid}/`（含 `full.mp4`、`cover.png`、`manifest`、`segments/`）

新讲：先读 skill 的 `new-lesson-workflow.md`，再查 `lessons-catalog.md` 能否复用图解。

## 与前端

- 题目：`public/data/problems/{N}.json`
- 播放：`SolutionVideoPlayer.vue` + `videoAssets.ts`（子路径用 `publicUrl`）
- 大厅卡片：`GridCard.vue` → 视频目录 `cover.png`（缺失回退 SVG）；悬浮 tip 显示题型识别

## 60 讲

Scene 与制作管线已覆盖第 1～60 讲。维护时改图解后对该讲 `ql` 重渲即可。
