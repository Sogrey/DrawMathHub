<template>
  <div
    class="grid-card group rounded-card shadow-elevation cursor-pointer transform transition-all duration-300 hover:scale-[1.03] hover:shadow-elevation-hover border border-border overflow-hidden relative backdrop-blur-md"
    :style="{ backgroundColor: cardBgColor }"
    @click="onCardClick"
    @mouseenter="onTipEnter"
    @mousemove="onTipMove"
    @mouseleave="onTipLeave"
    @pointerdown="onPointerDown"
    @pointerup="onPointerUp"
    @pointercancel="onPointerUp"
    @pointerleave="onPointerLeaveCard"
  >
    <img
      v-if="coverOk && coverSrc"
      :src="coverSrc"
      alt=""
      class="card-cover absolute inset-0 w-full h-full object-cover pointer-events-none"
      @error="coverOk = false"
    />
    <!-- 无封面时的统一占位 -->
    <svg
      v-else
      class="absolute inset-x-0 bottom-0 h-[55%] w-full opacity-[0.18] pointer-events-none"
      viewBox="0 0 100 100"
      preserveAspectRatio="xMidYMid slice"
    >
      <circle cx="25" cy="50" r="8" stroke="#C9563A" stroke-width="3" fill="none" />
      <circle cx="50" cy="50" r="8" stroke="#C9563A" stroke-width="3" fill="none" />
      <circle cx="75" cy="50" r="8" stroke="#C9563A" stroke-width="3" fill="none" />
      <circle cx="37" cy="50" r="4" fill="#C9563A" opacity="0.3" />
      <circle cx="62" cy="50" r="4" fill="#C9563A" opacity="0.3" />
    </svg>

    <div class="card-scrim absolute inset-0 pointer-events-none" aria-hidden="true" />

    <div class="relative z-10 flex h-full min-h-[inherit] flex-col p-4 sm:p-5">
      <div class="flex items-start justify-between gap-3 shrink-0">
        <span
          class="size-10 shrink-0 rounded-xl flex items-center justify-center font-bold text-base leading-none tabular-nums text-accentCream shadow-sm"
          :style="{ backgroundColor: theme.badgeBg }"
        >
          {{ problem.lessonNumber }}
        </span>
        <div
          v-if="progress && progress.practiceCount > 0"
          class="status-chip flex items-center gap-1 text-xs px-2.5 py-1 rounded-full"
        >
          <span class="text-textTertiary">{{ progress.practiceCount }}次</span>
          <span class="text-textTertiary/60">·</span>
          <span class="font-bold tabular-nums" :style="{ color: accuracyColor }">{{ accuracy }}%</span>
        </div>
        <div
          v-else-if="progress?.learned"
          class="status-chip text-xs text-successText font-medium px-2.5 py-1 rounded-full"
        >
          ✓ 已学
        </div>
      </div>

      <div class="flex-1 min-h-[2.5rem]" aria-hidden="true" />

      <div class="flex items-end justify-between gap-3 mt-auto">
        <h3 class="card-title text-text font-semibold text-lg sm:text-xl leading-snug tracking-body line-clamp-2 min-w-0">
          {{ problem.title }}
        </h3>
        <span
          class="shrink-0 inline-flex text-xs font-medium px-3 py-1.5 rounded-full"
          :style="{ backgroundColor: theme.pillBg, color: theme.pillFg }"
        >
          {{ problem.methodType }}
        </span>
      </div>
    </div>
  </div>

  <Teleport to="body">
    <div
      v-show="tipVisible"
      class="card-tip"
      :style="tipStyle"
      role="tooltip"
    >
      <span class="tip-method">{{ problem.methodType }}</span>
      <p class="tip-body">{{ problem.problemIdentification }}</p>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Problem, LearningProgress } from '@/data/problems'
import { getCoverUrl } from '@/data/videoAssets'

const props = defineProps<{
  problem: Problem
  progress?: LearningProgress | null
}>()

const router = useRouter()

const tipVisible = ref(false)
const tipX = ref(0)
const tipY = ref(0)
const tipOnLeft = ref(false)

const TOUCH_HOLD_MS = 400
let touchHoldTimer: ReturnType<typeof setTimeout> | null = null
let touchTipShown = false
let suppressNextClick = false

function clearTouchHold() {
  if (touchHoldTimer) {
    clearTimeout(touchHoldTimer)
    touchHoldTimer = null
  }
}

function onTipEnter(e: MouseEvent) {
  tipVisible.value = true
  onTipMove(e)
}

function onTipMove(e: MouseEvent) {
  tipX.value = e.clientX
  tipY.value = e.clientY
  tipOnLeft.value = e.clientX > window.innerWidth * 0.55
}

function onTipLeave() {
  tipVisible.value = false
}

function onPointerDown(e: PointerEvent) {
  if (e.pointerType !== 'touch') return
  clearTouchHold()
  touchTipShown = false
  const x = e.clientX
  const y = e.clientY
  touchHoldTimer = setTimeout(() => {
    tipX.value = x
    tipY.value = y
    tipOnLeft.value = x > window.innerWidth * 0.55
    tipVisible.value = true
    touchTipShown = true
    suppressNextClick = true
  }, TOUCH_HOLD_MS)
}

