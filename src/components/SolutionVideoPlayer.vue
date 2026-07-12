<template>
  <div class="solution-video-player w-full flex flex-col">
    <!-- 加载探测 -->
    <div
      v-if="availability.status === 'loading'"
      class="w-full aspect-video glass-card-secondary rounded-card border border-border flex flex-col items-center justify-center gap-3"
    >
      <Loader2 class="animate-spin text-primary" :size="40" />
      <p class="text-textTertiary text-body-sm">正在加载讲解视频…</p>
    </div>

    <!-- 视频尚未制作 -->
    <div
      v-else-if="!isVideoReady"
      class="w-full aspect-video bg-gradient-to-br from-cardSecondary to-card rounded-card border border-border flex flex-col items-center justify-center p-8 text-center"
    >
      <div class="w-16 h-16 rounded-full glass-card-secondary flex items-center justify-center mb-4">
        <Clapperboard class="text-primaryDark" :size="32" />
      </div>
      <p class="text-lg font-bold text-text mb-2">{{ VIDEO_PENDING_TITLE }}</p>
      <p v-if="VIDEO_PENDING_MESSAGE" class="text-body-sm text-textSecondary max-w-sm leading-relaxed">
        {{ VIDEO_PENDING_MESSAGE }}
      </p>
    </div>

    <!-- 视频已就绪 -->
    <template v-else>
      <div class="flex items-center justify-between mb-3 gap-3 flex-wrap">
        <div class="inline-flex rounded-button border border-border overflow-hidden glass-card-secondary p-0.5">
          <button
            type="button"
            class="px-4 py-2 text-sm font-medium rounded-[10px] transition-colors"
            :class="mode === 'full'
              ? 'bg-primaryDark text-accentCream shadow-sm'
              : 'text-textSecondary hover:text-text'"
            :disabled="!availability.hasFullVideo"
            @click="setMode('full')"
          >
            <Play class="inline-block mr-1.5" :size="16" />
            完整播放
          </button>
          <button
            type="button"
            class="px-4 py-2 text-sm font-medium rounded-[10px] transition-colors"
            :class="mode === 'interactive'
              ? 'bg-primaryDark text-accentCream shadow-sm'
              : 'text-textSecondary hover:text-text'"
            :disabled="!availability.hasInteractive"
            @click="setMode('interactive')"
          >
            <StepForward class="inline-block mr-1.5" :size="16" />
            分步学习
          </button>
        </div>
        <p v-if="mode === 'interactive'" class="text-body-sm text-textTertiary">
          每段播完自动暂停，点击「继续」或分段按钮进入下一段
        </p>
      </div>

      <div
        class="relative w-full aspect-video bg-[#111122] rounded-card overflow-hidden border border-border"
      >
        <video
          v-if="mode === 'full' && availability.hasFullVideo"
          ref="fullVideoRef"
          class="absolute inset-0 w-full h-full object-contain"
          :src="availability.fullVideoUrl"
          controls
          playsinline
          preload="metadata"
        />

        <template v-else-if="mode === 'interactive' && availability.hasInteractive">
          <video
            ref="videoA"
            class="absolute inset-0 w-full h-full object-contain transition-opacity duration-150"
            :class="activeSlot === 'a' ? 'opacity-100 z-[2]' : 'opacity-0 z-[1]'"
            playsinline
            preload="auto"
            @click="togglePlay"
          />
          <video
            ref="videoB"
            class="absolute inset-0 w-full h-full object-contain transition-opacity duration-150"
            :class="activeSlot === 'b' ? 'opacity-100 z-[2]' : 'opacity-0 z-[1]'"
            playsinline
            preload="auto"
            @click="togglePlay"
          />

          <div
            v-if="isLoading"
            class="absolute inset-0 z-[3] flex items-center justify-center bg-black/40"
          >
            <Loader2 class="animate-spin text-white" :size="36" />
          </div>

          <div
            v-else-if="waitingForContinue && !isLastSegment"
            class="absolute inset-x-0 bottom-0 z-[3] p-4 bg-gradient-to-t from-black/75 to-transparent"
          >
            <div class="flex items-center justify-center gap-3">
              <p class="text-white/90 text-sm">本段已播完</p>
              <button
                type="button"
                class="px-5 py-2 rounded-button bg-primary text-white font-medium hover:bg-primaryDark transition-colors shadow-lg"
                @click="continueToNext"
              >
                继续下一段
                <ChevronRight class="inline-block ml-1" :size="18" />
              </button>
            </div>
          </div>

          <div
            v-else-if="waitingForContinue && isLastSegment"
            class="absolute inset-x-0 bottom-0 z-[3] p-4 bg-gradient-to-t from-black/75 to-transparent text-center"
          >
            <p class="text-white font-medium">🎉 本分步讲解已看完，可以完成学习啦</p>
          </div>

          <button
            v-if="!isPlaying && !isLoading && !waitingForContinue && segmentReady"
            type="button"
            class="absolute inset-0 z-[3] flex items-center justify-center bg-black/20 hover:bg-black/30 transition-colors group"
            @click="togglePlay"
          >
            <span class="w-16 h-16 rounded-full glass-card flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform">
              <Play class="text-primary ml-1" :size="32" fill="currentColor" />
            </span>
          </button>
        </template>
      </div>

      <div
        v-if="mode === 'interactive' && availability.hasInteractive && manifest"
        class="mt-4 flex flex-col gap-3"
      >
        <div class="flex items-center justify-center gap-1.5 flex-wrap">
          <button
            type="button"
            class="nav-btn nav-btn-arrow"
            :disabled="isFirstSegment"
            title="上一段"
            @click="goPrevSegment"
          >
            上一步
          </button>

          <button
            v-for="(seg, index) in segments"
            :key="seg.id"
            type="button"
            class="nav-btn nav-btn-segment min-w-[2.5rem]"
            :class="{
              'nav-btn-active': currentSegmentIndex === index,
              'nav-btn-done': index < currentSegmentIndex,
            }"
            @click="goToSegment(index)"
          >
            {{ seg.label }}
          </button>

          <button
            type="button"
            class="nav-btn nav-btn-arrow"
            :disabled="isLastSegment"
            title="下一段"
            @click="goNextSegment"
          >
            下一步
          </button>
        </div>

        <p
          v-if="currentSegment?.hint"
          class="text-center text-body-sm text-textSecondary glass-card-secondary rounded-card px-4 py-2"
        >
          {{ currentSegment.hint }}
        </p>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { Play, StepForward, Loader2, ChevronRight, Clapperboard } from '@lucide/vue'
