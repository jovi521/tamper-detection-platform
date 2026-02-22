"""LangChain AI 分析链：多模态二次验证与摘要（可选集成）。"""
from typing import Optional

from backend.app.config import get_settings


def get_ai_analysis_chain():
    """
    返回 LangChain 分析链实例（可选）。
    需配置 OPENAI_API_KEY 或其它多模态模型后启用。
    """
    settings = get_settings()
    if not settings.enable_ai_chain or not settings.openai_api_key:
        return None
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough

        llm = ChatOpenAI(
            model="gpt-4o",  # 或多模态模型
            api_key=settings.openai_api_key,
            temperature=0,
        )

        def chain_input(x: dict):
            prompt = (
                "你是一个图像篡改检测的二次验证专家。"
                "根据以下检测结果摘要，给出简短分析结论（是否同意篡改判定、风险建议等），控制在 2-3 句话内。\n"
                f"摘要: {x.get('summary', '无')}"
            )
            return [HumanMessage(content=prompt)]

        chain = (
            RunnablePassthrough.assign(summary=lambda x: x.get("summary", ""))
            | chain_input
            | llm
            | StrOutputParser()
        )
        return chain
    except ImportError:
        return None


def run_ai_analysis(summary: str, image_base64: Optional[str] = None) -> Optional[str]:
    """
    运行 AI 分析链，对检测结果做二次验证或生成报告摘要。
    :param summary: 检测结果摘要文本
    :param image_base64: 可选，图片 Base64 用于多模态模型
    :return: 分析文本，未启用时返回 None
    """
    chain = get_ai_analysis_chain()
    if chain is None:
        return None
    try:
        result = chain.invoke({"summary": summary, "image_base64": image_base64 or ""})
        return result if isinstance(result, str) else str(result)
    except Exception:
        return None
