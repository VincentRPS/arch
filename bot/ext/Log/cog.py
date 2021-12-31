# Advanced logging built into arch.
# Logs most events available in disnake.

#############
## Imports ##
#############

import asyncio
import time
import os
import typing
import aiohttp
import logging
import random
from disnake.ext import commands
from disnake import Webhook
from dotenv import load_dotenv

load_dotenv()

#########
## Cog ##
#########


class LogCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
        self.webhook = Webhook.from_url(
            os.getenv("logging_webhook"), session=self._session
        )

    # an easier send function to WebHooks
    async def send(
        self,
        message: str,
        avatar: typing.Optional[
            str
        ] = "https://cdn.discordapp.com/attachments/925935640544149585/926464382706278461/16074589.png",
        username: typing.Optional[str] = "arch",
    ):
        await asyncio.sleep(random.randint(10, 30))
        await self.webhook.send(content=message, username=username, avatar_url=avatar)
        time.sleep(random.randint(10, 30))
        pass

    @commands.Cog.listener()
    async def on_socket_event_type(self, event_type):
        return await self.send(message=f"on_socket_event_type: {event_type}")

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        return await self.send(message=f"on_socket_raw_receive: {msg}")

    @commands.Cog.listener()
    async def on_socket_raw_send(self, payload):
        return await self.send(message=f"on_socket_raw_sen: {payload}")

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        return await self.send(
            message=f"on_typing: channel: {channel}, user: {user}, when: {when}"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        return await self.send(message=f"on_message: {message}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        return await self.send(message=f"on_message_delete: {message}")

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        return await self.send(message=f"on_bulk_message_delete: {messages}")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        return await self.send(message=f"on_raw_message_delete: {payload}")

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        return await self.send(message=f"on_raw_bulk_message_delete: {payload}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        return await self.send(
            message=f"on_message_edit: before: {before}, after: {after}"
        )

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        return await self.send(message=f"on_raw_message_edit: {payload}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        return await self.send(
            message=f"on_reaction_add: reaction: {reaction}, user: {user}"
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        return await self.send(message=f"on_raw_reaction_add: {payload}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        return await self.send(
            message=f"on_reaction_remove: reaction: {reaction}, user: {user}"
        )

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        return await self.send(message=f"on_raw_reaction_remove: {payload}")

    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        return await self.send(
            message=f"on_reaction_clear: message: {message}, reactions: {reactions}"
        )

    @commands.Cog.listener()
    async def on_raw_reaction_clear(self, payload):
        return await self.send(message=f"on_raw_reaction_clear: {payload}")

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, reaction):
        return await self.send(message=f"on_reaction_clear_emoji: {reaction}")

    @commands.Cog.listener()
    async def on_raw_reaction_clear_emoji(self, payload):
        return await self.send(message=f"on_raw_reaction_clear_emoji: {payload}")

    # todo on_interaction on..


def setup(bot):
    bot.add_cog(LogCog(bot))
