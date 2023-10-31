#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from __future__ import unicode_literals
import logging
import uuid
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import List, Union, Optional
from langchain.schema import BaseMessage, ChatMessage
from pangukitsappdev.agent.agent_action import AgentAction
from pangukitsappdev.agent.agent_session import AgentSession
from pangukitsappdev.api.llms.base import LLMApi, to_message_in_req
from pangukitsappdev.api.retriever.base import ToolRetriever
from pangukitsappdev.api.tool.base import AbstractTool

logger = logging.getLogger(__name__)


class AgentListener(ABC):
    """Agent监听，允许对Agent的各个阶段进行处理
    """
    @abstractmethod
    def on_session_start(self, agent_session: AgentSession):
        """
        Session启动时调用
        :param agent_session: AgentSession
        """

    @abstractmethod
    def on_session_iteration(self, agent_session: AgentSession):
        """
        Session迭代过程中调用
        :param agent_session: AgentSession
        """
    @abstractmethod
    def on_session_end(self, agent_session: AgentSession):
        """
        Session结束时调用
        :param agent_session: AgentSession
        """


class Agent(ABC):

    @abstractmethod
    def add_tool(self, tool: AbstractTool):
        """
        为Agent增加工具类
        :param tool: Tool
        """

    @abstractmethod
    def remove_tool(self, tool: AbstractTool):
        """
        删除tool
        :param tool: Tool
        """

    @abstractmethod
    def run(self, prompt: Union[List[BaseMessage], str]) -> str:
        """
        执行agent
        :param prompt: 用户的输入, 支持多轮List[BaseMessage]或str
        :return: 计划的结果
        """

    @abstractmethod
    def set_max_iterations(self, iterations: int):
        """
        设置最大迭代次数
        :param iterations: 次数
        """

    @abstractmethod
    def set_tool_retriever(self, tool_retriever: ToolRetriever):
        """
        设置工具检索器
        :param tool_retriever: 工具检索器
        """

    @abstractmethod
    def add_listener(self, agent_listener: AgentListener):
        """
        添加一个Agent监听器
        :param agent_listener: Agent监听器
        """


