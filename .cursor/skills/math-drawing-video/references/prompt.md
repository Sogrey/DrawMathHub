# 小学数学画图法教学视频制作 Prompt

> 基于 Manim + SafeScene 框架，制作小学数学"画图解题法"系列教学视频的经验规则。
> 覆盖多种图解方法——用图形、表格、线段等可视化手段表示数学关系，帮助学生直观理解。

---

## 一、视频结构模板

```
片头（show_title） → 概念引入 → 题目展示 → 分步画图 → 画图分析 → 列式计算 → 作答 → 片尾（show_credits）
```

各环节规则：

| 环节 | 要点 |
|------|------|
| 片头 | `show_title("主题", subtitle="画图解题法 · 方法名")`，副标题必须体现具体图解方法 |
| 概念引入 | 用生活场景引入（排队、楼层数等），停留3-4秒让学生理解 |
| 题目展示 | 题目从出现起**始终保留**直到片尾前最后一刻，绝不提前淡出 |
| 分步画图 | 每步3-5秒停顿，步骤文字与图分区域不重叠 |
| 画图分析 | 复用已画好的图（缩小+偏移），不重新画 |
| 列式计算 | 分步→合并，逐步显示，保留到最后一屏 |
| 作答 | 格式 `答：xxxx。`（带单位），同屏保留题目+图+计算+答案 |
| 片尾 | `show_credits("THE END")` |

---

## 二、布局规则（最重要，决定画面质量）

### 2.1 事先规划区域，杜绝重叠

**在写代码之前**，先画区域草图，明确每个元素的位置和大小。

推荐的四区域布局（16:9 画面，已扣除顶部标题常驻区）：

```
┌──────────────────────────────────────┐
│ 标题常驻区 (safe_top → content_top)   │  ← show_title 缩移后占据
├──────────────────────────────────────┤
│ ① 题目区                              │  ← 紧接标题组下方
│   题目框（紧凑，内边距小）              │     高度约 0.8~1.2
├──────────────────────────────────────┤
│ ② 步骤提示区                          │  ← 题目框与画图区之间
│   "第X步：..."                        │     一行文字即可
├──────────────────────────────────────┤
│ ③ 画图区（居中，空间最大）             │  ← 画面中下部主体区域
│   圆圈/线段/方格 + 标注                │
│                                      │
├──────────────────────────────────────┤
│ ④ 底部信息区                          │  ← safe_subtitle 位置
│   逐条解释说明                        │     或计算过程
└──────────────────────────────────────┘
```

### 2.2 区域定位关键公式

```python
# 段内小标题（题型讲解「什么是…？」等）：
s_title = self.place_section_title("什么是之间问题？", font_size=40)
body = VGroup(...).arrange(DOWN)
self.place_below_section_title(body, s_title, buff=0.55)
# 关键点拨等全屏段落：正文用 content_center 居中，勿用 safe_subtitle

# 题目框：紧跟标题组底部
title_bottom = self._title_group.get_bottom()[1]
prob_top = title_bottom - 0.35     # PROB_TOP_GAP，留足间距
prob_h = 1.0                       # 紧凑高度
prob_bottom = prob_top - prob_h

# 步骤提示：题目框下方
step_y = prob_bottom - 0.25

# 画图区：步骤提示至画面底部之间居中
draw_area_top = prob_bottom - 0.5
draw_area_bottom = self.safe_bottom + 0.3
draw_y_center = (draw_area_top + draw_area_bottom) / 2

# 计算/分析：画图缩小偏移后，腾出的左侧空间
left_x = self.safe_left + 0.8
```

### 2.3 重叠检查清单

每写完一段动画代码，检查：

