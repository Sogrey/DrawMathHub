<template>
  <div class="space-y-4">
    <!-- 可自动判分 -->
    <div v-if="answerKey" class="space-y-3">
      <div class="flex flex-wrap items-center gap-2 text-textSecondary text-body-sm leading-relaxed">
        <template v-if="answerKey.type === 'remainder'">
          <input
            v-model="inputs[0]"
            type="text"
            inputmode="decimal"
            class="blank-input"
            @keyup.enter="submit"
          />
          <span class="text-text font-medium tracking-widest">······</span>
          <input
            v-model="inputs[1]"
            type="text"
            inputmode="decimal"
            class="blank-input"
            @keyup.enter="submit"
          />
        </template>

        <template v-else-if="answerKey.type === 'blanks'">
          <template v-for="(seg, si) in blankSegments" :key="si">
            <span v-if="seg.kind === 'text'">{{ seg.text }}</span>
            <input
              v-else
              v-model="inputs[seg.index]"
              type="text"
              inputmode="decimal"
              class="blank-input"
              @keyup.enter="submit"
            />
          </template>
        </template>

        <template v-else>
          <span class="text-textSecondary shrink-0">答案：</span>
          <input
            v-model="inputs[0]"
            type="text"
            class="flex-1 min-w-[12rem] px-4 py-2 rounded-button border-2 border-border focus:border-primary focus:outline-none bg-background"
            :placeholder="answerKey.type === 'exact' ? '请输入答案' : '数字即可，单位可省略'"
            @keyup.enter="submit"
          />
        </template>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <button
          type="button"
          class="px-6 py-2 rounded-button font-medium bg-primary text-white hover:bg-primaryDark transition-colors"
          @click="submit"
        >
          提交判分
        </button>
        <span v-if="emptyHint" class="text-sm text-dangerText">请先填写答案再提交</span>
        <span v-else-if="graded" class="text-sm" :class="correct ? 'text-successText' : 'text-dangerText'">
          {{ correct ? '回答正确！' : '还不对，可对照参考答案再试试' }}
        </span>
      </div>
    </div>

    <!-- 仅参考：无 answerKey -->
    <div v-else class="space-y-2">
      <div class="flex items-center gap-4">
        <span class="text-textSecondary shrink-0">我的答案：</span>
        <input
          v-model="inputs[0]"
          type="text"
          class="flex-1 px-4 py-2 rounded-button border-2 border-border focus:border-primary focus:outline-none bg-background"
          placeholder="请先作答后再提交"
          @keyup.enter="recordOnly"
        />
        <button
          type="button"
          class="px-6 py-2 rounded-button font-medium bg-primary text-white hover:bg-primaryDark transition-colors"
          @click="recordOnly"
        >
          记录练习
        </button>
      </div>
      <p v-if="emptyHint" class="text-sm text-dangerText">请先填写答案再提交</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import type { AnswerKey } from '@/data/problems'
import { emptyInputsForKey, gradeAnswerKey } from '@/utils/answerGrade'

const props = defineProps<{
  answerKey?: AnswerKey
}>()

const emit = defineEmits<{
  graded: [correct: boolean]
  recorded: []
}>()

const inputs = ref<string[]>([''])
const graded = ref(false)
const correct = ref(false)
const emptyHint = ref(false)

type Seg = { kind: 'text'; text: string } | { kind: 'blank'; index: number }

const blankSegments = computed<Seg[]>(() => {
  const key = props.answerKey
  if (!key || key.type !== 'blanks') return []
  if (key.template) {
    const parts = key.template.split(/\{(\d+)\}/)
    const segs: Seg[] = []
    for (let i = 0; i < parts.length; i++) {
      if (i % 2 === 0) {
        if (parts[i]) segs.push({ kind: 'text', text: parts[i] })
      } else {
        segs.push({ kind: 'blank', index: Number(parts[i]) })
      }
    }
    return segs
  }
  // fallback: prefix/suffix per blank
  const segs: Seg[] = []
  key.blanks.forEach((b, i) => {
    if (b.prefix) segs.push({ kind: 'text', text: b.prefix })
    segs.push({ kind: 'blank', index: i })
    if (b.suffix) segs.push({ kind: 'text', text: b.suffix })
    if (i < key.blanks.length - 1) segs.push({ kind: 'text', text: '，' })
  })
  return segs
})

function reset() {
  inputs.value = emptyInputsForKey(props.answerKey)
  graded.value = false
  correct.value = false
  emptyHint.value = false
}

watch(
  () => props.answerKey,
  () => reset(),
  { immediate: true },
)

watch(
  inputs,
  () => {
    if (emptyHint.value && hasAllFilled()) emptyHint.value = false
  },
  { deep: true },
)

function requiredSlotCount(): number {
  const key = props.answerKey
  if (!key) return 1
  if (key.type === 'blanks' || key.type === 'remainder') return key.blanks.length
  return 1
}

function hasAllFilled(): boolean {
  const n = requiredSlotCount()
  for (let i = 0; i < n; i++) {
    if (!(inputs.value[i] ?? '').trim()) return false
  }
  return true
}

function submit() {
  if (!props.answerKey) return
  if (!hasAllFilled()) {
    emptyHint.value = true
    graded.value = false
    return
  }
  emptyHint.value = false
  const result = gradeAnswerKey(props.answerKey, inputs.value)
  graded.value = true
  correct.value = result.correct
  emit('graded', result.correct)
}

function recordOnly() {
  if (!hasAllFilled()) {
    emptyHint.value = true
    return
  }
  emptyHint.value = false
  emit('recorded')
}

defineExpose({ reset })
</script>

<style scoped>
.blank-input {
  width: 5.5rem;
  padding: 0.35rem 0.5rem;
  border-radius: 0.5rem;
  border: 2px solid var(--color-border, #3a3f46);
  background: var(--color-background, #1a1d21);
  text-align: center;
  color: inherit;
}
.blank-input:focus {
  outline: none;
  border-color: var(--color-primary, #6b9eff);
}
</style>
