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
          <div v-if="isLearned" class="text-successText">
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
              class="px-8 py-3 rounded-button font-medium transition-colors"
              :class="isLearned
                ? 'bg-success/30 text-successText cursor-default'
                : 'bg-success text-successText hover:bg-success/80'"
              :disabled="isLearned"
              @click="markAsLearned"
            >
              <CheckCircle v-if="isLearned" class="inline-block mr-2" :size="18" />
              <Circle v-else class="inline-block mr-2" :size="18" />
              {{ isLearned ? '已完成学习' : '完成学习' }}
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

          <div
            v-if="currentExtension.answer"
            class="glass-card-secondary rounded-card overflow-hidden"
          >
            <button
              type="button"
              class="w-full px-4 py-3 flex items-center justify-between gap-2 text-left hover:bg-white/5 transition-colors"
              @click="showReferenceAnswer = !showReferenceAnswer"
            >
              <h3 class="font-bold text-primaryDark flex items-center gap-2">
                <FileText class="text-primary" :size="18" />
                参考答案
              </h3>
              <ChevronDown
                class="text-textTertiary shrink-0 transition-transform"
                :class="{ 'rotate-180': showReferenceAnswer }"
                :size="18"
              />
            </button>
            <div v-if="showReferenceAnswer" class="px-4 pb-4 pt-0">
              <p class="text-textSecondary text-body-sm leading-relaxed whitespace-pre-line border-t border-border pt-3">
                {{ currentExtension.answer }}
              </p>
              <p class="text-textTertiary text-xs mt-2">仅供对照，不做正误判定</p>
            </div>
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

          <ExerciseAnswerPanel
            :key="`${problem.lessonNumber}-${currentExerciseIndex}-${currentExercise.question}`"
            :answer-key="currentExercise.answerKey"
            @graded="onExerciseGraded"
            @recorded="onExerciseRecorded"
          />

          <div
            v-if="currentExercise.answer"
            class="glass-card-secondary rounded-card overflow-hidden"
          >
            <div class="px-4 py-3 flex items-center justify-between gap-2">
              <h3 class="font-bold text-primaryDark flex items-center gap-2">
                <FileText class="text-primary" :size="18" />
                参考答案
              </h3>
              <span v-if="!showReferenceAnswer" class="text-textTertiary text-xs">提交后显示</span>
            </div>
            <div v-if="showReferenceAnswer" class="px-4 pb-4 pt-0">
              <p class="text-textSecondary text-body-sm leading-relaxed whitespace-pre-line border-t border-border pt-3">
                {{ currentExercise.answer }}
              </p>
              <p class="text-textTertiary text-xs mt-2">
                {{ currentExercise.answerKey ? '完整参考文案，判分以填空为准' : '本题暂不自动判分，请自行对照' }}
              </p>
            </div>
          </div>

          <div class="bg-background rounded-card p-4 h-[600px] flex flex-col">
            <PracticeCanvas />
          </div>

          <div
            v-if="showResult"
            class="rounded-card p-4"
            :class="lastGradeCorrect === null ? 'bg-primary/10' : lastGradeCorrect ? 'bg-success/20' : 'bg-danger/20'"
          >
            <div class="flex items-center gap-2">
              <CheckCircle
                v-if="lastGradeCorrect !== false"
                :class="lastGradeCorrect ? 'text-successText' : 'text-primary'"
                :size="24"
              />
              <span
                class="font-bold"
                :class="lastGradeCorrect === null ? 'text-primaryDark' : lastGradeCorrect ? 'text-successText' : 'text-dangerText'"
              >
                <template v-if="lastGradeCorrect === true">回答正确！太棒了！</template>
                <template v-else-if="lastGradeCorrect === false">回答错误，请对照下方参考答案</template>
                <template v-else>已记录本次练习，参考答案已显示</template>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="isLoading" class="min-h-screen flex items-center justify-center bg-background">
      <Loader2 class="animate-spin text-primary" :size="48" />
    </div>

    <div
      v-else
      class="min-h-[60vh] flex flex-col items-center justify-center px-4"
    >
      <p class="text-xl font-bold text-text mb-2">题目未找到</p>
      <p class="text-textTertiary mb-6 text-body-sm">请检查讲次编号，或从首页重新进入</p>
      <RouterLink
        to="/"
        class="px-6 py-3 rounded-button bg-primaryDark text-accentCream font-medium hover:opacity-90"
      >
        返回首页
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { CheckCircle, Circle, Search, BookOpen, Pencil, ArrowLeft, ArrowRight, Loader2, Lightbulb, PenTool, FileText, Star, ChevronDown } from '@lucide/vue'
import Navigation from '@/components/Navigation.vue'
import SolutionVideoPlayer from '@/components/SolutionVideoPlayer.vue'
import PracticeCanvas from '@/components/PracticeCanvas.vue'
import ExerciseAnswerPanel from '@/components/ExerciseAnswerPanel.vue'
import { useProblemStore } from '@/stores/problemStore'
import { useProgressStore } from '@/stores/progressStore'
import type { LearningProgress } from '@/data/problems'

