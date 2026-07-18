# 制作经验与踩坑记录

> 基于第 1～60 讲实战沉淀。**本文件是「技巧与踩坑」的单一事实来源（SSOT）**；人类可读摘要见 [`doc/manim/技巧与踩坑.md`](../../../doc/manim/技巧与踩坑.md)。

**三份 reference 如何分工（勿整份合并）**：

| 文件 | 职责 | 更新频率 |
|------|------|----------|
| [lessons-catalog.md](lessons-catalog.md) | **库存索引**：讲次 ↔ Scene ↔ 图解 API | 每做完一讲 |
| [new-lesson-workflow.md](new-lesson-workflow.md) | **制作流程**：规划→实现→渲染检查清单 | 流程变更时 |
| **本文** | **经验与踩坑**：布局/动画/数据/前端 | 每次踩坑后追加 |

讲次总表只维护在 catalog；workflow 不要再复制整表。

**新开对话**：workflow（怎么做）+ catalog（查复用）+ 本文相关章节（避坑）。

## 一、布局与重叠

### 1.1 左上角标题改为一行后，段内小标题易重叠

**现象**：片头缩到左上角后，段内标题与常驻标题几乎重叠。

**错误做法**：全局下移 `content_top` / `content_center`。

**正确做法**：段内小标题用 `place_section_title()`；正文用 `place_below_section_title()`；`content_center` 保持静态值。

### 1.2 底部字幕占画图空间

`safe_video.SUBTITLE_BOTTOM_OFFSET = 0.35`，字幕更靠下。

### 1.3 题目框定位

`init_layout_after_title()` 中 `prob_top = title_bottom - 0.35`，勿用固定 `content_top`。

### 1.4 多行图解标签互相抢位（第 56、59 讲）

**现象**：总量括号与分段标签同侧重叠；双行速度条中间「上行速度」与「行走×级/秒」叠字。

**做法**：上下错开 `Brace`；加大 `row_gap`；易撞标签改到条**右侧**；折返用直角，勿外绕。

---

## 二、之间问题图解（图示法）

勿一开始画满全部位置。`make_between_diagram`：前缀/之间边圈+横向省略号/后缀冗余圈；第四步待求区边圈+省略号全部标红。

---

## 三、关键点拨段

- `keyPoints` 可用 `\n`；否则 `safe_wrapped_text` 自动折行
- 作答段缩小图**勿淡出**；点拨用 `play_keypoints_only(..., diagram=..., from_scale=...)`

---

## 四、Python / Manim 环境

| 坑 | 处理 |
|----|------|
| Python 3.8 `float \| None` | `from __future__ import annotations` |
| Manim 0.18 `scene.time` | 用 `scene.renderer.time` |
| `Rectangle(corner_radius=...)` | `RoundedRectangle` |
| 渲染中断 | 删 `partial_movie_files/` 再渲 |
| MathTex / `%`（第50讲） | 优先 `safe_text` |
| ImageMobject + `VGroup` | 改用 `Group`（第55、58讲） |

---

## 五、分段视频与前端

- manifest **禁止手写**，由 `segment()` + `finalize_lesson()` 生成
- 非画图段 label 2～4 字；画图段仅数字
- 分步切换后 `nextTick` 再播第一段
- 视频路径：`public/videos/{problemUuid}/{exampleUuid}/`
- `fullVideo` 用相对路径 `full.mp4`（Pages 子路径，见下）
- 封面+讲解合并为单段 `intro`

### 5.5 GitHub Pages 子路径

`fullVideo` 勿写 `/videos/...` 绝对根路径；前端用 `publicUrl()` 补 `VITE_BASE_PATH`。

---

## 六、题型讲解段一屏布局（intro）

上下分栏：上=**题型识别**（统一文案，勿写「什么是 XX？」）+ 1～2 行定义；下=要点 + `layout_numbered_features`。

下板块相对 `concept_block.get_bottom()` **链式定位**，勿固定 y。

动画：概念 → 分隔线/特征标题 → 特征行逐条 → FadeOut。

---

## 七、GitHub Pages 部署

CI：`VITE_BASE_PATH=/DrawMathHub/`；`404.html` 回退；Settings → Pages → GitHub Actions。

---

## 八、制作节奏

先 `-ql` 再 `-qh`；改公共布局后必重渲 + `post_render`；段间 `wait(3)` 不计入分段 mp4。

---

## 九、参考文件

| 文件 | 作用 |
|------|------|
| `图示法/problem_1.py` | 完整 Scene 模板 |
| `lesson_base.py` | 基类、布局、分段 |
| `safe_video.py` / `video_export.py` | 安全区、manifest |
| `public/data/problems/1.json` | 元数据示例 |

---

## 十、图解模块拆分

按**题型**建 `diagrams/xxx.py`，非按讲次。完整 API 表见 [lessons-catalog.md](lessons-catalog.md)。

---

## 十一、图解布局与坐标（第 7～9 讲）

- `arrange(DOWN)` 易破坏刻度对齐 → 共用 Group + 只调 x/y
- 辅助图全程 `self.add` 保留
- 多层 Brace 上下分工、抬高锚点
- 多段标注可分批 FadeIn

---

## 十二、数据与母题

一题一型；与 `datas/draw_math_all_lessons.json` 同步；视频只演示母题。

---

## 十三、作答段

列式前 GREY_B 说明 → 算式 → 答（YELLOW+红框）。

---

## 十四、methodType 子目录

路径必须与 JSON `methodType` 一致。

---

## 十五、透明度与 FadeIn（第 58 讲起必读）

### 15.1 先 `set_opacity(0)` 再 `FadeIn` → 永久不可见

`FadeIn` 以**当前透明度**为目标；已是 0 则终点仍是 0。

| 对象 | 推荐 |
|------|------|
| 线/色块/Brace/Arrow/PNG | 保持不透明，需要时 `FadeIn`/`Create` |
| 延迟文字 | `set_opacity(0)` + **`animate.set_opacity(1)`** |
| 填充条 | 显现后必要时再 `set_fill` |

### 15.2 PNG 图标

`manim/assets/icons/` + `load_icon_png`；容器用 `Group`。

### 15.3 行程折返（第 60 讲）

```
───────────────┐
        ◁──────┘
```

直角折回 + 方向箭头；勿外绕矩形环。

---

## 十六、填充条 opacity

可用 `animate.set_opacity(1)`，但记得恢复 fill；更稳：直接 `FadeIn` 不预置 0。

---

## 十七、近期可借鉴讲次

| 讲次 | 可借鉴点 |
|------|----------|
| 1 | intro 模板 |
| 50 | `safe_text` 避 MathTex/`%` |
| 55 | PNG + `Group` |
| 56～57 | 工程分段、标签错开 |
| 58 | FadeIn/透明度 |
| 59 | 双行速度条防叠字 |
| 60 | 多次相遇、直角折返 |

完整索引：[lessons-catalog.md](lessons-catalog.md)。
