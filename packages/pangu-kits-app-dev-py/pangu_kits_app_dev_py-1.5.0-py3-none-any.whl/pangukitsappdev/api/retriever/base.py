#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from abc import ABC, abstractmethod
from typing import List, Optional
from pangukitsappdev.api.tool.base import AbstractTool


class ToolRetriever(ABC):
    """工具检索器接口类
    """
    @abstractmethod
    def add(self, tools: List[AbstractTool]) -> List[str]:
        """
        工具入库
        :param tools: tools工具
        :return: 添加的工具id列表
        """

    @abstractmethod
    def search(self, query: str,
               top_k: Optional[int] = None,
               score_threshold: Optional[float] = None) -> List[AbstractTool]:
        """
        工具检索
        :param query: 查询语句
        :param top_k: top k条
        :param score_threshold: 评分阈值
        :return: 相似工具列表
        """

    @abstractmethod
    def remove(self, tools: List[AbstractTool]):
        """
        删除工具
        :param tools: tools工具
        """