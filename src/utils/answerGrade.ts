import type { AnswerBlank, AnswerKey, Exercise } from '@/data/problems'

/** 全角数字/常见标点 → 半角，空白折叠 */
export function normalizeAnswerText(raw: string): string {
  let s = raw.trim()
  s = s.replace(/[\u3000\s]+/g, ' ')
  s = s.replace(/[０-９]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - 0xfee0))
  s = s.replace(/[．。]/g, '.')
  s = s.replace(/[，、]/g, ',')
  s = s.replace(/[：]/g, ':')
  s = s.replace(/[％]/g, '%')
  s = s.replace(/[／]/g, '/')
  // 余数点号统一
  s = s.replace(/[·•⋅･・.…]+/g, '…')
  s = s.replace(/余/g, '…')
  return s.trim()
}

/** 抽出规范化后的数字串（保留小数） */
export function extractNumbers(raw: string): string[] {
  const s = normalizeAnswerText(raw)
  return [...s.matchAll(/\d+(?:\.\d+)?/g)].map((m) => normalizeNumber(m[0]))
}

function normalizeNumber(n: string): string {
  if (!n.includes('.')) return String(Number(n))
  const v = Number(n)
  if (!Number.isFinite(v)) return n
  // 去掉多余尾随 0：3.50 → 3.5，但保留有意义小数
  return String(parseFloat(v.toFixed(10)))
}

function blankMatches(input: string, blank: AnswerBlank): boolean {
  const norm = normalizeAnswerText(input)
  if (!norm) return false

  const candidates = blank.values.map((v) => normalizeAnswerText(String(v)))
  const numsIn = extractNumbers(norm)

  for (const c of candidates) {
    if (norm === c) return true
    // 允许多写单位：输入「60只」对答案「60」
    const cNums = extractNumbers(c)
    if (cNums.length === 1 && numsIn.length === 1 && cNums[0] === numsIn[0]) {
      return true
    }
    // 答案带单位时，纯数字也对
    if (cNums.length === 1 && norm === cNums[0]) return true
  }

  if (blank.aliases?.length) {
    for (const a of blank.aliases) {
      if (norm === normalizeAnswerText(a)) return true
    }
  }
  return false
}

export function gradeAnswerKey(
  key: AnswerKey,
  inputs: string[],
): { correct: boolean; detail: boolean[] } {
  if (key.type === 'exact') {
    const blank: AnswerBlank = { values: key.values, aliases: key.aliases }
    const ok = blankMatches(inputs[0] ?? '', blank)
    return { correct: ok, detail: [ok] }
  }

  if (key.type === 'number') {
    const blank: AnswerBlank = { values: key.values, aliases: key.aliases }
    const ok = blankMatches(inputs[0] ?? '', blank)
    return { correct: ok, detail: [ok] }
  }

  if (key.type === 'remainder' || key.type === 'blanks') {
    const detail = key.blanks.map((b, i) => blankMatches(inputs[i] ?? '', b))
    // remainder：也尝试从单框整串解析「13……1」
    if (key.type === 'remainder' && detail.some((d) => !d) && inputs.length === 1) {
      const nums = extractNumbers(inputs[0] ?? '')
      if (nums.length >= 2) {
        const d0 = blankMatches(nums[0], key.blanks[0])
        const d1 = blankMatches(nums[1], key.blanks[1])
        return { correct: d0 && d1, detail: [d0, d1] }
      }
    }
    return { correct: detail.every(Boolean), detail }
  }

  return { correct: false, detail: [] }
}

export function emptyInputsForKey(key: AnswerKey | undefined): string[] {
  if (!key) return ['']
  if (key.type === 'blanks' || key.type === 'remainder') {
    return key.blanks.map(() => '')
  }
  return ['']
}

export function exerciseHasAutoGrade(ex: Exercise | null | undefined): boolean {
  return Boolean(ex?.answerKey)
}
