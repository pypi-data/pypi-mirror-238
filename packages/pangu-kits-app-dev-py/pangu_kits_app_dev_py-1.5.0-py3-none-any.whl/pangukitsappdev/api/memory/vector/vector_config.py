#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from typing import Optional

from pydantic import Field

from pangukitsappdev.api.common_config import ServerInfo, HttpConfig
from pangukitsappdev.api.config_loader import SdkBaseSettings
from pangukitsappdev.api.embeddings.base import EmbeddingApi


class ServerInfoCss(ServerInfo):

    def get_urls(self) -> [str]:
        return self.get_http_urls()


class VectorStoreConfig(SdkBaseSettings):
    """
    向量库相关配置
    Attributes:
        store_name: 存储名称
        server_info: ServerInfoCss，存储服务器链接相关信息，默认使用sdk.store.css前缀的配置
        index_name: 索引名称
        embedding: embedding库
        distance_strategy: 检索模式，默认使用内积inner_product
        text_key: 文本内容字段名
        metadata_key: 扩展元数据字段名
        vector_key: 向量内容字段名
        bulk_size: 文本入库时， 每批次记录数； 默认50， 受向量库及模型能力影响
        ttl: 老化时间，单位 秒；向量存储场景，默认不设置TTL
        verify_certs: 是否校验https的证书。默认是True
        http_config: http代理配置
    """

    store_name: Optional[str]
    server_info: ServerInfo = Field(default_factory=lambda: ServerInfoCss(env_prefix="sdk.memory.css"))
    index_name: Optional[str]
    embedding: Optional[EmbeddingApi]
    distance_strategy: str = Field(default="inner_product")
    text_key: str = Field(default="text")
    metadata_key: str = Field(default="metadata")
    vector_key: str = Field(default="vector")
    bulk_size: int = Field(default=50)
    ttl: Optional[int]
    verify_certs: bool = Field(default=True)
    http_config: HttpConfig = Field(default_factory=lambda: HttpConfig(env_prefix="sdk.memory.css.proxy"))
