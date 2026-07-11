import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

/** 与 src/config/app.ts 中 getAppBase 规则一致 */
function normalizeBase(base: string | undefined): string {
  const value = base?.trim() || '/'
  if (value === '/') return '/'
  return value.endsWith('/') ? value : `${value}/`
}

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const base = normalizeBase(env.VITE_BASE_PATH)

  return {
    base,
    plugins: [vue()],
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
  }
})
