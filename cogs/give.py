import logging

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="give")
class GiveCog(object):
    """
    Give command managed here
    """

    def __init__(self, bot: commands.Bot, storage: Storage):
        self.storage = storage
        self.bot = bot

    @commands.command(name="give")
    async def give(self, ctx, item_name, amount: int, r_player):
        logger.info(f"Give command called {item_name}, {amount}, {r_player}")
        s_player = self.storage.game_data.get_player(ctx)
        r_player = self.storage.game_data.get_player(r_player.replace("@", ""))

        if s_player is None:
            await ctx.send("you don't have a character")
            return
        elif r_player is None:
            await ctx.send("receiving player not found.")
            return

        if item_name == "gold":
            if s_player.gold < amount:
                await ctx.send("You don't have enough gold to give away.")
            else:
                s_player.gold -= amount
                r_player.gold += amount
                await ctx.send(f"given {amount}G to @{r_player.owner}")
        else:
            items = []
            for _ in range(amount):
                item = s_player.inventory.get_item(item_name)
                if item is None:
                    for item in items:
                        s_player.inventory.add_item(item)
                    await ctx.send(f"item not found, or you are trying to give to many")
                    return
                else:
                    s_player.inventory.remove_item(item)
                    items.append(item)
            if item_name == "rotting pear":
                if r_player.inventory.get_item("anti-pear amulet") is not None:
                    for item in items:
                        s_player.inventory.add_item(item)
                    s_player.health -= 2
                    s_player.health = min(s_player.health, 1)
                    await ctx.send("The pears fly back at you for some reason, -2 health. ( you wont died from this)")
                    return
            for item in items:
                r_player.inventory.add_item(item)
            await ctx.send(f"given {amount} {item_name} to @{r_player.owner}")