class AbstractAgent(Agent):
    FINAL_ACTION = "FINAL_ANSWER"

    def __init__(self, llm: LLMApi):
        """
        构造一个agent
        :param llm: LLMApi
        """
        self.llm = llm
        self.tool_map: dict[str, AbstractTool] = {}
        self.max_iterations = 15
        self.agent_listener: Optional[AgentListener] = None
        self.tool_retriever: Optional[ToolRetriever] = None

    def add_tool(self, tool: AbstractTool):
        tool_id = tool.get_tool_id()
        if not tool_id or tool_id in self.tool_map.keys():
            raise ValueError("tool_name must not be empty or repeat")
        self.tool_map.update({tool_id: tool})

    def remove_tool(self, tool: AbstractTool):
        self.tool_map.pop(tool.get_tool_id())

    def run(self, prompt: Union[List[BaseMessage], str]) -> str:
        """
        执行agent
        :param prompt: 用户的输入, 支持多轮List[BaseMessage]或str
        :return: 计划的结果
        """
        messages = [ChatMessage(role="user", content=prompt)] if isinstance(prompt, str) else prompt
        # tool检索器处理
        self.init_tool_from_retriever(messages)

        agent_session = self.notice_session_start(messages)
        try:
            self.react(agent_session)
        except (ValueError, JSONDecodeError, TypeError) as e:
            logger.debug("run error when call react", e)
            self.notice_session_end(agent_session)
            raise e

        self.notice_session_end(agent_session)
        actions = agent_session.history_action
        if not actions:
            return "no action has been taken"
        self.print_plan(agent_session)
        return str(actions[-1].action_input)

    @abstractmethod
    def react(self, agent_session: AgentSession):
        """
        迭代解决问题
        :param agent_session: 历史迭代几率
        """

    def add_listener(self, agent_listener: AgentListener):
        self.agent_listener = agent_listener

    def set_max_iterations(self, iterations: int):
        if iterations <= 0:
            raise ValueError("iterations value not legal.")
        self.max_iterations = iterations

    def set_tool_retriever(self, tool_retriever: ToolRetriever):
        self.tool_retriever = tool_retriever

    def notice_session_start(self, messages: List[BaseMessage]):
        agent_session = AgentSession(messages=messages,
                                     session_id=str(uuid.uuid4()),
                                     history_action=[],
                                     agent_session_status="INIT")
        if self.agent_listener:
            self.agent_listener.on_session_start(agent_session)
        return agent_session

    def notice_session_iteration(self, agent_session: AgentSession, action: AgentAction):
        agent_session.history_action.append(action)
        agent_session.agent_session_status = "RUNNING"

        if self.agent_listener:
            self.agent_listener.on_session_iteration(agent_session)

    def notice_session_end(self, agent_session: AgentSession):
        agent_session.agent_session_status = "FINISHED"
        if self.agent_listener:
            self.agent_listener.on_session_end(agent_session)
        if agent_session.current_action:
            agent_session.history_action.append(agent_session.current_action)

    def tool_execute(self, tool: AbstractTool, tool_input: Union[str, dict], agent_session: AgentSession):
        tool_result = tool.run(tool_input)
        action = agent_session.current_action
        if isinstance(tool_result, (str, int, float, bool)):
            action.observation = str(tool_result)
        else:
            action.observation = tool_result.json(ensure_ascii=False)
        self.notice_session_iteration(agent_session, action)

    def print_plan(self, agent_session: AgentSession):
        log_msg = "\n"
        for message in agent_session.messages:
            msg_dict = to_message_in_req(message)
            log_msg += f"{msg_dict.get('role')}: {msg_dict.get('content')}\n"
        log_msg += "计划已执行完成,自动编排步骤:"
        for i, action in enumerate(agent_session.history_action):
            thought = action.thought.replace("\n", "")
            log_msg += f"\n步骤{i + 1}:\n思考:{thought}"
            if self.is_final(action):
                log_msg += "\n问题已求解:"
            else:
                log_msg += f"\n行动:使用工具[{action.action}],传入参数{action.action_input}\n工具返回:{action.observation}"
        logger.info(log_msg)

    def is_final(self, action: AgentAction) -> bool:
        return action.action == self.FINAL_ACTION

    @staticmethod
    def sub_str_between(origin_str: str, start_str: str, end_str: str):
        if origin_str:
            start_pos = origin_str.find(start_str)
            if start_pos != -1:
                end_pos = origin_str.find(end_str)
                if end_pos != -1:
                    return origin_str[start_pos + len(start_str): end_pos]
        return ""

    @staticmethod
    def sub_str_before(origin_str: str, separator: str):
        if origin_str:
            if not separator:
                return ""
            else:
                pos = origin_str.find(separator)
                return origin_str if pos == -1 else origin_str[:pos]
        else:
            return origin_str

    @staticmethod
    def sub_str_after(origin_str: str, separator: str):
        if origin_str:
            if separator == "":
                return ""
            else:
                pos = origin_str.find(separator)
                return "" if pos == -1 else origin_str[pos + len(separator):]
        else:
            return origin_str

    @staticmethod
    def remove_start(origin_str: str, remove: str):
        if origin_str and remove:
            return origin_str[len(remove):] if origin_str.startswith(remove) else origin_str
        else:
            return origin_str

    @staticmethod
    def convert_role_to_desc(text: str):
        if text == "user":
            return "用户"
        elif text == "assistant":
            return "助手"
        elif text == "system":
            return "系统"
        else:
            raise ValueError("Agent message role only support user, assistant or system！")

    def check_max_iteration(self, agent_session: AgentSession):
        if len(agent_session.history_action) >= self.max_iterations:
            logger.debug("stopped due to iteration limit. maxIterations is %s", self.max_iterations)
            raise ValueError("stopped due to iteration limit.")

    def init_tool_from_retriever(self, messages: List[BaseMessage]):
        if self.tool_retriever is None:
            return

        query = ""
        for message in reversed(messages):
            if to_message_in_req(message).get("role") == "user":
                query = message.content
                break
        if not query:
            return
        tools = self.tool_retriever.search(query)
        self.tool_map.clear()
        for tool in tools:
            self.add_tool(tool)

    def get_system_prompt(self, agent_session: AgentSession):
        # 优先取设置到的LLM人设
        system_prompt = self.llm.get_llm_config().llm_module_config.system_prompt
        if system_prompt is not None:
            return system_prompt
        # 其次取message中最后一个人设
        for message in reversed(agent_session.messages):
            if to_message_in_req(message).get("role") == "system":
                return message.content
        return None
