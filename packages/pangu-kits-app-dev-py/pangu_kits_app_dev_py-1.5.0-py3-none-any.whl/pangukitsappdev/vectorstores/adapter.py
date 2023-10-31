#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.

try:
    from langchain.vectorstores import VectorStore
except ImportError:
    from langchain.schema.vectorstore import VectorStore

from pangukitsappdev.api.memory.vector.base import AbstractVectorApi
from pangukitsappdev.api.memory.vector.vector_config import VectorStoreConfig
from pangukitsappdev.vectorstores.css_store import CSSVectorSearch


class CSSVectorApi(AbstractVectorApi):
    def create_vector_store(self, vector_config: VectorStoreConfig) -> VectorStore:
        config = {
            "elasticsearch_url": vector_config.server_info.get_urls(),
            "index_name": vector_config.index_name,
            "embedding": vector_config.embedding,
            "verify_certs": vector_config.verify_certs,
            "proxies": vector_config.http_config.requests_proxies()
        }

        return CSSVectorSearch(**config)

    def clear(self):
        if not self.vector_store.client.indices.exists(self.vector_store.index_name):
            return
        # 插件模式下不清除索引
        if self.vector_config.embedding:
            self.vector_store.client.indices.delete(index=self.vector_store.index_name)
        else:
            delete_query = {
                "query": {
                    "match_all": {}
                }
            }
            # 发送删除请求
            self.vector_store.client.delete_by_query(index=self.vector_store.index_name,
                                                     body=delete_query)
