import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

/**
 * 上传本地文件进行篡改检测
 * @param {File} file
 * @returns {Promise<DetectionResult>}
 */
export async function detectUpload(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/api/detect/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

/**
 * 通过 URL 进行篡改检测
 * @param {string} url
 * @returns {Promise<DetectionResult>}
 */
export async function detectByUrl(url) {
  const form = new FormData()
  form.append('url', url.trim())
  const { data } = await api.post('/api/detect/url', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

/**
 * @typedef {Object} DetectionResultItem
 * @property {string} field_name
 * @property {string} content
 *
 * @typedef {Object} DetectionResult
 * @property {boolean} success
 * @property {boolean} is_tampered
 * @property {DetectionResultItem[]} result_items
 * @property {string|null} heatmap_url
 * @property {string|null} ai_analysis
 * @property {string|null} message
 */
