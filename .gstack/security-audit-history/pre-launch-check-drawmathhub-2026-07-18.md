# DrawMathHub 上线前全检报告（复审）

**日期**：2026-07-18
**场景**：上线前检查（代码审查 + 安全审计 + QA测试与发布）· 复审
**审查目标**：`F:\woekspace\rust\DrawMathHub`（Vue 3 + TS 前端项目，小学数学画图解题法学习平台）
**参与成员**：产品官（gstack-product-reviewer，review skill） + 安全卫士（gstack-security-officer，OWASP+STRIDE） + 质量门神（gstack-qa-lead，qa skill）
**基线对比**：2026-07-12 安全审计 + 2026-07-14 上线前全检（上次结论 🔴 No-Go，6 项 P0 阻塞）

---

## 📌 TL;DR（执行摘要）

- **整体结论**：🔴 **No-Go** — 三方独立审查结论一致。距上次全检（07-14）已 4 天，但 6 项 P0 中仅 2 项发布流程阻塞（B-1 源码提交 / B-2 commit 推送）已修复，4 项功能/安全 P0（B-3 答案校验 / B-4 画板触屏 / B-5 密码哈希 / B-6 N+1）**全部未动**，代码与上次几乎无变化。
- **阻塞项数量**：🔴 8 项 P0（含 2 项新发现：4 个 src 文件未提交 + Exercise 数据无 answer 字段）
- **最大亮点**：发布流程本身已通（B-1/B-2 修复、构建零类型错误、CI 配置合规、零依赖漏洞、无密钥泄露）；双缓冲视频播放器、会话恢复时序、fetchJson 安全处理等工程设计精巧。
- **最大风险**：核心学习功能失效——答案校验 `isCorrect=true` 硬编码 + 数据层 Exercise 接口根本没有 `answer` 字段，学生输入任何答案都判正确，"练习"功能失去教学意义；且当前工作区有 4 个 src 文件未提交，**部署版本 ≠ 开发版本**。
- **恶化项**：视频文件入 git 从 131MB/150 个 → **287MB/596 个 mp4**，`.git/` 已 167MB；安全态势评分 B → **C+（降级）**。
- **下一步**：先 `git commit + push` 4 个未提交 src 文件解决部署一致性；再按最小修复集（8 项）清零 P0，即可转 🟡 条件 Go。

---

## 🎯 核心结论卡片

| 项目 | 内容 |
|------|------|
| Go / No-Go | 🔴 **No-Go** — 修复 8 项 P0 后转 🟡 条件 Go |
| 三方结论 | 产品官 🔴No-Go / 安全卫士 🔴No-Go(有条件放行) / 质量门神 🔴No-Go |
| 严重度分布 | 🔴 8 / 🟠 6 / 🟡 9 / 🟢 12（含历史未修复项去重合并） |
| 关键行动项 | 10 条（P0×8 + P1×2） |
| 建议负责人 | 前端工程负责人（功能/代码）+ 安全负责人（密码哈希/sessionStorage） |
| 构建状态 | ✅ `vue-tsc` 零错误 / ✅ `vite build` 通过（1813 模块，18.1s）；本地 `npm run build` 因 safe-delete 拦截失败，CI(Ubuntu) 不受影响 |
| 测试覆盖 | ❌ 0%（零测试文件，与上次相同） |
| 密钥泄露 | ✅ 无泄露（`.env` 仅含部署路径） |
| 依赖漏洞 | ✅ `npm audit` 0 漏洞 |
| 安全态势 | **C+**（上次 B，降级；历史 13 项安全发现 0 项修复） |
| 发布配置 | ✅ 16 项检查全合规（deploy.yml 权限/并发/base path/.nojekyll/404.html） |
| 进度对比 | 已修复 2/6 P0（B-1/B-2）；未修复 4/6 P0；恶化 1 项（视频入 git） |

---

## 1. 各成员核心结论

