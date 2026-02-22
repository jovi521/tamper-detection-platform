<template>
  <aside class="sidebar right">
    <div class="panel-title">检测结果</div>

    <!-- JSON结果：始终展示该区域，加载时显示占位，有结果时显示内容 -->
    <details class="result-block" open>
      <summary>JSON结果</summary>
      <div v-if="loading" class="result-loading">
        <div class="loading-dots"></div>
        <span>检测中，请稍候…</span>
      </div>
      <pre v-else-if="jsonResult" class="json-result">{{ jsonResult }}</pre>
      <div v-else class="result-empty">暂无数据</div>
    </details>

    <!-- 识别结果：始终展示该区域，加载时显示动效，有结果时显示表格 -->
    <details class="result-block" open>
      <summary>识别结果</summary>
      <div v-if="loading" class="result-loading">
        <div class="loading-dots"></div>
        <span>识别中…</span>
      </div>
      <table v-else-if="result?.result_items?.length" class="result-table">
        <thead>
          <tr>
            <th>字段名</th>
            <th>信息内容</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in result.result_items" :key="i">
            <td>{{ row.field_name }}</td>
            <td>{{ row.content || '—' }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="result && !loading" class="result-empty">无识别项</div>
      <div v-else class="result-empty">暂无数据</div>
    </details>

    <div v-if="result?.heatmap_url" class="result-image-wrap">
      <img :src="result.heatmap_url" alt="篡改区域标注" />
    </div>
    <div v-if="result?.ai_analysis" class="ai-analysis">
      <strong>AI 分析</strong>
      <p>{{ result.ai_analysis }}</p>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  result: { type: Object, default: null },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})

const jsonResult = computed(() => {
  if (!props.result) return ''
  return JSON.stringify(props.result, null, 2)
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
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='4' cy='12' r='2' fill='%232563eb' opacity='.4'/%3E%3Ccircle cx='12' cy='12' r='2' fill='%232563eb' opacity='.8'/%3E%3Ccircle cx='20' cy='12' r='2' fill='%232563eb'/%3E%3C/svg%3E") center/contain no-repeat;
  animation: dots-pulse 0.8s ease-in-out infinite;
}
@keyframes dots-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}
.json-result {
  background: #1e293b;
  color: #e2e8f0;
  border-radius: 0 0 6px 6px;
  max-height: 200px;
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
