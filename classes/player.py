import logging
from typing import Dict, Union

import twitchio

from classes.dice import Dice
from classes.inventory import Inventory

logger = logging.getLogger(__name__)


class Player(object):
    """
    Stores info on a player.
    """

    def __init__(self, user: Union[twitchio.User, str], name: str, game_data: "GameData"):
        if type(user) == twitchio.User:
            self.owner = user.name
        else:
            self.owner = user

        self.name = name
        self.health = 40
        self.gold = 0
        self.dead = False
        self.attack = Dice(0, 0, 0)
        self.defence = Dice(0, 0, 0)

        self.game_data = game_data

        self.xp = 0
        self.level = 0
        self.gain_level()

        self.inventory = Inventory()

        self.item_data = {}
        for _ in "_" * 10:
            item = self.game_data.get_item("air")
            self.inventory.add_item(item)

    @property
    def stats(self):
        return (
            f"{self.name}, owned by {self.owner} -> "
            f"health: [{self.health}/40], "
            f"gold: [{self.gold}], "
            f"[lvl: {self.level}, xp: {self.xp}], "
            f"Attack: {self.attack}, defence: {self.defence}"
        )

    def to_dict(self) -> Dict[str, any]:
        """
        Return the object as a dict for saving
        :return: The dict created
        """
        return {
            "owner": self.owner,
            "name": self.name,
            "health": self.health,
            "gold": self.gold,
            "xp": self.xp,
            "level": self.level,
            "inventory": self.inventory.as_dict(),
            "item_data": self.item_data
        }

    @classmethod
    def from_dict(cls, player_data: Dict[str, any], game_data: "GameData") -> "Player":
        """
        User to load a user from a dict, used to load from disk.

        :param player_data: The player data to load
        :param game_data: A reference to the GameData object.
        :return: New player
        """
        player = cls(player_data["owner"], player_data["name"], game_data)
        player.health = player_data["health"]
        player.gold = player_data["gold"]
        player.xp = player_data["xp"]
        player.level = player_data["level"] - 1
        player.gain_level()
        player.inventory.load_from_dict(player_data["inventory"], game_data)
        player.item_data = player_data["item_data"]

        return player

    def take_dmg(self, dmg: int) -> bool:
        """
        take dmg, returns if the player died

        :param dmg: The dmg to take
        :return: Did the player die from the dmg
        """

        logger.info(f"{self.name} lost {dmg} health")
        self.health -= dmg
        if self.health < 0:
            self.health = 0

        if self.health == 0:
            self.died()
            return True
        else:
            return False

    def died(self) -> None:
        """
        The player has died.

        remove xp and gold, and set health to 20 (half of max health)

        :return: None
        """

        self.dead = True
        logger.info(f"{self.name} just died")
        self.gold = 0
        self.xp = 0
        self.health = 5

        self.inventory = Inventory()
        for _ in "_" * 10:
            item = self.game_data.get_item("air")
            self.inventory.add_item(item)

        self.game_data.save()

    def get_reward(self, reward_dict: Dict[str, int]) -> None:
        """
        Add rewards to the player
        :param reward_dict: The dict with "gold" and "xp" keys.
        :return: None
        """
        self.gold += reward_dict["gold"]
        self.get_xp(reward_dict["xp"])

    def get_xp(self, xp: int) -> None:
        """
        Gain xp
        :param xp: the to gain
        :return: None
        """
        self.xp += xp
        while self.xp >= 100:
            self.gain_level()
            self.xp -= 100

    def gain_level(self):
        """
        Gain a level
        :return: None
        """
        self.level += 1
        self.game_data.load_level_data_to_player(self, self.level)

