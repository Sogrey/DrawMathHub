# 已制作讲次目录（1～25）

> 新讲次先查本表：能否复用 `diagrams/` 模块与哪条 `problem_*.py` 作结构参考。

## 总览

| 讲次 | 题型 | methodType | Scene | 图解模块 | 状态 |
|------|------|------------|-------|----------|------|
| 1 | 之间问题 | 图示法 | `图示法/problem_1.py` | `between.py` | ✅ |
| 2 | 排队问题 | 图示法 | `图示法/problem_2.py` | `queue.py` | ✅ |
| 3 | 移多补少 | 图示法 | `图示法/problem_3.py` | `transfer.py` | ✅ |
| 4 | 人民币 | 列表法 | `列表法/problem_4.py` | `rmb_list.py` | ✅ |
| 5 | 逻辑推理（一） | 画线法 | `画线法/problem_5.py` | `line_compare.py` | ✅ |
| 6 | 搭配问题 | 连线法 | `连线法/problem_6.py` | `match_link.py` | ✅ |
| 7 | 爬井问题 | 图示法 | `图示法/problem_7.py` | `well_climb.py` | ✅ |
| 8 | 间隔问题（锯木头） | 图示法 | `图示法/problem_8.py` | `interval.py` | ✅ |
| 9 | 租船问题（进一法） | 线段图法 | `线段图法/problem_9.py` | `boat_rental.py` | ✅ |
| 13 | 倍数问题 | 线段图法 | `线段图法/problem_13.py` | `multiple_times.py` | ✅ |
| 14 | 错中求解问题 | 倒推法 | `倒推法/problem_14.py` | `wrong_subtract.py` | ✅ |
| 15 | 平均数问题（一） | 图示法 | `图示法/problem_15.py` | `average.py` | ✅ |
| 16 | 和倍问题 | 线段图法 | `线段图法/problem_16.py` | `sum_times.py` | ✅ |
| 17 | 差倍问题 | 线段图法 | `线段图法/problem_17.py` | `diff_times.py` | ✅ |
| 18 | 和差问题 | 线段图法 | `线段图法/problem_18.py` | `sum_diff.py` | ✅ |
| 19 | 年龄问题（一） | 线段图法 | `线段图法/problem_19.py` | `diff_times.py` | ✅ |
| 20 | 重叠问题 | 图示法 | `图示法/problem_20.py` | `overlap.py` | ✅ |
| 10 | 等量代换 | 图示法 | `图示法/problem_10.py` | `substitution.py` | ✅ |
| 11 | 时间问题 | 竖式法 | `竖式法/problem_11.py` | `time_vertical.py` | ✅ |
| 12 | 组数问题 | 树状图法 | `树状图法/problem_12.py` | `tree_digit.py` | ✅ |
| 21 | 周期问题 | 图示法 | `图示法/problem_21.py` | `period.py` | ✅ |
| 22 | 归一问题 | 线段图法 | `线段图法/problem_22.py` | `unitary.py` | ✅ |
| 23 | 归总问题 | 线段图法 | `线段图法/problem_23.py` | `aggregate.py` | ✅ |
| 24 | 方阵问题 | 图示法 | `图示法/problem_24.py` | `hollow_square.py` | ✅ |
| 25 | 还原问题（一） | 逆推法 | `逆推法/problem_25.py` | `restore_flow.py` | ✅ |

## 按 methodType 分目录

| 子目录 | 已有讲次 |
|--------|----------|
| `图示法/` | 1, 2, 3, 7, 8, 10, 15, 20, 21, 24 |
| `竖式法/` | 11（首个） |
| `树状图法/` | 12（首个） |
| `列表法/` | 4 |
| `画线法/` | 5 |
| `连线法/` | 6 |
| `线段图法/` | 9, 13, 16, 17, 18, 19, 22, 23 |
| `倒推法/` | 14（首个） |
| `逆推法/` | 25（首个） |

其余 11 种 methodType 目录尚未创建，新讲次首次使用时新建文件夹即可。

## 图解 API 速查

