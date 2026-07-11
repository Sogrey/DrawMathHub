/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** 见项目根目录 .env */
  readonly VITE_BASE_PATH: string
  readonly BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