function onPointerUp() {
  clearTouchHold()
  if (touchTipShown) {
    tipVisible.value = false
    touchTipShown = false
  }
}

function onPointerLeaveCard(e: PointerEvent) {
  if (e.pointerType === 'touch') {
    clearTouchHold()
    if (touchTipShown) {
      tipVisible.value = false
      touchTipShown = false
    }
  } else {
    onTipLeave()
  }
}

function onCardClick() {
  if (suppressNextClick) {
    suppressNextClick = false
    return
  }
  router.push(`/problem/${props.problem.lessonNumber}`)
}

onUnmounted(() => clearTouchHold())

const tipStyle = computed(() => {
  const gap = 10
  return {
    left: `${tipX.value}px`,
    top: `${tipY.value}px`,
    transform: tipOnLeft.value
      ? `translate(calc(-100% - ${gap}px), calc(-100% - ${gap}px))`
      : `translate(${gap}px, calc(-100% - ${gap}px))`,
  }
})

const coverSrc = computed(() => {
  const exampleId = props.problem.mainProblem?.id
  if (!props.problem.id || !exampleId) return ''
  return getCoverUrl(props.problem.id, exampleId)
})
const coverOk = ref(true)

watch(
  () => [props.problem.lessonNumber, coverSrc.value] as const,
  () => {
    coverOk.value = Boolean(coverSrc.value)
  },
  { immediate: true },
)

const bgColors = [
  'rgba(26, 24, 22, 0.75)',
  'rgba(30, 28, 26, 0.72)',
  'rgba(35, 33, 30, 0.70)',
  'rgba(48, 40, 36, 0.68)',
  'rgba(26, 24, 22, 0.78)',
  'rgba(40, 36, 32, 0.72)',
  'rgba(32, 30, 28, 0.74)',
  'rgba(44, 38, 34, 0.70)',
  'rgba(28, 26, 24, 0.76)',
  'rgba(36, 32, 28, 0.72)',
]

type MethodTheme = { badgeBg: string; pillBg: string; pillFg: string }

const DEFAULT_THEME: MethodTheme = {
  badgeBg: '#9A3D28',
  pillBg: 'rgba(154, 61, 40, 0.75)',
  pillFg: '#EAD6B8',
}

const methodThemes: Record<string, MethodTheme> = {
  '图示法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '列表法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '画线法': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '连线法': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '线段图法': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '树状图法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '倒推法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '逆推法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '竖式法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '表格法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '统计图法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '数轴法': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '坐标系法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '韦恩图法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '流程图法': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '假设法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '排除法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '枚举法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '转化法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '建模法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '归纳法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '类比法': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '插旗法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '年龄轴法': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '打包法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '移多补少法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '天平法': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '方阵问题': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '周期问题': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '重叠问题': { badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '利润问题': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '火车过桥': { badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '十字交叉法': { badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
}

const cardBgColor = computed(() => bgColors[props.problem.lessonNumber % bgColors.length])

const theme = computed(
  () => methodThemes[props.problem.methodType] ?? DEFAULT_THEME,
)

const accuracy = computed(() => {
  if (!props.progress || props.progress.practiceCount === 0) return 0
  return Math.round((props.progress.correctCount / props.progress.practiceCount) * 100)
})

const accuracyColor = computed(() => {
  if (accuracy.value >= 80) return '#A8D4C4'
  if (accuracy.value >= 60) return '#EAD6B8'
  return '#F0A898'
})
</script>

<style scoped>
.grid-card {
  min-height: 168px;
  aspect-ratio: 16 / 10;
}

.card-cover {
  opacity: 0.38;
  transform: scale(1);
  transform-origin: center 50%;
  filter: saturate(0.9) brightness(0.92);
}

.card-scrim {
  background:
    linear-gradient(
      180deg,
      rgba(12, 11, 10, 0.72) 0%,
      rgba(12, 11, 10, 0.18) 42%,
      rgba(12, 11, 10, 0.55) 100%
    );
}

.status-chip {
  background: rgba(20, 18, 16, 0.55);
  border: 1px solid rgba(234, 214, 184, 0.12);
  backdrop-filter: blur(6px);
}

.card-title {
  text-shadow: 0 1px 10px rgba(0, 0, 0, 0.55);
}

.card-tip {
  position: fixed;
  z-index: 80;
  max-width: 220px;
  padding: 0.45rem 0.65rem;
  border-radius: 0.5rem;
  background: rgba(22, 20, 18, 0.92);
  border: 1px solid rgba(234, 214, 184, 0.14);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  pointer-events: none;
}

.tip-method {
  display: inline-block;
  color: #c9563a;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-bottom: 0.2rem;
}

.tip-body {
  color: rgba(234, 214, 184, 0.88);
  font-size: 0.75rem;
  line-height: 1.4;
  margin: 0;
}

.line-clamp-2 {
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tracking-body {
  letter-spacing: 0.5px;
}
</style>