- [ ] 左上角标题与段内小标题是否重叠？（`place_section_title` 相对 `_title_group` 底边定位）
- [ ] 段内正文是否紧跟小标题？（`place_below_section_title`，勿单独用 `content_center` 偏移）
- [ ] 关键点拨等全屏段落正文是否居中？（`content_center`，勿用 `safe_subtitle`）
- [ ] 题目框与标题组副标题是否重叠？（用 `title_bottom` 动态定位）
- [ ] 步骤文字与圆圈/图形是否重叠？（步骤在画图区上方，不在同一 y 范围）
- [ ] 计算过程与题目框是否重叠？（计算区 y 起点必须 < prob_bottom）
- [ ] 缩小后的图与文字是否重叠？（用 `diagram_all.get_top()[1]` 作为文字区下界）
- [ ] 一行文字是否超出左右安全区？（`clamp_content` 保底）

---

## 三、题目显示规则

### 3.1 格式

```python
prob_line1 = self.safe_text("题目：操场排队，从左边数起，玲玲是第6个，丽丽是第16个。", ...)
prob_line2 = self.safe_text("玲玲和丽丽之间有几人？", ...)
```

- **不加**单独的"题目"标签（会重叠）
- 第一行以"题目："开头即可
- 用边框圈住可增强视觉，但内边距要小（高度 0.8~1.2）

### 3.2 生命周期

- **入**：FadeIn，约 4 秒阅读时间
- **全程保留**：画图、分析、计算过程中，题目框始终可见
- **出**：只在最终答案停留 5 秒后，与答案一起淡出，然后进片尾

---

## 四、画图规则

### 4.1 图解方法清单

副标题中的方法名必须从以下清单中选择（包括但不限于）：

| 方法 | 适用问题类型 | 图示方式 |
|------|------------|---------|
| 图示法 | 之间问题、排队问题 | `make_between_diagram`：前缀圈/省略号 + 关键人 + 之间(边圈+横省略号+边圈) + 关键人 + 后缀冗余圈 |
| 列表法 | 排列组合、枚举问题 | 表格行列，逐行逐列填入 |
| 画线法 | 距离问题、路线问题 | 线段+标记点，标注距离 |
| 连线法 | 对应问题、匹配问题 | 左右两组元素，线段一一连接 |
| 线段图法 | 和差倍分问题 | 线段+大括号，标注数量关系 |
| 竖式法 | 进退位加减法 | 竖式对齐，逐位计算，进位标注 |
| 树状图法 | 排列组合、分类讨论 | 从根节点逐层分支 |
| 倒推法 | 逆向计算问题 | 从结果倒推，箭头反向标注 |
| 逆推法 | 同倒推法 | 同上，不同教材叫法 |
| 年龄轴法 | 年龄问题 | 时间轴+人物年龄标注 |
| 假设法 | 鸡兔同笼类 | 假设全A→算差→调整比例 |
| 打包法 | 分组问题 | 将元素框成分组，标注每份数量 |
| 流程图法 | 多步骤问题 | 矩形框+箭头，逐步推进 |
| 移多补少法 | 平均数问题 | 两行元素，箭头表示移动 |
| 插旗法 | 周期问题 | 周期标记+插旗定位 |
| 十字交叉法 | 浓度/比例问题 | 交叉线标注比例 |
| 天平法 | 等量代换 | 天平两端，等量关系 |
| 韦恩图法 | 集合交并问题 | 圆圈重叠区域，标注各部分 |

**副标题格式**：`画图解题法 · {方法名}`

例：
- `show_title("之间问题", subtitle="画图解题法 · 图示法")`
- `show_title("鸡兔同笼", subtitle="画图解题法 · 假设法")`
- `show_title("和差问题", subtitle="画图解题法 · 线段图法")`

### 4.2 从题目复制信息（核心创新点）

画图中用到的关键信息（人名、数字），从题目文字位置**复制一份**，用动画飞到图上对应位置：

