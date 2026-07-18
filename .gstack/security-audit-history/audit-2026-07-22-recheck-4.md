# DrawMathHub 安全审计报告（第四轮上线前复审）

## Meta
- 审计模式: Comprehensive (全量回归复审)
- 日期: 2026-07-22
- 范围: DrawMathHub HEAD(ee498a6) 全量代码库 (F:\woekspace\rust\DrawMathHub)
- 执行阶段: 14/14
- 审计人: gstack-security-officer (CSO)
- 前序审计: 2026-07-12 (首次) + 2026-07-14 (全检) + 2026-07-18 (回归)
- 审计对象: HEAD = ee498a6 = origin/main（工作区干净，已推送 = 实际部署版本）

## Executive Summary

**GO.** 第三轮审计的 13 项历史发现在本轮全部回归确认：11 项完全修复、1 项部分修复(F-010)、1 项可接受(F-004)。上轮唯一阻塞条件（修复未提交）已解除——工作区完全干净，HEAD=origin/main=ee498a6。密码哈希已升级为 PBKDF2+盐+迁移，sessionStorage 不再存储 passwordHash，CSP 已部署，safeRedirect/timingSafeEqual/sourcemap 等全部到位。pnpm-only 工具链迁移完整一致，CI 无断裂风险。零依赖漏洞，17/17 测试通过，TypeScript 类型检查通过。剩余 3 项 P2/P3 防御纵深建议不阻塞上线。安全态势评分从 B+ 升至 **A-**。

---

## 1. 回归验证结论表（F-001 ~ F-013）

| # | 历史发现 | 严重度 | 上轮状态 | 本轮状态 | 证据 |
|---|----------|--------|----------|----------|------|
| F-001 | 密码无盐 SHA-256 | 🔴 Critical | ✅ 已修复 | ✅ **稳固** | `indexedDB.ts:86-114` — PBKDF2 100K 迭代 + 16 字节随机盐 + SHA-256，格式 `pbkdf2$iter$saltHex$hashHex`；`:119-152` verifyPassword 含旧 SHA-256 透明迁移逻辑 |
| F-002 | sessionStorage 存 passwordHash | 🟠 High | ✅ 已修复 | ✅ **稳固** | `userStore.ts:17-24` — SessionPayload 仅含 `{ nickname }`；`:147-174` restoreSession 仅恢复 nickname 后从 IndexedDB 重载，兼容旧 session 降级 |
| F-003 | 无 CSP | 🟠 High | ✅ 已修复(保留) | ✅ **已部署(保留意见持续)** | `index.html:7-8` — CSP meta 标签已部署：default-src 'self'; script-src 'self' 'unsafe-eval'; frame-ancestors 'none'; object-src 'none' 等。**unsafe-eval 与 ws:wss: 仍在**（见 N-001/N-004） |
| F-004 | 路由守卫纯客户端 | 🟡 Medium | ✅ 可接受 | ✅ **可接受** | `router/index.ts:37-53` — 纯前端 SPA 固有限制，route guard + safeInternalPath 已到位 |
| F-005 | .gitignore 未忽略 .env | 🟡 Medium | ✅ 已修复 | ✅ **稳固** | `.gitignore:7-9` — 忽略 `.env`/`.env.*`，保留 `!.env.example`；`git ls-files .env` 返回空（已从跟踪移除）；历史 `.env`（commit 65656bb）仅含 `VITE_BASE_PATH=/DrawMathHub/`，无密钥 |
| F-006 | 密码比较非常量时间 | 🟢 Low | ✅ 已修复 | ✅ **稳固** | `indexedDB.ts:63-70` — `timingSafeEqual` XOR 常量时间比较，verifyPassword 中 `:132`/`:137` 均使用 |
| F-007 | redirect 允许 `//evil.com` | 🟢 Low | ✅ 已修复 | ✅ **稳固** | `safeRedirect.ts:1-8` — safeInternalPath 拒绝 `//`、`://`、非字符串、空值；router `:46` 和 Login `:136` 均调用 |
| F-008 | 答案校验失效 | 🟢 Low | ✅ 已修复 | ✅ **稳固** | `answerGrade.ts:1-103` — 完整实现：normalizeAnswerText 全角转半角、extractNumbers 数字提取、blankMatches 多候选匹配、gradeAnswerKey exact/number/remainder/blanks 四类型 |
| F-009 | vite.config 未禁用 sourcemap | 🟢 Low | ✅ 已修复 | ✅ **稳固** | `vite.config.ts:27` — `build: { sourcemap: false }` |
| F-010 | manifest 无完整性校验/路径穿越 | 🟢 Low | ⚠️ 部分修复 | ⚠️ **仍部分修复** | `videoAssets.ts:22-37` — resolveSegmentUrl 已防护 `..`（safeRelativeFile + 绝对路径分支检查）；**但 `:39-49` resolveFullVideoUrl 仍缺 `..` 检查**（N-002 持续） |
| F-011 | dev server 路径穿越 | 🟢 Low | ✅ 已修复 | ✅ **稳固** | `vite-plugin-asset-404.ts:9-24` — resolvePublicFile 双重防护：`..` 拒绝 + path.startsWith(publicRoot) 包含校验 |
| F-012 | 无 XSS 向量 | ℹ️ Info | ✅ 已确认 | ✅ **持续确认** | 全量搜索 `v-html`/`innerHTML`/`eval(`/`document.write`/`new Function(` — 0 匹配。ee498a6 新增代码（App.vue/appErrorToast）均使用 `{{ }}` 文本插值自动转义 |
| F-013 | CI/CD 管道安全 | ℹ️ Info | ✅ 已确认 | ✅ **持续确认+改进** | `deploy.yml` — 已改用 pnpm（action-setup@v4 + cache:pnpm + frozen-lockfile）；新增 `pnpm test` 步骤；权限最小化不变；无 pull_request_target |

