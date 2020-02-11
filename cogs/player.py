import logging
from typing import Optional

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="player")
class PlayerCog(object):
    """
    Commands related to player creation and stats
    """
    def __init__(self, bot: commands.Bot, storage: Storage):
        self.bot = bot
        self.storage = storage

    @commands.command(name="create")
    async def create(self, ctx: twitchio.Context, name: str) -> None:
        """
        create a new player

        :param ctx: Command context
        :param name: The name of the character
        :return: None
        """
        logger.info("create command activated")
        player = self.storage.game_data.get_player(ctx)
        if player is None:
            self.storage.game_data.add_player(ctx.author, name)
            await ctx.send(f"Welcome {name} to vivlaxia!")
        else:
            await ctx.send(f"This mind looks familiar, did {player.name} not have this mind?")

    @commands.command(name="stats")
    async def stats(self, ctx: twitchio.Context) -> None:
        """
        Print a players stats

        :param ctx: Command Context
        :return: None
        """
        logger.info("stats command activated")
        player = self.storage.game_data.get_player(ctx)
        if player is not None:
            string = player.stats
            await ctx.send(string)
        else:
            await ctx.send("you need to create a character first.")