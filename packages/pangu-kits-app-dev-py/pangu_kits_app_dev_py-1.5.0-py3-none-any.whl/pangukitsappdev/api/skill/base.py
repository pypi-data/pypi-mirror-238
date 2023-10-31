#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from abc import ABC, abstractmethod
from typing import Any, Dict

from langchain.schema.prompt_template import BasePromptTemplate
from langchain.chains.llm import LLMChain

from pangukitsappdev.api.llms.base import LLMApi
from pangukitsappdev.api.llms.llm_config import LLMParamConfig


class Skill(ABC):

    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> str:
        """
        执行Executor
        :param inputs: 输入的参数，基本上都是用来渲染prompt_template的
        :return: 执行结果，LLM的返回结果
        """
        pass


class SimpleSkill(Skill):
    """
    一个Executor的简单实现，传递prompt_template和llm_api两个参数即可，面向api包下面的接口编程
    """

    def __init__(self, prompt_template: BasePromptTemplate, llm_api: LLMApi):
        self.prompt_template = prompt_template
        self.llm_api = llm_api

    def execute(self, inputs: Dict[str, Any], param_config: LLMParamConfig = None) -> str:
        prompt = self.prompt_template.format(**inputs)
        return self.llm_api.ask(prompt, param_config).answer


class ChainWrappedSkill(Skill):
    """
    通过封装一个Chain来实现Executor，方便集成langchain预置的一些chain
    """

    def __init__(self, chain: LLMChain):
        self.chain = chain

    def execute(self, inputs: Dict[str, Any]) -> str:
        # 默认返回output_keys的第一个元素所代表的输出内容，一般都是回答
        chain_output_key = self.chain.output_keys[0]

        return self.chain(inputs)[chain_output_key]
