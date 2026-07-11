import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { LearningProgress } from '@/data/problems'
import { useUserStore } from './userStore'
import {
  getAllProgress,
  getOrCreateProgress,
  saveProgress as saveProgressDB
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

    const records = await getAllProgress(userStore.currentUser.nickname)
    problems.value = records.map(record => ({
      problemId: record.problemId,
      learned: record.learned,
      practiceCount: record.practiceCount,
      correctCount: record.correctCount,
      lastPracticeTime: record.lastPracticeTime
    }))

    totalLearned.value = problems.value.filter(p => p.learned).length
    totalPracticed.value = problems.value.reduce((sum, p) => sum + p.practiceCount, 0)
    totalCorrect.value = problems.value.reduce((sum, p) => sum + p.correctCount, 0)
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

  async function getProgress(problemId: number): Promise<LearningProgress | null> {
    const userStore = useUserStore()
    if (!userStore.currentUser) return null

    const record = await getOrCreateProgress(userStore.currentUser.nickname, problemId)
    return {
      problemId: record.problemId,
      learned: record.learned,
      practiceCount: record.practiceCount,
      correctCount: record.correctCount,
      lastPracticeTime: record.lastPracticeTime
    }
  }

  function calculateAccuracy(practiceCount: number, correctCount: number): number {
    if (practiceCount === 0) return 0
    return Math.round((correctCount / practiceCount) * 100)
  }

  watch(
    () => useUserStore().currentUser,
    () => {
      loadProgress()
    }
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
    overallAccuracy,
    calculateAccuracy
  }
})
