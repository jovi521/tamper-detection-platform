"""FastAPI application entry."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import get_settings
from backend.app.routers import detection

app = FastAPI(
    title="通用篡改检测 API",
    description="基于白研篡改检测系统，提供图像篡改检测接口，可集成 LangChain AI 分析链进行二次验证。",
    version="0.1.0",
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detection.router)


@app.get("/")
async def root():
    return {"service": "tamper-detection-api", "docs": "/docs"}
