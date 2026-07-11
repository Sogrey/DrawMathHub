import type { InteractiveVideoManifest, VideoAvailability, VideoSegment } from '@/types/video'
import { publicUrl, fetchJson } from '@/utils/publicUrl'

export function getExampleBasePath(problemUuid: string, exampleUuid: string): string {
  return publicUrl(`videos/${problemUuid}/${exampleUuid}`)
}

export function getFullVideoUrl(problemUuid: string, exampleUuid: string): string {
  return `${getExampleBasePath(problemUuid, exampleUuid)}/full.mp4`
}

export function getManifestUrl(problemUuid: string, exampleUuid: string): string {
  return `${getExampleBasePath(problemUuid, exampleUuid)}/manifest.json`
}

export function resolveSegmentUrl(basePath: string, segment: VideoSegment): string {
  if (segment.file.startsWith('/')) return publicUrl(segment.file)
  return `${basePath}/${segment.file}`
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

async function resourceExists(url: string): Promise<boolean> {
  try {
    const res = await fetch(url, { method: 'HEAD' })
    if (res.ok) return true
    if (res.status === 405 || res.status === 404) {
      const getRes = await fetch(url, { method: 'GET', headers: { Range: 'bytes=0-0' } })
      return getRes.ok
    }
    return false
  } catch {
    return false
  }
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
  const manifest = await loadVideoManifest(problemUuid, exampleUuid)

  const manifestFullUrl = manifest
    ? resolveFullVideoUrl(basePath, manifest)
    : fullVideoUrl

  const hasFullVideo =
    (await resourceExists(fullVideoUrl)) ||
    (manifestFullUrl !== fullVideoUrl && (await resourceExists(manifestFullUrl)))

  let hasInteractive = false
  if (manifest && manifest.segments.length > 0) {
    const checks = await Promise.all(
      manifest.segments.map(seg => resourceExists(resolveSegmentUrl(basePath, seg))),
    )
    hasInteractive = checks.some(Boolean)
  }

  const ready = hasFullVideo || hasInteractive

  return {
    status: ready ? 'ready' : 'pending',
    manifest,
    hasFullVideo,
    hasInteractive,
    fullVideoUrl: manifestFullUrl,
  }
}
