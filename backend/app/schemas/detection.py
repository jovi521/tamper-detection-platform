"""Request/Response schemas for tamper detection API."""
from pydantic import BaseModel, Field


class PSResult(BaseModel):
    """PS检测结果"""
    tampered_positions: list[list[int]] = Field(default_factory=list, description="篡改位置坐标")
    is_tampered: bool = Field(..., description="是否存在篡改")
    image: str = Field(default="", description="图像数据")
    tampered_scores: list[list[float]] = Field(default_factory=list, description="篡改置信度分数")


class ImageProperty(BaseModel):
    """图像属性"""
    ps: PSResult = Field(..., description="PS检测结果")


class DetectionResult(BaseModel):
    """检测结果"""
    image_width: int = Field(..., description="图像宽度")
    image_property: ImageProperty = Field(..., description="图像属性")
    image_height: int = Field(..., description="图像高度")


class Data(BaseModel):
    """响应数据"""
    result: DetectionResult = Field(..., description="检测结果")
    file_type: str = Field(default="", description="文件类型")
    file_data: str = Field(default="", description="文件数据")


class DetectionResponse(BaseModel):
    """Tamper detection API response."""
    x_request_id: str = Field(..., description="请求ID")
    msg: str = Field(default="success", description="响应消息")
    data: Data = Field(..., description="响应数据")
    code: int = Field(default=200, description="响应代码")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    service: str = "tamper-detection"
