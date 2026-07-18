import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { useUserStore } from '@/stores/userStore'
import { showAppErrorToast } from '@/utils/appErrorToast'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

app.config.errorHandler = (err, _instance, info) => {
  console.error('[Vue]', info, err)
  const message =
    err instanceof Error
      ? err.message || '发生未知错误'
      : typeof err === 'string'
        ? err
        : '发生未知错误'
  showAppErrorToast(message)
}

async function bootstrap() {
  // 须在首屏路由守卫之前恢复登录态，否则刷新深链会先被踢到登录页再跳首页
  await useUserStore(pinia).restoreSession()
  app.use(router)
  app.mount('#app')
}

bootstrap()
