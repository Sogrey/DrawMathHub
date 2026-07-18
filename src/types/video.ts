export const VIDEO_PENDING_TITLE = '讲解视频正在加急制作，敬请期待'
export const VIDEO_PENDING_MESSAGE = '可以先阅读下方的规律分析与文字讲解。'

export const VIDEO_ERROR_TITLE = '讲解视频暂时无法加载'
export const VIDEO_ERROR_MESSAGE = '请检查网络后重试；若仍失败，可先阅读下方的规律分析与文字讲解。'

export interface VideoSegment {
  /** 分段视频 uuid */
  id: string
  /** 语义角色：intro / question / draw-1 … */
  role?: string
  label: string
  file: string
  hint?: string
  /** 完整版时间轴起止（秒），供 ffmpeg 切分；前端播放可忽略 */
  startTime?: number
  endTime?: number
}

export interface InteractiveVideoManifest {
  version: number
  problemId?: string
  exampleId?: string
  fullVideo?: string
  segments: VideoSegment[]
}

export type VideoPlayMode = 'full' | 'interactive'

export type VideoAvailabilityStatus = 'loading' | 'ready' | 'pending' | 'error'

export interface VideoAvailability {
  status: VideoAvailabilityStatus
  manifest: InteractiveVideoManifest | null
  hasFullVideo: boolean
  hasInteractive: boolean
  fullVideoUrl: string
}
