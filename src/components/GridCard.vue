<template>
  <div
    class="grid-card rounded-card p-5 shadow-elevation cursor-pointer transform transition-all duration-300 hover:scale-105 hover:shadow-elevation-hover border border-border overflow-hidden relative backdrop-blur-md"
    :style="{ backgroundColor: cardBgColor }"
    @click="$router.push(`/problem/${problem.lessonNumber}`)"
  >
    <svg class="absolute inset-0 w-full h-full opacity-20 pointer-events-none" viewBox="0 0 100 100">
      <g v-if="iconType === 'circles'">
        <circle cx="25" cy="50" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="50" cy="50" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="75" cy="50" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="37" cy="50" r="4" :fill="iconColor" opacity="0.3" />
        <circle cx="62" cy="50" r="4" :fill="iconColor" opacity="0.3" />
      </g>

      <g v-else-if="iconType === 'queue'">
        <rect x="15" y="35" width="12" height="30" :stroke="iconColor" stroke-width="3" fill="none" rx="2" />
        <rect x="32" y="35" width="12" height="30" :stroke="iconColor" stroke-width="3" fill="none" rx="2" />
        <rect x="49" y="35" width="12" height="30" :stroke="iconColor" stroke-width="3" fill="none" rx="2" />
        <rect x="66" y="35" width="12" height="30" :stroke="iconColor" stroke-width="3" fill="none" rx="2" />
        <circle cx="21" cy="28" r="6" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="38" cy="28" r="6" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="55" cy="28" r="6" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="72" cy="28" r="6" :stroke="iconColor" stroke-width="2" fill="none" />
      </g>

      <g v-else-if="iconType === 'balance'">
        <rect x="30" y="60" width="40" height="6" :stroke="iconColor" stroke-width="3" fill="none" />
        <line x1="50" y1="45" x2="50" y2="60" :stroke="iconColor" stroke-width="3" />
        <rect x="15" y="40" width="18" height="10" :stroke="iconColor" stroke-width="3" fill="none" rx="2" />
        <rect x="67" y="40" width="18" height="10" :stroke="iconColor" stroke-width="3" fill="none" rx="2" />
        <circle cx="24" cy="35" r="5" :fill="iconColor" opacity="0.3" />
        <circle cx="76" cy="35" r="5" :fill="iconColor" opacity="0.3" />
      </g>

      <g v-else-if="iconType === 'list'">
        <rect x="20" y="25" width="60" height="50" :stroke="iconColor" stroke-width="3" fill="none" />
        <line x1="20" y1="40" x2="80" y2="40" :stroke="iconColor" stroke-width="2" />
        <line x1="20" y1="50" x2="80" y2="50" :stroke="iconColor" stroke-width="2" />
        <line x1="20" y1="60" x2="80" y2="60" :stroke="iconColor" stroke-width="2" />
        <line x1="50" y1="25" x2="50" y2="75" :stroke="iconColor" stroke-width="2" />
      </g>

      <g v-else-if="iconType === 'line-link'">
        <circle cx="25" cy="35" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="75" cy="35" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="25" cy="65" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="75" cy="65" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <line x1="33" y1="35" x2="67" y2="35" :stroke="iconColor" stroke-width="3" />
        <line x1="33" y1="65" x2="67" y2="65" :stroke="iconColor" stroke-width="3" />
        <line x1="25" y1="43" x2="25" y2="57" :stroke="iconColor" stroke-width="3" />
        <line x1="75" y1="43" x2="75" y2="57" :stroke="iconColor" stroke-width="3" />
      </g>

      <g v-else-if="iconType === 'line-segment'">
        <line x1="15" y1="50" x2="85" y2="50" :stroke="iconColor" stroke-width="4" stroke-linecap="round" />
        <circle cx="15" cy="50" r="5" :fill="iconColor" opacity="0.6" />
        <circle cx="50" cy="50" r="5" :fill="iconColor" opacity="0.6" />
        <circle cx="85" cy="50" r="5" :fill="iconColor" opacity="0.6" />
        <rect x="30" y="42" width="20" height="16" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="60" y="42" width="25" height="16" :stroke="iconColor" stroke-width="3" fill="none" />
      </g>

      <g v-else-if="iconType === 'tree'">
        <line x1="50" y1="85" x2="50" y2="45" :stroke="iconColor" stroke-width="3" />
        <line x1="50" y1="45" x2="30" y2="25" :stroke="iconColor" stroke-width="3" />
        <line x1="50" y1="45" x2="70" y2="25" :stroke="iconColor" stroke-width="3" />
        <line x1="30" y1="25" x2="20" y2="10" :stroke="iconColor" stroke-width="2" />
        <line x1="30" y1="25" x2="40" y2="10" :stroke="iconColor" stroke-width="2" />
        <line x1="70" y1="25" x2="60" y2="10" :stroke="iconColor" stroke-width="2" />
        <line x1="70" y1="25" x2="80" y2="10" :stroke="iconColor" stroke-width="2" />
        <circle cx="50" cy="85" r="4" :fill="iconColor" />
      </g>

      <g v-else-if="iconType === 'arrow-back'">
        <line x1="70" y1="50" x2="30" y2="50" :stroke="iconColor" stroke-width="4" stroke-linecap="round" />
        <polygon points="30,50 42,43 42,57" :fill="iconColor" />
        <circle cx="70" cy="50" r="6" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="50" cy="50" r="6" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="30" cy="50" r="6" :fill="iconColor" opacity="0.3" />
      </g>

      <g v-else-if="iconType === 'time'">
        <circle cx="50" cy="50" r="25" :stroke="iconColor" stroke-width="3" fill="none" />
        <line x1="50" y1="30" x2="50" y2="70" :stroke="iconColor" stroke-width="2" />
        <line x1="30" y1="50" x2="70" y2="50" :stroke="iconColor" stroke-width="2" />
        <line x1="50" y1="50" x2="62" y2="38" :stroke="iconColor" stroke-width="3" stroke-linecap="round" />
        <circle cx="50" cy="50" r="3" :fill="iconColor" />
      </g>

      <g v-else-if="iconType === 'graph-bar'">
        <line x1="20" y1="75" x2="80" y2="75" :stroke="iconColor" stroke-width="3" />
        <line x1="20" y1="20" x2="20" y2="75" :stroke="iconColor" stroke-width="3" />
        <rect x="30" y="50" width="10" height="25" :stroke="iconColor" stroke-width="2" fill="none" />
        <rect x="45" y="40" width="10" height="35" :stroke="iconColor" stroke-width="2" fill="none" />
        <rect x="60" y="55" width="10" height="20" :stroke="iconColor" stroke-width="2" fill="none" />
        <rect x="75" y="30" width="10" height="45" :stroke="iconColor" stroke-width="2" fill="none" />
      </g>

      <g v-else-if="iconType === 'number-line'">
        <line x1="15" y1="50" x2="85" y2="50" :stroke="iconColor" stroke-width="4" stroke-linecap="round" />
        <line x1="15" y1="45" x2="15" y2="55" :stroke="iconColor" stroke-width="2" />
        <line x1="35" y1="45" x2="35" y2="55" :stroke="iconColor" stroke-width="2" />
        <line x1="55" y1="45" x2="55" y2="55" :stroke="iconColor" stroke-width="2" />
        <line x1="75" y1="45" x2="75" y2="55" :stroke="iconColor" stroke-width="2" />
        <line x1="85" y1="45" x2="85" y2="55" :stroke="iconColor" stroke-width="2" />
        <circle cx="55" cy="50" r="6" :fill="iconColor" opacity="0.5" />
      </g>

      <g v-else-if="iconType === 'coordinate'">
        <line x1="20" y1="80" x2="80" y2="80" :stroke="iconColor" stroke-width="3" />
        <line x1="20" y1="20" x2="20" y2="80" :stroke="iconColor" stroke-width="3" />
        <line x1="80" y1="78" x2="80" y2="82" :stroke="iconColor" stroke-width="2" />
        <line x1="18" y1="20" x2="22" y2="20" :stroke="iconColor" stroke-width="2" />
        <circle cx="45" cy="55" r="5" :fill="iconColor" />
        <circle cx="65" cy="35" r="5" :fill="iconColor" />
      </g>

      <g v-else-if="iconType === 'venn'">
        <circle cx="38" cy="50" r="22" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="62" cy="50" r="22" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="45" y="40" width="10" height="20" :stroke="iconColor" stroke-width="2" fill="none" />
      </g>

      <g v-else-if="iconType === 'flow'">
        <rect x="20" y="40" width="18" height="20" :stroke="iconColor" stroke-width="3" fill="none" rx="4" />
        <rect x="41" y="40" width="18" height="20" :stroke="iconColor" stroke-width="3" fill="none" rx="4" />
        <rect x="62" y="40" width="18" height="20" :stroke="iconColor" stroke-width="3" fill="none" rx="4" />
        <path d="M38,50 L41,50" :stroke="iconColor" stroke-width="3" />
        <path d="M59,50 L62,50" :stroke="iconColor" stroke-width="3" />
        <polygon points="41,50 35,46 35,54" :fill="iconColor" />
        <polygon points="62,50 56,46 56,54" :fill="iconColor" />
      </g>

      <g v-else-if="iconType === 'assume'">
        <circle cx="50" cy="50" r="20" :stroke="iconColor" stroke-width="3" fill="none" />
        <path d="M42,45 Q50,55 58,45" :stroke="iconColor" stroke-width="3" fill="none" />
        <path d="M50,55 L50,65" :stroke="iconColor" stroke-width="3" />
      </g>

      <g v-else-if="iconType === 'eliminate'">
        <circle cx="35" cy="40" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="65" cy="40" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="50" cy="60" r="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <line x1="27" y1="32" x2="43" y2="48" :stroke="iconColor" stroke-width="3" />
        <line x1="43" y1="32" x2="27" y2="48" :stroke="iconColor" stroke-width="3" />
      </g>

      <g v-else-if="iconType === 'enumerate'">
        <circle cx="30" cy="30" r="5" :fill="iconColor" opacity="0.6" />
        <circle cx="70" cy="30" r="5" :fill="iconColor" opacity="0.6" />
        <circle cx="30" cy="50" r="5" :fill="iconColor" opacity="0.6" />
        <circle cx="70" cy="50" r="5" :fill="iconColor" opacity="0.6" />
        <circle cx="30" cy="70" r="5" :fill="iconColor" opacity="0.6" />
        <circle cx="70" cy="70" r="5" :fill="iconColor" opacity="0.6" />
        <line x1="35" y1="30" x2="65" y2="30" :stroke="iconColor" stroke-width="2" stroke-dasharray="4" />
        <line x1="35" y1="50" x2="65" y2="50" :stroke="iconColor" stroke-width="2" stroke-dasharray="4" />
        <line x1="35" y1="70" x2="65" y2="70" :stroke="iconColor" stroke-width="2" stroke-dasharray="4" />
      </g>

      <g v-else-if="iconType === 'convert'">
        <rect x="20" y="40" width="18" height="20" :stroke="iconColor" stroke-width="3" fill="none" rx="3" />
        <rect x="62" y="40" width="18" height="20" :stroke="iconColor" stroke-width="3" fill="none" rx="3" />
        <path d="M38,50 L62,50" :stroke="iconColor" stroke-width="3" />
        <polygon points="62,50 54,45 54,55" :fill="iconColor" />
      </g>

      <g v-else-if="iconType === 'model'">
        <rect x="30" y="30" width="40" height="40" :stroke="iconColor" stroke-width="3" fill="none" rx="4" />
        <line x1="30" y1="50" x2="70" y2="50" :stroke="iconColor" stroke-width="2" />
        <line x1="50" y1="30" x2="50" y2="70" :stroke="iconColor" stroke-width="2" />
        <circle cx="50" cy="50" r="6" :fill="iconColor" opacity="0.4" />
      </g>

      <g v-else-if="iconType === 'flag'">
        <line x1="15" y1="70" x2="15" y2="20" :stroke="iconColor" stroke-width="3" />
        <polygon points="15,30 35,25 15,20" :stroke="iconColor" stroke-width="2" fill="none" />
        <line x1="40" y1="70" x2="40" y2="25" :stroke="iconColor" stroke-width="3" />
        <polygon points="40,35 60,30 40,25" :stroke="iconColor" stroke-width="2" fill="none" />
        <line x1="65" y1="70" x2="65" y2="30" :stroke="iconColor" stroke-width="3" />
        <polygon points="65,40 80,35 65,30" :stroke="iconColor" stroke-width="2" fill="none" />
        <line x1="15" y1="70" x2="80" y2="70" :stroke="iconColor" stroke-width="2" />
      </g>

      <g v-else-if="iconType === 'age-axis'">
        <line x1="15" y1="50" x2="85" y2="50" :stroke="iconColor" stroke-width="3" stroke-linecap="round" />
        <line x1="30" y1="45" x2="30" y2="55" :stroke="iconColor" stroke-width="2" />
        <line x1="50" y1="45" x2="50" y2="55" :stroke="iconColor" stroke-width="2" />
        <line x1="70" y1="45" x2="70" y2="55" :stroke="iconColor" stroke-width="2" />
        <circle cx="30" cy="50" r="4" :fill="iconColor" />
        <circle cx="50" cy="50" r="4" :fill="iconColor" />
        <circle cx="70" cy="50" r="4" :fill="iconColor" />
        <path d="M25,60 L35,60" :stroke="iconColor" stroke-width="2" />
        <path d="M45,60 L55,60" :stroke="iconColor" stroke-width="2" />
        <path d="M65,60 L75,60" :stroke="iconColor" stroke-width="2" />
      </g>

      <g v-else-if="iconType === 'package'">
        <rect x="30" y="35" width="40" height="30" :stroke="iconColor" stroke-width="3" fill="none" rx="4" />
        <line x1="30" y1="50" x2="70" y2="50" :stroke="iconColor" stroke-width="2" />
        <circle cx="42" cy="42" r="5" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="58" cy="58" r="5" :stroke="iconColor" stroke-width="2" fill="none" />
      </g>

      <g v-else-if="iconType === 'balance-scale'">
        <rect x="35" y="65" width="30" height="8" :stroke="iconColor" stroke-width="3" fill="none" />
        <line x1="50" y1="35" x2="50" y2="65" :stroke="iconColor" stroke-width="3" />
        <line x1="20" y1="45" x2="40" y2="45" :stroke="iconColor" stroke-width="3" />
        <line x1="60" y1="45" x2="80" y2="45" :stroke="iconColor" stroke-width="3" />
        <circle cx="30" cy="45" r="6" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="70" cy="45" r="6" :stroke="iconColor" stroke-width="2" fill="none" />
      </g>

      <g v-else-if="iconType === 'move-more-less'">
        <rect x="20" y="35" width="15" height="30" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="42" y="35" width="15" height="30" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="64" y="35" width="15" height="30" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="20" y="45" width="15" height="20" :fill="iconColor" opacity="0.2" />
        <rect x="64" y="35" width="15" height="10" :fill="iconColor" opacity="0.2" />
        <path d="M35,50 L42,50" :stroke="iconColor" stroke-width="3" />
        <polygon points="42,50 36,46 36,54" :fill="iconColor" />
      </g>

      <g v-else-if="iconType === 'matrix'">
        <rect x="30" y="30" width="40" height="40" :stroke="iconColor" stroke-width="3" fill="none" />
        <line x1="40" y1="30" x2="40" y2="70" :stroke="iconColor" stroke-width="2" />
        <line x1="50" y1="30" x2="50" y2="70" :stroke="iconColor" stroke-width="2" />
        <line x1="60" y1="30" x2="60" y2="70" :stroke="iconColor" stroke-width="2" />
        <line x1="30" y1="40" x2="70" y2="40" :stroke="iconColor" stroke-width="2" />
        <line x1="30" y1="50" x2="70" y2="50" :stroke="iconColor" stroke-width="2" />
        <line x1="30" y1="60" x2="70" y2="60" :stroke="iconColor" stroke-width="2" />
      </g>

      <g v-else-if="iconType === 'train'">
        <rect x="20" y="40" width="15" height="20" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="35" y="40" width="15" height="20" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="50" y="40" width="15" height="20" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="65" y="40" width="15" height="20" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="25" cy="62" r="4" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="42" cy="62" r="4" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="57" cy="62" r="4" :stroke="iconColor" stroke-width="2" fill="none" />
        <circle cx="72" cy="62" r="4" :stroke="iconColor" stroke-width="2" fill="none" />
        <line x1="15" y1="68" x2="85" y2="68" :stroke="iconColor" stroke-width="2" stroke-dasharray="4" />
      </g>

      <g v-else-if="iconType === 'cycle'">
        <circle cx="50" cy="50" r="25" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="35" cy="45" r="4" :fill="iconColor" />
        <circle cx="50" cy="30" r="4" :fill="iconColor" />
        <circle cx="65" cy="45" r="4" :fill="iconColor" />
        <circle cx="65" cy="60" r="4" :fill="iconColor" />
        <circle cx="50" cy="70" r="4" :fill="iconColor" />
        <circle cx="35" cy="60" r="4" :fill="iconColor" />
        <path d="M50,50 L50,25" :stroke="iconColor" stroke-width="2" />
      </g>

      <g v-else-if="iconType === 'overlap'">
        <rect x="25" y="30" width="30" height="40" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="45" y="30" width="30" height="40" :stroke="iconColor" stroke-width="3" fill="none" />
        <rect x="45" y="30" width="10" height="40" :fill="iconColor" opacity="0.2" />
      </g>

      <g v-else-if="iconType === 'profit'">
        <line x1="20" y1="70" x2="80" y2="70" :stroke="iconColor" stroke-width="3" />
        <line x1="20" y1="30" x2="20" y2="70" :stroke="iconColor" stroke-width="3" />
        <rect x="30" y="50" width="20" height="20" :stroke="iconColor" stroke-width="2" fill="none" />
        <rect x="30" y="40" width="20" height="10" :fill="iconColor" opacity="0.3" />
        <rect x="55" y="35" width="20" height="35" :stroke="iconColor" stroke-width="2" fill="none" />
      </g>

      <g v-else>
        <circle cx="50" cy="50" r="25" :stroke="iconColor" stroke-width="3" fill="none" />
        <circle cx="50" cy="50" r="15" :stroke="iconColor" stroke-width="2" fill="none" />
      </g>
    </svg>

    <div class="relative z-10">
      <div class="flex items-center gap-3 mb-3">
        <span 
          class="size-9 shrink-0 rounded-xl flex items-center justify-center font-bold text-sm leading-none tabular-nums text-accentCream"
          :style="{ backgroundColor: badgeBg }"
        >
          {{ problem.lessonNumber }}
        </span>
        <h3 class="text-text font-semibold text-lg line-clamp-1 tracking-body">{{ problem.title }}</h3>
      </div>

      <div class="flex items-center justify-between mt-4">
        <span 
          class="text-xs font-medium px-3 py-1.5 rounded-full"
          :style="{ backgroundColor: pillBg, color: pillFg }"
        >
          {{ problem.methodType }}
        </span>
        <div v-if="progress && progress.practiceCount > 0" class="flex items-center gap-1 text-xs">
          <span class="text-textTertiary">{{ progress.practiceCount }}次</span>
          <span class="text-textTertiary">/</span>
          <span class="font-bold" :style="{ color: accuracyColor }">{{ accuracy }}%</span>
        </div>
        <div v-else-if="progress?.learned" class="text-xs text-successText font-medium">
          ✓ 已学
        </div>
        <div v-else class="w-16"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Problem, LearningProgress } from '@/data/problems'

