#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from typing import Optional

from pydantic import Field

from pangukitsappdev.api.common_config import IAMConfig, OpenAIConfig, HttpConfig, IAMConfigWrapper
from pangukitsappdev.api.config_loader import SdkBaseSettings


class EmbeddingConfig(SdkBaseSettings):
    embedding_name: Optional[str] = Field(default="default_embedding_name")
    css_url: Optional[str] = Field(env="sdk.embedding.css.url")
    iam_config: IAMConfig = Field(default_factory=IAMConfigWrapper(env_prefix="sdk.embedding.css.iam").get_iam_config)
    openai_config: OpenAIConfig = Field(default_factory=OpenAIConfig)
    http_config: HttpConfig = Field(default_factory=lambda: HttpConfig(env_prefix="sdk.embedding.css.proxy"))
