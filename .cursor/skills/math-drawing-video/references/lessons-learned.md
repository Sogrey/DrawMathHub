# 制作经验与踩坑记录

> 基于第 1～9 讲实战沉淀，后续每讲有新发现请追加本节。

**新开对话快速上手**：先读 [new-lesson-workflow.md](new-lesson-workflow.md) 与 [lessons-catalog.md](lessons-catalog.md)。

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
| `manim/scenes/_shared/lesson_base.py` | Scene 基类、布局、分段导出（图解见 `diagrams/`） |
| `manim/scenes/_shared/safe_video.py` | 安全区、折行、字幕偏移 |
| `manim/scenes/_shared/video_export.py` | manifest 导出、`fullVideo` 相对路径 |
| `src/data/videoAssets.ts` | `publicUrl` 拼接、manifest 路径解析 |
| `public/data/problems/1.json` | 题目元数据与 keyPoints |

---

## 十、图解模块拆分（按题型，非按讲次）

**原则**：`manim/scenes/_shared/diagrams/` **按题型归类**，不是按讲次编号。同一题型的多道题共用一套 `make_*_diagram`，各讲在 `problem_N.py` 里传入自己的数字、颜色、文案即可。

| 题型 | 模块 | 入口方法 | 已用讲次 |
|------|------|----------|----------|
| 之间问题 | `diagrams/between.py` | `make_between_diagram` | 第1讲 |
| 排队问题 | `diagrams/queue.py` | `make_queue_total_diagram` | 第2讲 |
| 移多补少 | `diagrams/transfer.py` | `make_transfer_balance_diagram` | 第3讲 |
| 人民币列表 | `diagrams/rmb_list.py` | `make_rmb_payment_table` | 第4讲 |
| 画线比较 | `diagrams/line_compare.py` | `make_line_compare_diagram` | 第5讲 |
| 搭配连线 | `diagrams/match_link.py` | `make_match_link_diagram` | 第6讲 |
| 爬井问题 | `diagrams/well_climb.py` | `make_well_climb_diagram` | 第7讲 |
| 锯木头间隔 | `diagrams/interval.py` | `make_saw_diagram` | 第8讲 |
| 租船进一 | `diagrams/boat_rental.py` | `make_boat_rental_diagram` | 第9讲 |
| 周期珠子 | `diagrams/period.py` | `make_period_bead_diagram` | 第21讲 |
| 公共图元 | `diagrams/common.py` | `_person_circle`、`_horizontal_ellipsis` | 各题型 |
| 图标 | `diagrams/icon_assets.py` | `load_icon_png` | 第6讲饮料/菜品、第7讲蜗牛 |

**新讲次流程**：

1. 查 JSON 里该讲的 **题型**（如「周期问题」）—— 已有模块则直接复用，只写 `problem_N.py`
2. 全新题型才在 `diagrams/` 新建 `xxx.py` + `XxxDiagramMixin`，并在 `lesson_base` 继承
3. 若必须改已有 `make_*_diagram`，同步改所有调用该题型的 `problem_*.py`，并 `-ql` 预览
4. `lesson_base.py` 只组合 Mixin，不再内联图解逻辑

**共用示例（周期问题）**：

```python
# problem_21.py — 珠子，周期5，求第32颗
diag = self.make_period_bead_diagram(
    [GREY_B, GREY_B, GREY_B, BLUE_D, BLUE_D],
    ["灰", "灰", "灰", "蓝", "蓝"],
    32, draw_y, ...
)

# 以后 problem_XX.py — 彩灯，周期6，求第100盏 → 同一函数，换 pattern 与 total_index
```

---

## 十一、图解布局与坐标（第 7～9 讲）

### 11.1 `arrange(aligned_edge=DOWN)` 会破坏竖向刻度对齐

**现象**（第7讲爬井）：每日箭头列与井竖轴 0～7 米刻度错位；第5天图形尤其偏高。

**原因**：

