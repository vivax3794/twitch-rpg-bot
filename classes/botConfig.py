from typing import List


class BotConfig(object):
    """
    Stores the options for the setup of the bot.
    """
    TMI_TOKEN = "oauth:token"  # the bot accounts OAuth
    CLIENT_ID = "token"  # the bot's Client id
    BOT_NICK = "TheRealVivax"  # bot nick name
    BOT_PREFIX = "%"  # command prefix
    CHANNEL = "beginbot"  # twitch channel to be in
    COGS: List[str] = [
        "event",  # logging messages, and ready message
        "file",  # loading and saving commands.
        "test",  # testing commands
        "player",  # player creation and stats commands
        "fight",  # fight command
        "inventory",  # inventory command
        "random_events",  # random events
        "shop",  # shop command
        "give",  # give comma€nds
        "games"  # play a game of dice rolling.
    ]  # cogs to load

