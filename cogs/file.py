import asyncio
import concurrent
import logging

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="file")
class FileCog(object):
    """
    has all commands which has with files to do
    """
    def __init__(self, bot: commands.Bot, storage: Storage):
        self.storage = storage
        self.bot = bot

    @commands.command(name="save")
    async def save(self, ctx: twitchio.Context) -> None:
        """
        save all data.

        Invoke self.storage.save()

        :param ctx:  Command Context
        :return: None
        """
        logger.info("Save command activated")
        self.storage.save()
        await ctx.channel.send("/me Saved all json data")

    @commands.command(name="load")
    async def load_command(self, ctx: twitchio.Context) -> None:
        """
        load all data.

        invokes: self.storage.save()

        :param ctx: The command Context
        :return: None
        """
        logger.info("load command activated")

        if ctx.author.name.lower() == "vivax3794":
            self.storage.load()

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
                    logger.error("Error, streamer returned as None.")
                    await asyncio.sleep(2)

            await ctx.channel.send("/me reloaded all json data")
        else:
            await ctx.channel.send("/me Hey you are not vivax? who are you?! where is my vivax?!!")
