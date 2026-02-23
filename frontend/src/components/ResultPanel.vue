<template>
  <aside class="sidebar right">
    <div class="panel-title">检测结果</div>

    <details :class="styles.resultBlock" open>
      <summary>JSON结果</summary>
      <div v-if="loading" :class="styles.resultLoading">
        <div :class="styles.loadingDots" />
        <span>检测中，请稍候…</span>
      </div>
      <pre v-else-if="jsonResult" :class="styles.jsonResult">{{ jsonResult }}</pre>
      <div v-else :class="styles.resultEmpty">暂无数据</div>
    </details>

    <details :class="styles.resultBlock" open>
      <summary>篡改结论</summary>
      <div v-if="loading" :class="styles.resultLoading">
        <div :class="styles.loadingDots" />
        <span>检测中…</span>
      </div>
      <div v-else-if="result?.image_property?.ps" :class="styles.resultSummary">
        <p><strong>是否篡改：</strong>{{ result.image_property.ps.is_tampered ? '是' : '否' }}</p>
        <p v-if="result.image_property.ps.tampered_positions?.length">
          <strong>篡改区域数：</strong>{{ result.image_property.ps.tampered_positions.length }}
        </p>
      </div>
      <div v-else-if="result && !loading" :class="styles.resultEmpty">无篡改结论</div>
      <div v-else :class="styles.resultEmpty">暂无数据</div>
    </details>

    <div v-if="heatmapDataUrl" :class="styles.resultImageWrap">
      <img :src="heatmapDataUrl" alt="篡改区域标注" />
    </div>
  </aside>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import type { DetectionResult } from '@/types'
import styles from '@/styles/components/ResultPanel.module.css'

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
  if (!img) return ''
  return img.startsWith('data:') ? img : `data:image/png;base64,${img}`
})
</script>
