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
  const { useUserStore } = await import('@/stores/userStore')
  const userStore = useUserStore()

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }
  if (to.path === '/login' && userStore.isAuthenticated) {
    const redirect = typeof to.query.redirect === 'string' ? to.query.redirect : '/'
    next(redirect.startsWith('/') ? redirect : '/')
    return
  }
  next()
})

export default router
