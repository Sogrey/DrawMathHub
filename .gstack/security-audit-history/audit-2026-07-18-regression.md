# DrawMathHub 安全审计报告（上线前回归复审）

## Meta
- 审计模式: Comprehensive (全量回归复审)
- 日期: 2026-07-18
- 范围: DrawMathHub 全量代码库 (F:\woekspace\rust\DrawMathHub)
- 执行阶段: 14/14
- 审计人: gstack-security-officer (CSO)
- 前序审计: 2026-07-12 (首次全量) + 2026-07-14 (上线前全检)

## 核心结论

**No-Go（有条件放行）** — 历史安全审计共发现 13 项问题，**本次回归复审确认 0 项已修复**。其中 🔴Critical（密码无盐 SHA-256）经两轮审计仍未修复，且 sessionStorage 仍明文存储 passwordHash、仍无 CSP。安全态势评分从 B 降为 **C+**。建议至少修复 F-001（P0）后上线，或由项目负责人签署书面的风险接受声明后放行。

## 1. 回归验证结论表

| # | 历史发现 | 严重度 | 当前状态 | 当前代码行号证据 |
|---|----------|--------|----------|------------------|
| F-001 | 密码无盐 SHA-256 | 🔴 Critical | ❌ 未修复 | `src/db/indexedDB.ts:64-71` — `hashPassword` 仍为 `crypto.subtle.digest('SHA-256', data)`，无盐、无 PBKDF2、无迭代。`createUser:75`、`updateUserPassword:112`、`login:41`、`deleteUser:102` 全部调用此函数，无迁移逻辑 |
| F-002 | sessionStorage 存 passwordHash | 🟠 High | ❌ 未修复 | `src/stores/userStore.ts:49` — `sessionStorage.setItem(SESSION_KEY, JSON.stringify(user))` 仍存完整 User 对象（含 passwordHash）；`:71` 同；`restoreSession():120-129` 仍 `JSON.parse(stored)` 直接恢复含 passwordHash 的对象 |
| F-003 | 无 CSP | 🟠 High | ❌ 未修复 | `index.html:1-15` — 仍无 Content-Security-Policy meta 标签。Google Fonts CDN 仍无限制加载 |
| F-004 | 路由守卫纯客户端可绕过 | 🟡 Medium | ❌ 未修复（SPA 固有） | `src/router/index.ts:30-47` — 仍为纯客户端 `beforeEach` 守卫，可修改 sessionStorage 绕过 |
| F-005 | .gitignore 未忽略 .env | 🟡 Medium | ❌ 未修复 | `.gitignore:6-9` — 仍仅忽略 `.env.local`/`.env.*.local`/`*.local`，未忽略 `.env` 本身。`git ls-files .env` 确认 `.env` 仍被 git 跟踪（commit 65656bb 引入） |
| F-006 | 密码比较非常量时间 | 🟢 Low | ❌ 未修复 | `src/stores/userStore.ts:42` — `if (inputHash !== user.passwordHash)` 仍用 `!==`；`:103` 同 |
| F-007 | redirect 允许 `//evil.com` | 🟢 Low | ❌ 未修复 | `src/router/index.ts:40` — `next(redirect.startsWith('/') ? redirect : '/')` 仍仅校验 `startsWith('/')`；`src/views/Login.vue:134` — `resolveRedirect()` 同 |
| F-008 | 答案校验失效 | 🟢 Low | ❌ 未修复 | `src/views/Problem.vue:370-371` — `isCorrect.value = true` 仍硬编码，无实际校验 |
| F-009 | vite.config 未禁用 sourcemap | 🟢 Low | ❌ 未修复 | `vite.config.ts:17-26` — 仍无 `build: { sourcemap: false }`（Vite 默认 false，风险低） |
| F-010 | 题目/manifest 无完整性校验、segment.file 无路径穿越过滤 | 🟢 Low | ❌ 未修复 | `src/data/videoAssets.ts:22-23` — `resolveSegmentUrl` 仍无 `../` 过滤；`src/data/problems.ts:67-76` — 仍无 SRI/hash 校验 |
| F-011 | 开发服务器 resolvePublicFile 路径穿越 | 🟢 Low | ❌ 未修复 | `scripts/vite-plugin-asset-404.ts:16` — 仍 `path.join(root, 'public', decodeURIComponent(relative))` 无 contain 校验（仅影响 dev server） |
| F-012 | 无 XSS 向量 | ℹ️ Info | ✅ 已确认 | 全量搜索 `v-html`/`innerHTML`/`eval(`/`document.write`/`new Function(` — 0 匹配。Vue 模板自动转义生效 |
| F-013 | CI/CD 管道安全良好 | ℹ️ Info | ✅ 已确认 | `.github/workflows/deploy.yml` — 仍使用 checkout@v4 + npm ci，权限最小化（contents:read, pages:write, id-token:write），仅 main 部署，无 `pull_request_target` |

