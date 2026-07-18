import { ref } from 'vue'

/** 全局轻量错误提示（无第三方 toast 依赖） */
export const appErrorToast = ref<string | null>(null)

let hideTimer: ReturnType<typeof setTimeout> | null = null

export function showAppErrorToast(message: string, durationMs = 4000): void {
  appErrorToast.value = message
  if (hideTimer) clearTimeout(hideTimer)
  hideTimer = setTimeout(() => {
    appErrorToast.value = null
    hideTimer = null
  }, durationMs)
}

export function clearAppErrorToast(): void {
  if (hideTimer) clearTimeout(hideTimer)
  hideTimer = null
  appErrorToast.value = null
}
