import asyncio
import logging
import random
import time
from operator import itemgetter

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="games")
class GameCog(object):
    """
    Bet money on games
    """

    def __init__(self, bot: commands.Bot, storage: Storage):
        self.storage = storage
        self.bot = bot
        self.bet_going = False
        self.betters = {}

    @commands.command(name="start-bet")
    async def start_bet(self, ctx):
        if self.bet_going:
            await ctx.send("bet already running")
        else:
            self.bet_going = True
            self.betters = {}
            await ctx.send("Bet started, 1 minutes. your chances of being a winnner is based on how much of the total you bet! %bet <amount>, to enter! winnes split all the money put in.")
            await asyncio.sleep(60)
            
            if len(self.betters) == 0:
                await ctx.send("No bets given :-(")
                return
            
            total = sum(self.betters.values())
            logger.info("bet calculating")
            winners = []
            while len(winners) == 0:
                for player, bet in self.betters.items():
                    chance = bet / total
                    logger.debug(f"{player.owner} has a {chance * 100}% chance of winning")
                    winner = random.random() <= chance
                    if winner:  # or True:
                        logger.info(f"{player.owner} won")
                        winners.append(player)

            per_person = total // len(winners)
            for winner in winners:
                logger.debug(f"{winner.owner} got {per_person}G")
                winner.gold += per_person

            string = " ".join("@" + winner.owner for winner in winners)
            string += f" Won {per_person}G each!"
            await ctx.send(string)
            logger.info("Calculating done")

            self.bet_going = False

    @commands.command(name="bet")
    async def bet(self, ctx, amount: int):
        if not self.bet_going:
            await ctx.send("no bet going at the moment")
            return

        player = self.storage.game_data.get_player(ctx)
        if player is None:
            await ctx.send(f"@{ctx.author.name} you don't have a character")
            return

        if player in self.betters.keys():
            await ctx.send(f"@{player.owner} you have already put in a bet.")
            return

        if amount > player.gold:
            await ctx.send(f"@{player.owner} you don't have the amount of money.")
            return

        if amount <= 0:
            await ctx.send(f"@{player.owner} you cant bet 0G or lower.")
            return

        self.betters[player] = amount
        player.gold -= amount
        await ctx.send(f"@{player.owner} you put a {amount}G bet in! total is now {sum(self.betters.values())}G")