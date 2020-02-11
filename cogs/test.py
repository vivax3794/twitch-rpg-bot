import logging

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="test")
class TestCog(object):
    """
    Commands for testing
    """
    def __init__(self, bot: commands.Bot, storage: Storage):
        self.storage = storage
        self.bot = bot

    @commands.command(name="error")
    async def error(self, ctx: twitchio.Context) -> None:
        """
        print error.

        Print latest error from self.storage.latest_error.
        :param ctx: Command Context
        :return: None
        """
        logger.info("error command activated")
        await ctx.channel.send(str(self.storage.latest_error))

    @commands.command(name="test")
    async def test(self, ctx: twitchio.Context) -> None:
        """
        print message.

        Prints as message to chat to test that it's online.

        :param ctx: Command context
        :return: None
        """
        logger.info("test command activated")
        await ctx.channel.send("/me bot is online :-)")
        
    @commands.command(name="make_error")
    async def make_error(self, ctx: twitchio.Context) -> None:
        """
        create error.

        Raises a error to check that error handling works.

        :param ctx: Command Context
        :return: None
        """
        logger.info("make_error command activated")
        raise ValueError("test test")