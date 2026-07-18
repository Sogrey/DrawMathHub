/** 仅允许站内相对路径，拒绝协议相对 URL（//evil.com）与外链 */
export function safeInternalPath(redirect: unknown, fallback = '/'): string {
  if (typeof redirect !== 'string' || !redirect) return fallback
  if (!redirect.startsWith('/')) return fallback
  if (redirect.startsWith('//')) return fallback
  if (redirect.includes('://')) return fallback
  return redirect
}
