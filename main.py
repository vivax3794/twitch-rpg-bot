import logging
from typing import Optional

import twitchio
from twitchio.ext import commands

from classes.storage import Storage

logging.basicConfig(
    level=logging.DEBUG,
    format=" %(asctime)s [%(name)s %(lineno)s] %(levelname)s -> %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("bot.log", mode="w+"),
        logging.StreamHandler()
    ]
)

for logger in ["websockets.client", "websockets.protocol", "twitchio.websocket", "asyncio"]:
    logging.getLogger(logger).disabled = True

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    """
    The top bot class
    """
    def __init__(self, storage: Storage):

        super().__init__(
            irc_token=storage.bot_config.TMI_TOKEN,
            client_id=storage.bot_config.CLIENT_ID,
            nick=storage.bot_config.BOT_NICK,
            prefix=storage.bot_config.BOT_PREFIX,
            initial_channels=[storage.bot_config.CHANNEL]
        )

        self.storage = storage
        logger.debug("__init__ done")

    def add_cog_with_args(self, name: str) -> None:
        """
        load a cog based on it's file name

        load the file with the name 'name',
        then find a object with "Cog" in the name and runs that object.
        then calls self.add_cog with the cog, passing the cog it's self and self.storage

        :param name: the file name of the cog
        :return:None
        """
        # load file
        cog_module = getattr(__import__(f"cogs.{name}"), name)

        # find cog object
        object_names = dir(cog_module)
        for object_name in object_names:
            if "Cog" in object_name:
                cog_class = getattr(cog_module, object_name)
                break

        # load cog
        cog = cog_class(self, self.storage)
        self.add_cog(cog)
        logger.info(f"Loaded cog: {object_name}")
        
    def load_cogs(self) -> None:
        """
        Load all the cogs defined in self.storage.bot_config.COGS
        :return: None
        """
        for cog_name in self.storage.bot_config.COGS:
            self.add_cog_with_args(cog_name)

    async def event_command_error(self, ctx: twitchio.Context, error: Exception):
        """
        on error save it and log it.
        :param ctx: The command context of the command that triggered it.
        :param error: the error that was raised
        :return:
        """
        self.storage.latest_error = error
        logger.exception(f"Command error triggered")

    async def event_error(self, error: Exception, data=None):
        """
        on error save it and log it.
        :param ctx: The command context of the command that triggered it.
        :param error: the error that was raised
        :return:
        """
        self.storage.latest_error = error
        logger.exception(f"Event error triggered")

    @commands.command(name="help")
    async def help(self, ctx: twitchio.Context) -> None:
        await ctx.send("https://docs.google.com/document/d/10AL1wO-QCxW7J1b66fa9b-4qUX0kp_UYVkXcXxOHm7E")


logger.info("==============================")
if __name__ == "__main__":
    logger.debug("Starting bot")
    storage = Storage()
    bot = Bot(storage)
    bot.load_cogs()
    bot.run()

# MAYBE: make a exploding creeper.
# MAYBE: make item's level locked.
