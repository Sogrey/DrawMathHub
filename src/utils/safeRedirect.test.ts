import { describe, expect, it } from 'vitest'
import { safeInternalPath } from '@/utils/safeRedirect'

describe('safeInternalPath', () => {
  it('allows relative in-app paths', () => {
    expect(safeInternalPath('/problem/1')).toBe('/problem/1')
    expect(safeInternalPath('/')).toBe('/')
  })

  it('rejects protocol-relative and absolute URLs', () => {
    expect(safeInternalPath('//evil.com')).toBe('/')
    expect(safeInternalPath('https://evil.com')).toBe('/')
    expect(safeInternalPath('http://evil.com/x')).toBe('/')
  })

  it('rejects non-string and empty', () => {
    expect(safeInternalPath(undefined)).toBe('/')
    expect(safeInternalPath('')).toBe('/')
    expect(safeInternalPath(1)).toBe('/')
  })

  it('uses custom fallback', () => {
    expect(safeInternalPath('//x', '/home')).toBe('/home')
  })
})
