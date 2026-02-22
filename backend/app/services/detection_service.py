"""Tamper detection service (stub: replace with real model inference)."""
import io

from PIL import Image

from backend.app.schemas.detection import DetectionResponse, DetectionResultItem


class DetectionService:
    """图像篡改检测服务。当前为占位实现，可替换为实际深度学习模型推理。"""

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp", "gif"}

    def __init__(self):
        pass

    def detect_from_bytes(self, raw: bytes, filename: str = "") -> DetectionResponse:
        """
        从图片字节流执行篡改检测。
        :param raw: 图片二进制数据
        :param filename: 原始文件名（用于判断格式）
        :return: 检测结果
        """
        try:
            img = Image.open(io.BytesIO(raw))
            img.load()
        except Exception as e:
            return DetectionResponse(
                success=False,
                is_tampered=False,
                result_items=[],
                message=f"图像解析失败: {e}",
            )

        # 占位逻辑：可根据图片尺寸等做简单规则，或调用真实模型
        # 此处返回示例结果，便于前端联调
        result_items = [
            DetectionResultItem(field_name="is_tampered", content="有篡改" if self._stub_detect(raw) else "无篡改"),
            DetectionResultItem(field_name="ps", content=""),
        ]
        is_tampered = self._stub_detect(raw)

        return DetectionResponse(
            success=True,
            is_tampered=is_tampered,
            result_items=result_items,
            heatmap_url=None,  # 可后续返回热力图 Base64 或 URL
        )

    def _stub_detect(self, raw: bytes) -> bool:
        """占位检测逻辑（可替换为模型推理）。"""
        # 示例：根据文件大小做简单区分，实际应调用篡改检测模型
        return len(raw) % 2 == 0


def get_detection_service() -> DetectionService:
    return DetectionService()
