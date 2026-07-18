# 小学数学画图解题法

一个面向小学生的数学解题法学习平台，通过可视化的画图方式帮助学生理解和掌握各类数学题型的解题方法。

## 功能特性

- **目录展示**：宫格形式展示60种解题方法，面向小学生，通俗易懂，可视化操作
- **规律分析**：先展示这类题的规律分析切入口（找规律、找关系、找结构等），说明该使用哪种画图法解决比较合理
- **例题引导**：Manim 预渲染演示视频，分步展示母题精讲的画图分析与规范解答（替代手动画板演示）
- **举一反三**：提供扩展题目练习，支持箭头切换和序号选择
- **练习区域**：解题页面提供练习区域，学生在画板上练习该类题型解决方法，填写答案，系统判定是否正确并给出提示
- **动态生成**：每次打开例题和练习题，重新生成新的题目和答案（待实现）
- **学习进度追踪**：本地存储已学习的题型，在目录列表上显示标记，并记录练习题正确率
- **匿名登录**：使用前先选择已有的昵称或新建一个昵称，学习记录和答题记录存储到 IndexedDB
- **密码保护**：对应昵称可以选择设置密码（默认不设置）

## 技术栈

| 分类 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 框架 | Vue | 3.x | 渐进式 JavaScript 框架 |
| 语言 | TypeScript | 5.x | 类型安全的 JavaScript |
| 构建工具 | Vite | 6.x | 快速构建工具 |
| UI样式 | TailwindCSS | 3.x | 原子化 CSS 框架 |
| 路由 | Vue Router | 4.x | Vue 路由管理 |
| 状态管理 | Pinia | 2.x | Vue 状态管理 |
| 演示视频 | Manim CE + SafeScene | - | 预渲染解题演示 MP4，供前端播放 |
| 练习画板 | 原生 Canvas API | - | 练习区自由绘制（画笔、圆形、矩形、橡皮擦） |
| 图标 | Lucide Vue | 1.x | 图标库 |
| 数据库 | IndexedDB (idb) | 8.x | 本地数据库存储用户和学习进度 |

## 项目结构

```
DrawMathHub/
├── src/
│   ├── components/          # 通用组件
│   │   ├── GridCard.vue       # 题型大厅卡片（Manim 封面背景 + 学习标记）
│   │   ├── Navigation.vue     # 导航组件
│   │   ├── SolutionVideoPlayer.vue # 解题演示视频（完整播放 + 分步交互）
│   │   └── PracticeCanvas.vue # 练习区域画布（原生 Canvas）
│   ├── views/               # 页面视图
│   │   ├── Home.vue         # 首页（目录展示）
│   │   ├── Problem.vue      # 解题页面（三Tab：学习例题/举一反三/练习）
│   │   └── Login.vue        # 登录页面（匿名登录+密码保护）
│   ├── data/                # 数据层
│   │   └── problems.ts      # 题目数据模型和加载函数
│   ├── stores/              # 状态管理
│   │   ├── problemStore.ts  # 解题状态
│   │   ├── progressStore.ts # 学习进度状态
│   │   └── userStore.ts     # 用户状态管理
│   ├── db/                  # 数据库操作
│   │   └── indexedDB.ts     # IndexedDB 数据库操作封装（idb）
│   ├── router/              # 路由配置
│   │   └── index.ts
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── public/                  # 静态资源
│   ├── data/
│   │   └── problems/        # 60 个题型 JSON + index.json（id、methodType 等元数据）
│   └── videos/              # Manim 渲染产出（UUID 目录，见 doc/manim）
│       └── {problemUuid}/{exampleUuid}/
│           ├── full.mp4
│           ├── cover.png    # 大厅封面（与完整视频同目录）
│           ├── manifest.json
│           └── segments/
├── manim/                   # Manim 脚本 → 见 doc/manim/
│   ├── README.md
│   └── scenes/
│       ├── _shared/         # safe_video, lesson_base, video_export
│       └── {methodType}/    # 共 18 种，如 图示法/problem_1.py
├── .cursor/skills/
│   └── math-drawing-video/  # Manim 垂域规范 + 踩坑记录
├── doc/                     # 文档
│   ├── 需求.md
│   ├── 项目规划.md
│   └── manim/               # Manim 专题：环境、脚本、制作流程、技巧与踩坑
│       ├── README.md
│       ├── 环境搭建.md
│       ├── 脚本编写.md
│       ├── 制作流程.md
│       ├── 批量渲染.md
│       └── 技巧与踩坑.md
├── public/data/problems/    # 运行时题目 JSON（含 index.json）
├── scripts/
│   └── convertData.js       # 可选：本地 datas 汇总 → public/data/problems/
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

> `datas/` 为本地可选原始汇总，已 gitignore；线上与开发均以 `public/data/problems/` 为准。

## 快速开始

### 安装依赖

```bash
pnpm install
```

### 开发模式

```bash
pnpm dev
```

访问 http://localhost:5173/ 即可开始学习。

### 构建生产版本

```bash
pnpm build
```

### 预览生产版本

```bash
pnpm preview
```

### 运行单元测试

```bash
pnpm test
```

## 主题配色（中国风 Chinoiserie）

深色磨砂质感，参考 [cncolor.art](https://cncolor.art/) 噪点纹理 + 玻璃态卡片，色系来自中国风配色系列：

| 色值 | 占比 | 用途 |
|------|------|------|
| `#C9563A` | 18.5% | 主色 / 强调按钮 |
| `#EAD6B8` | 17.4% | 正文 / 高亮文字 |
| `#777A86` | 12.9% | 次级文字 |
| `#292C30` | 6.9% | 页面底色 |
| `#684131` | 5.9% | 深棕辅助色 |

