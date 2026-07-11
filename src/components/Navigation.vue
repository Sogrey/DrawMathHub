<template>
  <nav class="glass-nav border-b border-border shadow-elevation-nav sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <div class="flex items-center gap-3 cursor-pointer" @click="$router.push('/')">
          <div class="w-10 h-10 bg-primary/25 rounded-xl flex items-center justify-center border border-primary/30">
            <BookOpen class="text-accentCream" :size="24" />
          </div>
          <span class="text-accentCream font-bold text-xl">画图解题法</span>
        </div>
        <div v-if="showBack">
          <button
            class="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/10 text-accentCream hover:bg-white/15 transition-colors border border-border"
            @click="$router.push('/')"
          >
            <ArrowLeft :size="18" />
            <span>返回大厅</span>
          </button>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <div v-if="userStore.currentUser" class="flex items-center gap-2">
          <span class="text-textTertiary text-sm">欢迎，{{ userStore.currentUser.nickname }}</span>
          <button
            class="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-white/10 text-accentCream text-sm hover:bg-white/15 transition-colors border border-border"
            @click="handleLogout"
          >
            <LogOut :size="16" />
            <span>退出</span>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { BookOpen, ArrowLeft, LogOut } from '@lucide/vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

defineProps<{
  showBack?: boolean
}>()

const router = useRouter()
const userStore = useUserStore()

async function handleLogout() {
  await userStore.logout()
  router.push('/login')
}
</script>