**回归总结：13 项历史发现中，11 项完全修复且稳固，1 项部分修复(F-010)，1 项可接受(F-004)。**

---

## 2. 上轮新发现项回归（N-001 ~ N-004）

| # | 上轮发现 | 严重度 | 上轮建议 | 本轮状态 | 证据 |
|---|----------|--------|----------|----------|------|
| N-001 | CSP `unsafe-eval` 生产不必要 | 🟢 Low | P2 | ⚠️ **未处理** | `index.html:8` — `script-src 'self' 'unsafe-eval'` 仍在。Vite 生产构建不含 eval，但单一 index.html 无法区分 dev/prod CSP |
| N-002 | resolveFullVideoUrl 缺路径穿越检查 | 🟢 Low | P3 | ⚠️ **未处理** | `videoAssets.ts:39-49` — manifest.fullVideo 未做 `..` 过滤。实际风险极低（客户端 fetch 同源静态文件，浏览器规范化 URL） |
| N-003 | 所有安全修复未提交 | 🔴 P0 | P0 | ✅ **已解除** | `git status` 空输出；HEAD=ee498a6=origin/main；091ecaa 安全修复已提交并推送 |
| N-004 | CSP connect-src 含 ws:wss: | 🟢 Low | P3 | ⚠️ **未处理** | `index.html:8` — `connect-src 'self' ws: wss:` 仍在。生产环境无 WebSocket，但同 N-001 原因无法区分 |

---

## 3. STRIDE 威胁建模表

| 组件 | 威胁类型 | 风险描述 | 严重度 | 当前缓解 | 残余风险 |
|------|----------|----------|--------|----------|----------|
| 登录认证 | Spoofing | 匿名登录无服务端身份验证，IndexedDB 本地存储 | 🟢 Low | 纯前端固有；可选密码保护 PBKDF2 | 可接受 |
| 登录认证 | Information Disclosure | ~~passwordHash 存 sessionStorage~~ | ✅ 已修复 | sessionStorage 仅存 nickname | 无 |
| 登录认证 | Denial of Service | 密码输入无次数限制/锁定 | 🟢 Low | 客户端固有限制 | P3 待办 |
| 数据存储 | Tampering | IndexedDB 可被开发者工具读写 | 🟢 Low | 纯前端固有；PBKDF2 增加篡改成本 | 可接受 |
| 数据存储 | Information Disclosure | ~~密码哈希无盐 SHA-256~~ | ✅ 已修复 | PBKDF2 100K 迭代 + 随机盐 | 无 |
| 视频播放 | Tampering | manifest.fullVideo 未做 `..` 过滤 | 🟢 Low | 同源静态文件，浏览器 URL 规范化 | P3 防御纵深 |
| 题目数据 | Tampering | 静态 JSON 无完整性校验(SRI) | 🟢 Low | 同源部署，篡改需仓库写入权限 | 可接受 |
| 题目数据 | Repudiation | ~~答题校验硬编码 true~~ | ✅ 已修复 | answerGrade 完整实现 | 无 |
| 路由跳转 | Spoofing | ~~redirect 允许 `//evil.com`~~ | ✅ 已修复 | safeInternalPath 多重校验 | 无 |
| 全局 | Information Disclosure | errorHandler console.error 输出 | ℹ️ Info | 仅浏览器本地控制台，不外传 | 可接受 |
| CSP | Elevation of Privilege | unsafe-eval 允许 eval() 执行 | 🟢 Low | 生产构建不含 eval；script-src 限制 'self' | P2 防御纵深 |

---

## 4. OWASP Top 10 检查表

