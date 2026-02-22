/** 后端 API 响应外壳 */
export interface DetectionApiResponse<T> {
  x_request_id: string
  msg: string
  data: T
  code: number
}

/** 检测接口 data 结构 */
export interface DetectionApiData {
  result: DetectionResult
  file_type: string
  file_data: string
}

/** image_property.ps 单算法结果 */
export interface PsResult {
  tampered_positions: number[][]
  is_tampered: boolean
  image?: string
  tampered_scores: number[][]
}

/** image_property（可扩展其他算法） */
export interface ImageProperty {
  ps: PsResult
  [key: string]: unknown
}

/** 篡改检测结果（即后端 data.result） */
export interface DetectionResult {
  image_width: number
  image_height: number
  image_property: ImageProperty
}

/** 历史记录项（图片列表） */
export interface HistoryItem {
  id: number
  name: string
  file?: File
  preview: string
  result?: DetectionResult
}