### 🔍 产品官（代码审查 · review skill）
- **核心判断**：🔴 No-Go。回归验证发现 3 项历史 P0（B-3 答案校验 / B-4 画板触屏 / B-6 N+1）**全部未修复**，3 项 P1（视频错误 UI / 404 路由 / 题目未找到空白页）也全部未修复，"代码与上次审查时几乎无变化"。最致命的 B-3 让核心练习功能完全失效。
- **关键建议**：Exercise 接口加 `answer` 字段 + 实现容差比对；PracticeCanvas 改 Pointer Events；Home 用 `progressStore.problems` 构建 Map 消除 N+1；`getProgress` getter 去除写副作用（新发现 N-1，是 B-6 根因）；补 catch-all 404 与"题目未找到"状态。
- **新增发现**：10 项（含 N-1 getter 写副作用、N-2 recordPractice 未 await+double-count、N-4 视频探测无 error 状态致网络故障被误判为"视频未制作"）。
- **代码亮点**：视频探测周全（Range 请求排除 SPA 404 回退）、双 video 无缝切换、会话恢复时序正确、`isLearned` 防护性校验、fetchJson content-type 安全检查、TS strict 基线高。

### 🛡️ 安全卫士（OWASP Top 10 + STRIDE 审计）
- **核心判断**：🔴 No-Go（有条件放行）。历史 13 项安全发现 **0 项已修复**（修复率 0%），安全态势评分 **B → C+（降级）**。F-001 密码无盐 SHA-256 经两轮审计仍未动。
- **关键建议**：推荐**路径 A**——上线前修复 F-001（PBKDF2+随机盐，~40 行）+ F-002（sessionStorage 仅存 nickname，~15 行）即可升至 B+ 并 Go；否则需项目负责人签署书面风险接受声明（路径 B）。
- **STRIDE/OWASP**：A02 加密失败为 🔴Critical（密码无盐 + passwordHash 入 sessionStorage）；A05 配置错误 🟠（无 CSP）；A03 注入 ℹ️（无 XSS 向量，确认安全）；A06 脆弱依赖 ℹ️（0 漏洞）。
- **新增发现**：N-001 工作区 4 个 src 文件未提交（🟡，与 QA 的新发现一致）；N-002 大量未跟踪视频/manim 文件（ℹ️）。

### ✅ 质量门神（QA测试 + 发布检查 · qa skill）
- **核心判断**：🔴 No-Go。上次 6 项 P0 中仅 B-1/B-2 两项**发布流程硬阻塞已修复**，4 项功能/安全 P0 全部未修复；新发现 2 项 P0（4 个 src 未提交 + Exercise 无 answer 字段）。发布配置本身 16 项全合规，**发布流程无硬阻塞**。
- **关键建议**：达成 🟡 条件 Go 的最小集为 5 项——提交推送 4 个 src 文件、补 Exercise answer 字段+实现校验、PracticeCanvas 加 pointer/touch、indexedDB 加 try/catch、router 加 catch-all 404；B-5 密码哈希与 B-6 N+1 可作上线后快速迭代项。
- **构建/发布**：vue-tsc ✅、vite build ✅（1813 模块/18.1s，index.js 166KB gzip 58KB）；deploy.yml 权限最小化、并发控制、base path、.nojekyll、404.html fallback 全 ✅；pnpm-lock 与 package-lock 并存 🟡。
- **恶化项**：视频入 git 131MB→**287MB/596 个 mp4**；Google Fonts 加载 Noto Sans SC 但 tailwind fontFamily 根本未引用，纯属浪费带宽且带来大陆访问风险。

> 本次上场成员：产品官 + 安全卫士 + 质量门神（设计师、排障手未参与）

---

## 🚨 上线前阻塞项清单（P0，必须修复才能上线）