const route = useRoute()
const problemStore = useProblemStore()
const progressStore = useProgressStore()

const showResult = ref(false)
/** true/false=已判分；null=仅记录 */
const lastGradeCorrect = ref<boolean | null>(null)
const showReferenceAnswer = ref(false)
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

/** 仅当进度记录与当前讲次一致时才视为已学，避免切换题目时沿用上一讲状态 */
const isLearned = computed(() => {
  if (!problem.value || !currentProgress.value) return false
  return (
    currentProgress.value.problemId === problem.value.lessonNumber
    && currentProgress.value.learned === true
  )
})

async function loadProblemProgress() {
  if (!problem.value) {
    currentProgress.value = null
    return
  }
  currentProgress.value = await progressStore.getProgress(problem.value.lessonNumber)
}

async function initPage(lessonId: number) {
  currentProgress.value = null
  await problemStore.selectProblem(lessonId)
  await loadProblemProgress()
}

function nextExtension() {
  showReferenceAnswer.value = false
  problemStore.nextExtension()
}

function prevExtension() {
  showReferenceAnswer.value = false
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

function resetExerciseUi() {
  showResult.value = false
  lastGradeCorrect.value = null
  showReferenceAnswer.value = false
}

function selectExercise(index: number) {
  currentExerciseIndex.value = index
  resetExerciseUi()
}

function nextExercise() {
  if (!problem.value || currentExerciseIndex.value >= problem.value.exercises.length - 1) return
  currentExerciseIndex.value++
  resetExerciseUi()
}

function prevExercise() {
  if (currentExerciseIndex.value <= 0) return
  currentExerciseIndex.value--
  resetExerciseUi()
}

function switchTab(tab: 'learning' | 'extension' | 'practice') {
  problemStore.switchTab(tab)
  showReferenceAnswer.value = false
  if (tab === 'practice') {
    initExerciseShuffle()
    resetExerciseUi()
  }
}

async function markAsLearned() {
  if (!problem.value || isLearned.value) return
  await progressStore.markAsLearned(problem.value.lessonNumber)
  await loadProblemProgress()
}

async function recordPractice(correct: boolean) {
  if (!problem.value) return
  await progressStore.recordPractice(problem.value.lessonNumber, correct)
  await loadProblemProgress()
}

async function onExerciseGraded(correct: boolean) {
  lastGradeCorrect.value = correct
  showResult.value = true
  showReferenceAnswer.value = true
  await recordPractice(correct)
}

async function onExerciseRecorded() {
  lastGradeCorrect.value = null
  showResult.value = true
  showReferenceAnswer.value = true
  await recordPractice(false)
}

watch(() => route.params.id, (id) => {
  const lessonId = Number(id)
  if (lessonId) initPage(lessonId)
})

onMounted(async () => {
  await progressStore.loadProgress()
  const id = Number(route.params.id)
  if (id) {
    await initPage(id)
  }
})
</script>