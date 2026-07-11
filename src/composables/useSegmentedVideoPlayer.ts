import { ref, computed, watch, onUnmounted, nextTick, type Ref } from 'vue'
import type { InteractiveVideoManifest, VideoPlayMode } from '@/types/video'
import { resolveSegmentUrl, resolveFullVideoUrl } from '@/data/videoAssets'

export interface UseSegmentedVideoPlayerOptions {
  manifest: Ref<InteractiveVideoManifest | null>
  basePath: Ref<string>
  mode: Ref<VideoPlayMode>
}

export function useSegmentedVideoPlayer(options: UseSegmentedVideoPlayerOptions) {
  const videoA = ref<HTMLVideoElement | null>(null)
  const videoB = ref<HTMLVideoElement | null>(null)
  const activeSlot = ref<'a' | 'b'>('a')

  const currentSegmentIndex = ref(0)
  const isPlaying = ref(false)
  const isLoading = ref(false)
  const waitingForContinue = ref(false)
  const loadError = ref<string | null>(null)
  const segmentReady = ref(false)

  const segments = computed(() => options.manifest.value?.segments ?? [])
  const segmentCount = computed(() => segments.value.length)
  const isFirstSegment = computed(() => currentSegmentIndex.value <= 0)
  const isLastSegment = computed(
    () => segmentCount.value === 0 || currentSegmentIndex.value >= segmentCount.value - 1,
  )

  const fullVideoUrl = computed(() => {
    if (!options.manifest.value) return ''
    return resolveFullVideoUrl(options.basePath.value, options.manifest.value)
  })

  function activeVideo(): HTMLVideoElement | null {
    return activeSlot.value === 'a' ? videoA.value : videoB.value
  }

  function inactiveVideo(): HTMLVideoElement | null {
    return activeSlot.value === 'a' ? videoB.value : videoA.value
  }

  function segmentUrl(index: number): string {
    const seg = segments.value[index]
    if (!seg) return ''
    return resolveSegmentUrl(options.basePath.value, seg)
  }

  function swapActiveSlot() {
    activeSlot.value = activeSlot.value === 'a' ? 'b' : 'a'
  }

  function attachEndedHandler(video: HTMLVideoElement) {
    video.onended = () => {
      isPlaying.value = false
      if (options.mode.value === 'interactive') {
        waitingForContinue.value = true
      }
    }
  }

  function detachHandlers(video: HTMLVideoElement | null) {
    if (!video) return
    video.onended = null
    video.oncanplay = null
    video.onerror = null
  }

  function playSegment(index: number, autoplay = true): Promise<void> {
    return new Promise((resolve, reject) => {
      if (options.mode.value === 'full') {
        reject(new Error('full mode'))
        return
      }

      const url = segmentUrl(index)
      if (!url) {
        reject(new Error('invalid segment'))
        return
      }

      const inactive = inactiveVideo()
      const active = activeVideo()
      if (!inactive) {
        reject(new Error('no video element'))
        return
      }

      isLoading.value = true
      loadError.value = null
      waitingForContinue.value = false
      currentSegmentIndex.value = index
      segmentReady.value = false

      if (active) {
        active.pause()
      }

      detachHandlers(inactive)

      inactive.onerror = () => {
        isLoading.value = false
        reject(new Error('segment load failed'))
      }

      inactive.oncanplay = () => {
        inactive.oncanplay = null
        isLoading.value = false
        segmentReady.value = true

        swapActiveSlot()
        const nowActive = activeVideo()
        if (nowActive) {
          attachEndedHandler(nowActive)
        }

        if (autoplay && nowActive) {
          nowActive
            .play()
            .then(() => {
              isPlaying.value = true
              resolve()
            })
            .catch(() => {
              isPlaying.value = false
              resolve()
            })
        } else {
          isPlaying.value = false
          resolve()
        }

        preloadAdjacent(index)
      }

      inactive.src = url
      inactive.load()
    })
  }

  function preloadAdjacent(index: number) {
    const targets = [index + 1, index - 1].filter(i => i >= 0 && i < segmentCount.value)
    for (const i of targets) {
      const link = document.createElement('link')
      link.rel = 'prefetch'
      link.as = 'video'
      link.href = segmentUrl(i)
      document.head.appendChild(link)
      setTimeout(() => link.remove(), 30_000)
    }
  }

  function playCurrentSegment() {
    return playSegment(currentSegmentIndex.value, true)
  }

  function pause() {
    activeVideo()?.pause()
    isPlaying.value = false
  }

  function togglePlay() {
    const video = activeVideo()
    if (!video) return
    if (video.paused) {
      video.play().then(() => {
        isPlaying.value = true
        waitingForContinue.value = false
      })
    } else {
      pause()
    }
  }

  function goPrevSegment() {
    if (isFirstSegment.value) return
    playSegment(currentSegmentIndex.value - 1)
  }

  function goNextSegment() {
    if (isLastSegment.value) return
    playSegment(currentSegmentIndex.value + 1)
  }

  function goToSegment(index: number) {
    if (index < 0 || index >= segmentCount.value) return
    playSegment(index)
  }

  function continueToNext() {
    waitingForContinue.value = false
    if (!isLastSegment.value) {
      goNextSegment()
    }
  }

  function resetInteractive(autoplay = true): Promise<void> {
    currentSegmentIndex.value = 0
    waitingForContinue.value = false
    isPlaying.value = false
    loadError.value = null
    if (segments.value.length === 0) return Promise.resolve()
    return nextTick().then(() => playSegment(0, autoplay))
  }

  watch(
    () => options.mode.value,
    mode => {
      waitingForContinue.value = false
      isPlaying.value = false
      loadError.value = null
      if (mode === 'interactive' && segments.value.length > 0) {
        void resetInteractive(true)
      }
    },
  )

  watch(
    () => options.manifest.value,
    manifest => {
      if (manifest && options.mode.value === 'interactive' && manifest.segments.length > 0) {
        void resetInteractive(true)
      }
    },
  )

  onUnmounted(() => {
    detachHandlers(videoA.value)
    detachHandlers(videoB.value)
  })

  return {
    videoA,
    videoB,
    activeSlot,
    currentSegmentIndex,
    isPlaying,
    isLoading,
    waitingForContinue,
    loadError,
    segmentReady,
    segments,
    segmentCount,
    isFirstSegment,
    isLastSegment,
    fullVideoUrl,
    playSegment,
    playCurrentSegment,
    pause,
    togglePlay,
    goPrevSegment,
    goNextSegment,
    goToSegment,
    continueToNext,
    resetInteractive,
    activeVideo,
  }
}
