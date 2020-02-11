import logging
import random

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="fight")
class FightCog(object):
    def __init__(self, bot: commands.Bot, storage: Storage):
        self.bot = bot
        self.storage = storage

    @commands.command(name="fight")
    async def fight(self, ctx: twitchio.Context, monster_name: str):
        """
        Fight a monster

        :param ctx: The command Context
        :param monster_name: The monster name
        :return: None
        """
        monster = self.storage.game_data.get_monster(monster_name)
        player = self.storage.game_data.get_player(ctx)

        if player is None:
            await ctx.send("you need to make a character first")
            return None

        if monster is None:
            await ctx.send("Monster not found")
        else:
            response_string = monster.fight(player)
            await ctx.send(response_string)

    @commands.command(name="spawn")
    async def spawn(self, ctx: twitchio.Context, monster_name: str) -> None:
        """
        Spawn a new monster.

        spawns a monster from it's name, locked to vivax.

        :param ctx: The command context
        :param monster_name: The name of the monster to spawn
        :return: None
        """
        if ctx.author.name == "vivax3794":
            monster = self.storage.game_data.add_monster(monster_name)
            if monster is None:
                await ctx.send("Monster not found or already added")
            else:
                await ctx.send(f"monster {monster.name} {monster.icon} added :-)")
        else:
            await ctx.send("Sorry, only vivax may use this command")

    @commands.command(name="monsters")
    async def monsters(self, ctx: twitchio.Context) -> None:
        """
        Prints current monsters.

        :param ctx: the Command Context
        :return: None
        """
        monster_string = "; ".join(map(str, self.storage.game_data.monsters.values()))
        if monster_string:
            await ctx.send(monster_string)
        else:
            await ctx.send("No monsters in the area.")

    @commands.command(name="set_spawn")
    async def set_spawn(self, ctx: twitchio.Context, new_spawn: float) -> None:
        """
        Change the monsters spawn rate

        :param ctx: command context
        :param new_spawn: The new spawn rate
        :return: None
        """
        if ctx.author.name == "vivax3794":
            logger.info(f"Chanced enemy spawn rate to {new_spawn}")
            self.storage.game_data.game_settings.enemy_spawn_rate = new_spawn
            await ctx.send(f"Chanced enemy spawn rate to {new_spawn}")
        else:
            await ctx.send("You need to be vivax to use this command")