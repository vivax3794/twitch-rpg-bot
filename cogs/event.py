import asyncio
import concurrent
import logging
import random

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="event")
class EventCog(object):
    """
    stores all events, except error handlers
    """
    def __init__(self, bot: commands.Bot, storage: Storage):
        self.storage = storage
        self.bot = bot

    async def event_ready(self) -> None:
        """
        Print welcome message

        :return: None
        """
        logger.debug("ready function ran.")
        ws = self.bot._ws

        channel: str = self.bot.initial_channels[0]
        channel: twitchio.Channel = self.bot.get_channel(channel)
        try:
            # await asyncio.wait_for(fut, timeout=5)
            streamer_info = await asyncio.wait_for(channel.get_stream(), timeout=10)
        except concurrent.futures._base.TimeoutError as e:
            logger.error("Error, timeout getting streamer.")
            await asyncio.sleep(2)
        else:
            if streamer_info is not None:
                streamer_name = streamer_info["user_name"]
                self.storage.game_data.streamer_name = streamer_name
            else:
                logger.error(self.storage.bot_config.CHANNEL, "Error, streamer returned as None.")
                await asyncio.sleep(2)

        await ws.send_privmsg(self.storage.bot_config.CHANNEL, f"/me has landed!")
        logger.info("Bot is online")

    async def event_message(self, message: twitchio.Message) -> None:
        """
        Print all chat message to chat for debugging.
        :param message:
        :return: None
        """
        logger.debug(f"MESSAGE: {message.author.name}: {message.content}")
        # self.storage.save()
