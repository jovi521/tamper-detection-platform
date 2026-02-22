<template>
  <aside class="sidebar left">
    <div class="panel-title">图片列表</div>
    <div class="thumb-list">
      <div
        v-for="item in historyList"
        :key="item.id"
        :class="{ active: currentImage?.id === item.id }"
        class="thumb-item"
        @click="emit('select', item)"
      >
        <img :alt="item.name" :src="item.preview" />
      </div>
    </div>
  </aside>
</template>

<script lang="ts" setup>
import type { HistoryItem } from '@/types'

defineProps<{
  historyList: HistoryItem[]
  currentImage: HistoryItem | null
}>()

const emit = defineEmits<{
  select: [item: HistoryItem]
}>()
</script>

<style scoped>
.sidebar {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0.75rem;
  overflow: auto;
}

.sidebar.left {
  display: flex;
  flex-direction: column;
}

.panel-title {
  font-weight: 600;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.thumb-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.thumb-item {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
}

.thumb-item:hover {
  border-color: #93c5fd;
}

.thumb-item.active {
  border-color: #2563eb;
}

.thumb-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
</style>