| # | 阻塞项 | 位置 | 来源 | 修复方式 | 状态(vs07-14) |
|---|--------|------|------|----------|---------------|
| P0-1 | 4 个 src 文件未提交，部署≠开发 | `GridCard.vue`(559行重构)、`router/index.ts`(+scrollTo)、`Home.vue`(布局)、`videoAssets.ts`(+getCoverUrl) | QA+安全 | `git add` + commit + push（CI 从 main 构建） | 🆕 新发现 |
| P0-2 | 答案校验失效 + 数据层无 answer 字段 | `Problem.vue:371`(`isCorrect=true`硬编码) + `problems.ts:16-19`(Exercise 接口无 answer) + 38 个 JSON 无答案 | 产品+QA+安全 | 接口加 `answer` 字段 + 补全数据 + 实现容差比对；或临时改"练习模式(不判分)" | ❌ 未修复(=B-3，根因更深) |
| P0-3 | 画板无触屏支持 | `PracticeCanvas.vue:46-53`(仅 MouseEvent) + `getPoint(e:MouseEvent)` | 产品+QA | 改 Pointer Events 或加 `@touchstart/move/end` | ❌ 未修复(=B-4) |
| P0-4 | 密码哈希无盐 SHA-256 | `indexedDB.ts:64-71` | 安全+产品+QA | 改 PBKDF2 + 随机盐(≥16字节,迭代≥100000) + 旧哈希迁移 | ❌ 未修复(=B-5/F-001，两轮未动) |
| P0-5 | Home 页 N+1 + getter 写副作用 | `Home.vue:96-102` → `progressStore.getProgress` → `getOrCreateProgress` 创建空记录 | 产品+QA | `getProgress` 改只读；Home 用 `problems` 数组构建 Map | ❌ 未修复(=B-6) |
| P0-6 | sessionStorage 存完整 User(含 passwordHash) | `userStore.ts:49,71` | 安全+产品+QA | 仅存 `{ nickname }`，恢复时从 IndexedDB 读取 | ❌ 未修复(=F-002) |
| P0-7 | 无 CSP | `index.html` | 安全 | 添加 CSP meta 标签（注意 Google Fonts CDN 白名单） | ❌ 未修复(=F-003) |
| P0-8 | Exercise 数据无 answer 字段（P0-2 数据层根因，单列强调） | `problems.ts:16-19` + 全部 `public/data/problems/*.json` | QA | 为 38 个 JSON 的 exercises 补 answer 字段 | 🆕 新发现 |

> ⚠️ **P0-1 是部署一致性硬阻塞**：当前推送 main 触发 CI，部署的是已提交的旧代码，不含 GridCard 重构等 4 项改动。上线前必须先确认这些改动是否需要上线，再决定提交或丢弃。
> ⚠️ **P0-2 + P0-8 是同一根因的两个层面**：代码层 `isCorrect=true` 硬编码 + 数据层 Exercise 根本没有 answer 字段，需数据+代码双重修复。

---

## 2. 综合审查发现（去重合并后按严重度排序）

