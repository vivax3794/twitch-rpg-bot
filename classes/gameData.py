import json
import logging
import random
from typing import Dict, List, Iterable, Optional

import twitchio

from classes.dice import Dice
from classes.gameSettings import GameSettings
from classes.item import new_item, Item
from classes.monster import Monster
from classes.player import Player
from classes.shop import Shop

logger = logging.getLogger(__name__)

class GameData(object):
    """
    Store all the data for the game it self.
    """
    game_settings = GameSettings()

    players: Dict[str, Player] = {}
    monsters: Dict[str, Monster] = {}
    monster_data: Dict[str, Dict] = {}
    level_data: List[Dict[str, str]] = []
    item_data: Dict[str, Dict[str, any]] = {}
    event_data: List[Dict[str, any]] = []
    shop = Shop()
    streamer_name = "streamer name"

    def load(self) -> None:
        """
        Load all the info from disk
        :return: None
        """
        self.load_level_data()
        self.load_items()
        self.load_event_data()
        self.load_players()
        self.load_monsters()
        self.shop.load_shop(self.item_data.values())

    def save(self) -> None:
        """
        save all the info to disk
        :return: None
        """
        self.save_players(self.players.values())

    def add_player(self, user: twitchio.User, *args: List[any]) -> Player:
        """
        Add a new player to the player list

        :param user: the user object that created the player
        :param args: the args to pass to the Player constructor
        :return: The new player added
        """
        player = Player(user, *args, game_data=self)
        self.players[player.owner] = player
        return player

    def get_player(self, ctx) -> Optional[Player]:
        """
        Return the player from the ctx, if the user does not have a character return None
        :param ctx: The Command Context for the player
        :return: The player, None if not found
        """
        if type(ctx) == str:
            name = ctx.lower()
        else:
            name = ctx.author.name.lower()

        if name in self.players.keys():
            logger.info(f"player found for {name}")
            return self.players[name]
        else:
            logger.info(f"NO player found for {name}")
            return None

    @staticmethod
    def save_players(players: Iterable[Player]) -> None:
        """
        Save the players data
        :param players: The players to save
        :return: None
        """
        players_as_dict = []
        for player in players:
            players_as_dict.append(player.to_dict())

        with open("data/players.json", "w+") as f:
            json.dump(players_as_dict, f, indent=4)

    def load_players(self) -> None:
        """
        load in players from disk.
        :return: None
        """
        self.players = {}
        with open("data/players.json") as f:
            player_data_list = json.load(f)

        for player_data in player_data_list:
            player = Player.from_dict(player_data, self)
            owner = player.owner
            self.players[owner] = player

    def get_monster(self, name: str) -> Optional[Monster]:
        """
        Returns a stored monster object from it's name
        :param name: The name of the monster
        :return: The monster object, if not found return None
        """
        if name in self.monsters.keys():
            return self.monsters[name]
        else:
            return None

    def add_monster(self, name: str) -> Optional[Monster]:
        """
        Adds a monster to the game
        return True if found, if not returns False

        :param name: The name (type) of monster to add
        :return: If monster was found
        """
        if name in self.monster_data.keys() and name not in self.monsters.keys():
            if name == "streamer":
                if self.streamer_name not in self.monsters.keys():
                    monster = Monster(self.monster_data[name], self)
                    monster.name = self.streamer_name
                    self.monsters[self.streamer_name] = monster
                else:
                    return None
            else:
                monster = Monster(self.monster_data[name], self)
                self.monsters[name] = monster
            return monster
        else:
            return None

    def remove_monster(self, monster: Monster) -> None:
        """
        Removes monster, from the monster list.

        :param monster: The monster to remove
        :return: None
        """
        del self.monsters[monster.name]

    def load_monsters(self) -> None:
        """
        Load monster data from disk
        :return: None
        """
        with open("data/monsters.json") as f:
            self.monster_data = json.load(f)

    # MAYBE: make levels dynamic?
    def load_level_data(self) -> None:
        """
        load the level info from disk
        :return: None
        """
        with open("data/level.json") as f:
            self.level_data = json.load(f)

    # MAYBE: move this onto the player?
    def load_level_data_to_player(self, player: Player, level: int):
        """
        Set the attrs of a player object to the level data.

        :param player: The player to level up
        :param level: The level to set
        :return: None
        """
        if level <= len(self.level_data):
            level_data = self.level_data[level - 1]
            player.attack = Dice.from_string(level_data["attack"])
            player.defence = Dice.from_string(level_data["defence"])

    def get_item(self, item_name: str) -> Optional[Item]:
        logger.info(f"getting item: {item_name}")
        logger.debug(str(self.item_data))
        if item_name in self.item_data.keys():
            return new_item(self.item_data[item_name])
        else:
            return None

    def load_items(self):
        with open("data/items.json") as f:
            self.item_data = json.load(f)

    def get_random_event_data(self) -> Dict[str, any]:
        return random.choice(self.event_data)

    def load_event_data(self):
        with open("data/events.json") as f:
            self.event_data = json.load(f)

