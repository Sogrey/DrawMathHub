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
}

export interface Exercise {
  difficulty: string
  question: string
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
