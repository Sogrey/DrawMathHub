import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/db/indexedDB'
import {
  getAllUsers,
  getUser,
  createUser,
  updateUserLastLogin,
  hashPassword,
  deleteUser as deleteUserDB,
  getAllProgress,
  saveProgress
} from '@/db/indexedDB'

const SESSION_KEY = 'drawMathCurrentUser'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)
  const users = ref<User[]>([])
  const isLoading = ref(false)

  const isAuthenticated = computed(() => currentUser.value !== null)

  async function loadUsers() {
    isLoading.value = true
    try {
      users.value = await getAllUsers()
    } finally {
      isLoading.value = false
    }
  }

  async function login(nickname: string, password?: string): Promise<boolean> {
    isLoading.value = true
    try {
      const user = await getUser(nickname)
      if (!user) return false

      if (user.passwordHash) {
        if (!password) return false
        const inputHash = await hashPassword(password)
        if (inputHash !== user.passwordHash) return false
      }

      await updateUserLastLogin(nickname)
      currentUser.value = user
      users.value = await getAllUsers()

      sessionStorage.setItem(SESSION_KEY, JSON.stringify(user))
      return true
    } finally {
      isLoading.value = false
    }
  }

  async function logout(): Promise<void> {
    currentUser.value = null
    sessionStorage.removeItem(SESSION_KEY)
  }

  async function createUserWithNickname(nickname: string, password?: string): Promise<User | null> {
    isLoading.value = true
    try {
      const existing = await getUser(nickname)
      if (existing) return null

      const user = await createUser(nickname, password)
      users.value = await getAllUsers()
      currentUser.value = user

      sessionStorage.setItem(SESSION_KEY, JSON.stringify(user))
      return user
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
        const inputHash = await hashPassword(password)
        if (inputHash !== user.passwordHash) return false
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

  function restoreSession(): void {
    const stored = sessionStorage.getItem(SESSION_KEY)
    if (stored) {
      try {
        currentUser.value = JSON.parse(stored)
      } catch {
        sessionStorage.removeItem(SESSION_KEY)
      }
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
            lastPracticeTime: problem.lastPracticeTime || 0
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
    isAuthenticated,
    loadUsers,
    login,
    logout,
    createUserWithNickname,
    updatePassword,
    deleteUser,
    restoreSession,
    migrateFromLocalStorage,
    getUserProgress
  }
})