| 编号 | 类别 | 是否涉及 | 发现 | 严重度 |
|------|------|----------|------|--------|
| A01 | 失效访问控制 | ⚠️ 部分 | 路由守卫纯客户端（SPA 固有，可接受）；safeInternalPath 已防护 redirect 注入 | ℹ️ Info |
| A02 | 加密失败 | ✅ 已修复 | PBKDF2+盐+迁移到位；sessionStorage 不存 passwordHash；timingSafeEqual 常量时间比较 | ✅ 通过 |
| A03 | 注入 | ❌ 否 | 无 v-html/innerHTML/eval/document.write；Vue 自动转义；无 SQL/模板注入 | ✅ 通过 |
| A04 | 不安全设计 | ✅ 已修复 | answerGrade 完整校验逻辑；nickname 输入正则验证 `[\u4e00-\u9fffA-Za-z0-9_]{1,20}` | ✅ 通过 |
| A05 | 安全配置错误 | ⚠️ 部分 | CSP 已部署但含 unsafe-eval/ws:wss:（P2/P3）；sourcemap 已禁用；.env 已从 git 移除 | 🟢 Low |
| A06 | 脆弱依赖 | ❌ 否 | pnpm audit: 0 vulnerabilities | ✅ 通过 |
| A07 | 认证失败 | ⚠️ 部分 | PBKDF2 强哈希；无暴力破解防护（客户端固有）；session 恢复仅 nickname | 🟢 Low |
| A08 | 数据完整性 | ⚠️ 部分 | CI/CD 使用 frozen-lockfile；静态 JSON 无 SRI（同源可接受） | 🟢 Low |
| A09 | 日志监控失败 | ⚠️ N/A | 纯前端无后端审计日志（架构固有） | ℹ️ Info |
| A10 | SSRF | ❌ 否 | 纯前端，fetch 仅同源静态资源；fetchJson 检查 content-type 防 HTML 注入 | ✅ 通过 |

---

## 5. 本轮新发现清单

### 本轮无新增安全发现。

ee498a6 引入的新代码（vitest 测试、pnpm-only 工具链、phase-2 健壮性）经审计未引入新的安全风险：

- **vitest 测试代码**：3 个测试文件（answerGrade.test.ts / safeRedirect.test.ts / publicUrl.test.ts），仅含数学答案测试数据和 mock 对象，无敏感信息，使用 vi.stubGlobal 正确隔离。
- **appErrorToast**：纯字符串 ref + Vue `{{ }}` 文本插值，无 XSS 风险。
- **errorHandler (main.ts:14-23)**：console.error 输出到浏览器本地控制台（不外传），toast 仅显示 err.message（不含堆栈）。
- **nickname 验证 (Login.vue:151-159)**：正则 `[\u4e00-\u9fffA-Za-z0-9_]{1,20}` + 长度/空格检查，防止注入。
- **pnpm.onlyBuiltDependencies**：限制仅 esbuild/vue-demi 可执行 install 脚本，减少供应链攻击面。

---

## 6. CI/CD 工具链变更安全影响

### pnpm-only 迁移 — ✅ 一致且安全

| 检查项 | 结果 |
|--------|------|
| package-lock.json 是否移除 | ✅ 已移除（ee498a6 删除 2703 行） |
| pnpm-lock.yaml 是否存在 | ✅ 存在（62373 bytes） |
| deploy.yml 是否改用 pnpm | ✅ action-setup@v4 + cache:pnpm + install --frozen-lockfile |
| CI 是否有残留 npm 命令 | ✅ 无（npm ci → pnpm install, npm run build → pnpm build） |
| package.json packageManager 字段 | ✅ `pnpm@10.32.1` 声明 |
| frozen-lockfile 安全性 | ✅ 比 npm ci 更严格，锁定文件必须与 package.json 完全一致 |
| CI 是否新增 test 步骤 | ✅ `pnpm test`（vitest run）在 build 前执行 |

**结论**：pnpm-only 迁移完整一致，无 CI 断裂风险。frozen-lockfile 提供比 npm ci 更强的依赖完整性保证。

### vitest 引入 — ✅ 安全

- vitest@^3.2.4 为开发依赖，不进入生产构建
- 测试环境为 node（非 jsdom），无 DOM 模拟风险
- 测试代码不访问真实网络/文件系统（使用 vi.stubGlobal mock fetch）

---

## 7. 密钥/敏感信息泄露检查结论

**✅ 无泄露。**

1. `git ls-files .env` 返回空 — .env 不再被 git 跟踪
2. 历史 `.env`（commit 65656bb）仅含 `VITE_BASE_PATH=/DrawMathHub/`，无密钥
3. `.env.example` 仅含路径配置模板，无密钥
4. 全量搜索 `api_key|secret|password[:=]|token[:=]|credential|BEGIN RSA|BEGIN PRIVATE|AKIA` — 0 匹配
5. 全量搜索 IP 地址 `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` — 0 匹配
6. 无 base64 编码长字符串（>40 字符）可疑凭证

