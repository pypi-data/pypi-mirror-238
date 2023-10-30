# -*- coding: utf-8 -*-
__package__name__ = "llmkira.extra.plugins.alarm"
__plugin_name__ = "set_alarm_reminder"
__openapi_version__ = "20231027"

from llmkira.sdk.func_calling import verify_openapi_version

verify_openapi_version(__package__name__, __openapi_version__)

import datetime
import re
import time

from loguru import logger
from pydantic import validator, BaseModel

from llmkira.receiver.aps import SCHEDULER
from llmkira.schema import RawMessage
from llmkira.sdk.endpoint.openai import Function
from llmkira.sdk.func_calling import PluginMetadata, BaseTool
from llmkira.sdk.func_calling.schema import FuncPair
from llmkira.task import Task, TaskHeader

alarm = Function(name=__plugin_name__, description="Set a timed reminder (only for minutes)")
alarm.add_property(
    property_name="delay",
    property_description="The delay time, in minutes",
    property_type="integer",
    required=True
)
alarm.add_property(
    property_name="content",
    property_description="reminder content",
    property_type="string",
    required=True
)


class Alarm(BaseModel):
    delay: int
    content: str

    class Config:
        extra = "allow"

    @validator("delay")
    def delay_validator(cls, v):
        if v < 0:
            raise ValueError("delay must be greater than 0")
        return v


class AlarmTool(BaseTool):
    """
    搜索工具
    """
    silent: bool = False
    function: Function = alarm
    keywords: list = ["闹钟", "提醒", "定时", "到点", '分钟']
    pattern = re.compile(r"(\d+)(分钟|小时|天|周|月|年)后提醒我(.*)")
    require_auth: bool = True

    # env_required: list = ["SCHEDULER", "TIMEZONE"]

    def pre_check(self):
        return True

    def func_message(self, message_text, **kwargs):
        """
        如果合格则返回message，否则返回None，表示不处理
        """
        for i in self.keywords:
            if i in message_text:
                return self.function
        # 正则匹配
        if self.pattern:
            match = self.pattern.match(message_text)
            if match:
                return self.function
        return None

    async def failed(self, task: TaskHeader, receiver, arg, exception, **kwargs):
        _meta = task.task_meta.reply_notify(
            plugin_name=__plugin_name__,
            callback=TaskHeader.Meta.Callback(
                role="function",
                name=__plugin_name__
            ),
            write_back=True,
            release_chain=True
        )
        await Task(queue=receiver.platform).send_task(
            task=TaskHeader(
                sender=task.sender,
                receiver=receiver,
                task_meta=_meta,
                message=[
                    RawMessage(
                        user_id=receiver.user_id,
                        chat_id=receiver.chat_id,
                        text=f"{__plugin_name__} Run failed {exception}"
                    )
                ]
            )
        )

    async def callback(self, task, receiver, arg, result, **kwargs):
        return None

    async def run(self, task: TaskHeader, receiver: TaskHeader.Location, arg, **kwargs):
        """
        处理message，返回message
        """
        _set = Alarm.parse_obj(arg)
        _meta = task.task_meta.child(__plugin_name__)
        _meta.callback_forward = True
        _meta.callback_forward_reprocess = False
        _meta.callback = TaskHeader.Meta.Callback(
            role="function",
            name=__plugin_name__
        )

        async def _send(receiver, _set):
            await Task(queue=receiver.platform).send_task(
                task=TaskHeader(
                    sender=task.sender,  # 继承发送者
                    receiver=receiver,  # 因为可能有转发，所以可以单配
                    task_meta=_meta,
                    message=[
                        RawMessage(
                            user_id=receiver.user_id,
                            chat_id=receiver.chat_id,
                            text=_set.content
                        )
                    ]
                )
            )

        logger.debug("Plugin:set alarm {} minutes later".format(_set.delay))
        SCHEDULER.add_job(
            func=_send,
            id=str(time.time()),
            trigger="date",
            replace_existing=True,
            run_date=datetime.datetime.now() + datetime.timedelta(minutes=_set.delay),
            args=[receiver, _set]
        )
        try:
            SCHEDULER.start()
        except Exception as e:
            pass
        await Task(queue=receiver.platform).send_task(
            task=TaskHeader(
                sender=task.sender,  # 继承发送者
                receiver=receiver,  # 因为可能有转发，所以可以单配
                task_meta=_meta,
                message=[
                    RawMessage(
                        user_id=receiver.user_id,
                        chat_id=receiver.chat_id,
                        text=f"🍖 The alarm is now set,just wait for {_set.delay} min!"
                    )
                ]
            )
        )


__plugin_meta__ = PluginMetadata(
    name=__plugin_name__,
    description="Set a timed reminder (only for minutes)",
    usage="set_alarm_reminder 10 minutes later remind me to do something",
    openapi_version=__openapi_version__,
    function={
        FuncPair(function=alarm, tool=AlarmTool)
    },
    homepage="https://github.com/LlmKira"
)
