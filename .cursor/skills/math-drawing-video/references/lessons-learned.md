# 制作经验与踩坑记录

> 基于第 1 讲（之间问题 / 图示法）实战沉淀，后续每讲有新发现请追加本节。

## 一、布局与重叠

### 1.1 左上角标题改为一行后，段内小标题易重叠

**现象**：片头缩到左上角后，`content_top - 0.4` 定位的段内标题（如「什么是之间问题？」）与常驻标题几乎重叠。

**错误做法**：全局下移 `content_top` / `content_center`——会导致正文、画图区整体下沉，其他仍按旧坐标布局的组件反而叠在一起。

**正确做法**：

- 段内小标题用 `place_section_title()`，相对 `_title_group.get_bottom()` 定位
- 段内正文用 `place_below_section_title(body, section_title)` 紧跟小标题
- `content_center` 保持 setup 时的静态值，供关键点拨等全屏段落居中

### 1.2 底部字幕占画图空间

**做法**：`safe_video.SUBTITLE_BOTTOM_OFFSET = 0.35`（原 0.5），字幕更靠下，给正文和图解留空间。

### 1.3 题目框定位

`init_layout_after_title()` 中 `prob_top = title_bottom - 0.35`（`PROB_TOP_GAP`），勿用固定 `content_top` 推算。

---

## 二、之间问题图解（图示法）

### 2.1 勿一开始就画满全部位置

学生要算的是「之间有几人」，中间人数未知，**不能**一开始画 16 个圈。

**推荐结构**（`make_between_diagram`）：

```
[前缀圈/···] ⚪玲玲 [边圈] ··· [边圈] ⚪丽丽 [后缀冗余圈]
```

| 区域 | 规则 |
|------|------|
| 前缀 | ≤5 人全画；>5 人用横向 `···` + 靠近关键人的若干圈 |
| 之间 | 关键人两侧各留 `between_edge` 圈，中间用**横向**省略号 |
| 后缀 | 丽丽后加 2 个冗余圈，表示她不一定排最后 |
| 待求标红 | 第四步：`between_zone_circles`（边圈）+ 省略号 **全部** 标红，勿只染省略号 |

### 2.2 省略号方向

用 `_horizontal_ellipsis()`（横向四点），勿用竖向 `⋮`，与圆圈同行才直观。

---

## 三、关键点拨段

### 3.1 长句折行

`keyPoints` 支持 JSON 内 `\n` 强制换行；未写 `\n` 时 `safe_wrapped_text()` 按安全区宽度自动折行。

```json
"keyPoints": "已知两人从左（或右）数分别排第几，求两人之间有几人，\n先用大数减1，再减小数。"
```

### 3.2 图解 + 点拨同屏（更浅显）

作答段缩小图解到右下角后**不要淡出**；点拨段调用：

```python
self.play_keypoints_only(
    mp["keyPoints"], wait=6,
    diagram=diagram_all, from_scale=0.55,
)
```

效果：图解放大回中间，点拨文字在图解下方。

无图解的讲次仍可只传 `key_points`，正文居中显示。

---

## 四、Python / Manim 环境

| 坑 | 处理 |
|----|------|
| Python 3.8 不支持 `float \| None` | `safe_video.py` 等文件加 `from __future__ import annotations` |
| Manim 0.18 无 `scene.time` | 用 `scene.renderer.time` |
| `Rectangle(corner_radius=...)` | 改用 `RoundedRectangle` |
| 渲染中断后报错 | 删除 `media/.../partial_movie_files/` 再渲 |
| 类型注解在类体求值 | 共享模块统一 `from __future__ import annotations` |

---

## 五、分段视频与前端

### 5.1 manifest 禁止手写

必须由 Scene 内 `segment()` + `finalize_lesson()` 生成，保证与代码步骤一致。

### 5.2 导航 label

- 非画图段：2～4 字语义名（题型讲解、题目、作答、点拨、结尾）
- 画图段：仅数字 `1`、`2`…

### 5.3 分步学习切换不自动播第一段

**原因**：切到 interactive 时 `resetInteractive()` 在 `videoA`/`videoB` 挂载前执行。

**修复**：`nextTick()` 后再 `playSegment(0)`（见 `useSegmentedVideoPlayer.ts`）。

### 5.4 视频目录（UUID）

```
public/videos/{problemUuid}/{exampleUuid}/
├── full.mp4
├── manifest.json
└── segments/01.mp4 …
```

路由/进度仍用 `lessonNumber`；视频路径用 JSON 中的 `id` / `mainProblem.id`。

### 5.5 manifest 中 `fullVideo` 勿用站点根绝对路径

**现象**：GitHub Pages 部署在子路径（如 `/DrawMathHub/`）时，`full.mp4` 404，但 `segments/*.mp4` 正常。

**原因**：

- `manifest.fullVideo` 若写成 `/videos/.../full.mp4`，浏览器请求 `https://<user>.github.io/videos/...`（缺子路径）
- `segments` 用相对路径 `segments/01.mp4`，拼接 `basePath` 后正确

**正确做法**：

