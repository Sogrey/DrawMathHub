import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { LearningProgress } from '@/data/problems'
import { useUserStore } from './userStore'
import {
  getAllProgress,
  getProgress as getProgressDB,
  getOrCreateProgress,
  saveProgress as saveProgressDB,
} from '@/db/indexedDB'

export const useProgressStore = defineStore('progress', () => {
  const totalLearned = ref(0)
  const totalPracticed = ref(0)
  const totalCorrect = ref(0)
  const problems = ref<LearningProgress[]>([])

  const overallAccuracy = computed(() => {
    if (totalPracticed.value === 0) return 0
    return Math.round((totalCorrect.value / totalPracticed.value) * 100)
  })

  async function loadProgress() {
    const userStore = useUserStore()
    if (!userStore.currentUser) {
      totalLearned.value = 0
      totalPracticed.value = 0
      totalCorrect.value = 0
      problems.value = []
      return
    }

    try {
      const records = await getAllProgress(userStore.currentUser.nickname)
      problems.value = records.map((record) => ({
        problemId: record.problemId,
        learned: record.learned,
        practiceCount: record.practiceCount,
        correctCount: record.correctCount,
        lastPracticeTime: record.lastPracticeTime,
      }))

      totalLearned.value = problems.value.filter((p) => p.learned).length
      totalPracticed.value = problems.value.reduce((sum, p) => sum + p.practiceCount, 0)
      totalCorrect.value = problems.value.reduce((sum, p) => sum + p.correctCount, 0)
    } catch {
      problems.value = []
      totalLearned.value = 0
      totalPracticed.value = 0
      totalCorrect.value = 0
    }
  }

  async function markAsLearned(problemId: number) {
    const userStore = useUserStore()
    if (!userStore.currentUser) return

    const record = await getOrCreateProgress(userStore.currentUser.nickname, problemId)
    record.learned = true
    await saveProgressDB(record)
    await loadProgress()
  }

  async function recordPractice(problemId: number, isCorrect: boolean) {
    const userStore = useUserStore()
    if (!userStore.currentUser) return

    const record = await getOrCreateProgress(userStore.currentUser.nickname, problemId)
    record.practiceCount++
    if (isCorrect) {
      record.correctCount++
    }
    record.lastPracticeTime = Date.now()
    await saveProgressDB(record)
    await loadProgress()
  }

  /** 只读：不存在则返回 null，不创建空记录 */
  async function getProgress(problemId: number): Promise<LearningProgress | null> {
    const userStore = useUserStore()
    if (!userStore.currentUser) return null

    const record = await getProgressDB(userStore.currentUser.nickname, problemId)
    if (!record) return null
    return {
      problemId: record.problemId,
      learned: record.learned,
      practiceCount: record.practiceCount,
      correctCount: record.correctCount,
      lastPracticeTime: record.lastPracticeTime,
    }
  }

  /** 从已 load 的 problems 构建 Map，供首页一次性读取 */
  function getProgressMap(): Record<number, LearningProgress | null> {
    const map: Record<number, LearningProgress | null> = {}
    for (const p of problems.value) {
      map[p.problemId] = p
    }
    return map
  }

  function calculateAccuracy(practiceCount: number, correctCount: number): number {
    if (practiceCount === 0) return 0
    return Math.round((correctCount / practiceCount) * 100)
  }

  watch(
    () => useUserStore().currentUser,
    () => {
      loadProgress()
    },
  )

  return {
    totalLearned,
    totalPracticed,
    totalCorrect,
    problems,
    loadProgress,
    markAsLearned,
    recordPractice,
    getProgress,
    getProgressMap,
    overallAccuracy,
    calculateAccuracy,
  }
})
