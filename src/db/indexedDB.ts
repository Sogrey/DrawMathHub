import { openDB, type DBSchema, type IDBPDatabase } from 'idb'

export interface User {
  nickname: string
  passwordHash: string | null
  createdAt: number
  lastLoginAt: number
}

export interface ProgressRecord {
  id: string
  nickname: string
  problemId: number
  learned: boolean
  practiceCount: number
  correctCount: number
  lastPracticeTime: number
}

interface DrawMathDBSchema extends DBSchema {
  users: {
    key: string
    value: User
    indexes: {
      'by-nickname': string
    }
  }
  progress: {
    key: string
    value: ProgressRecord
    indexes: {
      'by-nickname': string
      'by-problem': [string, number]
    }
  }
}

const DB_NAME = 'DrawMathDB'
const DB_VERSION = 1

let db: IDBPDatabase<DrawMathDBSchema> | null = null

export async function getDB(): Promise<IDBPDatabase<DrawMathDBSchema>> {
  if (db) return db
  
  db = await openDB<DrawMathDBSchema>(DB_NAME, DB_VERSION, {
    upgrade(database) {
      if (!database.objectStoreNames.contains('users')) {
        const userStore = database.createObjectStore('users', { keyPath: 'nickname' })
        userStore.createIndex('by-nickname', 'nickname')
      }
      
      if (!database.objectStoreNames.contains('progress')) {
        const progressStore = database.createObjectStore('progress', { keyPath: 'id' })
        progressStore.createIndex('by-nickname', 'nickname')
        progressStore.createIndex('by-problem', ['nickname', 'problemId'])
      }
    }
  })
  
  return db
}

export async function hashPassword(password: string): Promise<string> {
  const encoder = new TextEncoder()
  const data = encoder.encode(password)
  const hash = await crypto.subtle.digest('SHA-256', data)
  return Array.from(new Uint8Array(hash))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')
}

export async function createUser(nickname: string, password?: string): Promise<User> {
  const database = await getDB()
  const passwordHash = password ? await hashPassword(password) : null
  const now = Date.now()
  
  const user: User = {
    nickname,
    passwordHash,
    createdAt: now,
    lastLoginAt: now
  }
  
  await database.put('users', user)
  return user
}

export async function getUser(nickname: string): Promise<User | undefined> {
  const database = await getDB()
  return database.get('users', nickname)
}

export async function getAllUsers(): Promise<User[]> {
  const database = await getDB()
  return database.getAll('users')
}

export async function updateUserLastLogin(nickname: string): Promise<void> {
  const database = await getDB()
  const user = await database.get('users', nickname)
  if (user) {
    user.lastLoginAt = Date.now()
    await database.put('users', user)
  }
}

export async function updateUserPassword(nickname: string, newPassword: string): Promise<void> {
  const database = await getDB()
  const user = await database.get('users', nickname)
  if (user) {
    user.passwordHash = await hashPassword(newPassword)
    await database.put('users', user)
  }
}

export async function deleteUser(nickname: string): Promise<void> {
  const database = await getDB()
  await database.delete('users', nickname)
  
  const progresses = await database.getAllFromIndex('progress', 'by-nickname', nickname)
  for (const progress of progresses) {
    await database.delete('progress', progress.id)
  }
}

export function generateProgressId(nickname: string, problemId: number): string {
  return `${nickname}#${problemId}`
}

export async function getProgress(nickname: string, problemId: number): Promise<ProgressRecord | undefined> {
  const database = await getDB()
  const id = generateProgressId(nickname, problemId)
  return database.get('progress', id)
}

export async function getAllProgress(nickname: string): Promise<ProgressRecord[]> {
  const database = await getDB()
  return database.getAllFromIndex('progress', 'by-nickname', nickname)
}

export async function saveProgress(record: ProgressRecord): Promise<void> {
  const database = await getDB()
  await database.put('progress', record)
}

export async function deleteProgress(nickname: string, problemId: number): Promise<void> {
  const database = await getDB()
  const id = generateProgressId(nickname, problemId)
  await database.delete('progress', id)
}

export async function getOrCreateProgress(nickname: string, problemId: number): Promise<ProgressRecord> {
  const existing = await getProgress(nickname, problemId)
  if (existing) return existing
  
  const newRecord: ProgressRecord = {
    id: generateProgressId(nickname, problemId),
    nickname,
    problemId,
    learned: false,
    practiceCount: 0,
    correctCount: 0,
    lastPracticeTime: 0
  }
  
  await saveProgress(newRecord)
  return newRecord
}
