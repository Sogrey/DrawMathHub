# 新讲次制作流程（前 10 讲经验沉淀）

> **新开对话时**：把本文 + [lessons-catalog.md](./lessons-catalog.md) + 对应 `public/data/problems/{N}.json` 发给 AI，即可快速上手第 11 讲及以后。

## 0. 一分钟判断：复用还是新建？

```
读 JSON.methodType + 题型
    │
    ├─ diagrams/ 已有 make_*_diagram？ → 只写 problem_N.py（改数字/文案）
    │
    └─ 全新题型？ → 新建 diagrams/xxx.py + lesson_base 注册 + problem_N.py
```

**脚本目录必须与 JSON `methodType` 一致**（18 种子目录名，含中文）：

| 讲次 | 题型 | methodType | 脚本 | 图解入口 |
|------|------|------------|------|----------|
| 1 | 之间问题 | 图示法 | `图示法/problem_1.py` | `make_between_diagram` |
| 2 | 排队问题 | 图示法 | `图示法/problem_2.py` | `make_queue_total_diagram` |
| 3 | 移多补少 | 图示法 | `图示法/problem_3.py` | `make_transfer_balance_diagram` |
| 4 | 人民币 | 列表法 | `列表法/problem_4.py` | `make_rmb_payment_table` |
| 5 | 逻辑推理 | 画线法 | `画线法/problem_5.py` | `make_line_compare_diagram` |
| 6 | 搭配问题 | 连线法 | `连线法/problem_6.py` | `make_match_link_diagram` |
| 7 | 爬井问题 | 图示法 | `图示法/problem_7.py` | `make_well_climb_diagram` |
| 8 | 间隔问题 | 图示法 | `图示法/problem_8.py` | `make_saw_diagram` |
| 9 | 租船问题 | 线段图法 | `线段图法/problem_9.py` | `make_boat_rental_diagram` |
| 13 | 倍数问题 | 线段图法 | `线段图法/problem_13.py` | `make_multiple_times_diagram` |
| 14 | 错中求解问题 | 倒推法 | `倒推法/problem_14.py` | `make_wrong_subtract_diagram` |
| 15 | 平均数问题（一） | 图示法 | `图示法/problem_15.py` | `make_middle_average_diagram` |
| 16 | 和倍问题 | 线段图法 | `线段图法/problem_16.py` | `make_sum_times_diagram` |
| 17 | 差倍问题 | 线段图法 | `线段图法/problem_17.py` | `make_diff_times_diagram` |
| 18 | 和差问题 | 线段图法 | `线段图法/problem_18.py` | `make_sum_diff_diagram` |
| 19 | 年龄问题（一） | 线段图法 | `线段图法/problem_19.py` | `make_diff_times_diagram` |
| 20 | 重叠问题 | 图示法 | `图示法/problem_20.py` | `make_overlap_bars_diagram` |
| 22 | 归一问题 | 线段图法 | `线段图法/problem_22.py` | `make_unitary_line_diagram` |
| 23 | 归总问题 | 线段图法 | `线段图法/problem_23.py` | `make_aggregate_line_diagram` |
| 24 | 方阵问题 | 图示法 | `图示法/problem_24.py` | `make_hollow_square_diagram` |
| 25 | 还原问题（一） | 逆推法 | `逆推法/problem_25.py` | `make_restore_flow_diagram` |
| 11 | 时间问题 | 竖式法 | `竖式法/problem_11.py` | `make_time_subtract_vertical` |
| 12 | 组数问题 | 树状图法 | `树状图法/problem_12.py` | `make_digit_tree_diagram` |
| 21 | 周期问题 | 图示法 | `图示法/problem_21.py` | `make_period_bead_diagram` |

完整对照见 [lessons-catalog.md](./lessons-catalog.md)。

---

## 1. 数据准备（先做）

1. 核对 `public/data/problems/{N}.json` 与 `datas/draw_math_all_lessons.json` **母题一致**
2. **一题一型**：母题勿混不同情境（例：第 8 讲曾混锯木头+爬楼梯，已拆分）
3. 数据变更来自 Excel/总表时：`node scripts/convertData.js`
4. 记录 UUID：`id`（problemUuid）、`mainProblem.id`（exampleUuid）→ 视频输出路径

---

## 2. 规划（建议写 tasks/lesson-NN-xxx/summary.md）

| 项 | 内容 |
|----|------|
| 母题数字 | 从 JSON 提取，写成 Scene 类常量 |
| 教材图解 | 对照「母题精讲」配图，列分步动画 |
| 分段设计 | intro → question → draw-1…n → written → keypoints → end |
| 是否新 Mixin | 查 `manim/scenes/_shared/diagrams/` |
| 资源 | PNG 图标放 `manim/assets/icons/`，用 `load_icon_png` |

---

## 3. 实现顺序

```
diagrams/xxx.py（若需要）
    → lesson_base.py 注册 Mixin
    → manim/scenes/{methodType}/problem_N.py
    → ql 渲染预览
    → 用户目视反馈 → 微调
    → （可选）qh 成片
```

### 3.1 Scene 固定骨架（与第 1～9 讲一致）

