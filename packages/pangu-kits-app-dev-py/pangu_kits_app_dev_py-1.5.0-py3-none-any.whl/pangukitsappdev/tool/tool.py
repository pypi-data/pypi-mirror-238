#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
from typing import Optional, Type, Union, Callable, Any
from pydantic import BaseModel
from pydantic.typing import NoneType

from pangukitsappdev.prompt.prompt_tmpl import PromptTemplates
from pangukitsappdev.api.tool.base import AbstractTool, PanguFunction, DEFAULT_SINGLE_ARG


class Tool(AbstractTool):
    tool_input_schema: Optional[str]
    tool_output_schema: Optional[str]
    pangu_function: Optional[str]

    def _run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Use the tool."""
        if self.func:
            return self.func(*args, **kwargs)
        raise NotImplementedError("Tool does not support sync")

    def get_input_schema(self) -> str:
        if not self.tool_input_schema:
            self.tool_input_schema = self.build_tool_schema(self.input_desc, self.input_type)
        return self.tool_input_schema

    def get_output_schema(self) -> str:
        if not self.tool_output_schema:
            self.tool_output_schema = self.build_tool_schema(self.output_desc, self.output_type)
        return self.tool_output_schema

    def get_pangu_function(self) -> str:
        if not self.pangu_function:
            self.pangu_function = self.build_pangu_function()
        return self.pangu_function

    @staticmethod
    def build_tool_schema(desc: str, class_type: Union[Type, BaseModel]):
        desc = "空" if class_type == NoneType else desc
        if class_type in [int, float, str, bool, list, dict, NoneType]:
            return PromptTemplates.get("agent_tool_simple_schema").format(desc=desc,
                                                                          type=class_type.__name__)
        # 复杂类型返回JSON schema
        return PromptTemplates.get("agent_tool_json_schema"). \
            format(desc=desc, schema={"properties": class_type.schema().get('properties')})

    def build_pangu_function(self):
        return PanguFunction(name=self.get_tool_id(),
                             description=self.get_tool_name(),
                             principle=self.principle,
                             arguments=self.get_pang_tool_schema(self.input_desc, self.input_type),
                             results=self.get_pang_tool_schema(self.output_desc,
                                                               self.output_type)).json(ensure_ascii=False)

    @staticmethod
    def get_pang_tool_schema(desc: str, class_type: Union[Type, BaseModel]) -> dict:
        desc = "空" if class_type == NoneType else desc
        arguments = {}
        # 基本类型
        if class_type in [int, float, str, bool, NoneType]:
            arguments.update({DEFAULT_SINGLE_ARG: f"{class_type.__name__}: {desc}"})
            return arguments
        # 复杂类型(BaseModel子类)
        properties = class_type.schema().get('properties')
        for field in properties:
            arguments.update({field: f"{properties[field].get('type')}: {properties[field].get('description')}"})
        return arguments

    @classmethod
    def from_function(
            cls,
            func: Optional[Callable],
            name: str,
            description: str,
            principle: str,
            input_desc: str,
            output_desc: str,
            args_schema: Optional[Type[BaseModel]] = None,
            return_type: Optional[Type] = None
    ) -> AbstractTool:
        """Initialize tool from a function."""
        if func is None:
            raise ValueError("Function must be provided")
        return cls(
            name=name,
            func=func,
            description=description,
            principle=principle,
            input_desc=input_desc,
            output_desc=output_desc,
            args_schema=args_schema,
            return_type=return_type
        )
