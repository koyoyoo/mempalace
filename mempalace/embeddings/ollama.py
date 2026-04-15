"""
Ollama embedding provider for MemPalace.

支持使用 Ollama 本地模型服务生成文本嵌入向量，
可替代 ChromaDB 默认的 ONNX embedding 模型。
"""

import os
from typing import Any, Dict, List, Optional, Union

import requests


class OllamaEmbeddingFunction:
    """
    ChromaDB-compatible embedding function using Ollama API.

    自动适配 ChromaDB 的 EmbeddingFunction 协议：
    - __call__(texts: List[str]) -> List[List[float]]
    - 支持同步批量 embedding 生成

    Args:
        model: Ollama 模型名称，默认为 "qwen3-embedding"
        base_url: Ollama API 基础 URL，默认从环境变量 OLLAMA_BASE_URL 读取，
                  或使用 http://localhost:11434
        timeout: 请求超时时间（秒），默认 30 秒

    Raises:
        requests.RequestException: Ollama 服务不可用时
        ValueError: 响应格式无效时

    Example:
        >>> from mempalace.embeddings import OllamaEmbeddingFunction
        >>> ef = OllamaEmbeddingFunction(model="qwen3-embedding")
        >>> embeddings = ef(["hello world", "another text"])
    """

    def __init__(
        self,
        model: str = "qwen3-embedding",
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.model = model
        self.base_url = (
            base_url or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        ).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()

    def __call__(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        生成文本的 embedding 向量。

        Args:
            texts: 单个字符串或字符串列表

        Returns:
            浮点数向量的列表，每个向量对应一个输入文本
        """
        if isinstance(texts, str):
            texts = [texts]
        if not texts:
            return []

        # 批量请求 Ollama API
        url = f"{self.base_url}/api/embed"
        payload: Dict[str, Any] = {
            "model": self.model,
            "input": texts,
        }

        try:
            response = self._session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(f"Ollama embedding request failed: {e}") from e

        data = response.json()

        # 解析响应格式
        # Ollama /api/embed 返回: {"embeddings": [[...], [...]]}
        embeddings = data.get("embeddings")
        if not isinstance(embeddings, list) or len(embeddings) != len(texts):
            raise ValueError(f"Unexpected Ollama response format: {data}")

        return embeddings

    def __repr__(self) -> str:
        return f"OllamaEmbeddingFunction(model={self.model!r}, base_url={self.base_url!r})"
