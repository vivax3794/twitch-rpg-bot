import logging
import random

logger = logging.getLogger(__name__)


class Dice(object):
    """
    Object to store dice
    """
    def __init__(self, times: int, dice_type: int, changer: int):
        self.times = times
        self.dice_type = dice_type
        self.changer = changer

        # set to get more info for debugging
        self.dice = []

    def __str__(self):
        if self.changer > 0:
            return f"{self.times}d{self.dice_type} + {self.changer}"
        else:
            return f"{self.times}d{self.dice_type} - {-self.changer}"

    def roll(self) -> int:
        """
        Roll the dice

        :return: The result of the dice roll
        """
        self.dice = []
        for _ in range(self.times):
            result = random.randint(1, self.dice_type)
            self.dice.append(result)
            logger.debug(f"Rolled a {result}")

        result = max(sum(self.dice) + self.changer, 0)
        logger.info(f"Total rolled {result}")
        return result

    @classmethod
    def from_string(cls, dice_string: str):
        """
        return a dice object made from a string.

        the format of the string must be: {time}d{dice_type}

        example: 2d6 + 3
        result: Dice(2, 6, 3)

        example: 1d10 - 6
        result: Dice(1, 10, -6)

        :param dice_string: The string to make into a Dice object
        :return: the new Dice object
        """
        times = int(dice_string.split("d")[0])
        if "+" in dice_string:
            dice_type = int(dice_string.split("+")[0].split("d")[1])
            changer = int(dice_string.split("+")[1])
        else:
            dice_type = int(dice_string.split("-")[0].split("d")[1])
            changer = -int(dice_string.split("-")[1])

        logger.debug(f"from string: {dice_string} -> Dice({times}, {dice_type}, {changer})")
        return cls(times, dice_type, changer)