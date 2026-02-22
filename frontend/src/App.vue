<template>
  <div class="app">
    <AppHeader />
    <main class="main">
      <ImageSidebar
        :history-list="historyList"
        :current-image="currentImage"
        @select="selectHistory"
      />
      <MainImageArea
        :current-image="currentImage"
        :loading="loading"
        v-model:image-url="imageUrl"
        @file-select="onFileSelect"
        @url-submit="submitUrl"
        @copy="copyImage"
      />
      <ResultPanel
        :result="result"
        :loading="loading"
        :error="error"
      />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import ImageSidebar from './components/ImageSidebar.vue'
import MainImageArea from './components/MainImageArea.vue'
import ResultPanel from './components/ResultPanel.vue'
import { detectUpload, detectByUrl } from './api/detection.js'

const historyList = ref([])
const currentImage = ref(null)
const imageUrl = ref('')
const result = ref(null)
const loading = ref(false)
const error = ref('')

let idCounter = 0

function addToHistory(file, preview) {
  const id = ++idCounter
  const name = file?.name || `图片 ${id}`
  historyList.value.unshift({ id, name, file, preview })
  return historyList.value[0]
}

function selectHistory(item) {
  currentImage.value = item
  result.value = item.result ?? null
}

function onFileSelect(file) {
  if (!file) return
  error.value = ''
  const preview = URL.createObjectURL(file)
  const item = addToHistory(file, preview)
  currentImage.value = item
  runDetectUpload(file, item)
}

async function runDetectUpload(file, item) {
  loading.value = true
  result.value = null
  try {
    const res = await detectUpload(file)
    result.value = res
    if (item) item.result = res
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '请求失败'
  } finally {
    loading.value = false
  }
}

function submitUrl() {
  const url = imageUrl.value?.trim()
  if (!url) return
  error.value = ''
  const item = addToHistory(null, url)
  item.name = url
  currentImage.value = item
  runDetectUrl(url, item)
}

async function runDetectUrl(url, item) {
  loading.value = true
  result.value = null
  try {
    const res = await detectByUrl(url)
    result.value = res
    if (item) item.result = res
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '请求失败'
  } finally {
    loading.value = false
  }
}

function copyImage() {
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
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
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
