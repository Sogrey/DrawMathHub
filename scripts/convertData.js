import * as fs from 'fs'
import * as path from 'path'
import { randomUUID } from 'crypto'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

const inputFile = path.join(__dirname, '../datas/draw_math_all_lessons.json')
const outputDir = path.join(__dirname, '../public/data/problems')

const rawData = fs.readFileSync(inputFile, 'utf-8')
const lessons = JSON.parse(rawData)

let sourceUpdated = false

function ensureId(value) {
  if (value && typeof value === 'string' && value.length > 0) return value
  sourceUpdated = true
  return randomUUID()
}

lessons.forEach(lesson => {
  lesson.id = ensureId(lesson.id)
  lesson.mainExampleId = ensureId(lesson.mainExampleId)

  const extensions = lesson['举一反三']
  if (Array.isArray(extensions)) {
    extensions.forEach(ep => {
      ep.id = ensureId(ep.id)
    })
  }
})

if (sourceUpdated) {
  fs.writeFileSync(inputFile, JSON.stringify(lessons, null, 2), 'utf-8')
  console.log(`Updated UUIDs in source: ${inputFile}`)
}

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true })
}

const convertedProblems = []

lessons.forEach((lesson, index) => {
  const lessonNumber = index + 1
  const main = lesson['母题精讲']

  const converted = {
    id: lesson.id,
    lessonNumber,
    lesson: lesson['讲次'],
    title: lesson['题型'],
    method: lesson['画图法'],
    methodType: lesson['画图法'],
    problemIdentification: lesson['问题识别'],
    mainProblem: {
      id: lesson.mainExampleId,
      originalQuestion: main['考试原型题'],
      drawingAnalysis: main['画图分析'],
      standardSolution: main['规范解答'],
      keyPoints: main['关键点拨'],
    },
    extensionProblems: (lesson['举一反三'] || []).map(ep => ({
      id: ep.id,
      difficulty: ep['难度'],
      question: ep['题目'],
      hint: ep['提示'],
    })),
    exercises: (lesson['练习册'] || []).map(ex => ({
      difficulty: ex['难度'],
      question: ex['题目'],
    })),
  }

  convertedProblems.push(converted)

  const outputFile = path.join(outputDir, `${lessonNumber}.json`)
  fs.writeFileSync(outputFile, JSON.stringify(converted, null, 2), 'utf-8')
  console.log(`Generated: ${outputFile}`)
})

const indexFile = path.join(outputDir, 'index.json')
fs.writeFileSync(indexFile, JSON.stringify(convertedProblems, null, 2), 'utf-8')
console.log(`Generated index file: ${indexFile}`)

console.log('\nConversion completed!')
console.log(`Total problems: ${convertedProblems.length}`)
