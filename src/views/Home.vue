<template>
  <div class="min-h-screen bg-background">
    <Navigation />
    <div class="max-w-6xl mx-auto px-4 py-8">
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-2xl mb-4">
          <span class="text-4xl">📐</span>
        </div>
        <h1 class="text-title-lg font-bold text-text mb-3">小学数学画图解题法</h1>
        <p class="text-textTertiary text-body-sm max-w-md mx-auto">通过画图的方式，让数学变得简单有趣</p>
        <div class="mt-6 flex flex-wrap justify-center gap-4">
          <div class="glass-card rounded-card px-6 py-4 shadow-elevation border border-border">
            <div class="text-2xl font-bold text-primaryDark">{{ progressStore.totalLearned }}</div>
            <div class="text-caption text-textTertiary mt-1">已学习</div>
          </div>
          <div class="glass-card rounded-card px-6 py-4 shadow-elevation border border-border">
            <div class="text-2xl font-bold text-primaryDark">{{ progressStore.totalPracticed }}</div>
            <div class="text-caption text-textTertiary mt-1">练习次数</div>
          </div>
          <div class="glass-card rounded-card px-6 py-4 shadow-elevation border border-border">
            <div class="text-2xl font-bold" :class="accuracyColor">{{ progressStore.overallAccuracy }}%</div>
            <div class="text-caption text-textTertiary mt-1">正确率</div>
          </div>
        </div>
      </div>

      <div class="mb-8">
        <div class="flex flex-wrap gap-3 justify-center">
          <button
            class="px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-200"
            :class="selectedType === 'all' ? 'bg-primaryDark text-accentCream shadow-elevation' : 'glass-card text-textTertiary hover:glass-card-hover border border-border'"
            @click="selectedType = 'all'"
          >
            全部
          </button>
          <button
            v-for="type in methodTypes"
            :key="type"
            class="px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-200"
            :class="selectedType === type ? 'bg-primaryDark text-accentCream shadow-elevation' : 'glass-card text-textTertiary hover:glass-card-hover border border-border'"
            @click="selectedType = type"
          >
            {{ type }}
          </button>
        </div>
      </div>

      <div v-if="isLoading" class="text-center py-16">
        <Loader2 class="animate-spin text-primary mx-auto" :size="48" />
        <p class="text-textTertiary mt-4">加载中...</p>
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <GridCard
          v-for="problem in filteredProblems"
          :key="problem.lessonNumber"
          :problem="problem"
          :progress="progressMap[problem.lessonNumber]"
        />
      </div>

      <div v-if="!isLoading && filteredProblems.length === 0" class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <p class="text-textTertiary">暂无该类型的题目</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Navigation from '@/components/Navigation.vue'
import GridCard from '@/components/GridCard.vue'
import { methodTypes, loadAllProblems } from '@/data/problems'
import { useProgressStore } from '@/stores/progressStore'
import type { Problem, LearningProgress } from '@/data/problems'
import { Loader2 } from '@lucide/vue'

const progressStore = useProgressStore()
const selectedType = ref('all')
const progressMap = ref<Record<number, LearningProgress | null>>({})
const problems = ref<Problem[]>([])
const isLoading = ref(true)

const filteredProblems = computed(() => {
  if (selectedType.value === 'all') return problems.value
  return problems.value.filter(p => p.methodType === selectedType.value)
})

const accuracyColor = computed(() => {
  if (progressStore.overallAccuracy >= 80) return 'text-successText'
  if (progressStore.overallAccuracy >= 60) return 'text-warningText'
  return 'text-dangerText'
})

async function loadAllProgress() {
  await progressStore.loadProgress()
  for (const problem of problems.value) {
    const progress = await progressStore.getProgress(problem.lessonNumber)
    progressMap.value[problem.lessonNumber] = progress
  }
}

async function initData() {
  isLoading.value = true
  problems.value = await loadAllProblems()
  await loadAllProgress()
  isLoading.value = false
}

onMounted(() => {
  initData()
})
</script>