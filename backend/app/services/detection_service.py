"""Tamper detection service (stub: replace with real model inference)."""
import base64
import io
import uuid
from pathlib import Path

from PIL import Image

from backend.app.config import get_settings
from backend.app.schemas.detection import DetectionResponse, PSResult, ImageProperty, DetectionResult, Data


class DetectionService:
    """图像篡改检测服务。当前为占位实现，可替换为实际深度学习模型推理。"""

    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "tiff", "tif", "webp", "gif"}

    def __init__(self):
        self.settings = get_settings()

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
            image_width, image_height = img.size
        except Exception as e:
            # 生成请求ID
            x_request_id = str(uuid.uuid4())
            # 创建错误响应
            return DetectionResponse(
                x_request_id=x_request_id,
                msg=f"图像解析失败: {e}",
                data=Data(
                    result=DetectionResult(
                        image_width=0,
                        image_property=ImageProperty(
                            ps=PSResult(
                                tampered_positions=[],
                                is_tampered=False,
                                image="",
                                tampered_scores=[]
                            )
                        ),
                        image_height=0
                    ),
                    file_type="",
                    file_data=""
                ),
                code=400
            )

        # 保存文件到temp目录
        file_path = self._save_to_temp(raw, filename)

        # 占位逻辑：可根据图片尺寸等做简单规则，或调用真实模型
        # 添加sleep 5秒的效果，模拟处理过程
        import time
        time.sleep(5)
        # 此处返回示例结果，便于前端联调
        is_tampered = self._stub_detect(raw)

        # 生成请求ID
        x_request_id = str(uuid.uuid4())

        # 将图片转换为Base64编码
        image_base64 = base64.b64encode(raw).decode('utf-8')

        # 创建响应结构
        ps_result = PSResult(
            tampered_positions=[[464, 718, 593, 718, 593, 762, 464, 762]] if is_tampered else [],
            is_tampered=is_tampered,
            image=image_base64,  # 返回图像的Base64编码
            tampered_scores=[[1]] if is_tampered else []
        )

        image_property = ImageProperty(ps=ps_result)

        detection_result = DetectionResult(
            image_width=image_width,
            image_property=image_property,
            image_height=image_height
        )

        data = Data(
            result=detection_result,
            file_type=filename.split('.')[-1].lower() if '.' in filename else '',
            file_data=""
        )

        return DetectionResponse(
            x_request_id=x_request_id,
            msg="success",
            data=data,
            code=200
        )

    def _stub_detect(self, raw: bytes) -> bool:
        """占位检测逻辑（可替换为模型推理）。"""
        # 示例：根据文件大小做简单区分，实际应调用篡改检测模型
        return len(raw) % 2 == 0

    def _save_to_temp(self, raw: bytes, filename: str) -> Path:
        """
        保存文件到temp目录
        :param raw: 图片二进制数据
        :param filename: 原始文件名
        :return: 保存路径
        """
        # 生成唯一文件名
        unique_id = str(uuid.uuid4())
        ext = filename.split('.')[-1].lower() if '.' in filename else 'jpg'
        temp_filename = f"{unique_id}.{ext}"
        temp_path = self.settings.temp_dir / temp_filename

        # 保存文件
        with open(temp_path, 'wb') as f:
            f.write(raw)

        return temp_path


def get_detection_service() -> DetectionService:
    return DetectionService()
