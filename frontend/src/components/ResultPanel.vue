<template>
  <aside class="sidebar right">
    <div class="panel-title">检测结果</div>

    <details class="result-block" open>
      <summary>JSON结果</summary>
      <div v-if="loading" class="result-loading">
        <div class="loading-dots" />
        <span>检测中，请稍候…</span>
      </div>
      <pre v-else-if="jsonResult" class="json-result">{{ jsonResult }}</pre>
      <div v-else class="result-empty">暂无数据</div>
    </details>

    <details class="result-block" open>
      <summary>篡改结论</summary>
      <div v-if="loading" class="result-loading">
        <div class="loading-dots" />
        <span>检测中…</span>
      </div>
      <div v-else-if="result?.image_property?.ps" class="result-summary">
        <p><strong>是否篡改：</strong>{{ result.image_property.ps.is_tampered ? '是' : '否' }}</p>
        <p v-if="result.image_property.ps.tampered_positions?.length">
          <strong>篡改区域数：</strong>{{ result.image_property.ps.tampered_positions.length }}
        </p>
      </div>
      <div v-else-if="result && !loading" class="result-empty">无篡改结论</div>
      <div v-else class="result-empty">暂无数据</div>
    </details>

    <div v-if="heatmapDataUrl" class="result-image-wrap">
      <img :src="heatmapDataUrl" alt="篡改区域标注" />
    </div>
  </aside>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { DetectionResult } from '@/types'

const props = defineProps<{
  result: DetectionResult | null
  loading: boolean
  error: string
}>()

/** 展示用：data.result 的 JSON，省略 base64 image 避免过长 */
const jsonResult = computed(() => {
  if (!props.result) return ''
  const omitImage = (obj: unknown): unknown => {
    if (obj && typeof obj === 'object' && !Array.isArray(obj)) {
      const out: Record<string, unknown> = {}
      for (const [k, v] of Object.entries(obj)) {
        if (k === 'image' && typeof v === 'string' && v.length > 100) {
          out[k] = `[base64 已省略，长度 ${v.length}]`
        } else {
          out[k] = omitImage(v)
        }
      }
      return out
    }
    return obj
  }
  return JSON.stringify(omitImage(props.result), null, 2)
})

/** 热力图：使用 image_property.ps.image（base64） */
const heatmapDataUrl = computed(() => {
  const img = props.result?.image_property?.ps?.image
  if (!img || typeof img !== 'string') return ''
  return img.startsWith('data:') ? img : `data:image/png;base64,${img}`
})
</script>

<style scoped>
.sidebar {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0.75rem;
  overflow: auto;
}

.panel-title {
  font-weight: 600;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.result-block {
  margin-bottom: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}

.result-block summary {
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  cursor: pointer;
  font-weight: 500;
}

.result-block pre,
.result-block table {
  margin: 0;
  padding: 0.75rem;
  font-size: 0.8rem;
  overflow: auto;
}

.result-loading {
  padding: 1rem 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  font-size: 0.85rem;
}

.loading-dots {
  width: 20px;
  height: 20px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='4' cy='12' r='2' fill='%232563eb' opacity='.4'/%3E%3Ccircle cx='12' cy='12' r='2' fill='%232563eb' opacity='.8'/%3E%3Ccircle cx='20' cy='12' r='2' fill='%232563eb'/%3E%3C/svg%3E")
    center/contain no-repeat;
  animation: dots-pulse 0.8s ease-in-out infinite;
}

@keyframes dots-pulse {
  0%,
  100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

.json-result {
  background: #1e293b;
  color: #e2e8f0;
  border-radius: 0 0 6px 6px;
  max-height: 200px;
}

.result-summary {
  padding: 0.75rem;
  font-size: 0.85rem;
}

.result-summary p {
  margin: 0.25rem 0;
}

.result-empty {
  padding: 0.75rem;
  color: #94a3b8;
  font-size: 0.85rem;
}

.result-table {
  width: 100%;
  border-collapse: collapse;
}

.result-table th,
.result-table td {
  border: 1px solid #e2e8f0;
  padding: 0.4rem 0.6rem;
  text-align: left;
}

.result-table th {
  background: #f8fafc;
  font-weight: 600;
}

.result-image-wrap {
  margin-top: 0.75rem;
}

.result-image-wrap img {
  max-width: 100%;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.ai-analysis {
  margin-top: 0.75rem;
  padding: 0.75rem;
  background: #f0f9ff;
  border-radius: 6px;
  font-size: 0.85rem;
}

.error {
  margin-top: 0.75rem;
  padding: 0.75rem;
  color: #dc2626;
  font-size: 0.85rem;
}
</style>