- `well_block` 含 `bottom_label`，底边低于井底刻度
- `days_block` 与 `final_graphics` 未在同一 Group，布局只移动了前4天
- `align_to` / `arrange(DOWN)` 按外接矩形底边对齐，改变了 y 坐标

**正确做法**：

- 共用刻度元素纳入同一 `Group` 再水平排布
- 用 `_sync_block_floor_to_well` 只调 y，`_place_right_of` 只调 x
- 引导虚线从主轴线 `well_x` 连到各天箭头，勿中途断开

### 11.2 辅助说明图要全程保留

**现象**（第7讲）：图解3 绘制每日箭头时左侧「一天」循环图消失。

**做法**：下一段用 `self.add(..., cycle_block, ...)` 显式保留；**勿** `FadeOut` 教学用辅助图。

### 11.3 多层 Brace 防重叠

**现象**（第9讲租船）：上方总船数大括号与下方各段「4人」小括号文字重叠。

**做法**：

- **上下大括号文案分工**：上=总人数，下=船数（与教材一致）
- 上方大括号锚到**高于小标注**的虚拟横线（`people_span_y = base_y + tick_h + 0.50`），勿直接 `Brace(main_line, UP, buff=0.62)`

### 11.4 满员段较多时分批动画

8 段「4人」若逐个 `FadeIn` 过慢，可每 2 段一批（第9讲 `batch_size=2`），保持节奏。

---

## 十二、数据与母题（第 8 讲教训）

### 12.1 一题一型，母题勿混

第 8 讲 JSON 曾把「锯木头」与「爬楼梯」写在同一 `mainProblem`，与教材母题精讲不符。

**处理**：

- 同步改 `public/data/problems/8.json` 与 `datas/draw_math_all_lessons.json`
- 拓展题/练习册中异型题可保留，但**视频只演示母题那一型**
- 爬楼梯间隔问题若单独成讲，另建 lesson 数据

---

## 十三、作答段文字说明（第 8～9 讲）

列式前加 1～2 行 **GREY_B 说明**（`font_size=24`），分步 `FadeIn`，学生更易跟上：

```python
# 第8讲示例
explain = self.safe_text("锯断后总共4段，每段4米，那么原木长度为：", ...)

# 第9讲示例
explain = self.safe_text(f"先租满{quotient}条船，还剩{remainder}人，", ...)
explain2 = self.safe_text("所有人都要有船坐，还要再租1条：", ...)
```

再显示 `3+1=4` 或 `8+1=9` 等算式。

---

## 十四、methodType 子目录（多画法并存）

脚本路径 **必须** 与 JSON `methodType` 一致，不能全堆在 `图示法/`：

| methodType | 示例讲次 |
|------------|----------|
| 图示法 | 1, 2, 3, 7, 8, 21 |
| 列表法 | 4 |
| 画线法 | 5 |
| 连线法 | 6 |
| 线段图法 | 9 |

`render_all_videos.py` 扫描 `manim/scenes/{methodType}/problem_*.py`，新画法首次使用时**新建中文子目录**。

---

## 十五、第 1～9 讲参考文件索引

| 讲次 | Scene | 图解 | 可借鉴点 |
|------|-------|------|----------|
| 1 | `图示法/problem_1.py` | between | intro 模板、待求标红 |
| 2 | `图示法/problem_2.py` | queue | BraceBetweenPoints |
| 3 | `图示法/problem_3.py` | transfer | 移多补少、FadeOut 后从树摘除 |
| 4 | `列表法/problem_4.py` | rmb_list | 表格枚举 |
| 5 | `画线法/problem_5.py` | line_compare | 左对齐线段 |
| 6 | `连线法/problem_6.py` | match_link | PNG 图标、上下连线 |
| 7 | `图示法/problem_7.py` | well_climb | 多区布局、引导虚线、单轴单图标 |
| 8 | `图示法/problem_8.py` | interval | 实线+虚线+作答说明 |
| 9 | `线段图法/problem_9.py` | boat_rental | 线段图法首讲、进一法、5 步图解 |

完整表见 [lessons-catalog.md](lessons-catalog.md)。
