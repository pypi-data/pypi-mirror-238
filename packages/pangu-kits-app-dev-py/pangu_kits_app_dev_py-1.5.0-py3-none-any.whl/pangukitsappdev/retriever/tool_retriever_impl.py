#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from typing import List, Optional
from pangukitsappdev.api.common_config import HttpConfig
from pangukitsappdev.api.memory.vector.vector_config import VectorStoreConfig
from pangukitsappdev.api.retriever.base import ToolRetriever
from pangukitsappdev.api.tool.base import AbstractTool
from pangukitsappdev.tool.tool_provider import ToolProvider
from pangukitsappdev.vectorstores.ny_tool_store import NyToolVectorStore


class ToolRetrieverImpl(ToolRetriever):
    def __init__(self, tool_provider: ToolProvider, vector_store_config: VectorStoreConfig):
        self.tool_provider = tool_provider
        vector_store_config.http_config = HttpConfig(env_prefix="sdk.memory.tool.proxy")
        self.ny_tool_vector = NyToolVectorStore(vector_store_config)

    def add(self, tools: List[AbstractTool]) -> List[str]:
        # 保存ny向量检索信息
        tool_metas = [NyToolVectorStore.ToolMeta(tool_ids=[tool.get_tool_id()],
                                                 tool_desc=tool.get_tool_name() + "，" + tool.principle)
                      for tool in tools]
        return self.ny_tool_vector.add_tools(tool_metas)

    def search(self, query: str,
               top_k: Optional[int] = 5,
               score_threshold: Optional[float] = 0.2) -> List[AbstractTool]:
        tool_ids = self.ny_tool_vector.search_tools(query, top_k, score_threshold)
        return self.tool_provider.provide(tool_ids)

    def remove(self, tools: List[AbstractTool]):
        # ny向量库不支持删除
        pass
