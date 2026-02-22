<template>
  <section class="center">
    <div class="image-area" ref="areaRef">
      <template v-if="currentImage?.preview">
        <img :src="currentImage.preview" alt="当前图片" class="main-image" />
        <!-- 扫描光标：有图且在检测中时显示 -->
        <div v-if="loading" class="scan-cursor" aria-hidden="true"></div>
        <div class="image-actions">
          <button type="button" class="icon-btn" title="放大">🔍</button>
          <button type="button" class="icon-btn" title="复制" @click="$emit('copy')">📋</button>
        </div>
      </template>
      <div v-else class="placeholder">
        请上传本地文件或输入在线 URL 进行检测
      </div>
    </div>
    <div class="upload-bar">
      <label class="btn primary">
        上传本地文件
        <input
          type="file"
          accept=".jpg,.jpeg,.png,.bmp,.pdf,.tiff,.tif,.webp,.gif"
          @change="onFileChange"
        />
      </label>
      <div class="url-input-wrap">
        <input
          :value="imageUrl"
          type="text"
          class="url-input"
          placeholder="输入在线文件 URL，回车/Enter 发起调用"
          @input="(e) => $emit('update:imageUrl', e.target?.value ?? '')"
          @keydown.enter.prevent="submitUrl"
        />
      </div>
    </div>
    <p class="hint">
      要上传的图片，目前支持 jpg、png、bmp、pdf、tiff、webp、单帧 gif，文件大小不超过 10M
    </p>
  </section>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  currentImage: { type: Object, default: null },
  imageUrl: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})
const emit = defineEmits(['update:imageUrl', 'file-select', 'url-submit', 'copy'])

const areaRef = ref(null)

function onFileChange(e) {
  const file = e.target?.files?.[0]
  if (file) emit('file-select', file)
  e.target.value = ''
}

function submitUrl() {
  emit('url-submit')
}
</script>

<style scoped>
.center {
  display: flex;
  flex-direction: column;
  padding: 0 1rem;
  min-width: 0;
}
.image-area {
  flex: 1;
  min-height: 280px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.main-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.placeholder {
  color: #94a3b8;
  text-align: center;
  padding: 2rem;
}
/* 扫描光标：半透明蓝色横条自上而下移动 */
.scan-cursor {
  position: absolute;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(37, 99, 235, 0.6),
    transparent
  );
  box-shadow: 0 0 12px rgba(37, 99, 235, 0.5);
  pointer-events: none;
  animation: scan-move 1.5s ease-in-out infinite;
}
@keyframes scan-move {
  0% {
    top: 0;
    opacity: 1;
  }
  100% {
    top: 100%;
    opacity: 0.8;
  }
}
.image-actions {
  position: absolute;
  bottom: 8px;
  right: 8px;
  display: flex;
  gap: 4px;
}
.icon-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  font-size: 1rem;
}
.upload-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.75rem;
}
.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  white-space: nowrap;
}
.btn.primary {
  background: #2563eb;
  color: #fff;
  border: none;
}
.btn.primary input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
}
.url-input-wrap {
  flex: 1;
  min-width: 0;
}
.url-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.9rem;
}
.url-input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}
.hint {
  margin: 0.5rem 0 0 0;
  font-size: 0.8rem;
  color: #64748b;
}
</style>