```python
# 从题目复制"玲玲"
lingling_copy = self.safe_text("玲玲", font_size=22, color=YELLOW)
lingling_copy.move_to(prob_text 中"玲玲"的大致位置)
self.add(lingling_copy)

# 设置目标位置（图上标注处）
lingling_copy_target = lingling_name.copy()

# 飞行动画
self.play(Transform(lingling_copy, lingling_copy_target), run_time=0.8)
self.remove(lingling_copy)

# 然后显示正式标注
self.play(FadeIn(lingling_fill), FadeIn(lingling_name), ...)
```

**为什么这样做**：
- 学生直观看到"数据从题目来"，不是凭空捏造
- 强化"读题→提取信息→画图"的思维链路
- 动画过程本身就是教学

### 4.3 画图步骤动画节奏

**之间问题（图示法）**：关键人两侧各留几圈标明起止，仅「之间」中段用**横向**省略号；前缀/后缀人数过大时也用省略号，勿画满。

```python
diag = self.make_between_diagram(lingling_rank, lili_rank, draw_y)
# 示意：⚪⚪⚪⚪⚪ ⚪玲玲 ⚪ ··· ⚪ ⚪丽丽 ⚪⚪
# 50/500 人前：··· ⚪⚪ ⚪玲玲 …（前缀超 5 人时左侧也用横向省略号）

for part in diag["draw_order"]:
    ...
self.safe_subtitle("关键人两侧各留几圈，之间未知人数用横向省略号表示", wait=3)
```

其他题型可逐个画圆圈；每步完成后 3–5 秒停顿 + 底部字幕解释。

### 4.4 图的复用

画图完成后需腾出空间做计算时，**缩小+偏移**而非重画：

```python
diagram_all.generate_target()
diagram_all.target.scale(0.55)
diagram_all.target.move_to(右下目标位置)
self.play(MoveToTarget(diagram_all), run_time=1.0)
```

---

## 五、计算与作答规则

### 5.1 列式计算

分步展示，保留全流程：

```python
# 步骤1：丽丽前面的人数
step1: "丽丽前面的人数：" + "16 - 1 = 15" + "（人）"
# 步骤2：之间的人数
step2: "之间的人数：" + "15 - 6 = 9" + "（人）"
# 合并算式（高亮框）
combined: "合并算式：" + "16 - 1 - 6 = 9" + "（人）"
```

合并算式用 `SurroundingRectangle` 加红色高亮框。

### 5.2 最终作答

```
答：玲玲和丽丽之间有9人。
```

- 不加框，正常文字显示
- 位于计算过程下方
- **同屏保留**：题目框 + 缩小图 + 计算过程 + 答案
- 停留 5 秒，供学生截图

### 5.3 最后一屏画面

```
┌──────────────────────────────────────┐
│ § 之间问题  画图解题法·图示法          │  ← 标题
│ ┌─ 题目框 ─────────────────────────┐ │
│ │ 题目：操场排队...之间有几人？     │ │  ← 题目
│ └──────────────────────────────────┘ │
│                                      │
│ 列式计算                             │  ← 计算标题
│ 丽丽前面的人数：16-1=15（人）         │  ← 步骤1
│ 之间的人数：15-6=9（人）              │  ← 步骤2
│ 合并算式：[16-1-6=9（人）]            │  ← 合并（高亮）
│ 答：玲玲和丽丽之间有9人。             │  ← 作答
│                    ┌──缩小图──┐       │  ← 右侧缩小图
│                    │○○○●○○○○●│       │
│                    └─────────┘       │
└──────────────────────────────────────┘
```

这一屏可以截图 = 完整的解题过程。

---

## 六、Manim CE 坑点速查

> 更多实战踩坑见 [lessons-learned.md](lessons-learned.md)。