**回归总结：13 项历史发现中，0 项已修复，11 项未修复，2 项状态确认（Info 级）。**

## 2. STRIDE 威胁建模表

| 组件 | 威胁类型 | 风险描述 | 严重度 | 缓解建议 |
|------|----------|----------|--------|----------|
| 登录认证 | Spoofing (伪造) | 任何人可创建任意昵称，无服务端身份验证。数据存储在本地 IndexedDB，影响限于同一浏览器 | 🟡 Medium | 纯前端固有限制，可接受 |
| 登录认证 | Information Disclosure | 用户完整对象（含 passwordHash）以 JSON 存入 sessionStorage，任何同源 JS 可读取 | 🟠 High | sessionStorage 中仅存 `{ nickname }`（F-002 未修复） |
| 登录认证 | Denial of Service | 密码输入无次数限制、无锁定机制 | 🟢 Low | 可加客户端延时重试 |
| 数据存储 (IndexedDB) | Tampering (篡改) | IndexedDB 数据可被开发者工具直接读写修改 | 🟡 Medium | 纯前端固有限制。密码哈希应用带盐 PBKDF2 增加篡改成本 |
| 数据存储 (IndexedDB) | Information Disclosure | 密码哈希以无盐 SHA-256 存储，易被彩虹表破解 | 🔴 Critical | 改用 PBKDF2 + 随机盐，迭代 ≥100000（F-001 未修复） |
| 数据存储 (IndexedDB) | Elevation of Privilege | 用户可通过直接操作 IndexedDB 读取/修改其他用户进度 | 🟢 Low | 纯前端固有限制，数据敏感度低 |
| 视频播放 | Tampering (篡改) | manifest 中 `segment.file` 字段未做路径校验 | 🟢 Low | 同源静态文件，GitHub Pages 不执行服务端读取，风险极低 |
| 题目数据 | Tampering (篡改) | 题目 JSON 为静态文件，无完整性校验 | 🟢 Low | 同源静态文件，篡改需仓库写入权限 |
| 题目数据 | Repudiation (抵赖) | 答题提交始终标记正确，无法真实记录学习效果 | 🟢 Low | 修复答题校验逻辑（F-008 未修复） |
| 路由跳转 | Spoofing (伪造) | redirect 参数仅校验 `startsWith('/')`，允许 `//evil.com` 协议相对 URL | 🟢 Low | 增加 `!startsWith('//')` 校验（F-007 未修复） |

## 3. OWASP Top 10 检查表

| 编号 | 类别 | 是否涉及 | 发现 | 严重度 |
|------|------|----------|------|--------|
| A01 | 失效访问控制 | ✅ 是 | 路由守卫纯客户端可绕过；redirect 允许协议相对 URL | 🟡 Medium |
| A02 | 加密失败 | ✅ 是 | 密码无盐 SHA-256（🔴）；passwordHash 存入 sessionStorage（🟠） | 🔴 Critical |
| A03 | 注入 | ❌ 否 | 无 v-html/innerHTML/eval/document.write，Vue 自动转义生效 | ℹ️ Info |
| A04 | 不安全设计 | ✅ 是 | 答题校验逻辑缺失（isCorrect 硬编码 true）；密码比较非常量时间 | 🟢 Low |
| A05 | 安全配置错误 | ✅ 是 | 无 CSP（🟠）；.gitignore 未忽略 .env（🟡）；未显式禁用 sourcemap（🟢） | 🟠 High |
| A06 | 脆弱依赖 | ❌ 否 | npm audit 报告 0 漏洞 | ℹ️ Info |
| A07 | 认证失败 | ✅ 是 | 无暴力破解防护；session 恢复依赖 sessionStorage 可被伪造；密码比较非常量时间 | 🟢 Low |
| A08 | 数据完整性 | ✅ 是 | 题目数据 JSON 无完整性校验；答题结果始终正确 | 🟢 Low |
| A09 | 日志监控失败 | ⚠️ N/A | 纯前端无后端，无审计日志（架构固有限制） | ℹ️ Info |
| A10 | SSRF | ❌ 否 | 纯前端应用，fetch 仅针对同源静态资源 | ℹ️ Info |

