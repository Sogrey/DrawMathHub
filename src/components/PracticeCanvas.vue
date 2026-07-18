<template>
  <div class="w-full h-full flex flex-col" tabindex="0" @keydown="onKeyDown">
    <div class="flex gap-2 mb-4">
      <button
        v-for="tool in tools"
        :key="tool.id"
        class="p-2 rounded-lg transition-colors"
        :class="currentTool === tool.id ? 'bg-primaryDark text-accentCream' : 'glass-card text-textSecondary hover:bg-primary/10'"
        @click="currentTool = tool.id"
      >
        <component :is="tool.icon" :size="20" />
      </button>
      <div class="flex-1"></div>
      <div class="flex items-center gap-2">
        <input
          type="color"
          v-model="currentColor"
          class="w-8 h-8 rounded-lg cursor-pointer"
        />
        <div class="flex items-center gap-1">
          <button
            class="px-2 py-1 rounded text-sm"
            :class="currentSize === 2 ? 'bg-primaryDark text-accentCream' : 'glass-card text-textSecondary'"
            @click="currentSize = 2"
          >2px</button>
          <button
            class="px-2 py-1 rounded text-sm"
            :class="currentSize === 4 ? 'bg-primaryDark text-accentCream' : 'glass-card text-textSecondary'"
            @click="currentSize = 4"
          >4px</button>
          <button
            class="px-2 py-1 rounded text-sm"
            :class="currentSize === 6 ? 'bg-primaryDark text-accentCream' : 'glass-card text-textSecondary'"
            @click="currentSize = 6"
          >6px</button>
        </div>
        <button
          type="button"
          class="p-2 rounded-lg glass-card text-textSecondary hover:bg-primary/10 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          title="撤销 (Ctrl+Z)"
          :disabled="actions.length === 0"
          @click="undo"
        >
          <Undo2 :size="20" />
        </button>
        <button
          type="button"
          class="p-2 rounded-lg glass-card text-textSecondary hover:bg-primary/10 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          title="重做 (Ctrl+Shift+Z)"
          :disabled="redoStack.length === 0"
          @click="redo"
        >
          <Redo2 :size="20" />
        </button>
        <button
          class="p-2 rounded-lg bg-danger/10 text-danger hover:bg-danger/20 transition-colors"
          @click="clearCanvas"
        >
          <Trash2 :size="20" />
        </button>
      </div>
    </div>
    <div ref="canvasContainer" class="flex-1 glass-card rounded-lg border-2 border-dashed border-primary/20 overflow-hidden relative">
      <canvas
        ref="canvas"
        class="absolute inset-0 w-full h-full cursor-crosshair touch-none"
        @pointerdown="handlePointerDown"
        @pointermove="handlePointerMove"
        @pointerup="handlePointerUp"
        @pointercancel="handlePointerUp"
        @pointerleave="handlePointerUp"
      ></canvas>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Pencil, Eraser, Circle as CircleIcon, Square, Trash2, Undo2, Redo2 } from '@lucide/vue'

const tools = [
  { id: 'pencil', icon: Pencil },
  { id: 'eraser', icon: Eraser },
  { id: 'circle', icon: CircleIcon },
  { id: 'rect', icon: Square },
]

const currentTool = ref('pencil')
const currentColor = ref('#C9563A')
const currentSize = ref(4)
const isDrawing = ref(false)
const startPoint = ref<{ x: number; y: number } | null>(null)
const currentPath = ref<{ x: number; y: number }[]>([])
const activePointerId = ref<number | null>(null)

const canvas = ref<HTMLCanvasElement | null>(null)
const canvasContainer = ref<HTMLElement | null>(null)
let ctx: CanvasRenderingContext2D | null = null

interface DrawAction {
  type: 'line' | 'circle' | 'rect'
  color: string
  size: number
  points: { x: number; y: number }[]
}

const actions = ref<DrawAction[]>([])
const redoStack = ref<DrawAction[]>([])

function pushAction(action: DrawAction) {
  actions.value.push(action)
  redoStack.value = []
}

function undo() {
  const last = actions.value.pop()
  if (!last) return
  redoStack.value.push(last)
  redrawCanvas()
}

function redo() {
  const next = redoStack.value.pop()
  if (!next) return
  actions.value.push(next)
  redrawCanvas()
}

function onKeyDown(e: KeyboardEvent) {
  const mod = e.ctrlKey || e.metaKey
  if (!mod) return
  const key = e.key.toLowerCase()
  if (key === 'z' && e.shiftKey) {
    e.preventDefault()
    redo()
  } else if (key === 'z') {
    e.preventDefault()
    undo()
  } else if (key === 'y') {
    e.preventDefault()
    redo()
  }
}

