import logging

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="inventory")
class InventoryCog(object):
    def __init__(self, bot: commands.Bot, storage: Storage):
        self.bot = bot
        self.storage = storage

    @commands.command(name="inventory")
    async def inventory(self, ctx: twitchio.Context, arg1=None, arg2=None, arg3=None):
        logger.info(f"invetory callled: {arg1}, {arg2}")
        player = self.storage.game_data.get_player(ctx)

        if player is None:
            await ctx.send('sorry no character found, create one :-) %create "character name"')
            return

        if arg1 is None:
            string = str(player.inventory)
        elif arg2 is None:
            item = player.inventory.get_item(arg1)
            if item is not None:
                string = item.description
            else:
                string = "Item not found"
        elif arg1 == "use":
            item = player.inventory.get_item(arg2)
            logger.debug(f"player selected item : {arg2}, object gotten: {item}")
            if item is not None:
                logger.info(f"using {item.name}")
                monster = self.storage.game_data.get_monster(str(arg3))
                could_use = item.use(player, monster)
                logger.info(f"player could use item: {could_use}")
                if could_use:
                    string = item.used
                else:
                    string = item.cant_use
            else:
                string = "Item not found"
        else:
            string = "Invalid arguments"
        await ctx.send(string)
