import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Problem } from '@/data/problems'
import { loadProblem, loadAllProblems } from '@/data/problems'

export const useProblemStore = defineStore('problem', () => {
  const currentProblem = ref<Problem | null>(null)
  const currentExtensionIndex = ref(0)
  const activeTab = ref<'learning' | 'extension' | 'practice'>('learning')
  const isLoading = ref(false)
  const allProblems = ref<Problem[]>([])

  const currentExtension = computed(() => {
    if (!currentProblem.value) return null
    return currentProblem.value.extensionProblems[currentExtensionIndex.value] || null
  })

  const isLastExtension = computed(() => {
    if (!currentProblem.value) return true
    return currentExtensionIndex.value >= currentProblem.value.extensionProblems.length - 1
  })

  const hasExtensions = computed(() => {
    if (!currentProblem.value) return false
    return currentProblem.value.extensionProblems.length > 0
  })

  const hasExercises = computed(() => {
    if (!currentProblem.value) return false
    return currentProblem.value.exercises.length > 0
  })

  async function loadAllProblemList() {
    if (allProblems.value.length === 0) {
      allProblems.value = await loadAllProblems()
    }
    return allProblems.value
  }

  async function selectProblem(problemId: number) {
    isLoading.value = true
    const problem = await loadProblem(problemId)
    if (problem) {
      currentProblem.value = problem
      currentExtensionIndex.value = 0
      activeTab.value = 'learning'
    } else {
      currentProblem.value = null
    }
    isLoading.value = false
  }

  function nextExtension() {
    if (!currentProblem.value) return
    if (currentExtensionIndex.value < currentProblem.value.extensionProblems.length - 1) {
      currentExtensionIndex.value++
    }
  }

  function prevExtension() {
    if (currentExtensionIndex.value > 0) {
      currentExtensionIndex.value--
    }
  }

  function switchTab(tab: 'learning' | 'extension' | 'practice') {
    activeTab.value = tab
  }

  function resetProblem() {
    currentProblem.value = null
    currentExtensionIndex.value = 0
    activeTab.value = 'learning'
    isLoading.value = false
  }

  return {
    currentProblem,
    currentExtensionIndex,
    activeTab,
    isLoading,
    allProblems,
    currentExtension,
    isLastExtension,
    hasExtensions,
    hasExercises,
    loadAllProblemList,
    selectProblem,
    nextExtension,
    prevExtension,
    switchTab,
    resetProblem
  }
})