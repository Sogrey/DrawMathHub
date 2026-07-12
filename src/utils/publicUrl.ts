import { getAppBase } from '@/config/app'

/** 拼接部署 base 与 public 目录下的资源路径 */
export function publicUrl(path: string): string {
  const normalized = path.replace(/^\//, '')
  return `${getAppBase()}${normalized}`
}

/** 安全拉取 JSON，避免 404 回退为 index.html 时 parse 报错 */
export async function fetchJson<T>(url: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(url)
    if (!response.ok) return fallback
    const contentType = response.headers.get('content-type') ?? ''
    if (contentType.includes('text/html')) return fallback
    if (!contentType.includes('json')) return fallback
    return (await response.json()) as T
  } catch {
    return fallback
  }
}
