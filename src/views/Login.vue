<template>
  <div class="min-h-screen bg-background flex items-center justify-center p-4">
    <div class="w-full max-w-lg">
      <div class="text-center mb-8">
        <div class="text-6xl mb-4">🎨</div>
        <h1 class="text-title-lg font-bold text-text mb-2">欢迎来到数学乐园</h1>
        <p class="text-textTertiary">选择你的昵称开始学习吧！</p>
      </div>

      <div v-if="showCreateForm" class="glass-card rounded-card p-6 shadow-elevation border border-border mb-6">
        <h2 class="text-lg font-bold text-text mb-4 text-center">创建新昵称</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-textTertiary mb-1">昵称</label>
            <input
              v-model="newNickname"
              type="text"
              placeholder="请输入昵称"
              class="w-full px-4 py-3 rounded-button border-2 border-border focus:border-primary focus:outline-none transition-colors glass-card-secondary text-text"
              maxlength="20"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-textTertiary mb-1">密码（可选）</label>
            <input
              v-model="newPassword"
              type="password"
              placeholder="设置密码保护你的学习记录（可不填）"
              class="w-full px-4 py-3 rounded-button border-2 border-border focus:border-primary focus:outline-none transition-colors glass-card-secondary text-text"
            />
          </div>
          <div class="flex gap-3">
            <button
              @click="cancelCreate"
              class="flex-1 px-4 py-3 rounded-button text-textTertiary hover:glass-card-secondary transition-colors border border-border"
            >
              取消
            </button>
            <button
              @click="submitCreate"
              :disabled="!newNickname || isLoading"
              class="flex-1 px-4 py-3 rounded-button bg-primary text-white font-medium hover:bg-primaryDark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isLoading ? '创建中...' : '创建' }}
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4 mb-6">
        <div
          v-for="user in userStore.users"
          :key="user.nickname"
          @click="handleUserClick(user)"
          class="glass-card rounded-card p-4 shadow-elevation cursor-pointer hover:shadow-elevation-hover hover:glass-card-hover border border-border transition-all duration-200"
        >
          <div class="text-center">
            <div class="text-4xl mb-2">{{ getUserAvatar(user.nickname) }}</div>
            <div class="font-bold text-text">{{ user.nickname }}</div>
            <div class="text-caption text-textTertiary mt-1">
              {{ user.passwordHash ? '🔒 已加密' : '🔓 公开' }}
            </div>
          </div>
        </div>

        <div
          @click="showCreateForm = true"
          class="glass-card-secondary rounded-card p-4 shadow-elevation cursor-pointer hover:shadow-elevation-hover hover:glass-card-hover border-2 border-dashed border-primary/30 hover:border-primary transition-all duration-200"
        >
          <div class="text-center h-full flex flex-col items-center justify-center">
            <div class="text-4xl mb-2">+</div>
            <div class="font-bold text-primary">新建昵称</div>
          </div>
        </div>
      </div>

      <div v-if="userStore.users.length === 0 && !showCreateForm" class="text-center text-textTertiary">
        <p>还没有昵称，点击上方卡片创建吧！</p>
      </div>
    </div>

    <div
      v-if="showPasswordModal"
      class="fixed inset-0 bg-black/30 flex items-center justify-center p-4 z-50"
      @click.self="closePasswordModal"
    >
      <div class="glass-card rounded-card p-6 shadow-elevation border border-border w-full max-w-sm">
        <h2 class="text-lg font-bold text-text mb-2 text-center">请输入密码</h2>
        <p class="text-textTertiary text-sm text-center mb-4">昵称 "{{ passwordModalNickname }}" 需要密码验证</p>
        <div class="space-y-4">
          <input
            v-model="passwordInput"
            type="password"
            placeholder="输入密码"
            class="w-full px-4 py-3 rounded-button border-2 border-border focus:border-primary focus:outline-none transition-colors glass-card-secondary text-text"
            @keyup.enter="submitPassword"
          />
          <div v-if="passwordError" class="text-dangerText text-sm text-center">
            {{ passwordError }}
          </div>
          <div class="flex gap-3">
            <button
              @click="closePasswordModal"
              class="flex-1 px-4 py-3 rounded-button text-textTertiary hover:glass-card-secondary transition-colors border border-border"
            >
              取消
            </button>
            <button
              @click="submitPassword"
              :disabled="!passwordInput || isLoading"
              class="flex-1 px-4 py-3 rounded-button bg-primary text-white font-medium hover:bg-primaryDark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isLoading ? '验证中...' : '登录' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import type { User } from '@/db/indexedDB'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

function resolveRedirect(): string {
  const redirect = route.query.redirect
  if (typeof redirect === 'string' && redirect.startsWith('/')) {
    return redirect
  }
  return '/'
}

const showCreateForm = ref(false)
const newNickname = ref('')
const newPassword = ref('')
const showPasswordModal = ref(false)
const passwordModalNickname = ref('')
const passwordInput = ref('')
const passwordError = ref('')

const isLoading = ref(false)

const avatars = ['🐶', '🐱', '🐼', '🐨', '🦊', '🦁', '🐯', '🐮', '🐷', '🐸', '🐵', '🐰']

function getUserAvatar(nickname: string): string {
  let hash = 0
  for (let i = 0; i < nickname.length; i++) {
    hash = nickname.charCodeAt(i) + ((hash << 5) - hash)
  }
  return avatars[Math.abs(hash) % avatars.length]
}

function handleUserClick(user: User) {
  if (user.passwordHash) {
    passwordModalNickname.value = user.nickname
    passwordInput.value = ''
    passwordError.value = ''
    showPasswordModal.value = true
  } else {
    doLogin(user.nickname)
  }
}

async function doLogin(nickname: string, password?: string) {
  isLoading.value = true
  passwordError.value = ''
  try {
    const success = await userStore.login(nickname, password)
    if (success) {
      await userStore.migrateFromLocalStorage()
      router.replace(resolveRedirect())
    } else {
      passwordError.value = '登录失败，请检查昵称或密码'
    }
  } finally {
    isLoading.value = false
  }
}

async function submitPassword() {
  await doLogin(passwordModalNickname.value, passwordInput.value)
}

function closePasswordModal() {
  showPasswordModal.value = false
  passwordInput.value = ''
  passwordError.value = ''
}

function cancelCreate() {
  showCreateForm.value = false
  newNickname.value = ''
  newPassword.value = ''
}

async function submitCreate() {
  if (!newNickname.value.trim()) return
  
  isLoading.value = true
  try {
    const user = await userStore.createUserWithNickname(
      newNickname.value.trim(),
      newPassword.value || undefined
    )
    if (user) {
      await userStore.migrateFromLocalStorage()
      router.replace(resolveRedirect())
    } else {
      alert('该昵称已存在，请选择其他昵称')
    }
  } finally {
    isLoading.value = false
  }
}

watch(() => userStore.isAuthenticated, (authenticated) => {
  if (authenticated && route.name === 'Login') {
    router.replace(resolveRedirect())
  }
})

onMounted(() => {
  userStore.loadUsers()
})
</script>
