# -*- coding: utf-8 -*-
# @Time    : 2023/8/17 下午8:18
# @Author  : sudoskys
# @File    : app.py
# @Software: PyCharm
import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()
__area__ = "sender"


def run():
    import asyncio

    from llmkira import load_plugins
    from llmkira.sdk import load_from_entrypoint, get_entrypoint_plugins
    from .discord import DiscordBotRunner
    from .kook import KookBotRunner
    from .rss import RssAppRunner
    from .slack import SlackBotRunner
    from .telegram import TelegramBotRunner

    # 初始化插件系统
    load_plugins("llmkira/extra/plugins")
    load_from_entrypoint("llmkira.extra.plugin")

    loaded_message = "\n >>".join(get_entrypoint_plugins())
    logger.success(f"\n===========Third Party Plugins Loaded==========\n >>{loaded_message}")

    async def _main():
        await asyncio.gather(
            # 异步事件
            TelegramBotRunner().run(),
            RssAppRunner().run(interval=60 * 60 * 1),
            DiscordBotRunner().run(),
            KookBotRunner().run(),
            SlackBotRunner().run(),
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_main())
