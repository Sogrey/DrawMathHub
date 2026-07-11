import { createRouter, createWebHistory } from 'vue-router'
import { getAppBase } from '@/config/app'
import Home from '@/views/Home.vue'
import Problem from '@/views/Problem.vue'
import Login from '@/views/Login.vue'

const router = createRouter({
  history: createWebHistory(getAppBase()),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/problem/:id',
      name: 'Problem',
      component: Problem,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, _from, next) => {
  if (to.meta.requiresAuth) {
    const { useUserStore } = await import('@/stores/userStore')
    const userStore = useUserStore()
    if (!userStore.isAuthenticated) {
      next('/login')
      return
    }
  }
  next()
})

export default router
