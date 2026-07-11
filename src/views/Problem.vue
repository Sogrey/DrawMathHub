<template>
  <div class="min-h-screen bg-background">
    <Navigation :showBack="true" />
    <div v-if="problem" class="max-w-4xl mx-auto px-4 py-8">
      <div class="glass-card rounded-card shadow-elevation p-6 mb-6 border border-border">
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <span class="glass-card-hover text-primaryDark px-3 py-1 rounded-full text-sm font-bold">{{ problem.lesson }}</span>
              <span class="glass-card-secondary text-textTertiary px-3 py-1 rounded-full text-sm">{{ problem.methodType }}</span>
            </div>
            <h1 class="text-xl font-bold text-text">{{ problem.title }}</h1>
            <p class="text-textTertiary mt-2 text-body-sm">{{ problem.problemIdentification }}</p>
          </div>
          <div v-if="progress?.learned" class="text-successText">
            <CheckCircle :size="32" />
          </div>
        </div>
      </div>

      <div class="glass-card rounded-card shadow-elevation p-6 mb-6 border border-border">
        <h2 class="text-lg font-bold text-text mb-3 flex items-center gap-2">
          <Search class="text-primary" :size="20" />
          规律分析
        </h2>
        <div class="glass-card-secondary rounded-card p-4 space-y-3">
          <p class="text-textSecondary text-body-sm leading-relaxed">
            <span class="font-medium text-primaryDark">分析切入口：</span>{{ problem.problemIdentification }}
          </p>
          <p class="text-textSecondary text-body-sm leading-relaxed">
            <span class="font-medium text-primaryDark">推荐画图法：</span>{{ problem.method }}
          </p>
        </div>
      </div>

      <div class="flex gap-4 mb-6">
        <button
          class="flex-1 py-3 rounded-button font-medium transition-colors"
          :class="activeTab === 'learning' ? 'bg-primaryDark text-accentCream hover:opacity-90' : 'glass-card-secondary text-textSecondary hover:glass-card-hover border border-border'"
          @click="switchTab('learning')"
        >
          <BookOpen class="inline-block mr-2" :size="18" />
          学习例题
        </button>
        <button
          v-if="hasExtensions"
          class="flex-1 py-3 rounded-button font-medium transition-colors"
          :class="activeTab === 'extension' ? 'bg-primaryDark text-accentCream hover:opacity-90' : 'glass-card-secondary text-textSecondary hover:glass-card-hover border border-border'"
          @click="switchTab('extension')"
        >
          <Lightbulb class="inline-block mr-2" :size="18" />
          举一反三
        </button>
        <button
          v-if="hasExercises"
          class="flex-1 py-3 rounded-button font-medium transition-colors"
          :class="activeTab === 'practice' ? 'bg-primaryDark text-accentCream hover:opacity-90' : 'glass-card-secondary text-textSecondary hover:glass-card-hover border border-border'"
          @click="switchTab('practice')"
        >
          <Pencil class="inline-block mr-2" :size="18" />
          练习
        </button>
      </div>

      <div v-if="activeTab === 'learning'" class="glass-card rounded-card shadow-elevation p-6 border border-border">
        <div v-if="problem.mainProblem" class="space-y-6">
          <div class="glass-card-secondary rounded-card p-4">
            <p class="text-textSecondary font-medium text-body">{{ problem.mainProblem.originalQuestion }}</p>
          </div>

          <div class="bg-background rounded-card p-4">
            <SolutionVideoPlayer
              :problem-uuid="problem.id"
              :example-uuid="problem.mainProblem.id"
            />
          </div>

          <div class="space-y-4">
            <div class="glass-card-secondary rounded-card p-4">
              <h3 class="font-bold text-text mb-2 flex items-center gap-2">
                <PenTool class="text-primary" :size="18" />
                画图分析
              </h3>
              <p class="text-textSecondary text-body-sm leading-relaxed">{{ problem.mainProblem.drawingAnalysis }}</p>
            </div>

            <div class="glass-card-secondary rounded-card p-4">
              <h3 class="font-bold text-text mb-2 flex items-center gap-2">
                <FileText class="text-primary" :size="18" />
                规范解答
              </h3>
              <p class="text-textSecondary text-body-sm leading-relaxed whitespace-pre-line">{{ problem.mainProblem.standardSolution }}</p>
            </div>

            <div class="bg-success/20 rounded-card p-4">
              <h3 class="font-bold text-successText mb-2 flex items-center gap-2">
                <Star class="text-successText" :size="18" />
                关键点拨
              </h3>
              <p class="text-textSecondary text-body-sm leading-relaxed">{{ problem.mainProblem.keyPoints }}</p>
            </div>
          </div>

          <div class="flex justify-center">
            <button
              class="px-8 py-3 rounded-button font-medium bg-success text-successText hover:bg-success/80 transition-colors"
              @click="markAsLearned"
            >
              <CheckCircle class="inline-block mr-2" :size="18" />
              完成学习
            </button>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'extension'" class="glass-card rounded-card shadow-elevation p-6 border border-border">
        <div v-if="currentExtension" class="space-y-6">
          <div class="flex items-center justify-center gap-4 mb-4">
            <button
              class="px-4 py-2 rounded-button glass-card-hover text-primaryDark hover:glass-card-secondary transition-colors"
              :disabled="currentExtensionIndex === 0"
              @click="prevExtension"
            >
              <ArrowLeft :size="18" />
            </button>
            <span class="text-lg font-bold text-text">{{ currentExtensionIndex + 1 }} / {{ problem.extensionProblems.length }}</span>
            <button
              class="px-4 py-2 rounded-button glass-card-hover text-primaryDark hover:glass-card-secondary transition-colors"
              :disabled="isLastExtension"
              @click="nextExtension"
            >
              <ArrowRight :size="18" />
            </button>
          </div>

          <div class="glass-card-secondary rounded-card p-4">
            <div class="flex items-center gap-3 mb-2">
              <span class="text-primary font-medium">难度：</span>
              <span class="text-text">{{ currentExtension.difficulty }}</span>
            </div>
            <p class="text-textSecondary font-medium text-body">{{ currentExtension.question }}</p>
          </div>

          <div v-if="currentExtension.hint" class="glass-card-secondary rounded-card p-4">
            <h3 class="font-bold text-primaryDark mb-2 flex items-center gap-2">
              <Lightbulb class="text-primary" :size="18" />
              提示
            </h3>
            <p class="text-textSecondary text-body-sm leading-relaxed">{{ currentExtension.hint }}</p>
          </div>

          <div class="bg-background rounded-card p-6 h-[400px] flex flex-col">
            <PracticeCanvas />
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'practice'" class="glass-card rounded-card shadow-elevation p-6 border border-border">
        <div class="flex items-center justify-between mb-6">
          <div class="flex gap-2 flex-wrap">
            <button
              v-for="(_, index) in problem.exercises"
              :key="index"
              class="w-10 h-10 rounded-button font-bold transition-colors"
              :class="currentExerciseIndex === index 
                ? 'bg-primaryDark text-accentCream'
                : 'glass-card-secondary text-textSecondary hover:glass-card-hover border border-border'"
              @click="selectExercise(index)"
            >
              {{ index + 1 }}
            </button>
          </div>
          <div class="flex items-center gap-4">
            <button
              class="px-4 py-2 rounded-button glass-card-hover text-primaryDark hover:glass-card-secondary transition-colors"
              :disabled="currentExerciseIndex === 0"
              @click="prevExercise"
            >
              <ArrowLeft :size="18" />
            </button>
            <span class="text-lg font-bold text-text">{{ currentExerciseIndex + 1 }} / {{ problem.exercises.length }}</span>
            <button
              class="px-4 py-2 rounded-button glass-card-hover text-primaryDark hover:glass-card-secondary transition-colors"
              :disabled="currentExerciseIndex === problem.exercises.length - 1"
              @click="nextExercise"
            >
              <ArrowRight :size="18" />
            </button>
          </div>
        </div>

        <div v-if="currentExercise" class="space-y-6">
          <div class="glass-card-secondary rounded-card p-4">
            <div class="flex items-center gap-3 mb-2">
              <span class="text-primary font-medium">难度：</span>
              <span class="text-text">{{ currentExercise.difficulty }}</span>
            </div>
            <p class="text-textSecondary font-medium text-body">{{ currentExercise.question }}</p>
          </div>

          <div class="flex items-center gap-4">
            <span class="text-textSecondary">答案：</span>
            <input
              v-model="answer"
              type="text"
              class="flex-1 px-4 py-2 rounded-button border-2 border-border focus:border-primary focus:outline-none bg-background"
              placeholder="请输入答案"
            />
            <button
              class="px-6 py-2 rounded-button font-medium bg-primary text-white hover:bg-primaryDark transition-colors"
              @click="submitAnswer"
            >
              提交答案
            </button>
          </div>

          <div class="bg-background rounded-card p-4 h-[600px] flex flex-col">
            <PracticeCanvas />
          </div>

          <div
            v-if="showResult"
            class="rounded-card p-4"
            :class="isCorrect ? 'bg-success/20' : 'bg-danger/20'"
          >
            <div class="flex items-center gap-2">
              <CheckCircle v-if="isCorrect" class="text-successText" :size="24" />
              <XCircle v-else class="text-dangerText" :size="24" />
              <span class="font-bold" :class="isCorrect ? 'text-successText' : 'text-dangerText'">
                {{ isCorrect ? '回答正确！太棒了！' : '回答错误，继续加油！' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="isLoading" class="min-h-screen flex items-center justify-center bg-background">
      <Loader2 class="animate-spin text-primary" :size="48" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { CheckCircle, Search, BookOpen, Pencil, ArrowLeft, ArrowRight, Loader2, XCircle, Lightbulb, PenTool, FileText, Star } from '@lucide/vue'
import Navigation from '@/components/Navigation.vue'
import SolutionVideoPlayer from '@/components/SolutionVideoPlayer.vue'
import PracticeCanvas from '@/components/PracticeCanvas.vue'
import { useProblemStore } from '@/stores/problemStore'
import { useProgressStore } from '@/stores/progressStore'
import type { LearningProgress } from '@/data/problems'

const route = useRoute()
const problemStore = useProblemStore()
const progressStore = useProgressStore()

const answer = ref('')
const showResult = ref(false)
const isCorrect = ref(false)
const currentProgress = ref<LearningProgress | null>(null)
const currentExerciseIndex = ref(0)
const shuffledExerciseIndices = ref<number[]>([])

const problem = computed(() => problemStore.currentProblem)
const currentExtension = computed(() => problemStore.currentExtension)
const currentExtensionIndex = computed(() => problemStore.currentExtensionIndex)
const isLastExtension = computed(() => problemStore.isLastExtension)
const hasExtensions = computed(() => problemStore.hasExtensions)
const hasExercises = computed(() => problemStore.hasExercises)
const activeTab = computed(() => problemStore.activeTab)
const currentExercise = computed(() => {
  if (!problem.value) return null
  const shuffledIndex = shuffledExerciseIndices.value[currentExerciseIndex.value]
  return problem.value.exercises[shuffledIndex] || null
})
const isLoading = computed(() => problemStore.isLoading)

const progress = computed(() => currentProgress.value)

async function loadProblemProgress() {
  if (problem.value) {
    currentProgress.value = await progressStore.getProgress(problem.value.lessonNumber)
  }
}

function selectProblem(problemId: number) {
  problemStore.selectProblem(problemId)
}

function nextExtension() {
  problemStore.nextExtension()
}

function prevExtension() {
  problemStore.prevExtension()
}

function shuffleArray<T>(array: T[]): T[] {
  const result = [...array]
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[result[i], result[j]] = [result[j], result[i]]
  }
  return result
}

function initExerciseShuffle() {
  if (!problem.value) return
  const indices = Array.from({ length: problem.value.exercises.length }, (_, i) => i)
  shuffledExerciseIndices.value = shuffleArray(indices)
  currentExerciseIndex.value = 0
}

function selectExercise(index: number) {
  currentExerciseIndex.value = index
  answer.value = ''
  showResult.value = false
}

function nextExercise() {
  if (!problem.value || currentExerciseIndex.value >= problem.value.exercises.length - 1) return
  currentExerciseIndex.value++
  answer.value = ''
  showResult.value = false
}

function prevExercise() {
  if (currentExerciseIndex.value <= 0) return
  currentExerciseIndex.value--
  answer.value = ''
  showResult.value = false
}

function switchTab(tab: 'learning' | 'extension' | 'practice') {
  problemStore.switchTab(tab)
  if (tab === 'practice') {
    initExerciseShuffle()
    answer.value = ''
    showResult.value = false
  }
}

function markAsLearned() {
  if (problem.value) {
    progressStore.markAsLearned(problem.value.lessonNumber)
    currentProgress.value = { ...currentProgress.value!, learned: true }
  }
}

function submitAnswer() {
  if (!currentExercise.value || !answer.value.trim()) return

  showResult.value = true
  isCorrect.value = true

  if (problem.value) {
    progressStore.recordPractice(problem.value.lessonNumber, isCorrect.value)
    if (currentProgress.value) {
      currentProgress.value.practiceCount++
      if (isCorrect.value) {
        currentProgress.value.correctCount++
      }
      currentProgress.value.lastPracticeTime = Date.now()
    }
  }
}

watch(() => route.params.id, (id) => {
  selectProblem(Number(id))
  loadProblemProgress()
})

onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    selectProblem(id)
  }
  progressStore.loadProgress()
  loadProblemProgress()
})
</script>