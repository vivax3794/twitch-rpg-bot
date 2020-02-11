import logging
from typing import Optional

from classes.botConfig import BotConfig
from classes.gameData import GameData

logger = logging.getLogger(__name__)


class Storage(object):
    """
    The root storage object
    stored references to all other Storage objects,
    """
    bot_config = BotConfig()
    game_data = GameData()
    latest_error: Optional[Exception] = None

    def __init__(self):
        self.load()

    def load(self) -> None:
        """
        Load all the info from disk
        :return: None
        """
        logger.info("loading files")
        self.game_data.load()
        logger.info("loading done")

    def save(self) -> None:
        """
        save all the info to disk
        :return: None
        """
        logger.info("saving files")
        self.game_data.save()
        logger.info("saving done")