| 坑 | 正确做法 |
|----|---------|
| Python 3.8 类型注解 `float \| None` | 文件头加 `from __future__ import annotations` |
| `scene.time`（0.18 不存在） | 用 `scene.renderer.time` |
| 段内标题与左上角标题重叠 | `place_section_title` + `place_below_section_title`，勿全局下移 `content_center` |
| 之间问题画满全部圈 | 用 `make_between_diagram`，中间横省略号 + 边圈标红 |
| 关键点拨长句溢出 | `safe_wrapped_text`；JSON 内 `\n` 强制换行 |
| `Rectangle(corner_radius=...)` | 改用 `RoundedRectangle` |
| `VGroup.bounding_box` | 用 `get_left/right/top/bottom()` |
| 渲染中断后再次渲染报错 | 删除 `partial_movie_files` 再重渲 |
| 分步学习切换不播第一段 | 前端 `nextTick` 后再 `playSegment(0)` |

---

## 七、完整脚本骨架

```python
"""主题 — 画图解题法（{方法名}）
用法: python -m manim script.py SceneName -qh
"""
from safe_video import SafeScene
from manim import *
import numpy as np

class MyVideo(SafeScene):
    def construct(self):
        # 0. 区域规划（动态基于标题组）
        self.show_title("主题", subtitle="画图解题法 · {方法名}")
        self.init_layout_after_title(prob_h=1.0)
        # 段内小标题示例：
        # s_title = self.place_section_title("什么是…？", font_size=40)
        title_bottom = self._title_group.get_bottom()[1]
        prob_top = title_bottom - 0.35
        prob_h = 1.0
        prob_bottom = prob_top - prob_h
        step_y = prob_bottom - 0.25
        draw_area_top = prob_bottom - 0.5
        draw_area_bottom = self.safe_bottom + 0.3
        draw_y = (draw_area_top + draw_area_bottom) / 2

        # 1. 概念引入（用完即清除）
        # ...

        # 2. 题目展示（保留到片尾前）
        prob_all = VGroup(prob_bg, prob_line1, prob_line2)
        self.play(FadeIn(prob_all, shift=DOWN * 0.3), run_time=0.8)
        self.wait(4)

        # 3. 分步画图（步骤文字在 step_y，图在 draw_y）
        for step in steps:
            label = self.safe_text(step_text, font_size=26, color=ORANGE)
            label.move_to([0, step_y, 0])
            self.play(FadeIn(label), run_time=0.5)

            # 从题目复制关键信息动画
            # ... Transform(copy, target) ...

            # 画图动画
            # ...

            self.safe_subtitle(explanation, wait=3)
            self.play(FadeOut(label), run_time=0.3)

        # 4. 图缩小偏移
        diagram_all.generate_target()
        diagram_all.target.scale(0.55).move_to(右下位置)
        self.play(MoveToTarget(diagram_all), run_time=1.0)

        # 5. 画图分析（左侧）
        # ...

        # 6. 列式计算（左侧，分步→合并→高亮）
        # ...

        # 7. 作答（同屏保留所有）
        answer = self.safe_text("答：xxx。", font_size=34, color=YELLOW)
        # 定位在合并算式下方
        self.play(FadeIn(answer, shift=UP * 0.2), run_time=0.8)
        self.wait(5)

        # 8. 全部淡出 → 片尾
        self.play(FadeOut(VGroup(all_elements)), run_time=0.5)
        self.show_credits("THE END")
```

---

## 八、渲染命令

```bash
# 模块方式（不依赖 PATH）
cd 工作目录 && python -m manim script.py SceneName -qh

# 全路径方式
cd 工作目录 && C:\...\python.exe -m manim script.py SceneName -qh
```

输出：`manim/scenes/{methodType}/media/videos/problem_{id}/1080p60/{SceneName}.mp4`

归档至 Vue 静态目录：

```
public/videos/problem-{id}/example-{n}.mp4
```

- `{methodType}`：与 JSON 中 `methodType` 一致（图示法、线段图法…）
- `{id}`：题型 id，与 `public/data/problems/{id}.json` 一致
- `{n}`：0 = 母题精讲，1+ = 举一反三序号
