<template>
  <div class="min-h-screen bg-background flex flex-col items-center justify-center px-4">
    <p class="text-6xl font-bold text-primaryDark mb-4">404</p>
    <p class="text-textSecondary mb-8">页面不存在或链接已失效</p>
    <RouterLink
      to="/"
      class="px-6 py-3 rounded-button bg-primaryDark text-accentCream font-medium hover:opacity-90"
    >
      返回首页
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
