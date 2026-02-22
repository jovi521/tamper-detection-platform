# 通用篡改检测系统

基于 **FastAPI + LangChain + Vue** 的前后端分离架构，提供图像篡改检测 API 与 Web 界面。后端可集成 LangChain 实现 AI 分析链（如多模态模型二次验证），前端使用 Vue 实现文件上传与结果展示。

## 项目结构

```
tamper-detection-platform/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── main.py          # 应用入口
│   │   ├── config.py        # 配置
│   │   ├── routers/         # API 路由
│   │   ├── schemas/         # 请求/响应模型
│   │   └── services/        # 检测服务、LangChain 链
│   └── requirements.txt
├── frontend/                # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── App.vue          # 主界面（三栏布局）
│   │   ├── api/             # 接口封装
│   │   └── main.js
│   ├── index.html
│   └── package.json
└── README.md
```

## 功能说明

- **后端**
  - `POST /api/detect/upload`：上传本地图片进行篡改检测
  - `POST /api/detect/url`：通过图片 URL 发起检测
  - 检测结果包含：`is_tampered`、识别结果表、可选热力图、可选 AI 分析摘要
  - 可选 LangChain 分析链：配置 `OPENAI_API_KEY` 与 `ENABLE_AI_CHAIN=true` 后，对检测结果进行二次验证或摘要

- **前端**
  - 左侧：图片列表（历史/示例），点击切换当前图
  - 中间：当前图片展示、上传本地文件、输入在线 URL（回车发起调用）
  - 右侧：JSON 结果、识别结果表格、热力图（若有）、AI 分析（若有）

## 快速开始

### 1. 后端

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env   # 按需编辑
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API 文档：<http://127.0.0.1:8000/docs>

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

浏览器访问：<http://localhost:5173>。前端已配置代理，将 `/api` 转发到 `http://127.0.0.1:8000`。

### 3. 启用 LangChain AI 分析链（可选）

在 `backend/.env` 中设置：

```env
OPENAI_API_KEY=sk-xxx
ENABLE_AI_CHAIN=true
```

重启后端后，检测结果中会多出 `ai_analysis` 字段（二次验证/摘要）。

## 检测逻辑说明

当前 `DetectionService` 为**占位实现**，仅做简单规则返回示例结果。接入真实篡改检测模型时，请：

1. 在 `backend/app/services/detection_service.py` 中替换 `detect_from_bytes` / `_stub_detect` 为实际模型推理；
2. 如需返回热力图，在响应中设置 `heatmap_url`（Base64 或 URL）。

## 技术栈

- **后端**：FastAPI、Pydantic、Pillow、LangChain（可选）、httpx
- **前端**：Vue 3、Vite、Axios

## 许可

按项目需求自行约定。
