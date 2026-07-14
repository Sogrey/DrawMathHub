# DrawMathHub 上线前全检报告

**日期**：2026-07-14
**场景**：上线前检查（代码审查 + 安全审计 + QA测试与发布）
**审查目标**：`F:\woekspace\rust\DrawMathHub`（Vue 3 + TS 前端项目，小学数学画图解题法学习平台）
**参与成员**：产品官（gstack-product-reviewer） + 安全卫士（gstack-security-officer） + 质量门神（gstack-qa-lead）

---

## 📌 TL;DR（执行摘要）

- **整体结论**：🔴 **No-Go（有条件放行）** — 三方均倾向 Conditional Go，但 QA 门神明确指出存在上线硬阻塞项。综合判定：必须修复 6 项 P0 阻塞项后方可上线。
- **阻塞项数量**：🔴 6 项（其中 2 项为发布流程硬阻塞：源码未提交 + 未推送；4 项为功能/安全硬伤）
- **最大亮点**：工程基线扎实（TS strict 零错误、构建通过、零依赖漏洞、无密钥泄露、CI/CD 配置正确、双缓冲视频播放器设计精巧）
- **最大风险**：练习答案校验完全失效（`isCorrect=true` 硬编码）+ 关键源码（会话恢复/路由守卫/登录）未提交未推送 → 当前推送将部署缺少会话恢复逻辑的旧代码
- **下一步**：先 `git commit` + `git push` 解决发布流程阻塞；再依次修复答案校验、画板触屏、密码哈希、N+1 查询；P0 清零后即可上线

---

## 🎯 核心结论卡片

| 项目 | 内容 |
|------|------|
| Go / No-Go | 🔴 **No-Go（有条件放行）** — 修复 6 项 P0 后转 🟢 Go |
| 严重度分布 | 🔴 6 / 🟠 5 / 🟡 6 / 🟢 5 |
| 关键行动项 | 9 条（P0×6 + P1×3） |
| 建议负责人 | 前端工程负责人（功能/代码）+ 安全负责人（密码哈希/CSP） |
| 构建状态 | ✅ `vue-tsc` 零错误 / ✅ `vite build` 通过（1813 模块，9.6s） |
| 测试覆盖 | ❌ 0%（零测试文件） |
| 密钥泄露 | ✅ 无泄露（`.env` 仅含部署路径配置） |
| 依赖漏洞 | ✅ `npm audit` 0 漏洞（184 依赖） |

---

## 1. 各成员核心结论

### 🔍 产品官（代码审查 · review skill）
- **核心判断**：Conditional Go。代码工程质量较高 —— TypeScript strict 模式零错误、无 `any` 滥用、Composition API 规范、双缓冲视频播放器与 fetchJson 防 SPA 404 回退等设计精巧。但存在 3 个 🔴：练习答案校验完全失效（`isCorrect=true` 硬编码，`Exercise` 接口甚至无 `answer` 字段）、Home 页 N+1 查询（60 题逐个 DB 读写并污染数据库）、视频加载失败无 UI 反馈。
- **关键建议**：优先实现答案校验逻辑（接口加 `answer` 字段 + 容差比对），用 `progressStore.problems` 直接构建 Map 消除 N+1，在视频组件展示 `loadError` 并加重试按钮。

### 🛡️ 安全卫士（OWASP Top 10 + STRIDE 审计）
- **核心判断**：Conditional Go。安全基线良好 —— 无密钥泄露、无 XSS 向量（无 v-html/innerHTML/eval）、零依赖漏洞、CI/CD 干净。但面向小学生群体应提高标准，密码使用**无盐 SHA-256 哈希**存在真实彩虹表风险（🔴），且 `passwordHash` 随完整 User 对象存入 sessionStorage（🟠）、无 CSP（🟠）。安全态势评分 B（良好）。
- **关键建议**：密码哈希改用 PBKDF2 + 随机盐（≥16 字节，迭代 ≥100000）；sessionStorage 仅存 `{ nickname }`；`index.html` 添加 CSP meta 标签。

### ✅ 质量门神（QA测试 + 发布检查 · qa skill）
- **核心判断**：**No-Go（条件性 Go）**。构建与 CI 配置本身正确（base path / .nojekyll / 404.html fallback / deploy.yml 全部合规），但存在 4 个 🔴 上线阻塞项，其中"答案判定永远正确"和"关键源码未提交/未推送"是硬阻塞。零测试覆盖是显著质量隐患。视频仅覆盖 25%（15/60 题）。
- **关键建议**：立即提交并推送 `main.ts`/`router/index.ts`/`Login.vue` 及 2 个未推送 commit；实现答案校验或至少改为"练习模式（不判分）"；画板添加 touch 事件。

> 本次上场成员：产品官 + 安全卫士 + 质量门神（设计师、排障手未参与）

---

## 🚨 上线前阻塞项清单（P0，必须修复才能上线）

