import { afterEach, describe, expect, it, vi } from 'vitest'
import { fetchJson, publicUrl } from '@/utils/publicUrl'

describe('publicUrl', () => {
  it('joins base and path without double slash issues', () => {
    expect(publicUrl('data/problems/1.json')).toMatch(/data\/problems\/1\.json$/)
    expect(publicUrl('/videos/a/b/full.mp4')).toMatch(/videos\/a\/b\/full\.mp4$/)
  })
})

describe('fetchJson', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('returns parsed JSON on success', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        headers: { get: () => 'application/json' },
        json: async () => ({ a: 1 }),
      }),
    )
    await expect(fetchJson('/x.json', null)).resolves.toEqual({ a: 1 })
  })

  it('returns fallback on 404', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 404,
        headers: { get: () => 'text/html' },
      }),
    )
    await expect(fetchJson('/missing.json', { empty: true })).resolves.toEqual({ empty: true })
  })

  it('returns fallback when SPA serves HTML', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        headers: { get: () => 'text/html; charset=utf-8' },
        json: async () => {
          throw new Error('not json')
        },
      }),
    )
    await expect(fetchJson('/videos/x/manifest.json', null)).resolves.toBeNull()
  })

  it('returns fallback when fetch throws', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockRejectedValue(new TypeError('Failed to fetch')),
    )
    await expect(fetchJson('/x.json', [])).resolves.toEqual([])
  })
})