- **页面背景**：`#292C30` + SVG 噪点纹理
- **卡片**：半透明磨砂玻璃（`backdrop-blur` + `rgba` 底色）
- **导航栏**：半透明深色玻璃态

## 解题方法目录

共60种解题方法，覆盖以下类型：

- **图示法**（20讲）：之间问题、排队问题、移多补少问题等
- **线段图法**（24讲）：倍数问题、和倍问题、差倍问题、行程问题等
- **列表法**（3讲）：人民币问题、策略问题、逻辑推理问题等
- **连线法**（2讲）：搭配问题、逻辑推理问题等
- **树状图法**（2讲）：组数问题、概率问题等
- **假设法**（1讲）：鸡兔同笼问题等
- **其他方法**（8讲）：倒推法、逆推法、竖式法、流程图法等

## Manim 演示视频资产

例题演示使用 **Manim 预渲染视频**，支持完整播放与分步学习。

| 类型 | 路径 | 说明 |
|------|------|------|
| Python 脚本 | `manim/scenes/{methodType}/problem_{n}.py` | 按图解方法分子目录 |
| 题目数据 | `public/data/problems/{n}.json` | 含 `id`、`mainProblem.id` 等 uuid |
| 渲染产物 | `public/videos/{problemUuid}/{exampleUuid}/` | `full.mp4` + `cover.png` + `manifest.json` + `segments/` |
| 大厅封面 | 同上目录 `cover.png` | keypoints 图解裁切；`GridCard` 背景 |

**分步学习**：`SolutionVideoPlayer` 读取 manifest 的 `label` 与 `segments/*.mp4`。

**批量渲染**（默认自动出封面）：

```powershell
python scripts/render_all_videos.py                  # 全量 qh 成片 + 封面
python scripts/render_all_videos.py --quality ql --lessons 1-60   # 预览/补封面
```

详见 [doc/manim/批量渲染.md](doc/manim/批量渲染.md)。关闭封面：`EXPORT_HALL_COVER=0`。

**文档入口**：

- [doc/manim/README.md](doc/manim/README.md) — 环境、脚本、制作流程、批量渲染
- [doc/manim/技巧与踩坑.md](doc/manim/技巧与踩坑.md) — 画图解题技巧摘要、三份 Skill 文档如何分工
- [.cursor/skills/math-drawing-video/](.cursor/skills/math-drawing-video/SKILL.md) — Agent 规范（workflow / catalog / learned）
- [manim/README.md](manim/README.md) — 快速命令

**example 序号**：母题 `EXAMPLE_INDEX=0`；举一反三为 `extensionProblems` 对应序号。

## 开发进度

### ✅ 已完成

| 模块 | 完成内容 |
|------|----------|
| 项目基础 | Vite + Vue 3 + TypeScript + TailwindCSS + Vue Router + Pinia |
| 首页 | 60种题型宫格展示（Manim 图解封面）、方法类型筛选、学习进度标记、正确率显示 |
| 解题页面 | 规律分析展示、母题精讲展示、三Tab布局（学习例题/举一反三/练习） |
| 举一反三 | 扩展题目展示、箭头切换、序号显示 |
| 练习区域 | 题目展示、答案输入、提交判定、正确/错误提示 |
| 画板功能 | 原生Canvas实现，支持画笔、橡皮擦、圆形、矩形、颜色选择、粗细调整 |
| 用户系统 | 匿名登录、昵称选择、新建昵称、密码保护（SHA-256哈希） |
| 学习进度 | IndexedDB存储、已学习标记、练习次数、正确率统计 |
| 数据处理 | 60个题型JSON文件拆分、中文字段转英文、异步加载 |
| Manim 演示视频 | **第 1～60 讲** Scene / 图解 Mixin / `ql` 渲染管线齐备；规范见 `doc/manim/` 与 skill |
| 前端视频播放 | `SolutionVideoPlayer` 完整播放 + 分步学习（manifest） |

### 🔄 进行中

| 模块 | 状态 |
|------|------|
| 动态生成 | 待实现（当前使用静态题目） |
| 成片质量 | 按讲次 `qh` 精渲与目视返修（按需） |

### 📋 待开发（二期）

- 语音讲解功能（Web Speech API）
- 错题本
- 学习报告
- 成就系统
- 家长监控

## 开发规范

- 使用 TypeScript 严格模式
- 组件命名使用 PascalCase
- 文件命名使用 kebab-case
- 函数命名使用 camelCase
- 常量命名使用 UPPER_CASE

## License

MIT