| # | 严重度 | 类别 | 位置 | 问题描述 | 建议 | 来源 |
|---|--------|------|------|---------|------|------|
| 1 | 🔴 | 功能Bug | `Problem.vue:371` + `problems.ts:16-19` | 答案校验 `isCorrect=true` 硬编码 + Exercise 接口无 answer 字段，练习功能失效 | 接口加 answer + 补数据 + 实现容差比对 | 产品+QA+安全 |
| 2 | 🔴 | 发布阻塞 | 4 个 src 文件未提交 | GridCard/router/Home/videoAssets 未 commit，部署≠开发 | git add+commit+push | QA+安全 |
| 3 | 🔴 | 兼容性 | `PracticeCanvas.vue:46-53` | 画板仅鼠标事件，平板/手机(小学生主力)无法画图 | Pointer Events / touch 事件 | 产品+QA |
| 4 | 🔴 | 安全 | `indexedDB.ts:64-71` | 密码无盐 SHA-256，彩虹表+GPU 暴力破解风险 | PBKDF2 + 随机盐 + 旧哈希迁移 | 安全+产品+QA |
| 5 | 🔴 | 性能/架构 | `Home.vue:96-102` + `progressStore.ts:70-82` | N+1 查询 + getter 写副作用，每次首页加载创建 60 条空记录污染 DB | getProgress 改只读 + Map 一次性查询 | 产品+QA |
| 6 | 🔴 | 安全 | `userStore.ts:49,71` | passwordHash 随完整 User 存 sessionStorage，XSS 可读 | 仅存 nickname | 安全+产品+QA |
| 7 | 🔴 | 安全 | `index.html` | 无 CSP，无纵深防御 | 添加 CSP meta | 安全 |
| 8 | 🔴 | 数据 | `problems.ts:16-19` + 38 个 JSON | Exercise 数据模型缺 answer 字段（#1 的数据层根因） | 补全 answer 字段 | QA |
| 9 | 🟠 | 健壮性 | `indexedDB.ts` 全文 | 零 try/catch，Safari 隐私模式/配额超限/DB 损坏白屏 | getDB 包 try/catch + 降级 | QA |
| 10 | 🟠 | 错误处理 | `useSegmentedVideoPlayer.ts:101` + `SolutionVideoPlayer.vue` | 视频加载失败 loadError 未在 UI 展示，用户无限转圈 | 展示错误状态 + 重试按钮 | 产品 |
| 11 | 🟠 | 路由 | `router/index.ts` | 无 catch-all 404 路由，无效路径空白页 | 加 `/:pathMatch(.*)*` | 产品+QA |
| 12 | 🟠 | 测试 | 全局 | 零测试覆盖（无 test script、无 vitest/playwright） | 至少覆盖 store/hashPassword/fetchJson | QA |
| 13 | 🟠 | 数据准确性 | `Problem.vue:367-383` | recordPractice 未 await + 本地 double-count（recordPractice 已递增，又手动递增） | 删本地递增，依赖 recordPractice+reload | 产品 |
| 14 | 🟠 | 仓库 | `.gitignore` | `.env` 被 git 跟踪（内容非敏感但违反惯例） | .gitignore 加 .env + git rm --cached | 安全+QA |
| 15 | 🟡 | 仓库/性能 | `public/videos/` | 视频入 git 恶化：131MB→287MB/596 个 mp4，.git 167MB | Git LFS 或 CDN（恶化项） | QA |
| 16 | 🟡 | 性能/可用性 | `index.html` + `tailwind.config.js` | Google Fonts 加载 Noto Sans SC 但 tailwind 未引用，纯浪费带宽+大陆访问风险 | 直接删除 fonts 链接 | QA |
| 17 | 🟡 | 健壮性 | `main.ts` / `App.vue` | 无 `app.config.errorHandler` / 错误边界 | 加全局错误处理 | QA |
| 18 | 🟡 | UX | `Problem.vue:243` | 无"题目未找到"状态，无效 ID 空白页 | 加 v-else 提示 + 返回首页 | 产品 |
| 19 | 🟡 | 健壮性 | `types/video.ts:27` + `videoAssets.ts:70-103` | 视频探测无 error 状态，网络故障被误判为"视频未制作" | 增加 error 状态 + 区分 404/网络错误 | 产品 |
| 20 | 🟡 | 健壮性 | `userStore.ts:120-129` | restoreSession 不验证用户是否仍存在于 DB | 改 async + getUser 验证 | 产品 |
| 21 | 🟡 | 内存 | `useSegmentedVideoPlayer.ts:141-151` | preloadAdjacent 的 setTimeout 未在 unmount 清理 | onUnmounted 清理定时器 | 产品 |
| 22 | 🟡 | 安全 | `router/index.ts:30-47` | 路由守卫纯客户端可绕过（SPA 固有） | 守卫中从 IndexedDB 验证用户存在 | 安全 |
| 23 | 🟡 | 构建 | `router`/`main.ts` | 动态导入无意义（已静态导入），不分块仅增噪音 | 改静态导入 | QA |
| 24 | 🟢 | 安全 | `router/index.ts:40` + `Login.vue:134` | redirect 仅校验 `startsWith('/')`，允许 `//evil.com` | 加 `!startsWith('//')` | 安全 |
| 25 | 🟢 | 安全 | `userStore.ts:42,103` | 密码比较非常量时间（`!==`） | 常量时间比较 | 安全 |
| 26 | 🟢 | 安全 | `vite.config.ts` | 未显式禁用 sourcemap | `build.sourcemap: false` | 安全 |
| 27 | 🟢 | 安全 | `videoAssets.ts:22-23` + `problems.ts:67-76` | manifest segment.file 无路径穿越过滤 / 无 SRI | 加 `../` 检测 | 安全 |
| 28 | 🟢 | 安全 | `scripts/vite-plugin-asset-404.ts:16` | dev server resolvePublicFile 路径穿越（仅 dev） | resolve 后校验目录包含 | 安全 |
| 29 | 🟢 | UX | `GridCard.vue:7-8` | tooltip 无触屏支持 | touchstart / :active | 产品 |
| 30 | 🟢 | 健壮性 | `progressStore.ts:89-94` | watch 中调用 useUserStore() 时序脆弱 | 组件中显式 watch | 产品 |
| 31 | 🟢 | 校验 | `Login.vue:16-21` | 昵称输入无字符集验证 | pattern / trim 校验 | 产品 |
| 32 | 🟢 | 性能 | `indexedDB.ts:121-124` | deleteUser 删除 progress 逐条删除未用事务 | transaction 批量删除 | 产品 |
| 33 | 🟢 | 可访问性 | `tailwind.config.js:43` | 移动端 12px 字号偏小 | 移动端增至 14px | QA |
| 34 | 🟢 | 仓库 | `public/videos/`+`manim/scenes/` | 大量未跟踪视频/manim 文件 | 确认是否需上线 | 安全 |
| 35 | 🟢 | UX | `PracticeCanvas.vue` | 画板无撤销功能 | actions.pop() + redraw | 产品 |

