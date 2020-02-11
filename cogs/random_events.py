import asyncio
import logging
import random
import time

import twitchio
from twitchio.ext import commands

from classes.event import new_event
from classes.storage import Storage

logger = logging.getLogger(__name__)


@commands.core.cog(name="event")
class RandomEventCog(object):
    """
    Random events triggered here :-)
    """

    def __init__(self, bot: commands.Bot, storage: Storage):
        self.storage = storage
        self.bot = bot

    async def event_message(self, message: twitchio.Message) -> None:
        """
        have a chance to trigger a random event on message

        :param message: The message object
        :return: None
        """

        if message.author.name.lower() == self.storage.bot_config.BOT_NICK.lower():
            return

        if message.content.startswith(self.storage.bot_config.BOT_NICK):
            return

        player = self.storage.game_data.players.get(message.author.name)
        if player is None:
            return

        chance = random.random()
        logger.debug(f"Chance for ranndom event: {chance}")
        if chance <= self.storage.game_data.game_settings.event_spawn_rate:
            event_data = self.storage.game_data.get_random_event_data()
            event = new_event(event_data)
            event.activate(player)
            message_to_send = f"@{player.owner} {event.message}"
            await message.channel.send(message_to_send)
            extra_messages = event.kwargs.get("extra messages")
            if extra_messages is not None:
                for message_to_send in extra_messages:
                    await asyncio.sleep(event.kwargs["time"])
                    await message.channel.send(message_to_send)
            return

        chance = random.random()
        logger.debug(f"Chance to spawn monster: {chance}")
        if chance <= self.storage.game_data.game_settings.enemy_spawn_rate:
            monster_name = random.choice(list(self.storage.game_data.monster_data.keys()))
            logger.debug(f"Trying to add monster: {monster_name}")
            monster = self.storage.game_data.add_monster(monster_name)
            if monster is not None:
                logger.info(f"added {monster.name} from chat, chance.")
                await message.channel.send(f"A wild {monster.name} {monster.icon} has joined the battle field!")

    @commands.command(name="event")
    async def command_event(self, ctx, index: int):
        if ctx.author.name == "vivax3794":
            player = self.storage.game_data.get_player(ctx)
            event_data = self.storage.game_data.event_data[index]
            event = new_event(event_data)
            event.activate(player)
            message_to_send = f"@{player.owner} {event.message}"
            await ctx.send(message_to_send)
            extra_messages = event.kwargs.get("extra messages")
            if extra_messages is not None:
                for message in extra_messages:
                    time.sleep(event.kwargs["time"])
                    await ctx.send(message)
            return
        else:
            await ctx.send("Sorry, only vivax may use this command")
