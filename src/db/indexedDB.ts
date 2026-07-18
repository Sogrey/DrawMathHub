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
const PBKDF2_ITERATIONS = 100_000
const SALT_BYTES = 16
const HASH_BITS = 256

let db: IDBPDatabase<DrawMathDBSchema> | null = null
let dbOpenError: Error | null = null

function toHex(bytes: ArrayBuffer | Uint8Array): string {
  const arr = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes)
  return Array.from(arr)
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('')
}

function fromHex(hex: string): Uint8Array {
  const out = new Uint8Array(hex.length / 2)
  for (let i = 0; i < out.length; i++) {
    out[i] = parseInt(hex.slice(i * 2, i * 2 + 2), 16)
  }
  return out
}

/** 常量时间比较两个等长 hex / 字符串 */
export function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false
  let diff = 0
  for (let i = 0; i < a.length; i++) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i)
  }
  return diff === 0
}

function isLegacySha256Hash(stored: string): boolean {
  return /^[0-9a-f]{64}$/i.test(stored)
}

function isPbkdf2Hash(stored: string): boolean {
  return stored.startsWith('pbkdf2$')
}

async function sha256Hex(password: string): Promise<string> {
  const data = new TextEncoder().encode(password)
  const hash = await crypto.subtle.digest('SHA-256', data)
  return toHex(hash)
}

async function pbkdf2Hex(password: string, salt: Uint8Array, iterations: number): Promise<string> {
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(password),
    'PBKDF2',
    false,
    ['deriveBits'],
  )
  const saltCopy = new Uint8Array(salt.length)
  saltCopy.set(salt)
  const bits = await crypto.subtle.deriveBits(
    {
      name: 'PBKDF2',
      salt: saltCopy,
      iterations,
      hash: 'SHA-256',
    },
    keyMaterial,
    HASH_BITS,
  )
  return toHex(bits)
}

/** 新密码：PBKDF2 + 随机盐，格式 pbkdf2$iter$saltHex$hashHex */
export async function hashPassword(password: string): Promise<string> {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_BYTES))
  const hash = await pbkdf2Hex(password, salt, PBKDF2_ITERATIONS)
  return `pbkdf2$${PBKDF2_ITERATIONS}$${toHex(salt)}$${hash}`
}

/**
 * 校验密码；若为旧版无盐 SHA-256 且匹配，则升级为 PBKDF2 并写回。
 */
export async function verifyPassword(
  nickname: string,
  password: string,
  storedHash: string,
): Promise<boolean> {
  if (isPbkdf2Hash(storedHash)) {
    const parts = storedHash.split('$')
    if (parts.length !== 4) return false
    const iterations = Number(parts[1])
    const saltHex = parts[2]
    const expected = parts[3]
    if (!iterations || !saltHex || !expected) return false
    const actual = await pbkdf2Hex(password, fromHex(saltHex), iterations)
    return timingSafeEqual(actual.toLowerCase(), expected.toLowerCase())
  }

  if (isLegacySha256Hash(storedHash)) {
    const legacy = await sha256Hex(password)
    if (!timingSafeEqual(legacy.toLowerCase(), storedHash.toLowerCase())) {
      return false
    }
    // 透明迁移
    const upgraded = await hashPassword(password)
    const database = await getDB()
    const user = await database.get('users', nickname)
    if (user) {
      user.passwordHash = upgraded
      await database.put('users', user)
    }
    return true
  }

  return false
}

export function getDbOpenError(): Error | null {
  return dbOpenError
}

export async function getDB(): Promise<IDBPDatabase<DrawMathDBSchema>> {
  if (db) return db
  try {
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
      },
    })
    dbOpenError = null
    return db
  } catch (e) {
    dbOpenError = e instanceof Error ? e : new Error(String(e))
    throw dbOpenError
  }
}

export async function createUser(nickname: string, password?: string): Promise<User> {
  const database = await getDB()
  const passwordHash = password ? await hashPassword(password) : null
  const now = Date.now()

  const user: User = {
    nickname,
    passwordHash,
    createdAt: now,
    lastLoginAt: now,
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
  const tx = database.transaction('progress', 'readwrite')
  await Promise.all([
    ...progresses.map((p) => tx.store.delete(p.id)),
    tx.done,
  ])
}

export function generateProgressId(nickname: string, problemId: number): string {
  return `${nickname}#${problemId}`
}

export async function getProgress(
  nickname: string,
  problemId: number,
): Promise<ProgressRecord | undefined> {
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

export async function getOrCreateProgress(
  nickname: string,
  problemId: number,
): Promise<ProgressRecord> {
  const existing = await getProgress(nickname, problemId)
  if (existing) return existing

  const newRecord: ProgressRecord = {
    id: generateProgressId(nickname, problemId),
    nickname,
    problemId,
    learned: false,
    practiceCount: 0,
    correctCount: 0,
    lastPracticeTime: 0,
  }

  await saveProgress(newRecord)
  return newRecord
}
