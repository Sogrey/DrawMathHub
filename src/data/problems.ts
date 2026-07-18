export interface MainProblem {
  id: string
  originalQuestion: string
  drawingAnalysis: string
  standardSolution: string
  keyPoints: string
}

export interface ExtensionProblem {
  id: string
  difficulty: string
  question: string
  hint?: string
  /** 参考答案，仅供对照，不做正误判定 */
  answer?: string
}

/** 单个填空的可接受值 */
export interface AnswerBlank {
  values: string[]
  /** 额外等价写法（如「小奇」「奇奇」） */
  aliases?: string[]
  /** 展示用前置文案，如「鸡有」 */
  prefix?: string
  /** 展示用后置文案，如「只」 */
  suffix?: string
}

/**
 * 自动判分键。无此字段则只展示参考答案。
 * - number: 单数字（单位可有可无）
 * - blanks: 多空，按序全对
 * - remainder: 商······余数 两空
 * - exact: 短文本精确/别名匹配
 */
export type AnswerKey =
  | { type: 'number'; values: string[]; aliases?: string[] }
  | { type: 'blanks'; blanks: AnswerBlank[]; template?: string }
  | { type: 'remainder'; blanks: AnswerBlank[] }
  | { type: 'exact'; values: string[]; aliases?: string[] }

export interface Exercise {
  difficulty: string
  question: string
  /** 完整参考答案文案（折叠展示） */
  answer?: string
  /** 结构化判分；缺失则不自动判 */
  answerKey?: AnswerKey
}

export interface Problem {
  /** 平台唯一 uuid，视频路径等稳定引用 */
  id: string
  /** 讲次序号，用于路由与学习进度 */
  lessonNumber: number
  lesson: string
  title: string
  method: string
  methodType: string
  problemIdentification: string
  mainProblem: MainProblem
  extensionProblems: ExtensionProblem[]
  exercises: Exercise[]
}

export interface LearningProgress {
  problemId: number
  learned: boolean
  practiceCount: number
  correctCount: number
  lastPracticeTime: number
}

export const methodTypes = [
  '图示法',
  '列表法',
  '画线法',
  '连线法',
  '线段图法',
  '竖式法',
  '树状图法',
  '倒推法',
  '逆推法',
  '年龄轴法',
  '假设法',
  '打包法',
  '流程图法',
  '移多补少法',
  '插旗法',
  '十字交叉法',
  '天平法',
  '韦恩图法'
]

import { publicUrl, fetchJson } from '@/utils/publicUrl'

export async function loadProblem(lessonNumber: number): Promise<Problem | null> {
  return fetchJson<Problem | null>(
    publicUrl(`data/problems/${lessonNumber}.json`),
    null,
  )
}

export async function loadAllProblems(): Promise<Problem[]> {
  return fetchJson<Problem[]>(publicUrl('data/problems/index.json'), [])
}
