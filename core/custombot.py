import asyncio

import aiohttp
import toml
from discord.ext import commands

from .context import ComicsContext


class ComicsBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.afk = {}
        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()
        self.config = toml.load('config.toml')

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or ComicsContext)

    async def start(self, token, *, reconnect=True):
        await self.load_extension('jishaku')
        await self.load_extension("cogs.gocomics")
        import os

        os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
        os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'
        os.environ['JISHAKU_HIDE'] = 'True'
        await self.reload_extension('jishaku')
        return await super().start(token, reconnect=reconnect)

    async def close(self):
        await self.session.close()
        return await super().close()

    async def on_message_edit(self, before, after):
        ...

    async def on_ready(self):
        print("The bot is ready")