| 模块 | 方法 | 主要参数 |
|------|------|----------|
| `between.py` | `make_between_diagram` | 左排名, 右排名, draw_y |
| `queue.py` | `make_queue_total_diagram` | 前人数, 后人数, draw_y |
| `transfer.py` | `make_transfer_balance_diagram` | 多/少数量, 人名, draw_y |
| `rmb_list.py` | `make_rmb_payment_table` | 面额配置, 目标金额, draw_y |
| `line_compare.py` | `make_line_compare_diagram` | items[{name,length}], draw_y |
| `match_link.py` | `make_match_link_diagram` | 上排项, 下排项, draw_y |
| `well_climb.py` | `make_well_climb_diagram` | 井深, 上爬, 下滑, draw_y |
| `interval.py` | `make_saw_diagram` | 锯次数, 每段长, draw_y |
| `boat_rental.py` | `make_boat_rental_diagram` | 总人数, 每船容量, draw_y |
| `multiple_times.py` | `make_multiple_times_diagram` | unit_value, multiple, draw_y, less_by/more_by |
| `period.py` | `make_period_bead_diagram` | 颜色周期, 名称, 总序号, draw_y |
| `substitution.py` | `make_substitution_diagram` | give_per_receive, target_receive, draw_y |
| `time_vertical.py` | `make_time_subtract_vertical` | end_h/m, start_h/m, draw_y, result, borrow |
| `tree_digit.py` | `make_digit_tree_diagram` | digits, fixed_first, draw_y |
| `wrong_subtract.py` | `make_wrong_subtract_diagram` | minuend tens / subtrahend units correct/wrong, wrong_result, draw_y |
| `average.py` | `make_middle_average_diagram` | count, total_avg, front_avg, back_avg, draw_y |
| `sum_times.py` | `make_sum_times_diagram` | total, multiple, top/bottom name, draw_y |
| `diff_times.py` | `make_diff_times_diagram` | difference, multiple, top/bottom name, draw_y（含年龄差倍） |
| `overlap.py` | `make_overlap_bars_diagram` | piece_len, count, joined_len, draw_y |
| `unitary.py` | `make_unitary_line_diagram` | known_parts/total, new_parts, draw_y |
| `aggregate.py` | `make_aggregate_line_diagram` | old_unit/parts, new_unit, draw_y |
| `sum_diff.py` | `make_sum_diff_diagram` | total, difference, large/small name, draw_y |
| `hollow_square.py` | `make_hollow_square_diagram` | side_n, draw_y（单层空心方阵） |
| `restore_flow.py` | `make_restore_flow_diagram` | forward_ops, result, draw_y（流程图逆推） |

## 分段数量参考

| 讲次 | intro | question | draw | written | keypoints | end | 合计 segments |
|------|-------|----------|------|---------|-----------|-----|---------------|
| 1～6, 21 | 01 | 02 | 03～06 (×4) | 07 | keypoints | end | 9 |
| 7～8 | 01 | 02 | 03～06 (×4) | 07 | keypoints | end | 9 |
| 9 | 01 | 02 | 03～07 (×5) | 08 | keypoints | end | 10 |
| 18 | 01 | 02 | 03～07 (×5) | 08 | keypoints | end | 10 |

## 数据 UUID（视频路径）

| 讲次 | problemUuid | exampleUuid (母题) |
|------|-------------|------------------|
| 1 | 见 `1.json` | mainProblem.id |
| … | `public/data/problems/{N}.json` → `id` | → `mainProblem.id` |

视频目录：`public/videos/{problemUuid}/{exampleUuid}/`

## 结构参考推荐

| 场景 | 优先参考 |
|------|----------|
| 通用 intro / written / keypoints | `problem_1.py` |
| 大括号分段标注 | `problem_2.py` |
| 双行物对比（移多补少） | `problem_3.py` |
| 表格/列表枚举 | `problem_4.py` |
| 水平线段比较 | `problem_5.py` |
| 上下两排连线 | `problem_6.py` |
| 复杂分区布局 + 引导线 | `problem_7.py` |
| 水平实线+虚线切分 | `problem_8.py` |
| 线段图+进一法+多层 Brace | `problem_9.py` |
