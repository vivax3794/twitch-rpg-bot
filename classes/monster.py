import logging
from typing import Dict

from classes.dice import Dice
from classes.player import Player

logger = logging.getLogger(__name__)


class Monster(object):
    """
    Stores info on a monster, also contains methods related to them.
    """
    def __init__(self, monster_data: Dict[str, any], game_data: "GameData"):
        self.name = monster_data["name"]
        self.icon = monster_data["icon"]
        self.attack = Dice.from_string(monster_data["attack"])
        self.defence = Dice.from_string(monster_data["defence"])
        self.reward = monster_data["reward"]
        self.health = monster_data["health"]

        self.game_data = game_data
        logger.info(f"monster made: {self.name}")

    def __str__(self) -> str:
        return f"{self.icon} {self.name} [{self.health}]"

    def calculate_dmg(self, player: Player):
        """
        calculates the dmg  the player and monster does.

        :param player: The player that deals / get dealt dmg to
        :return: player_dmg, monster_dmg
        """
        player_attack_roll = player.attack.roll()
        player_defence_roll = player.defence.roll()

        monster_attack_roll = self.attack.roll()
        monster_defence_roll = self.defence.roll()

        player_dmg = max(player_attack_roll - monster_defence_roll, 0)
        monster_dmg = max(monster_attack_roll - player_defence_roll, 0)

        logger.info(f"PLayer dmg: {player_dmg}, monster dmg: {monster_dmg}")

        return player_dmg, monster_dmg

    def fight(self, player: Player) -> str:
        """
        Resoles a fight and return a string explaining it

        :param player: The player that fights
        :return: the string to respond with
        """
        player_dmg, monster_dmg = self.calculate_dmg(player)

        monster_died = self.take_dmg(player_dmg)
        if monster_died:
            logger.info("Player killed monster")
            player.get_reward(self.reward)
            string = self.player_killed_monster_string(player, player_dmg)
            return string
        else:
            player_died = player.take_dmg(monster_dmg)
            if player_died:
                logger.info("Monster killed player")
                return self.player_died_response(player, monster_dmg, player_dmg)
            else:
                logger.info("Nobody died")
                return self.player_fight_draw_string(player, monster_dmg, player_dmg)

    def take_dmg(self, dmg: int) -> bool:
        """
        Deals dmg to the monster, returning True if it monster died, False if not.

        :param dmg: The dmg dealt to the monster
        :return: If the monster player_killed_monster_string.
        """
        self.health -= dmg
        if self.health < 0:
            self.health = 0
        if self.health == 0:
            self.game_data.remove_monster(self)
        return self.health == 0

    def player_killed_monster_string(self, player: Player, player_dmg: int) -> str:
        """
        Returns a string for when the monster player killed the monster from a player attack.

        :param player: The player that killed the monster
        :param player_dmg: The dmg the player dealt
        :return: The string made.
        """
        return (
            f"{player.name} hit {self.name} for {player_dmg} dmg, {self.name} hp: {self.health}; "
            f"{player.name} killed {self.name } and got {self.reward['gold']} gold and {self.reward['xp']} xp"
        )

    def player_died_response(self, player: Player, monster_dmg: int, player_dmg: int):
        """
        Generate response for when the player died.
        (player dying is handled by the player class)

        :param player: The player that died
        :param monster_dmg: The dmg the monster did
        :param player_dmg: The dmg the player did
        :return: The string calculated
        """
        return (
            f"{player.name} hit {self.name} for {player_dmg} dmg, {self.name} hp: {self.health}; "
            f"{self.name} hit {player.name} for {monster_dmg}, {player.name} hp: 0; "
            f"I am sorry to tell you this {player.name}, but you are dead. "
            "you will find your xp (not levels), items and gold removed. "
            "the game also saved."
        )

    def player_fight_draw_string(self, player: Player, monster_dmg: int, player_dmg: int) -> str:
        """
        make string for when neither the monster or player dies

        :param player: The player the is fighting
        :param monster_dmg: The dmg the monster did
        :param player_dmg: The dmg the player did
        :return: The created string
        """
        return (
            f"{player.name} hit {self.name} for {player_dmg} dmg, {self.name} hp: {self.health}; "
            f"{self.name} hit {player.name} for {monster_dmg}, {player.name} hp: {player.health}; "
        )
