/**
 * 应用部署 base（末尾带 /）
 * 来源：.env `VITE_BASE_PATH` → vite.config `base` → `import.meta.env.BASE_URL`
 */
export function getAppBase(): string {
  const base = import.meta.env.BASE_URL || import.meta.env.VITE_BASE_PATH || '/'
  if (base === '/') return '/'
  return base.endsWith('/') ? base : `${base}/`
}

/** 与 getAppBase() 相同，便于语义化引用 */
export const APP_BASE = getAppBase()
