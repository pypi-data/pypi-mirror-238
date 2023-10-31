#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from abc import abstractmethod, ABC
from typing import List
from pangukitsappdev.api.tool.base import AbstractTool


class ToolProvider(ABC):
    """工具实例化提供者，通过toolId列表给出实例化工具
    """
    @abstractmethod
    def provide(self, tool_ids: List[str]) -> List[AbstractTool]:
        """通过id查找工具
        Args:
            tool_ids: 工具id
        Returns: 工具列表
        """
