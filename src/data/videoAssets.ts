import type { InteractiveVideoManifest, VideoAvailability, VideoSegment } from '@/types/video'
import { publicUrl, fetchJson } from '@/utils/publicUrl'

export function getExampleBasePath(problemUuid: string, exampleUuid: string): string {
  return publicUrl(`videos/${problemUuid}/${exampleUuid}`)
}

export function getFullVideoUrl(problemUuid: string, exampleUuid: string): string {
  return `${getExampleBasePath(problemUuid, exampleUuid)}/full.mp4`
}

/** 与 full.mp4 同目录的大厅封面 */
export function getCoverUrl(problemUuid: string, exampleUuid: string): string {
  return `${getExampleBasePath(problemUuid, exampleUuid)}/cover.png`
}

export function getManifestUrl(problemUuid: string, exampleUuid: string): string {
  return `${getExampleBasePath(problemUuid, exampleUuid)}/manifest.json`
}

/** 拒绝路径穿越；非法则返回空串 */
function safeRelativeFile(file: string): string | null {
  const f = file.replace(/\\/g, '/').trim()
  if (!f || f.includes('..') || f.startsWith('/') || f.includes('://')) return null
  return f
}

export function resolveSegmentUrl(basePath: string, segment: VideoSegment): string {
  if (segment.file.startsWith('/')) {
    const stripped = segment.file.replace(/^\/+/, '')
    if (stripped.includes('..')) return ''
    return publicUrl(stripped)
  }
  const safe = safeRelativeFile(segment.file)
  if (!safe) return ''
  return `${basePath}/${safe}`
}

export function resolveFullVideoUrl(
  basePath: string,
  manifest: InteractiveVideoManifest,
): string {
  if (manifest.fullVideo) {
    return manifest.fullVideo.startsWith('/')
      ? publicUrl(manifest.fullVideo)
      : `${basePath}/${manifest.fullVideo}`
  }
  return `${basePath}/full.mp4`
}

function isVideoResponse(contentType: string): boolean {
  const ct = contentType.toLowerCase()
  if (!ct || ct.includes('text/html') || ct.includes('json')) return false
  return ct.includes('video/') || ct.includes('octet-stream') || ct.includes('mp4')
}

type ProbeResult = 'found' | 'missing' | 'error'

/** 探测 mp4 是否存在；区分 404/未制作 vs 网络/5xx 错误 */
async function probeResource(url: string): Promise<ProbeResult> {
  if (!url) return 'missing'
  try {
    const res = await fetch(url, { method: 'GET', headers: { Range: 'bytes=0-0' } })
    if (res.status === 404 || res.status === 410) return 'missing'
    if (res.status >= 500) return 'error'
    if (!res.ok) {
      // 其它 4xx（含 Range 不支持等）按缺失处理，避免误报 error
      if (res.status >= 400 && res.status < 500) return 'missing'
      return 'error'
    }
    const contentType = res.headers.get('content-type') ?? ''
    if (isVideoResponse(contentType)) return 'found'
    // SPA 404 回退 HTML
    if (contentType.includes('text/html') || contentType.includes('json')) return 'missing'
    // 部分环境 HEAD/Range 不返回准确 type，用 content-range 辅助判断
    if (res.status === 206 && res.headers.get('content-range') !== null) return 'found'
    return 'missing'
  } catch {
    return 'error'
  }
}

function mergeProbe(...results: ProbeResult[]): ProbeResult {
  if (results.some((r) => r === 'found')) return 'found'
  if (results.some((r) => r === 'error')) return 'error'
  return 'missing'
}

export async function loadVideoManifest(
  problemUuid: string,
  exampleUuid: string,
): Promise<InteractiveVideoManifest | null> {
  const data = await fetchJson<InteractiveVideoManifest | null>(
    getManifestUrl(problemUuid, exampleUuid),
    null,
  )
  if (!data || !Array.isArray(data.segments)) return null
  return data
}

export async function probeVideoAvailability(
  problemUuid: string,
  exampleUuid: string,
): Promise<VideoAvailability> {
  const basePath = getExampleBasePath(problemUuid, exampleUuid)
  const fullVideoUrl = getFullVideoUrl(problemUuid, exampleUuid)

  let manifest: InteractiveVideoManifest | null = null
  let manifestLoadError = false
  try {
    manifest = await loadVideoManifest(problemUuid, exampleUuid)
  } catch {
    manifestLoadError = true
  }

  const manifestFullUrl = manifest
    ? resolveFullVideoUrl(basePath, manifest)
    : fullVideoUrl

  const fullProbe = await probeResource(fullVideoUrl)
  const altProbe =
    manifestFullUrl !== fullVideoUrl
      ? await probeResource(manifestFullUrl)
      : ('missing' as ProbeResult)
  const fullMerged = mergeProbe(fullProbe, altProbe)
  const hasFullVideo = fullMerged === 'found'

  let hasInteractive = false
  let segmentProbe: ProbeResult = 'missing'
  if (manifest && manifest.segments.length > 0) {
    const checks = await Promise.all(
      manifest.segments.map((seg) => probeResource(resolveSegmentUrl(basePath, seg))),
    )
    segmentProbe = mergeProbe(...checks)
    hasInteractive = segmentProbe === 'found'
  }

  if (hasFullVideo || hasInteractive) {
    return {
      status: 'ready',
      manifest,
      hasFullVideo,
      hasInteractive,
      fullVideoUrl: manifestFullUrl,
    }
  }

  const anyError =
    manifestLoadError
    || fullMerged === 'error'
    || segmentProbe === 'error'

  return {
    status: anyError ? 'error' : 'pending',
    manifest: null,
    hasFullVideo: false,
    hasInteractive: false,
    fullVideoUrl: manifestFullUrl,
  }
}