const props = defineProps<{
  problem: Problem
  progress?: LearningProgress | null
}>()

const bgColors = [
  'rgba(26, 24, 22, 0.75)',
  'rgba(30, 28, 26, 0.72)',
  'rgba(35, 33, 30, 0.70)',
  'rgba(48, 40, 36, 0.68)',
  'rgba(26, 24, 22, 0.78)',
  'rgba(40, 36, 32, 0.72)',
  'rgba(32, 30, 28, 0.74)',
  'rgba(44, 38, 34, 0.70)',
  'rgba(28, 26, 24, 0.76)',
  'rgba(36, 32, 28, 0.72)',
]

const methodIcons: Record<string, { type: string; color: string; badgeBg: string; pillBg: string; pillFg: string }> = {
  '图示法': { type: 'circles', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '列表法': { type: 'list', color: '#EAD6B8', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '画线法': { type: 'line-segment', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '连线法': { type: 'line-link', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '线段图法': { type: 'line-segment', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '树状图法': { type: 'tree', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '倒推法': { type: 'arrow-back', color: '#EAD6B8', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '逆推法': { type: 'arrow-back', color: '#EAD6B8', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '竖式法': { type: 'list', color: '#EAD6B8', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '表格法': { type: 'list', color: '#EAD6B8', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '统计图法': { type: 'graph-bar', color: '#684131', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '数轴法': { type: 'number-line', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '坐标系法': { type: 'coordinate', color: '#684131', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '韦恩图法': { type: 'venn', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '流程图法': { type: 'flow', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '假设法': { type: 'assume', color: '#684131', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '排除法': { type: 'eliminate', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '枚举法': { type: 'enumerate', color: '#684131', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '转化法': { type: 'convert', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '建模法': { type: 'model', color: '#684131', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '归纳法': { type: 'enumerate', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '类比法': { type: 'convert', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '插旗法': { type: 'flag', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '年龄轴法': { type: 'age-axis', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '打包法': { type: 'package', color: '#684131', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '移多补少法': { type: 'move-more-less', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '天平法': { type: 'balance-scale', color: '#EAD6B8', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '方阵问题': { type: 'matrix', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '周期问题': { type: 'cycle', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' },
  '重叠问题': { type: 'overlap', color: '#777A86', badgeBg: '#454850', pillBg: 'rgba(69, 72, 80, 0.85)', pillFg: '#EAD6B8' },
  '利润问题': { type: 'profit', color: '#684131', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
  '火车过桥': { type: 'train', color: '#EAD6B8', badgeBg: '#4A2E22', pillBg: 'rgba(74, 46, 34, 0.85)', pillFg: '#EAD6B8' },
}

const cardBgColor = computed(() => {
  const index = props.problem.lessonNumber % bgColors.length
  return bgColors[index]
})

const iconInfo = computed(() => {
  return methodIcons[props.problem.methodType] || { type: 'circles', color: '#C9563A', badgeBg: '#9A3D28', pillBg: 'rgba(154, 61, 40, 0.75)', pillFg: '#EAD6B8' }
})

const iconType = computed(() => iconInfo.value.type)
const iconColor = computed(() => iconInfo.value.color)
const badgeBg = computed(() => iconInfo.value.badgeBg)
const pillBg = computed(() => iconInfo.value.pillBg)
const pillFg = computed(() => iconInfo.value.pillFg)

const accuracy = computed(() => {
  if (!props.progress || props.progress.practiceCount === 0) return 0
  return Math.round((props.progress.correctCount / props.progress.practiceCount) * 100)
})

const accuracyColor = computed(() => {
  if (accuracy.value >= 80) return '#A8D4C4'
  if (accuracy.value >= 60) return '#EAD6B8'
  return '#F0A898'
})
</script>

<style scoped>
.grid-card {
  min-height: 110px;
}

.line-clamp-1 {
  display: -webkit-box;  
  line-clamp: 1;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tracking-body {
  letter-spacing: 0.5px;
}
</style>