| # | 阻塞项 | 位置 | 来源 | 修复方式 |
|---|--------|------|------|----------|
| B-1 | 关键源码未提交 | `src/main.ts`、`src/router/index.ts`、`src/views/Login.vue` | QA | `git add` + commit（含会话恢复/路由守卫/登录流程） |
| B-2 | 2 个 commit 未推送 | main 领先 origin/main 2 commits | QA | `git push origin main` 触发部署 |
| B-3 | 答案校验失效 | `src/views/Problem.vue:371` | 产品+QA+安全 | `Exercise` 接口加 `answer` 字段 + 实现比对；或改"练习模式（不判分）" |
| B-4 | 画板无触屏支持 | `src/components/PracticeCanvas.vue:46-53` | 产品+QA | 添加 `@touchstart/move/end` 或用 Pointer Events 统一 |
| B-5 | 密码哈希无盐 | `src/db/indexedDB.ts:64-71` | 安全+产品+QA | 改 PBKDF2 + 随机盐（≥16 字节，迭代 ≥100000） |
| B-6 | Home 页 N+1 查询 | `src/views/Home.vue:96-102` | 产品 | 删除循环，用 `progressStore.problems` 构建 Map |

> ⚠️ **B-1 + B-2 是发布流程硬阻塞**：当前直接推送将部署**缺少会话恢复逻辑的旧代码**（刷新深链会被踢到登录页）。必须先提交再推送。

---

## 2. 综合审查发现（去重合并后按严重度排序）

| # | 严重度 | 类别 | 位置 | 问题描述 | 建议 | 来源 |
|---|--------|------|------|---------|------|------|
| 1 | 🔴 | 功能Bug | `Problem.vue:371` | `isCorrect.value=true` 硬编码，答案校验完全失效，正确率统计失真 | 接口加 `answer` 字段 + 实现容差比对 | 产品+QA+安全 |
| 2 | 🔴 | 发布阻塞 | `main.ts`/`router/index.ts`/`Login.vue` | 关键源码未提交（会话恢复/路由守卫/登录） | 立即 commit | QA |
| 3 | 🔴 | 发布阻塞 | main 分支 | 领先 origin/main 2 commits 未推送 | `git push origin main` | QA |
| 4 | 🔴 | 兼容性 | `PracticeCanvas.vue:46-53` | 画板仅鼠标事件，触屏设备（小学生主力平板）无法画图 | 添加 touch/pointer 事件 | 产品+QA |
| 5 | 🔴 | 安全 | `indexedDB.ts:64-71` | 密码无盐 SHA-256，彩虹表风险 | PBKDF2 + 随机盐 | 安全+产品+QA |
| 6 | 🔴 | 性能 | `Home.vue:96-102` | N+1 查询：60 题逐个 DB 读写 + 创建空记录污染 DB | 用 problems 数组构建 Map | 产品 |
| 7 | 🟠 | 安全 | `userStore.ts:49,71` | `passwordHash` 随完整 User 存入 sessionStorage | 仅存 `{ nickname }`，恢复时从 IndexedDB 读 | 安全+产品+QA |
| 8 | 🟠 | 安全 | `index.html` | 无 Content Security Policy | 添加 CSP meta 标签 | 安全 |
| 9 | 🟠 | 错误处理 | `useSegmentedVideoPlayer.ts:101` | 视频加载失败 `loadError` 未在 UI 展示，用户无限转圈 | 展示错误状态 + 重试按钮 | 产品 |
| 10 | 🟠 | 健壮性 | `indexedDB.ts` 全文 | 零 try/catch，Safari 隐私模式/配额超限/DB 损坏将白屏 | getDB 包 try/catch + 降级方案 | QA |
| 11 | 🟠 | 测试 | 全局 | 零测试覆盖（无 test script、无 vitest/playwright） | 至少覆盖 store/hashPassword/fetchJson | QA |
| 12 | 🟡 | 路由 | `router/index.ts` | 无 catch-all 404 路由，无效路径空白页 | 加 `/:pathMatch(.*)*` 兜底 | 产品+QA |
| 13 | 🟡 | 健壮性 | 全局 | 无 `app.config.errorHandler` / 错误边界 | main.ts 加全局错误处理 | QA |
| 14 | 🟡 | 性能/可用性 | `index.html` | Google Fonts CDN 大陆访问可能被墙，首屏 FOIT | 字体自托管或仅用系统字体 | QA |
| 15 | 🟡 | 仓库 | `public/videos/` | 131MB / 150 个 mp4 入 git，克隆/CI 慢 | 长期 Git LFS 或 CDN | QA |
| 16 | 🟡 | UX | `Problem.vue:243` | 无"题目未找到"状态，无效 ID 空白页 | 加 v-else 提示 + 返回首页 | 产品 |
| 17 | 🟡 | UX | `Problem.vue:278` | 练习编号与打乱顺序不匹配，点"1"可能展示第3题 | 显示原始题号或去掉打乱 | 产品 |
| 18 | 🟢 | 安全 | `router/index.ts:39` | redirect 仅校验 `startsWith('/')`，允许 `//evil.com` | 加 `!startsWith('//')` | 安全 |
| 19 | 🟢 | 规范 | `.env` / `.gitignore` | `.env` 被 git 跟踪（内容非敏感但违反惯例） | `.env` 加入 .gitignore | 安全+产品+QA |
| 20 | 🟢 | 构建 | `vite.config.ts` | 未显式禁用 sourcemap | `build.sourcemap: false` | 安全 |
| 21 | 🟢 | UX | `PracticeCanvas.vue` | 画板无撤销功能，画错只能全清 | 增加 `actions.pop()` 撤销 | 产品 |
| 22 | 🟢 | 可访问性 | `tailwind.config.js` | 固定像素字号，12px 对小学生移动端偏小 | 移动端 caption 增至 14px | QA |