---

## 🔁 回滚预案（GitHub Pages）

**部署机制**：GitHub Actions → `actions/deploy-pages@v4`，仅 main 分支 push 触发；PR 仅构建不部署。

1. **标准回滚（推荐）**：`git revert <bad-commit> && git push origin main` → CI 自动重新部署。适合单 commit 回退。
2. **多 commit 回滚**：`git revert <oldest>..<newest> && git push origin main`。
3. **强制回滚（谨慎）**：`git reset --hard <good-commit> && git push --force origin main`。会改写 main 历史，协作者需 `git fetch && git reset --hard origin/main`。
4. **紧急下线**：GitHub Repo → Settings → Pages → Source 改 "None"，立即下线。
5. **验证**：等待 CI 完成后访问 `https://sogrey.github.io/DrawMathHub/` 确认。

> ⚠️ 视频文件已入 git 历史，revert 不会清除历史中的大文件，彻底清理需 BFG Repo-Cleaner 或 git filter-repo。
> ⚠️ IndexedDB 数据存用户浏览器本地，回滚不影响已有学习进度（除非数据结构不兼容）。

---

## ✅ 行动清单

| # | 行动 | 负责方 | 紧急度 | 期望完成 |
|---|------|--------|--------|---------|
| 1 | 提交并推送 4 个未提交 src 文件（GridCard/router/Home/videoAssets），解决部署一致性 | 前端 | P0 | 立即 |
| 2 | Exercise 接口加 answer 字段 + 补全 38 个 JSON 答案 + submitAnswer 实现容差比对（或临时改"练习模式不判分"） | 前端+内容 | P0 | 上线前 |
| 3 | PracticeCanvas 改 Pointer Events（统一鼠标+触屏） | 前端 | P0 | 上线前 |
| 4 | 密码哈希改 PBKDF2 + 随机盐 + 旧哈希迁移逻辑 | 前端+安全 | P0 | 上线前 |
| 5 | Home 页消除 N+1：getProgress 改只读 + 用 problems 数组构建 Map | 前端 | P0 | 上线前 |
| 6 | sessionStorage 仅存 nickname，restoreSession 从 IndexedDB 重载 | 前端 | P0 | 上线前 |
| 7 | index.html 添加 CSP meta 标签（白名单 Google Fonts 若保留） | 前端 | P0 | 上线前 |
| 8 | indexedDB.ts 包 try/catch + 降级方案；router 加 catch-all 404 | 前端 | P0 | 上线前 |
| 9 | 视频加载失败 UI + 重试按钮；删除未使用的 Google Fonts 链接 | 前端 | P1 | 上线前 |
| 10 | 补单元测试（store/hashPassword/fetchJson）+ 全局 errorHandler | 前端 | P1 | 上线后1周 |

