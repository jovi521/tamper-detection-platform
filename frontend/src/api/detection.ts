import axios from 'axios'
import type { DetectionApiData, DetectionApiResponse, DetectionResult } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '',
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

function unwrapResult(res: DetectionApiResponse<DetectionApiData>): DetectionResult {
  if (res.code !== 200) {
    throw new Error(res.msg || `请求失败 (code: ${res.code})`)
  }
  return res.data.result
}

/**
 * 上传本地文件进行篡改检测
 * 返回后端 data.result
 */
export async function detectUpload(file: File): Promise<DetectionResult> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<DetectionApiResponse<DetectionApiData>>(
    '/api/detect/upload',
    form,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  )
  return unwrapResult(data)
}

/**
 * 通过 URL 进行篡改检测
 * 返回后端 data.result
 */
export async function detectByUrl(url: string): Promise<DetectionResult> {
  const form = new FormData()
  form.append('url', url.trim())
  const { data } = await api.post<DetectionApiResponse<DetectionApiData>>('/api/detect/url', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return unwrapResult(data)
}