---

## 8. 依赖漏洞检查结论

**✅ 零漏洞。**

```
$ pnpm audit
No known vulnerabilities found
```

| 依赖 | 版本 | 状态 |
|------|------|------|
| vue | ^3.4.21 | ✅ 无 CVE |
| vue-router | ^4.3.0 | ✅ 无 CVE |
| pinia | ^2.1.7 | ✅ 无 CVE |
| idb | ^8.0.3 | ✅ 无 CVE |
| @lucide/vue | ^1.0.0 | ✅ 无 CVE |
| vite | ^6.2.0 | ✅ 无 CVE |
| vitest | ^3.2.4 | ✅ 无 CVE |
| typescript | ^5.4.2 | ✅ 无 CVE |
| tailwindcss | ^3.4.1 | ✅ 无 CVE |

---

## 9. 安全态势评分

| 严重度 | 数量 | 变化 | 说明 |
|--------|------|------|------|
| 🔴 Critical | 0 | ⬇️ -1 | F-001 已修复 |
| 🟠 High | 0 | ⬇️ -2 | F-002、F-003 已修复 |
| 🟡 Medium | 0 | ⬇️ -2 | F-004 可接受，F-005 已修复，N-003 已解除 |
| 🟢 Low | 3 | 持平 | N-001(unsafe-eval) + N-002(fullVideo `..`) + N-004(ws:wss:)，均为防御纵深 |
| ℹ️ Info | 2 | 持平 | F-012(无XSS) + F-013(CI/CD良好) |
| **合计** | **5** | ⬇️ -8 | |

**安全态势评分：A-**（从 B+ 升级）

- 评分理由：所有 P0/P1 安全发现已修复并提交推送；零 Critical/High/Medium 残留；零依赖漏洞；CI/CD 工具链完整一致；工作区干净=部署版本。仅剩 3 项 P2/P3 防御纵深建议，不影响上线。

---

## 10. Go/No-Go 判断

### **🟢 GO**

### 判断理由：

1. **阻塞条件已解除**：上轮唯一阻塞条件（N-003 修复未提交）已完全解除。`git status` 空输出，HEAD=ee498a6=origin/main，安全修复 commit 091ecaa 已提交并推送。

2. **Critical 已清零**：F-001（密码无盐 SHA-256）已升级为 PBKDF2 100K 迭代 + 随机盐 + 旧哈希透明迁移，经代码逐行核对确认稳固。

3. **High 已清零**：F-002（sessionStorage 不再存 passwordHash）+ F-003（CSP 已部署）均已修复。

4. **工具链无断裂风险**：pnpm-only 迁移完整一致，CI deploy.yml 正确使用 pnpm，无残留 npm 命令，frozen-lockfile 提供更强依赖完整性保证。

5. **质量门通过**：17/17 测试通过，TypeScript 类型检查通过，pnpm audit 零漏洞。

6. **残余风险可接受**：3 项 P2/P3 防御纵深建议（unsafe-eval / fullVideo `..` / ws:wss:）均为非阻塞项，不影响上线安全性。

---

## 11. 修复路线图（残余项）

| 优先级 | 发现编号 | 修复内容 | 代码改动量 | 建议时间 |
|--------|----------|----------|-----------|----------|
| P2 | N-001 | 生产环境移除 CSP unsafe-eval（可用 Vite HTML 转换或构建时注入区分 dev/prod CSP） | ~10行 | 下迭代 |
| P3 | N-002 | resolveFullVideoUrl 添加 `..` 检查（与 resolveSegmentUrl 一致） | ~3行 | 待办 |
| P3 | N-004 | 生产环境移除 CSP connect-src ws:wss:（同 N-001 方案） | ~1行 | 待办 |

---

## 12. 趋势对比

| 维度 | 07-12 (首次) | 07-14 (全检) | 07-18 (回归) | 07-22 (本轮) | 趋势 |
|------|-------------|-------------|-------------|-------------|------|
| Critical | 1 | 1 | 0 | 0 | ✅ 清零 |
| High | 2 | 2 | 0 | 0 | ✅ 清零 |
| Medium | 2 | 2 | 0 | 0 | ✅ 清零 |
| Low | 5 | 5 | 5 | 3 | ⬇️ 改善 |
| Info | 3 | 3 | 4 | 2 | 持平 |
| 修复率 | N/A | N/A | 11/13 | 12/13 | ✅ 持续改善 |
| 评分 | B | B | C+→B+ | A- | ⬆️ 升级 |
| 判断 | — | — | Conditional Go | **GO** | ✅ 放行 |