## 4. 本次新发现清单

### N-001 🟡 Medium — 工作区有未提交的源码变更
- **位置**: `src/router/index.ts`、`src/views/Home.vue`、`src/components/GridCard.vue`、`src/data/videoAssets.ts`
- **问题**: `git status` 显示这 4 个源码文件有未提交的修改（router 增加 scrollTo，GridCard 重构为 tooltip 卡片，Home/videoAssets 有改动）。当前推送将部署已提交的旧代码，不包含这些变更。
- **修复建议**: 上线前确认是否需要提交这些变更；如需上线则 `git add` + commit + push。

### N-002 ℹ️ Info — 大量未跟踪的视频文件与 manim 脚本
- **位置**: `public/videos/`（30+ 新目录）、`manim/scenes/`（40+ 新文件）
- **问题**: 大量新视频和 manim 场景脚本未纳入版本控制，不会随部署上线。
- **修复建议**: 确认这些文件是否需要上线；如需则提交并推送。

## 5. 密钥/敏感信息泄露检查结论

**✅ 无泄露。** 具体检查结果：

1. `.env` 文件内容仅为 `VITE_BASE_PATH=/DrawMathHub/`（部署子路径配置），不含任何 API Key、Token、密码或凭证。
2. `.env.example` 与 `.env` 内容一致，为纯路径配置模板。
3. `git log --all -- .env` 确认 `.env` 仅在初始提交 (65656bb) 中添加，历史中从未包含密钥。
4. 全量代码搜索 `api_key|secret|token|credential|private_key|BEGIN RSA` 未发现硬编码密钥（仅 passwordHash 相关的业务逻辑匹配）。
5. 全量代码搜索 IP 地址模式 `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` 未发现硬编码 IP。
6. 无 base64 编码的长字符串（>40字符）可疑凭证。

**注意**: `.env` 仍被 git 跟踪（`.gitignore` 未忽略 `.env` 本身），当前内容无害但存在未来误提交密钥的风险（F-005 未修复）。

## 6. 依赖漏洞检查结论

**✅ 零漏洞。**

- `npm audit` 输出：`found 0 vulnerabilities`
- 依赖清单：vue@^3.4.21, vue-router@^4.3.0, pinia@^2.1.7, idb@^8.0.3, @lucide/vue@^1.0.0
- 开发依赖：vite@^6.2.0, typescript@^5.4.2, tailwindcss@^3.4.1 等，均无已知 CVE
- 无废弃/停止维护的包

## 7. 安全态势评分

| 严重度 | 数量 | 变化 |
|--------|------|------|
| 🔴 Critical | 1 | 持平（F-001 未修复） |
| 🟠 High | 2 | 持平（F-002、F-003 未修复） |
| 🟡 Medium | 2 | 持平（F-004、F-005 未修复）+ N-001 新增 |
| 🟢 Low | 5 | 持平（F-006~F-011 未修复） |
| ℹ️ Info | 3 | 持平（F-012、F-013 确认）+ N-002 新增 |
| **合计** | **13+2** | |

**安全态势评分：C+**（从 B 降级）

- 评分理由：历史 Critical 发现经两轮审计仍未修复，历史 High 发现均未修复，回归修复率为 0%。项目安全基线本身良好（无密钥泄露、无 XSS、零依赖漏洞、CI/CD 干净），但密码保护机制不达标且持续未改进。