function updateCanvasSize() {
  if (!canvas.value || !canvasContainer.value) return
  const rect = canvasContainer.value.getBoundingClientRect()
  const dpr = window.devicePixelRatio || 1
  canvas.value.width = rect.width * dpr
  canvas.value.height = rect.height * dpr
  ctx = canvas.value.getContext('2d')
  if (ctx) {
    ctx.scale(dpr, dpr)
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
  }
  redrawCanvas()
}

function redrawCanvas() {
  if (!ctx || !canvas.value || !canvasContainer.value) return
  const rect = canvasContainer.value.getBoundingClientRect()
  ctx.clearRect(0, 0, rect.width, rect.height)

  actions.value.forEach((action) => {
    ctx!.strokeStyle = action.color
    ctx!.lineWidth = action.size

    if (action.type === 'line') {
      ctx!.beginPath()
      ctx!.moveTo(action.points[0].x, action.points[0].y)
      for (let i = 1; i < action.points.length; i++) {
        ctx!.lineTo(action.points[i].x, action.points[i].y)
      }
      ctx!.stroke()
    } else if (action.type === 'circle') {
      const center = action.points[0]
      const end = action.points[1]
      const radius = Math.sqrt(
        Math.pow(end.x - center.x, 2) + Math.pow(end.y - center.y, 2),
      )
      ctx!.beginPath()
      ctx!.arc(center.x, center.y, radius, 0, Math.PI * 2)
      ctx!.stroke()
    } else if (action.type === 'rect') {
      const start = action.points[0]
      const end = action.points[1]
      ctx!.strokeRect(start.x, start.y, end.x - start.x, end.y - start.y)
    }
  })

  if (isDrawing.value && currentPath.value.length > 1) {
    const color = currentTool.value === 'eraser' ? '#292C30' : currentColor.value
    const size = currentTool.value === 'eraser' ? currentSize.value * 3 : currentSize.value

    ctx!.strokeStyle = color
    ctx!.lineWidth = size
    ctx!.beginPath()
    ctx!.moveTo(currentPath.value[0].x, currentPath.value[0].y)
    for (let i = 1; i < currentPath.value.length; i++) {
      ctx!.lineTo(currentPath.value[i].x, currentPath.value[i].y)
    }
    ctx!.stroke()
  }
}

function getPoint(e: PointerEvent): { x: number; y: number } {
  if (!canvas.value || !canvasContainer.value) return { x: 0, y: 0 }
  const rect = canvasContainer.value.getBoundingClientRect()
  return {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top,
  }
}

function handlePointerDown(e: PointerEvent) {
  if (!canvas.value) return
  e.preventDefault()
  activePointerId.value = e.pointerId
  canvas.value.setPointerCapture(e.pointerId)
  isDrawing.value = true
  const point = getPoint(e)
  startPoint.value = point
  currentPath.value = [point]
}

function handlePointerMove(e: PointerEvent) {
  if (!isDrawing.value || e.pointerId !== activePointerId.value) return
  e.preventDefault()
  const point = getPoint(e)
  currentPath.value.push(point)
  redrawCanvas()
}

function handlePointerUp(e: PointerEvent) {
  if (e.pointerId !== activePointerId.value && activePointerId.value !== null) return
  if (!isDrawing.value) return
  isDrawing.value = false
  activePointerId.value = null

  try {
    if (canvas.value?.hasPointerCapture(e.pointerId)) {
      canvas.value.releasePointerCapture(e.pointerId)
    }
  } catch {
    /* ignore */
  }

  if (currentPath.value.length >= 2) {
    const color = currentTool.value === 'eraser' ? '#292C30' : currentColor.value
    const size = currentTool.value === 'eraser' ? currentSize.value * 3 : currentSize.value

    if (currentTool.value === 'pencil' || currentTool.value === 'eraser') {
      pushAction({
        type: 'line',
        color,
        size,
        points: [...currentPath.value],
      })
    } else if (currentTool.value === 'circle' && startPoint.value) {
      pushAction({
        type: 'circle',
        color: currentColor.value,
        size: currentSize.value,
        points: [startPoint.value, currentPath.value[currentPath.value.length - 1]],
      })
    } else if (currentTool.value === 'rect' && startPoint.value) {
      pushAction({
        type: 'rect',
        color: currentColor.value,
        size: currentSize.value,
        points: [startPoint.value, currentPath.value[currentPath.value.length - 1]],
      })
    }
  }

  currentPath.value = []
  startPoint.value = null
  redrawCanvas()
}

function clearCanvas() {
  actions.value = []
  redoStack.value = []
  redrawCanvas()
}

onMounted(() => {
  updateCanvasSize()
  window.addEventListener('resize', updateCanvasSize)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateCanvasSize)
})

watch(canvasContainer, () => {
  setTimeout(updateCanvasSize, 100)
})
</script>
