"""Request/Response schemas for tamper detection API."""
from pydantic import BaseModel, Field


class DetectionResultItem(BaseModel):
    """Single field in recognition result (e.g. is_tampered, ps)."""
    field_name: str = Field(..., description="字段名")
    content: str = Field(default="", description="信息内容")


class DetectionResponse(BaseModel):
    """Tamper detection API response."""
    success: bool = True
    is_tampered: bool = Field(..., description="是否存在篡改: True=有篡改, False=无篡改")
    result_items: list[DetectionResultItem] = Field(
        default_factory=list,
        description="识别结果列表(字段名-信息内容)",
    )
    heatmap_url: str | None = Field(None, description="篡改区域热力图或标注图 URL/Base64")
    ai_analysis: str | None = Field(None, description="LangChain AI 二次验证分析摘要")
    message: str | None = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    service: str = "tamper-detection"
