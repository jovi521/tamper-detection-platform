<template>
  <aside :class="styles.sidebarLeft" class="sidebar">
    <div class="panel-title">图片列表</div>
    <div :class="styles.thumbList">
      <div
        v-for="item in historyList"
        :key="item.id"
        :class="[styles.thumbItem, { [styles.active]: currentImage?.id === item.id }]"
        @click="emit('select', item)"
      >
        <img :alt="item.name" :src="item.preview" />
      </div>
    </div>
  </aside>
</template>

<script lang="ts" setup>
import type { HistoryItem } from '@/types'
import styles from '@/styles/components/ImageSidebar.module.css'

defineProps<{
  historyList: HistoryItem[]
  currentImage: HistoryItem | null
}>()

const emit = defineEmits<{
  select: [item: HistoryItem]
}>()
</script>
