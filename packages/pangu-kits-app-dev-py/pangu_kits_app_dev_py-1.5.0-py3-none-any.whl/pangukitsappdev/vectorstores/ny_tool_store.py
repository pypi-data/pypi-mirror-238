#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from __future__ import annotations
import logging
from typing import Any, List, Optional, Tuple
import requests
from langchain.docstore.document import Document
from langchain.vectorstores.base import VectorStore
from pydantic import BaseModel
from pangukitsappdev.api.memory.vector.vector_config import VectorStoreConfig

logger = logging.getLogger(__name__)


class NyToolVectorStore(VectorStore):
    class ToolMeta(BaseModel):
        tool_ids: List[str]
        tool_desc: str

    def __init__(self, store_config: VectorStoreConfig):
        self.store_config = store_config

    def add_tools(self, tools: List[ToolMeta]):
        """添加工具，调试阶段，产品化后调整
        :param tools: 工具列表
        """
        metadatas = []
        for tool in tools:
            metadatas.append({'toolIds': tool.tool_ids, 'toolDesc': tool.tool_desc})
        return self.add_texts(texts=[], metadatas=metadatas)

    def search_tools(self, query: str, top_k: int, score_threshold: float) -> List[str]:
        """查询工具，返回id列表
        :param query: 查询语句
        :param top_k: 返回前k条
        :param score_threshold: 阈值
        """
        docs = self.similarity_search(query, top_k, score_threshold)
        tool_ids = []
        for doc in docs:
            tool_ids += doc.metadata.get("toolIds")
        return tool_ids

    def add_texts(self, texts: List[str], metadatas: Optional[List[dict]] = None, **kwargs: Any) -> List[str]:
        request_body = {
            "function": "database",
            "content": metadatas
        }

        headers = {"Content-Type": "application/json"}
        base_url = self.store_config.server_info.get_urls()[0]
        proxies = self.store_config.http_config.requests_proxies()
        rsp = requests.post(base_url, headers=headers, json=request_body, proxies=proxies)

        if 200 != rsp.status_code:
            rsp.raise_for_status()

        return texts


    def similarity_search(
            self, query: str, k: int = 5, score_threshold: float = 0.2, **kwargs: Any
    ) -> List[Document]:
        doc_with_scores = self.similarity_search_with_score(query, k, score_threshold, **kwargs)
        return [doc_with_score[0] for doc_with_score in doc_with_scores if doc_with_score[1] <= score_threshold]

    def similarity_search_with_score(
            self, query: str, k: int = 5, score_threshold: float = 0.2,
            **kwargs: Any
    ) -> List[Tuple[Document, float]]:
        request_body = {
            "function": "query",
            "content": query
        }

        headers = {"Content-Type": "application/json"}
        base_url = self.store_config.server_info.get_urls()[0]
        proxies = self.store_config.http_config.requests_proxies()
        rsp = requests.post(base_url, headers=headers, json=request_body, proxies=proxies)

        if 200 != rsp.status_code:
            rsp.raise_for_status()
        docs = []
        retriever_outputs = rsp.json()
        for retriever_output in retriever_outputs:
            docs.append((Document(page_content=retriever_output.get("toolDesc"), metadata=retriever_output), 0.0))
        return docs

    @classmethod
    def from_texts(
            cls,
            store_config: VectorStoreConfig,
            texts: List[str],
            metadatas: Optional[List[dict]] = None,
            **kwargs: Any,
    ) -> NyToolVectorStore:
        """Construct ElasticVectorSearch wrapper from raw documents.
        """
        ny_tool_store = cls(store_config)
        ny_tool_store.add_texts(
            texts, metadatas=metadatas, **kwargs
        )
        return ny_tool_store