---

## 📊 进度对比（vs 2026-07-14）

| 维度 | 07-14 | 07-18 | 趋势 |
|------|-------|-------|------|
| 整体结论 | 🔴 No-Go(6 P0) | 🔴 No-Go(8 P0) | ⚠️ 阻塞项反增 |
| 发布流程阻塞 | 2 项（源码未提交+未推送） | 0 项（已修复，但有新未提交） | ✅ 改善 |
| 功能/安全 P0 | 4 项 | 4 项（全部未动）+2 新增 | ❌ 停滞 |
| 安全态势 | B | C+ | ❌ 降级 |
| 视频入 git | 131MB/150 mp4 | 287MB/596 mp4 | ❌ 恶化 |
| 构建/CI | ✅ | ✅ | ✅ 持平 |
| 测试覆盖 | 0% | 0% | ⚠️ 持平 |

---

## ⚠️ 待完善 / 已知局限

- **零自动化测试**：全项目无单元/E2E 测试，核心逻辑（答案校验、进度追踪、密码验证）无回归保障。建议上线后第一周补齐 store 与工具函数单测。
- **视频覆盖仍偏低**：596 个 mp4 但分布不均，部分题型仍无演示，建议首页卡片标注"有/无视频"状态。
- **本地构建环境差异**：本地 Vite `emptyDir` 被 WorkBuddy safe-delete 拦截（非代码问题），GitHub Actions CI（Ubuntu）不受影响。
- **纯前端架构固有安全限制**：无后端认证、路由守卫可客户端绕过、IndexedDB 可被开发者工具篡改。符合产品定位（本地学习工具），长期若引入多端同步需重构认证。
- **字体 CDN 风险**：Google Fonts 在大陆可能被墙，且本次发现 tailwind 根本未引用该字体，纯属冗余加载。
- **修复执行率偏低**：距上次全检 4 天，6 项 P0 仅修复 2 项发布流程项，4 项功能/安全 P0 零执行，建议评估团队排期或拆分迭代。

---

## 📚 成员产出索引

- **gstack-product-reviewer（产品官）**原始产出：17 项发现（🔴3 历史 P0 未修复 + 10 项新发现 N-1~N-10 + 7 项代码亮点）；Go/No-Go: 🔴 No-Go；详见对话回传（team: gstack-pre-launch-recheck）
- **gstack-security-officer（安全卫士）**原始产出：历史 13 项 0 修复 + STRIDE 威胁建模 + OWASP Top 10 检查表 + 2 项新发现；安全态势 C+；Go/No-Go: 🔴 No-Go(有条件放行)；**已落盘**：`.gstack/security-audit-history/audit-2026-07-18-regression.md`
- **gstack-qa-lead（质量门神）**原始产出：回归验证表 + 构建验证 + 16 项发布检查清单 + 8 项新发现 + 回滚预案；Go/No-Go: 🔴 No-Go（9 项阻塞，5 项最小集达条件 Go）；详见对话回传
- **gstack-designer（设计师）**：本次未参与
- **gstack-investigator（排障手）**：本次未参与

### 历史报告索引
- `.gstack/security-audit-history/audit-2026-07-12-130000.md`（首次安全审计，基线 B）
- `.gstack/security-audit-history/pre-launch-check-drawmathhub-2026-07-14.md`（首次上线前全检，6 项 P0）
- `.gstack/security-audit-history/audit-2026-07-18-regression.md`（安全卫士本次复审原始产出，C+）
- `.gstack/security-audit-history/pre-launch-check-drawmathhub-2026-07-18.md`（本报告，主理人汇编）

---

> 本报告由软件工坊 AI 协作生成（GStack 工程团队 · 主理人汇编），关键决策请由工程负责人复核。
