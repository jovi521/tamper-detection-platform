<template>
  <section :class="styles.center">
    <div v-if="error" class="error-message">
      <span class="error-icon">⚠️</span>
      {{ error }}
    </div>
    <div ref="areaRef" :class="styles.imageArea">
      <template v-if="currentImage?.preview">
        <img
          :class="styles.mainImage"
          :src="currentImage.preview"
          :style="imageStyle"
          alt="当前图片"
        />
        <div v-if="loading" :class="styles.scanCursor" aria-hidden="true" />
        <div :class="styles.imageActions">
          <button :class="styles.iconBtn" title="放大" @click="zoomIn">🔍+</button>
          <button :class="styles.iconBtn" title="缩小" @click="zoomOut">🔍-</button>
          <button :class="styles.iconBtn" title="顺时针旋转" @click="rotateClockwise">↻</button>
          <button :class="styles.iconBtn" title="逆时针旋转" @click="rotateCounterClockwise">
            ↺
          </button>
          <button :class="styles.iconBtn" title="复原" @click="reset">⟲</button>
        </div>
      </template>
      <div v-else :class="styles.placeholder">请上传本地文件或输入在线 URL 进行检测</div>
    </div>
    <div :class="styles.uploadBar">
      <label :class="{ disabled: loading }" :disabled="loading" class="btn primary">
        <span>上传本地文件</span>
        <input accept="image/*" type="file" @change="onFileChange" />
      </label>
      <div :class="styles.urlInput">
        <div :class="styles.urlInputWrapper">
          <input
            v-model="localImageUrl"
            :disabled="loading"
            placeholder="输入在线文件 URL，回车后 Enter 键识别"
            type="url"
            @input="onLocalUrlChange"
            @keyup.enter="submitUrl"
          />
          <button v-if="localImageUrl && !loading" :class="styles.clearBtn" @click="clearUrl">
            ×
          </button>
        </div>
        <button
          :class="{ disabled: loading }"
          :disabled="loading"
          class="btn primary"
          @click="submitUrl"
        >
          识别
        </button>
      </div>
    </div>
    <p :class="styles.note">
      要上传的图片：目前支持 jpg、jpeg、png、bmp、gif、webp、svg、tiff，文件大小不超过 10M。
    </p>
  </section>
</template>

<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import type { HistoryItem } from '@/types'
import styles from '@/styles/components/MainImageArea.module.css'

const props = defineProps<{
  currentImage: HistoryItem | null
  imageUrl: string
  loading: boolean
  error: string
}>()

const emit = defineEmits<{
  'update:imageUrl': [value: string]
  'file-select': [file: File]
  'url-submit': []
}>()

// 本地响应式变量，用于存储输入框的值
const localImageUrl = ref(props.imageUrl)

// 监听props变化，更新本地变量
watch(
  () => props.imageUrl,
  (newValue) => {
    localImageUrl.value = newValue
  }
)

// 当本地变量变化时，通知父组件
function onLocalUrlChange() {
  emit('update:imageUrl', localImageUrl.value)
}

// 清除URL输入框
function clearUrl() {
  localImageUrl.value = ''
  emit('update:imageUrl', '')
}

const areaRef = ref<HTMLDivElement | null>(null)

// 图片操作状态
const zoom = ref(1)
const rotation = ref(0)

// 图片样式计算
const imageStyle = computed(() => {
  return {
    transform: `scale(${zoom.value}) rotate(${rotation.value}deg)`,
    transition: 'transform 0.3s ease',
  }
})

// 放大
function zoomIn(): void {
  if (zoom.value < 3) {
    zoom.value += 0.2
  }
}

// 缩小
function zoomOut(): void {
  if (zoom.value > 0.5) {
    zoom.value -= 0.2
  }
}

// 顺时针旋转
function rotateClockwise(): void {
  rotation.value = (rotation.value + 90) % 360
}

// 逆时针旋转
function rotateCounterClockwise(): void {
  rotation.value = (rotation.value - 90 + 360) % 360
}

// 复原
function reset(): void {
  zoom.value = 1
  rotation.value = 0
}

function onFileChange(e: Event): void {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) emit('file-select', file)
  target.value = ''
}

function submitUrl(): void {
  emit('url-submit')
}
</script>
