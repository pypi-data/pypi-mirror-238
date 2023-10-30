# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 下午10:34
# @Author  : sudoskys
# @File    : base.py
# @Software: PyCharm
__version__ = "0.0.1"

import hashlib
import os
from typing import Union, List, Optional, Literal

import httpx
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, root_validator, validator, Field, HttpUrl, BaseSettings

from .action import Tokenizer, TokenizerObj
from ...error import ValidationError
from ...network import request
from ...schema import Message, Function

load_dotenv()

MODEL = Literal[
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4"
]


def sha1_encrypt(string):
    """
    sha1加密算法
    """

    sha = hashlib.sha1(string.encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts[:8]


class OpenaiResult(BaseModel):
    class Usage(BaseModel):
        prompt_tokens: int
        completion_tokens: int
        total_tokens: int

    class Choices(BaseModel):
        index: int
        message: Message = None
        finish_reason: str
        delta: dict = None

    id: str
    object: str
    created: int
    model: str
    choices: List[Choices]
    usage: Usage

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    @property
    def result_type(self):
        return self.object

    @property
    def default_message(self):
        return self.choices[0].message


class Openai(BaseModel):
    class Proxy(BaseSettings):
        proxy_address: str = Field(None, env="OPENAI_API_PROXY")  # "all://127.0.0.1:7890"

        class Config:
            env_file = '.env'
            env_file_encoding = 'utf-8'
            case_sensitive = True
            arbitrary_types_allowed = True

    class Driver(BaseSettings):
        """
        不允许部分更新
        """
        endpoint: HttpUrl = Field(default="https://api.openai.com/v1/chat/completions")
        api_key: str = Field(default=None)
        org_id: Optional[str] = Field(None)
        model: MODEL = Field(default="gpt-3.5-turbo-0613")

        # TODO:AZURE API VERSION
        @property
        def detail(self):
            """
            脱敏
            """
            api_key = "****" + str(self.api_key)[-4:]
            return f"Endpoint: {self.endpoint}\nApi_key: {api_key}\nOrg_id: {self.org_id}\nModel: {self.model}"

        @property
        def available(self):
            """
            检查可用性
            :return:
            """
            return all([self.endpoint, self.api_key, self.model])

        @classmethod
        def from_public_env(cls):
            openai_api_key = os.getenv("OPENAI_API_KEY", None)
            openai_endpoint = os.getenv("OPENAI_API_ENDPOINT", "https://api.openai.com/v1/chat/completions")
            openai_org_id = os.getenv("OPENAI_API_ORG_ID", None)
            openai_model = os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo")
            return cls(
                endpoint=openai_endpoint,
                api_key=openai_api_key,
                org_id=openai_org_id,
                model=openai_model
            )

        @validator("model")
        def check_model(cls, v):
            if v not in MODEL.__args__:
                raise ValidationError("model only support {}".format(MODEL.__args__))
            return v

        @validator("api_key")
        def check_key(cls, v):
            if v:
                if not str(v).startswith("sk-"):
                    logger.warning("Validator:api_key should start with `sk-`")
                if len(str(v)) < 4:
                    raise ValidationError("api_key is too short")
                # 严格检查
                # if not len(str(v)) == 51:
                #    raise ValidationError("api_key must be 51 characters long")
            else:
                raise ValidationError("api_key is required,pls set OPENAI_API_KEY in .env")
            return v

        @property
        def uuid(self):
            """
            取 api key 最后 3 位 和 sha1 加密后的前 8 位
            :return: uuid for token
            """
            _flag = self.api_key[-3:]
            return f"{_flag}:{sha1_encrypt(self.api_key)}"

        class Config:
            env_file = '.env'
            env_file_encoding = 'utf-8'
            case_sensitive = True
            arbitrary_types_allowed = True
            extra = "allow"

    config: Driver
    messages: List[Message]
    functions: Optional[List[Function]] = None

    function_call: Optional[str] = None
    """
    # If you want to force the model to call a specific function you can do so by setting function_call: {"name": "<insert-function-name>"}. 
    # You can also force the model to generate a user-facing messages_box by setting function_call: "none". 
    # Note that the default behavior (function_call: "auto") is for the model to decide on its own whether to call a function and if so which function to call.
    """

    temperature: Optional[float] = 1
    top_p: Optional[float] = None
    n: Optional[int] = 1

    # Bot于流式响应负载能力有限
    stream: Optional[bool] = False

    stop: Optional[Union[str, List[str]]] = None
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[dict] = None
    user: Optional[str] = None

    # 用于调试
    echo: Optional[bool] = False

    @property
    def model(self):
        return self.config.model

    @property
    def get_request_data(self):
        _arg = self.dict(exclude_none=True, exclude={"config", "echo"})
        _arg["model"] = self.model
        return _arg

    def get_proxy_settings(self):
        proxy = self.Proxy()
        return proxy

    @staticmethod
    def get_model_list():
        return MODEL.__args__

    @staticmethod
    def get_token_limit(model: str):
        v = 2048
        if "gpt-3.5" in model:
            v = 4096
        elif "gpt-4" in model:
            v = 8192
        if "-16k" in model:
            v = v * 4
        elif "-32k" in model:
            v = v * 4
        return v

    @validator("presence_penalty")
    def check_presence_penalty(cls, v):
        if not (2 > v > -2):
            raise ValidationError("presence_penalty must be between -2 and 2")
        return v

    @validator("stop")
    def check_stop(cls, v):
        if isinstance(v, list) and len(v) > 4:
            raise ValidationError("stop list length must be less than 4")
        return v

    @validator("temperature")
    def check_temperature(cls, v):
        if not (2 > v > 0):
            raise ValidationError("temperature must be between 0 and 2")
        return v

    @root_validator
    def check_root(cls, values):
        return values

    @staticmethod
    def parse_single_reply(response: dict) -> Message:
        """
        解析响应
        :param response:
        :return:
        """
        # check
        if not response.get("choices"):
            raise ValidationError("Message is empty")

        _message = Message.parse_obj(response.get("choices")[0].get("message"))
        return _message

    @staticmethod
    def parse_usage(response: dict):
        if not response.get("usage"):
            raise ValidationError("usage is empty")
        return response.get("usage").get("total_tokens")

    async def create(self,
                     **kwargs
                     ) -> OpenaiResult:
        """
        请求
        :return:
        """
        """
        curl https://api.openai.com/v1/completions \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer YOUR_API_KEY" \
        -d '{"model": "text-davinci-003", "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7}'
        """
        # check
        num_tokens_from_messages = TokenizerObj.num_tokens_from_messages(
            messages=self.messages,
            model=self.model,
        )
        if num_tokens_from_messages > self.get_token_limit(self.model):
            raise ValidationError("messages_box num_tokens > max_tokens")
        # Clear tokenizer encode cache
        TokenizerObj.clear_cache()
        # 返回请求
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Authorization": f"Bearer {self.config.api_key}",
            "api-key": f"{self.config.api_key}",
        }
        if self.config.org_id:
            headers["Openai-Organization"] = self.config.org_id
        try:
            _response = await request(
                method="POST",
                url=self.config.endpoint,
                data=self.get_request_data,
                headers=headers,
                proxy=self.get_proxy_settings().proxy_address,
                json_body=True
            )
            return_result = OpenaiResult.parse_obj(_response)
        except httpx.ConnectError as e:
            logger.error(f"Openai connect error: {e}")
            raise e
        if self.echo:
            logger.info(f"Openai response: {return_result}")
        return return_result
