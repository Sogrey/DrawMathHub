import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import { useUserStore } from '@/stores/userStore'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
// 须在首屏路由守卫之前恢复登录态，否则刷新深链会先被踢到登录页再跳首页
useUserStore(pinia).restoreSession()
app.use(router)

app.mount('#app')