import type { VideoPlayMode, InteractiveVideoManifest, VideoAvailability } from '@/types/video'
import { VIDEO_PENDING_TITLE, VIDEO_PENDING_MESSAGE } from '@/types/video'
import { getExampleBasePath, probeVideoAvailability } from '@/data/videoAssets'
import { useSegmentedVideoPlayer } from '@/composables/useSegmentedVideoPlayer'

const props = withDefaults(
  defineProps<{
    problemUuid: string
    exampleUuid: string
  }>(),
  {},
)

const mode = ref<VideoPlayMode>('full')
const manifest = ref<InteractiveVideoManifest | null>(null)
const availability = ref<VideoAvailability>({
  status: 'loading',
  manifest: null,
  hasFullVideo: false,
  hasInteractive: false,
  fullVideoUrl: '',
})

const basePath = computed(() => getExampleBasePath(props.problemUuid, props.exampleUuid))

const {
  videoA,
  videoB,
  activeSlot,
  currentSegmentIndex,
  isPlaying,
  isLoading,
  waitingForContinue,
  segmentReady,
  segments,
  isFirstSegment,
  isLastSegment,
  togglePlay,
  goPrevSegment,
  goNextSegment,
  goToSegment,
  continueToNext,
} = useSegmentedVideoPlayer({
  manifest,
  basePath,
  mode,
})

const currentSegment = computed(() => segments.value[currentSegmentIndex.value])

const isVideoReady = computed(
  () =>
    availability.value.status === 'ready'
    && (availability.value.hasFullVideo || availability.value.hasInteractive),
)

function pickDefaultMode(avail: VideoAvailability): VideoPlayMode {
  if (avail.hasFullVideo) return 'full'
  if (avail.hasInteractive) return 'interactive'
  return 'full'
}

function setMode(next: VideoPlayMode) {
  if (next === 'full' && !availability.value.hasFullVideo) return
  if (next === 'interactive' && !availability.value.hasInteractive) return
  mode.value = next
}

async function probeAndInit() {
  availability.value = {
    status: 'loading',
    manifest: null,
    hasFullVideo: false,
    hasInteractive: false,
    fullVideoUrl: '',
  }

  const result = await probeVideoAvailability(props.problemUuid, props.exampleUuid)
  availability.value = result
  manifest.value = result.manifest

  if (result.status !== 'ready' || (!result.hasFullVideo && !result.hasInteractive)) return

  mode.value = pickDefaultMode(result)
}

watch(
  () => [props.problemUuid, props.exampleUuid] as const,
  () => probeAndInit(),
)

onMounted(() => probeAndInit())
</script>

<style scoped>
.nav-btn {
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  line-height: 1.25rem;
  font-weight: 500;
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
  border-width: 1px;
  border-style: solid;
  border-color: rgb(var(--color-border) / 0.15);
}

.nav-btn-arrow {
  color: rgb(var(--color-text-secondary));
  background-color: var(--glass-card-secondary-bg);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.nav-btn-arrow:hover:not(:disabled) {
  color: rgb(var(--color-primary-dark));
  background-color: var(--glass-card-hover-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.nav-btn-arrow:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  color: rgb(var(--color-text-secondary));
  background-color: var(--glass-card-secondary-bg);
}

.nav-btn-segment {
  color: rgb(var(--color-text-secondary));
  background-color: var(--glass-card-bg);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.nav-btn-segment:hover {
  color: rgb(var(--color-primary-dark));
  background-color: var(--glass-card-hover-bg);
}

.nav-btn-active {
  background-color: rgb(var(--color-primary-dark));
  color: rgb(var(--color-cream));
  border-color: rgb(var(--color-primary-dark));
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  transform: scale(1.05);
}

.nav-btn-done {
  background-color: rgb(var(--color-success) / 0.15);
  color: rgb(var(--color-success-text));
  border-color: rgb(var(--color-success) / 0.3);
}
</style>