## Go/No-Go 判断

**🔴 No-Go（有条件放行）**

### 判断理由：

1. **F-001（🔴Critical）经两轮审计未修复**：密码无盐 SHA-256 是唯一 Critical 级发现，已在上次审计中标记为 P0（上线前必修），本次复审确认代码完全未改动。这不是新发现，而是已承诺修复但未执行的回归失败。

2. **F-002 + F-003（🟠High）均未修复**：sessionStorage 明文存 passwordHash、无 CSP，均在上次审计中列为 P1（上线前修复），本次确认未改动。

3. **实际风险评估**：
   - 缓解因素：纯前端架构、数据全部本地存储、无服务端 API、无 PII（仅昵称）、无 XSS 向量、密码为可选功能
   - 加剧因素：面向小学生群体（应提高安全标准）、passwordHash 暴露在 sessionStorage（同源 JS 可读）、无 CSP 无纵深防御
   - 结论：F-001 在纯前端场景下实际可利用性有限（攻击者需先获得同源 JS 执行能力），但 passwordHash 存 sessionStorage 使其与 XSS 形成链式风险（一旦未来引入 XSS 向量，密码哈希直接泄露且可彩虹表破解）

### 建议路径：
- **路径 A（推荐）**：上线前修复 F-001（PBKDF2+盐，约 30 行代码改动）+ F-002（sessionStorage 仅存 nickname，约 10 行改动），即可升至 B+ 并 Go
- **路径 B（可接受）**：项目负责人签署书面风险接受声明（ acknowledging 纯前端场景下 F-001 实际影响有限），Conditional Go，但要求上线后首个迭代内修复 F-001~F-003
- **路径 C（不可接受）**：在当前状态下无条件 Go — 不推荐

## 修复路线图

| 优先级 | 发现编号 | 修复内容 | 代码改动量 | 建议时间 |
|--------|----------|----------|-----------|----------|
| P0 (立即) | F-001 | 密码哈希改用 PBKDF2 + 随机盐(≥16字节, 迭代≥100000) + 旧哈希迁移 | ~40行 | 上线前 |
| P0 (立即) | F-002 | sessionStorage 仅存 `{ nickname }`，restoreSession 从 IndexedDB 重载 | ~15行 | 上线前 |
| P1 (本迭代) | F-003 | index.html 添加 CSP meta 标签 | ~1行 | 上线前 |
| P1 (本迭代) | N-001 | 确认并提交/推送未提交的源码变更 | git操作 | 上线前 |
| P2 (下迭代) | F-005 | .gitignore 添加 .env，git rm --cached .env | ~2行 | 下次提交 |
| P2 (下迭代) | F-007 | redirect 增加 `!startsWith('//')` 校验 | ~2行 | 下迭代 |
| P2 (下迭代) | F-009 | vite.config 添加 `build: { sourcemap: false }` | ~1行 | 下迭代 |
| P3 (待办) | F-006 | 常量时间密码比较函数 | ~10行 | 待办 |
| P3 (待办) | F-008 | 实现答案校验逻辑（功能缺陷） | ~20行 | 待办 |
| P3 (待办) | F-010 | segment.file 添加 `../` 过滤 | ~3行 | 待办 |
| P3 (待办) | F-011 | dev server resolvePublicFile 添加 contain 校验 | ~5行 | 待办 |

## 趋势对比

| 维度 | 2026-07-12 (首次) | 2026-07-14 (全检) | 2026-07-18 (复审) | 趋势 |
|------|-------------------|-------------------|-------------------|------|
| Critical | 1 | 1 | 1 | ⚠️ 持平（未修复） |
| High | 2 | 2 | 2 | ⚠️ 持平（未修复） |
| Medium | 2 | 2 | 3 | ⬆️ +1（N-001 未提交源码） |
| Low | 5 | 5 | 5 | ⚠️ 持平（未修复） |
| Info | 3 | 3 | 4 | ⬆️ +1（N-002 未跟踪文件） |
| 修复率 | N/A | N/A | 0/11 = 0% | 🔴 零修复 |
| 评分 | B | B | C+ | ⬇️ 降级 |