```python
class ProblemNScene(MathLessonScene):
    EXAMPLE_INDEX = 0

    def construct(self):
        data = self.load_problem()
        self.init_video_recorder()
        mp = self.main_problem

        with self.segment("intro", "题型讲解", "segments/01.mp4", "..."):
            self.show_title(data["title"], subtitle=f"画图解题法 · {data['methodType']}")
            self.init_layout_after_title(prob_h=1.0)
            # 概念块 + 分隔线 + layout_numbered_features（3 条特征）

        with self.segment("question", "题目", "segments/02.mp4", "..."):
            prob_all = self.make_problem_box("题目：...", "...")
            # prob_all 保留到 written 结束

        draw_y = self.layout["draw_y"]
        diag = self.make_xxx_diagram(..., draw_y)

        # draw-1 … draw-n：每段 self.add 保留已有元素
        # written：缩小图 + 列式（见 §4）
        # keypoints：play_keypoints_only(..., diagram=..., from_scale=...)
        # end：show_credits

        self.finalize_lesson()
```

### 3.2 intro 段（所有已做讲次通用）

- **片头 + 题型讲解合并**为单段 `intro`（`segments/01.mp4`）
- 上：「什么是 XX？」+ 1～2 行定义
- 下：「XX 的三个特征」+ `layout_numbered_features`（≤3 单列，≥4 双列）
- 下板块相对 `concept_block.get_bottom()` **链式定位**，勿用固定 y

### 3.3 图解 Mixin 约定

- 返回 `dict`，含分步动画部件（`parts`、`cut_marks`、`layout_row` 等）
- 整体 `move_to([0, draw_y, 0])` 后 `clamp_content(full)`
- 底部 `hint` 一行说明图解含义
- **布局后勿破坏坐标**：见 [lessons-learned §十一](./lessons-learned.md)

### 3.4 图解段 `self.add` 规则

每进入新 `draw-*` 段，用 `self.add(...)` 显式保留：

- `prob_all`（题目框）
- 已出现的图解部件（勿依赖上一段末尾状态）

**辅助说明图**（如爬井「一天」图、锯木头示意图）**全程保留**，下一段勿 `FadeOut`。

---

## 4. 作答段（written）模板

```python
with self.segment("written", "作答", "segments/07.mp4", "..."):
    self.add(prob_all, diagram_all)
    written_diagram_scale = self.place_diagram_for_written(diagram_all)

    left_x = self.written_left_x()
    formula.move_to(np.array([left_x + formula.width / 2, self.written_left_y(0.45), 0]))
    formula.align_to(np.array([left_x, 0, 0]), LEFT)
    # 列式前 GREY_B 说明 → 算式 → 答（YELLOW + 红框）→ safe_subtitle
```

- 图解**右移**至右半区（`draw_y`），仅在超出右半宽时缩小
- 左侧 `written_left_x()` + `written_left_y(offset)` 放列式
- **勿用**旧写法 `scale(0.55)` + `content_bottom + 1.55` 贴右下角

点拨段：

```python
self.play_keypoints_only(mp["keyPoints"], wait=6,
    diagram=diagram_all, from_scale=written_diagram_scale)
```

---

## 5. 渲染与归档

```powershell
# 项目根目录 — 单讲预览（推荐）
python scripts/render_all_videos.py --quality ql --lessons 9

# 或进入脚本目录
cd manim/scenes/线段图法
python -m manim problem_9.py Problem9Scene -ql
python ..\_shared\post_render.py --lesson 9 `
  --rendered media\videos\problem_9\480p15\Problem9Scene.mp4
```

产出：`public/videos/{problemUuid}/{exampleUuid}/full.mp4` + `manifest.json` + `segments/`

**manifest 禁止手写**；`fullVideo` 用相对路径 `full.mp4`。

---

## 6. 质量检查（每讲必过）

- [ ] intro 概念与特征无重叠
- [ ] 题目框全程可见至 written 结束
- [ ] 图解与步骤行、底部字幕无重叠
- [ ] 分步图解逻辑与教材「画图分析」一致
- [ ] 作答列式前有文字说明（适用时）
- [ ] 点拨段图解回中放大
- [ ] `segments` 数量与 `segment()` 一致
- [ ] ql 目视通过后再 qh

---

## 7. 新对话推荐 Prompt 模板

```
制作第{N}讲 {题型} Manim 视频。
数据：@public/data/problems/{N}.json
教材：@datas/draw_math_all_lessons.json 对应母题精讲
规范：@.cursor/skills/math-drawing-video/references/new-lesson-workflow.md
参考：同 methodType 最近一讲 problem_{M}.py
请先读题规划 tasks/lesson-{NN}-xxx/summary.md，再实现。
```

---

## 8. 相关文档

| 文档 | 用途 |
|------|------|
| [lessons-learned.md](./lessons-learned.md) | 踩坑与细节 |
| [lessons-catalog.md](./lessons-catalog.md) | 1～10 讲索引 |
| [prompt.md](./prompt.md) | 四区域布局、18 种方法 |
| [../../doc/manim/制作流程.md](../../../doc/manim/制作流程.md) | 命令与归档 |
