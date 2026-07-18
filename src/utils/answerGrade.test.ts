import { describe, expect, it } from 'vitest'
import { normalizeAnswerText, gradeAnswerKey, extractNumbers } from '@/utils/answerGrade'

describe('normalizeAnswerText', () => {
  it('trims and folds whitespace', () => {
    expect(normalizeAnswerText('  60  只  ')).toBe('60 只')
  })

  it('converts full-width digits and punctuation', () => {
    expect(normalizeAnswerText('６０只')).toBe('60只')
    expect(normalizeAnswerText('13．5')).toBe('13.5')
  })

  it('normalizes remainder markers', () => {
    expect(normalizeAnswerText('13余1')).toBe('13…1')
    expect(normalizeAnswerText('13……1')).toBe('13…1')
  })
})

describe('extractNumbers', () => {
  it('extracts integers and decimals', () => {
    expect(extractNumbers('答：13……1')).toEqual(['13', '1'])
    expect(extractNumbers('3.50升')).toEqual(['3.5'])
  })
})

describe('gradeAnswerKey', () => {
  it('grades number answers with unit tolerance', () => {
    const r = gradeAnswerKey({ type: 'number', values: ['60'] }, ['60只'])
    expect(r.correct).toBe(true)
  })

  it('grades exact answers', () => {
    const r = gradeAnswerKey({ type: 'exact', values: ['9楼'] }, ['9楼'])
    expect(r.correct).toBe(true)
    expect(gradeAnswerKey({ type: 'exact', values: ['9楼'] }, ['8楼']).correct).toBe(false)
  })

  it('grades remainder from single string', () => {
    const r = gradeAnswerKey(
      {
        type: 'remainder',
        blanks: [{ values: ['13'] }, { values: ['1'] }],
      },
      ['13……1'],
    )
    expect(r.correct).toBe(true)
    expect(r.detail).toEqual([true, true])
  })

  it('grades blanks separately', () => {
    const r = gradeAnswerKey(
      {
        type: 'blanks',
        blanks: [{ values: ['3'] }, { values: ['5'] }],
      },
      ['3', '5'],
    )
    expect(r.correct).toBe(true)
  })
})
