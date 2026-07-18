import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/db/indexedDB'
import {
  getAllUsers,
  getUser,
  createUser,
  updateUserLastLogin,
  verifyPassword,
  deleteUser as deleteUserDB,
  getAllProgress,
  saveProgress,
} from '@/db/indexedDB'

const SESSION_KEY = 'drawMathCurrentUser'

interface SessionPayload {
  nickname: string
}

function persistSession(nickname: string): void {
  const payload: SessionPayload = { nickname }
  sessionStorage.setItem(SESSION_KEY, JSON.stringify(payload))
}

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)
  const users = ref<User[]>([])
  const isLoading = ref(false)
  const dbError = ref<string | null>(null)

  const isAuthenticated = computed(() => currentUser.value !== null)

  async function loadUsers() {
    isLoading.value = true
    dbError.value = null
    try {
      users.value = await getAllUsers()
    } catch (e) {
      dbError.value = e instanceof Error ? e.message : '无法打开本地数据库'
      users.value = []
    } finally {
      isLoading.value = false
    }
  }

  async function login(nickname: string, password?: string): Promise<boolean> {
    isLoading.value = true
    dbError.value = null
    try {
      const user = await getUser(nickname)
      if (!user) return false

      if (user.passwordHash) {
        if (!password) return false
        const ok = await verifyPassword(nickname, password, user.passwordHash)
        if (!ok) return false
      }

      await updateUserLastLogin(nickname)
      const refreshed = (await getUser(nickname)) ?? user
      currentUser.value = refreshed
      users.value = await getAllUsers()
      persistSession(nickname)
      return true
    } catch (e) {
      dbError.value = e instanceof Error ? e.message : '登录失败'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function logout(): Promise<void> {
    currentUser.value = null
    sessionStorage.removeItem(SESSION_KEY)
  }

  async function createUserWithNickname(
    nickname: string,
    password?: string,
  ): Promise<User | null> {
    isLoading.value = true
    dbError.value = null
    try {
      const existing = await getUser(nickname)
      if (existing) return null

      const user = await createUser(nickname, password)
      users.value = await getAllUsers()
      currentUser.value = user
      persistSession(nickname)
      return user
    } catch (e) {
      dbError.value = e instanceof Error ? e.message : '创建用户失败'
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function updatePassword(nickname: string, newPassword: string): Promise<boolean> {
    isLoading.value = true
    try {
      const user = await getUser(nickname)
      if (!user) return false

      const { updateUserPassword } = await import('@/db/indexedDB')
      await updateUserPassword(nickname, newPassword)

      users.value = await getAllUsers()
      if (currentUser.value?.nickname === nickname) {
        currentUser.value = (await getUser(nickname)) ?? currentUser.value
      }
      return true
    } finally {
      isLoading.value = false
    }
  }

  async function deleteUser(nickname: string, password?: string): Promise<boolean> {
    isLoading.value = true
    try {
      const user = await getUser(nickname)
      if (!user) return false

      if (user.passwordHash) {
        if (!password) return false
        const ok = await verifyPassword(nickname, password, user.passwordHash)
        if (!ok) return false
      }

      await deleteUserDB(nickname)
      users.value = await getAllUsers()

      if (currentUser.value?.nickname === nickname) {
        currentUser.value = null
        sessionStorage.removeItem(SESSION_KEY)
      }

      return true
    } finally {
      isLoading.value = false
    }
  }

  /** 仅恢复 nickname，再从 IndexedDB 重载完整用户（不含 passwordHash 进 session） */
  async function restoreSession(): Promise<void> {
    const stored = sessionStorage.getItem(SESSION_KEY)
    if (!stored) return

    try {
      const parsed = JSON.parse(stored) as SessionPayload | User
      const nickname = parsed?.nickname
      if (!nickname || typeof nickname !== 'string') {
        sessionStorage.removeItem(SESSION_KEY)
        return
      }

      // 兼容旧 session：若曾存入完整 User，立即降级为仅 nickname
      persistSession(nickname)

      const user = await getUser(nickname)
      if (!user) {
        sessionStorage.removeItem(SESSION_KEY)
        currentUser.value = null
        return
      }
      currentUser.value = user
    } catch {
      sessionStorage.removeItem(SESSION_KEY)
      currentUser.value = null
    }
  }

  async function migrateFromLocalStorage(): Promise<void> {
    const oldData = localStorage.getItem('drawMathProgress')
    if (!oldData || !currentUser.value) return

    try {
      const parsed = JSON.parse(oldData)
      if (parsed.problems && Array.isArray(parsed.problems)) {
        for (const problem of parsed.problems) {
          const record = {
            id: `${currentUser.value!.nickname}#${problem.problemId}`,
            nickname: currentUser.value!.nickname,
            problemId: problem.problemId,
            learned: problem.learned || false,
            practiceCount: problem.practiceCount || 0,
            correctCount: problem.correctCount || 0,
            lastPracticeTime: problem.lastPracticeTime || 0,
          }
          await saveProgress(record)
        }
      }
      localStorage.removeItem('drawMathProgress')
    } catch {
      console.warn('Failed to migrate data from localStorage')
    }
  }

  async function getUserProgress(nickname: string) {
    return getAllProgress(nickname)
  }

  return {
    currentUser,
    users,
    isLoading,
    dbError,
    isAuthenticated,
    loadUsers,
    login,
    logout,
    createUserWithNickname,
    updatePassword,
    deleteUser,
    restoreSession,
    migrateFromLocalStorage,
    getUserProgress,
  }
})
