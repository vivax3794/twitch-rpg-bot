import logging

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="shop")
class ShopCog(object):
    """
    Shop command managed here
    """

    def __init__(self, bot: commands.Bot, storage: Storage):
        self.storage = storage
        self.bot = bot

    @commands.command(name="shop")
    async def shop(self, ctx: twitchio.Context, shop_name=None, item=None, action=None) -> None:
        logger.debug(f"{shop_name}, {item}, {action}")
        if shop_name is None:
            await ctx.send(self.storage.game_data.shop.main_shop_string)
        elif item is None:
            await ctx.send(self.storage.game_data.shop.shop_string(shop_name))
        elif action is None:
            await ctx.send(self.storage.game_data.shop.item_dec(shop_name, item))
        elif action.strip() == "buy":
            player = self.storage.game_data.get_player(ctx)
            await ctx.send(self.storage.game_data.shop.buy(player, shop_name, item))
        else:
            await ctx.send("Invalid arguments")
