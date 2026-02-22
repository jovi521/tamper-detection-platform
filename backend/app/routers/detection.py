"""Tamper detection API routes."""
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from backend.app.config import get_settings
from backend.app.schemas.detection import DetectionResponse
from backend.app.services.detection_service import get_detection_service
from backend.app.services.langchain_chain import run_ai_analysis

router = APIRouter(prefix="/api", tags=["detection"])
settings = get_settings()


def _check_extension(filename: str) -> bool:
    ext = (filename or "").rsplit(".", 1)[-1].lower()
    return ext in settings.allowed_extensions


@router.post("/detect/upload", response_model=DetectionResponse)
async def detect_upload(file: UploadFile = File(...)):
    """
    上传本地文件进行篡改检测。
    支持: jpg, png, bmp, pdf, tiff, webp, 单帧 gif，文件不超过 10M。
    """
    if not file.filename or not _check_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。允许: {', '.join(sorted(settings.allowed_extensions))}",
        )
    raw = await file.read()
    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制（最大 {settings.max_upload_bytes // (1024 * 1024)}MB）",
        )
    service = get_detection_service()
    result = service.detect_from_bytes(raw, file.filename or "")

    if result.success and settings.enable_ai_chain:
        summary = f"is_tampered={result.is_tampered}, items={[r.model_dump() for r in result.result_items]}"
        ai_text = run_ai_analysis(summary)
        if ai_text:
            result = result.model_copy(update={"ai_analysis": ai_text})

    return result


@router.post("/detect/url", response_model=DetectionResponse)
async def detect_url(url: str = Form(..., description="图片 URL")):
    """
    通过在线文件 URL 发起检测（回车/Enter 发起调用）。
    """
    if not url or not url.strip():
        raise HTTPException(status_code=400, detail="请提供有效的图片 URL")
    try:
        import httpx
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url.strip())
            resp.raise_for_status()
            raw = resp.content
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取图片失败: {e}") from e

    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(status_code=400, detail="文件大小超过限制")

    service = get_detection_service()
    result = service.detect_from_bytes(raw, url)

    if result.success and settings.enable_ai_chain:
        summary = f"is_tampered={result.is_tampered}, items={[r.model_dump() for r in result.result_items]}"
        ai_text = run_ai_analysis(summary)
        if ai_text:
            result = result.model_copy(update={"ai_analysis": ai_text})

    return result


@router.get("/health")
async def health():
    """健康检查."""
    from backend.app.schemas.detection import HealthResponse
    return HealthResponse()
