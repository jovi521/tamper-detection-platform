<template>
  <div class="app">
    <AppHeader />
    <main class="main">
      <ImageSidebar
        :current-image="currentImage"
        :history-list="historyList"
        @select="selectHistory"
      />
      <MainImageArea
        v-model:image-url="imageUrl"
        :current-image="currentImage"
        :loading="loading"
        @copy="copyImage"
        @file-select="onFileSelect"
        @url-submit="submitUrl"
      />
      <ResultPanel :error="error" :loading="loading" :result="result" />
    </main>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import ImageSidebar from './components/ImageSidebar.vue'
import MainImageArea from './components/MainImageArea.vue'
import ResultPanel from './components/ResultPanel.vue'
import { detectByUrl, detectUpload } from '@/api/detection'
import type { DetectionResult, HistoryItem } from '@/types'

const historyList = ref<HistoryItem[]>([])
const currentImage = ref<HistoryItem | null>(null)
const imageUrl = ref('')
const result = ref<DetectionResult | null>(null)
const loading = ref(false)
const error = ref('')

let idCounter = 0

function addToHistory(file: File | null, preview: string): HistoryItem {
  const id = ++idCounter
  const name = file?.name ?? `图片 ${id}`
  const item: HistoryItem = { id, name, preview }
  if (file) item.file = file
  historyList.value.unshift(item)
  return historyList.value[0]
}

function selectHistory(item: HistoryItem): void {
  currentImage.value = item
  result.value = item.result ?? null
}

function onFileSelect(file: File | undefined): void {
  if (!file) return
  error.value = ''
  const preview = URL.createObjectURL(file)
  const item = addToHistory(file, preview)
  currentImage.value = item
  runDetectUpload(file, item)
}

async function runDetectUpload(file: File, item: HistoryItem): Promise<void> {
  loading.value = true
  result.value = null
  try {
    const res = await detectUpload(file)
    result.value = res
    item.result = res
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { detail?: string } }; message?: string }
    error.value = axiosErr.response?.data?.detail ?? axiosErr.message ?? '请求失败'
  } finally {
    loading.value = false
  }
}

function submitUrl(): void {
  const url = imageUrl.value?.trim()
  if (!url) return
  error.value = ''
  const item = addToHistory(null, url)
  item.name = url
  currentImage.value = item
  runDetectUrl(url, item)
}

async function runDetectUrl(url: string, item: HistoryItem): Promise<void> {
  loading.value = true
  result.value = null
  try {
    const res = await detectByUrl(url)
    result.value = res
    item.result = res
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { detail?: string } }; message?: string }
    error.value = axiosErr.response?.data?.detail ?? axiosErr.message ?? '请求失败'
  } finally {
    loading.value = false
  }
}

function copyImage(): void {
  if (!currentImage.value?.preview) return
  navigator.clipboard?.writeText(currentImage.value.preview)
}
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: #f5f6f8;
  color: #1a1a2e;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  display: grid;
  grid-template-columns: 180px 1fr 320px;
  gap: 0;
  min-height: 0;
  padding: 1rem;
}
</style>