- Manim 导出写相对路径：`"fullVideo": "full.mp4"`（`video_export.py` 已改）
- 前端 `resolveFullVideoUrl` / `resolveSegmentUrl` 对以 `/` 开头的路径统一走 `publicUrl()` 补 base
- 本地与 Pages 的 base 来源：`.env` `VITE_BASE_PATH` → `vite.config` `base` → `getAppBase()`

### 5.6 封面与题型讲解合并为一段

原先 `cover` + `intro` 两段内容少、切换拖沓，已合并为单段 `intro`（`segments/01.mp4`）。

```python
with self.segment("intro", "题型讲解", "segments/01.mp4", "片头标题与题型讲解"):
    self.show_title(...)
    self.init_layout_after_title(prob_h=1.0)
    # 概念 + 特征同屏 …
```

- manifest 少一段，分步导航首段即「题型讲解」
- 存量视频可用 ffmpeg 从 `full.mp4` 按新 `startTime/endTime` 重切，不必重渲 Manim（改布局后仍需重渲）

---

## 六、题型讲解段一屏布局（intro）

### 6.1 概念 + 特征合并一屏，用上下分栏

「什么是 XX？」与「XX 的特征」内容都较少，分两屏切换显得空。推荐**同屏上下两块**：

```
┌─────────────────────────────────────┐
│ [常驻标题]                           │
│  ▲ 上：概念定义（小标题 + 1～2 行正文） │
├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
│  ▼ 下：特征列表（小标题 + 序号行）    │
└─────────────────────────────────────┘
```

**不推荐左右分栏**：特征行含「序号圆 + 主句 + 副句」，需要横向宽度；左轻右重，窄列副句难读。

### 6.2 下板块须相对上板块动态定位（防重叠）

**错误做法**：用固定 `zone_mid = title_bottom - 2.35` 放分隔线和特征区——上板块正文高度一变就与下板块重叠。

**正确做法**：先排完 `concept_block`，再链式下移：

```python
divider_y = concept_block.get_bottom()[1] - 0.45
feature_title.move_to([0, divider_y - 0.60, 0])
top_y = feature_title.get_bottom()[1] - 0.50
feature_groups = self.layout_numbered_features(features, top_y=top_y)
```

间距可调：`0.45`（概念→线）、`0.60`（线→特征标题）、`0.50`（标题→首行）。

### 6.3 特征列表：`layout_numbered_features`

`lesson_base.py` 提供复用 API：

| 条数 | 布局 |
|------|------|
| ≤3 | 单列左对齐 |
| ≥4 | 左右两列，左列 `ceil(n/2)`，文字 `fit_to_width` 适配列宽 |

```python
features = [
    ("1", "主句", "副句"),
    # …
]
rows = self.layout_numbered_features(
    features,
    top_y=feature_title.get_bottom()[1] - 0.50,
    row_step=1.12,          # 单列行距
    two_column_min=4,       # 达到 4 条自动双列
)
```

单条构建：`make_numbered_feature_row(num, main, sub)`。

### 6.4 intro 段动画节奏

1. 概念块 `FadeIn` → `wait(2)`
2. 分隔线 + 特征标题 `FadeIn`
3. 特征行依次 `FadeIn`（各 `wait(1)`，保留分步感）
4. `wait(2)` → 整块 `FadeOut` 进入题目段

比「整屏切换」省约 3～4 秒；改布局后须重渲并 `post_render.py` 更新 `segments/01.mp4` 与 manifest 时间轴。

---

## 七、GitHub Pages 部署

| 项 | 说明 |
|----|------|
| Workflow | `.github/workflows/deploy.yml`，push `main` 自动构建部署 |
| 环境变量 | CI 中 `VITE_BASE_PATH=/DrawMathHub/` 与 `.env` 一致 |
| SPA 回退 | `scripts/gh-pages-postbuild.mjs` 复制 `index.html` → `404.html` |
| 仓库设置 | Settings → Pages → Source 选 **GitHub Actions** |
| 访问地址 | `https://<user>.github.io/DrawMathHub/` |

PR 仅跑 build 校验，不部署 artifact。

---

## 八、制作节奏建议

1. 先 `-ql` 快速预览布局与字幕，确认后再 `-qh` 出成片
2. 每写完一段动画，对照 [prompt.md](prompt.md) 重叠检查清单
3. 改布局类公共 API 后，务必重渲并跑 `post_render.py` 更新分段
4. 完整版段间 `wait(3)` 由 `FULL_VIDEO_SEGMENT_GAP` 控制，不计入分段 mp4

---

## 九、第 1 讲参考文件

| 文件 | 作用 |
|------|------|
| `manim/scenes/图示法/problem_1.py` | 完整 Scene 参考（intro 一屏上下布局） |
| `manim/scenes/_shared/lesson_base.py` | `make_between_diagram`、`layout_numbered_features`、`play_keypoints_only` |
| `manim/scenes/_shared/safe_video.py` | 安全区、折行、字幕偏移 |
| `manim/scenes/_shared/video_export.py` | manifest 导出、`fullVideo` 相对路径 |
| `src/data/videoAssets.ts` | `publicUrl` 拼接、manifest 路径解析 |
| `public/data/problems/1.json` | 题目元数据与 keyPoints |
