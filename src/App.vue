<template>
  <div class="min-h-screen bg-background">
    <router-view />
    <Teleport to="body">
      <Transition name="app-toast">
        <div
          v-if="appErrorToast"
          class="app-error-toast"
          role="alert"
          @click="clearAppErrorToast"
        >
          {{ appErrorToast }}
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { appErrorToast, clearAppErrorToast } from '@/utils/appErrorToast'
</script>

<style scoped>
.app-error-toast {
  position: fixed;
  z-index: 200;
  left: 50%;
  bottom: 1.5rem;
  transform: translateX(-50%);
  max-width: min(90vw, 28rem);
  padding: 0.75rem 1.1rem;
  border-radius: 0.75rem;
  background: rgba(40, 28, 24, 0.94);
  border: 1px solid rgba(240, 168, 152, 0.35);
  color: #f0a898;
  font-size: 0.875rem;
  line-height: 1.4;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
  cursor: pointer;
}

.app-toast-enter-active,
.app-toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.app-toast-enter-from,
.app-toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(0.5rem);
}
</style>
