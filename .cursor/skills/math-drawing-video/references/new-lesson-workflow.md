# 新讲次制作流程

> **新开对话**：本文（怎么做）+ [lessons-catalog.md](./lessons-catalog.md)（查复用）+ [lessons-learned.md](./lessons-learned.md)（避坑）+ `public/data/problems/{N}.json`。

**勿与 catalog 合并**：流程说明与讲次总表职责不同；总表只维护在 catalog。

## 0. 一分钟判断：复用还是新建？

```
读 JSON.methodType + 题型
    │
    ├─ catalog 已有 make_*_diagram？ → 只写 problem_N.py
    │
    └─ 全新题型？ → diagrams/xxx.py + lesson_base 注册 + problem_N.py
```

脚本目录必须与 JSON `methodType` 一致（18 种中文子目录）。**完整讲次表** → [lessons-catalog.md](./lessons-catalog.md)。

---

## 1. 数据准备

1. 核对 `public/data/problems/{N}.json` 与 `datas/draw_math_all_lessons.json` 母题一致
2. **一题一型**，母题勿混情境
3. 数据来自 Excel/总表时：`node scripts/convertData.js`
4. 记录 UUID：`id`、`mainProblem.id` → 视频路径

---

## 2. 规划（可选 tasks/lesson-NN-xxx/summary.md）

| 项 | 内容 |
|----|------|
| 母题数字 | Scene 类常量 |
| 教材图解 | 对照母题精讲，列分步 |
| 分段 | intro → question → draw-1…n → written → keypoints → end |
| Mixin | 查 `diagrams/` + catalog |
| 图标 | PNG → `manim/assets/icons/`，`load_icon_png` |

---

## 3. 实现顺序

```
diagrams/xxx.py（若需要）
  → lesson_base.py 注册 Mixin
  → manim/scenes/{methodType}/problem_N.py
  → ql 预览 → 微调 →（可选）qh
```

### 3.1 Scene 骨架

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
            # concept_title = "题型识别" + 要点 layout_numbered_features

        with self.segment("question", "题目", "segments/02.mp4", "..."):
            prob_all = self.make_problem_box(...)

        diag = self.make_xxx_diagram(..., self.layout["draw_y"])
        # draw-*：self.add 保留已有元素
        # written → keypoints → end
        self.finalize_lesson()
```

### 3.2 intro

- 片头+讲解合并为 `intro`
- 上：**题型识别** + 定义；下：要点列表（链式定位，见 lessons-learned §六）

### 3.3 图解 Mixin

- 返回 `dict`；`move_to([0,draw_y,0])` + `clamp_content`
- **图形勿** `set_opacity(0)` 再 `FadeIn`（见 lessons-learned §十五）
- PNG 用 `Group`；含图标的 `diagram_all` 也用 `Group`

### 3.4 段间 `self.add`

每段显式 `self.add(prob_all, …已有图元)`；辅助图全程保留。

---

## 4. 作答段

```python
written_diagram_scale = self.place_diagram_for_written(diagram_all)
# 左列式：written_left_x / written_left_y
# 点拨：play_keypoints_only(..., diagram=..., from_scale=written_diagram_scale)
```

---

## 5. 渲染

```powershell
python scripts/render_all_videos.py --quality ql --lessons N
```

产出：`public/videos/{problemUuid}/{exampleUuid}/`（`full.mp4` + `cover.png` 等同目录）。manifest 禁止手写。封面在 keypoints 自动导出（`EXPORT_HALL_COVER=0` 可关）。详见 `doc/manim/批量渲染.md`。

---

## 6. 质量检查

- [ ] intro「题型识别」与要点无重叠
- [ ] 题目框保留至 written 结束
- [ ] 图解/步骤/字幕无叠字
- [ ] 图形用 FadeIn/Create 时未预置 opacity 0
- [ ] 点拨图解回中
- [ ] 视频目录 `cover.png` 仅为图解（无关键点拨标题）
- [ ] ql 通过后再 qh

---

## 7. 新对话 Prompt 模板

```
制作第{N}讲 {题型} Manim 视频。
数据：@public/data/problems/{N}.json
规范：@math-drawing-video（先读 workflow + catalog）
参考：同 methodType 最近一讲 problem_{M}.py
```

---

## 8. 相关文档

| 文档 | 用途 |
|------|------|
| [lessons-catalog.md](./lessons-catalog.md) | 1～60 讲索引与 API |
| [lessons-learned.md](./lessons-learned.md) | 踩坑 SSOT |
| [prompt.md](./prompt.md) | 四区域、18 种方法 |
| [doc/manim/技巧与踩坑.md](../../../doc/manim/技巧与踩坑.md) | 人类可读摘要 |
| [doc/manim/制作流程.md](../../../doc/manim/制作流程.md) | 命令与归档 |
