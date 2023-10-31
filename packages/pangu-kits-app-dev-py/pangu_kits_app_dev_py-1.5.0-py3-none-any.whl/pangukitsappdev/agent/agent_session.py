#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from typing import Optional, List

from langchain.schema import BaseMessage
from pydantic import BaseModel
from pangukitsappdev.agent.agent_action import AgentAction


class AgentSession(BaseModel):
    """
    Agent运行Session，包含历史Action，当前Action，状态
    Attributes:
        messages: 本次session的用户的输入
        session_id: UUID，在一个session内唯一
        history_action: 历史Action
        current_action: 当前Action
        agent_session_status: Agent状态
    """
    messages: List[BaseMessage]
    session_id: str
    history_action: List[AgentAction]
    current_action: Optional[AgentAction]
    agent_session_status: str
