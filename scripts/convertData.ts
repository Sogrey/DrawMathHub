import * as fs from 'fs'
import * as path from 'path'
import { randomUUID } from 'crypto'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

const inputFile = path.join(__dirname, '../datas/draw_math_all_lessons.json')
const outputDir = path.join(__dirname, '../public/data/problems')

interface OriginalExtension {
  id?: string
  难度: string
  题目: string
  提示?: string
}

interface OriginalLesson {
  id?: string
  mainExampleId?: string
  讲次: string
  题型: string
  画图法: string
  问题识别: string
  母题精讲: {
    考试原型题: string
    画图分析: string
    规范解答: string
    关键点拨: string
  }
  举一反三: OriginalExtension[]
  练习册: { 难度: string; 题目: string }[]
}

const rawData = fs.readFileSync(inputFile, 'utf-8')
const lessons = JSON.parse(rawData) as OriginalLesson[]

let sourceUpdated = false

function ensureId(value?: string): string {
  if (value && value.length > 0) return value
  sourceUpdated = true
  return randomUUID()
}

lessons.forEach(lesson => {
  lesson.id = ensureId(lesson.id)
  lesson.mainExampleId = ensureId(lesson.mainExampleId)
  lesson['举一反三']?.forEach(ep => {
    ep.id = ensureId(ep.id)
  })
})

if (sourceUpdated) {
  fs.writeFileSync(inputFile, JSON.stringify(lessons, null, 2), 'utf-8')
}

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true })
}

const convertedProblems = lessons.map((lesson, index) => {
  const lessonNumber = index + 1
  const main = lesson['母题精讲']
  return {
    id: lesson.id!,
    lessonNumber,
    lesson: lesson['讲次'],
    title: lesson['题型'],
    method: lesson['画图法'],
    methodType: lesson['画图法'],
    problemIdentification: lesson['问题识别'],
    mainProblem: {
      id: lesson.mainExampleId!,
      originalQuestion: main['考试原型题'],
      drawingAnalysis: main['画图分析'],
      standardSolution: main['规范解答'],
      keyPoints: main['关键点拨'],
    },
    extensionProblems: (lesson['举一反三'] || []).map(ep => ({
      id: ep.id!,
      difficulty: ep['难度'],
      question: ep['题目'],
      hint: ep['提示'],
    })),
    exercises: (lesson['练习册'] || []).map(ex => ({
      difficulty: ex['难度'],
      question: ex['题目'],
    })),
  }
})

convertedProblems.forEach((problem, index) => {
  const outputFile = path.join(outputDir, `${index + 1}.json`)
  fs.writeFileSync(outputFile, JSON.stringify(problem, null, 2), 'utf-8')
})

fs.writeFileSync(path.join(outputDir, 'index.json'), JSON.stringify(convertedProblems, null, 2), 'utf-8')
console.log(`Converted ${convertedProblems.length} problems`)