---

## 🔁 回滚预案（GitHub Pages）

1. **查看部署历史**：仓库 → Settings → Pages → Source: GitHub Actions；Actions 页面找最近成功的 Deploy run
2. **代码回滚（推荐）**：`git log --oneline` 找稳定 commit → `git revert <commit>`（勿用 reset --hard）→ `git push origin main` 触发重新部署
3. **重新部署历史 commit**：Actions → Deploy workflow → Run workflow → 选历史 commit SHA（需先 checkout）
4. **紧急禁用**：Settings → Pages → Source 改 "Deploy from a branch" → 选空分支；或将仓库设 Private（免费版 Private 不支持 Pages，立即下线）
5. **验证**：访问 `https://<user>.github.io/DrawMathHub/` 确认回退

---

## ✅ 行动清单

| # | 行动 | 负责方 | 紧急度 | 期望完成 |
|---|------|--------|--------|---------|
| 1 | 提交并推送未提交的关键源码（main.ts/router/Login.vue）+ 2 个未推送 commit | 前端 | P0 | 立即 |
| 2 | 实现练习答案校验：`Exercise` 接口加 `answer` 字段，`submitAnswer` 实现容差比对；或临时改为"练习模式（不判分）" | 前端 | P0 | 上线前 |
| 3 | 画板添加 touch/pointer 事件支持（PracticeCanvas.vue） | 前端 | P0 | 上线前 |
| 4 | 密码哈希改 PBKDF2 + 随机盐（indexedDB.ts），并迁移已有密码 | 前端+安全 | P0 | 上线前 |
| 5 | Home 页消除 N+1 查询，用 problems 数组构建 Map | 前端 | P0 | 上线前 |
| 6 | sessionStorage 仅存 nickname，不存 passwordHash | 前端 | P1 | 上线前 |
| 7 | index.html 添加 CSP meta 标签 | 前端 | P1 | 上线前 |
| 8 | 视频加载失败 UI + 重试按钮（SolutionVideoPlayer.vue） | 前端 | P1 | 上线前 |
| 9 | IndexedDB 操作包 try/catch + 降级方案 + 全局 errorHandler | 前端 | P1 | 上线后1周内 |

---

## ⚠️ 待完善 / 已知局限

- **零自动化测试**：全项目无单元/E2E 测试，核心逻辑（答案校验、进度追踪、密码验证）无回归保障。建议上线后第一周补齐 store 与工具函数单测。
- **视频覆盖仅 25%**：60 题中仅 15 题有 Manim 预渲染视频，其余显示占位。建议首页卡片标注"有/无视频"状态，并在上线公告说明逐步上线计划。
- **本地构建环境差异**：本地 Vite `emptyDir` 被 WorkBuddy safe-delete 拦截（非代码问题），GitHub Actions CI（Ubuntu）不受影响。
- **纯前端架构固有安全限制**：无后端认证、路由守卫可被客户端绕过、IndexedDB 可被开发者工具篡改。符合产品定位（本地学习工具），但长期若引入多端同步需重构认证。
- **字体 CDN 风险**：Google Fonts 在大陆可能被墙，虽有系统字体回退但 `<link>` 仍阻塞首屏。

---

## 📚 成员产出索引

- **gstack-product-reviewer（产品官）**原始产出：17 项发现（🔴3/🟠5/🟡5/🟢4）+ 6 项代码亮点；详见对话回传（team: gstack-pre-launch-check）
- **gstack-security-officer（安全卫士）**原始产出：13 项发现（🔴1/🟠2/🟡2/🟢5/ℹ️3）+ STRIDE 威胁建模 + OWASP Top 10 检查表；安全态势评分 B；详见对话回传
- **gstack-qa-lead（质量门神）**原始产出：17 项发现（🔴4/🟠4/🟡5/🟢4）+ 14 项发布检查清单 + 回滚预案；详见对话回传
- **gstack-designer（设计师）**：本次未参与
- **gstack-investigator（排障手）**：本次未参与

---

> 本报告由软件工坊 AI 协作生成（GStack 工程团队 · 主理人汇编），关键决策请由工程负责人复核。
