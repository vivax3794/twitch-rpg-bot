import logging
from typing import Dict

logger = logging.getLogger(__name__)


def new_event(event_data: Dict[str, any]) -> "Event":
    if event_data["type"] == "item":
        return Item(event_data)
    elif event_data["type"] == "gold":
        return Gold(event_data)
    elif event_data["type"] == "healthTimes":
        return HealthTimes(event_data)
    elif event_data["type"] == "nothing":
        return Nothing(event_data)
    elif event_data["type"] == "magicStone":
        return MagicStone(event_data)
    elif event_data["type"] == "command":
        return Command(event_data)
    else:
        logger.error("Item missing type filed.")


class Event(object):
    """
    Represents a item.
    """

    def __init__(self, event_data: Dict[str, any]):
        logger.info(f"Event made")
        logger.debug(str(event_data))
        self.value = event_data["value"]
        self.type = event_data["type"]
        self.message = event_data["message"]

        self.kwargs = event_data["kwargs"]

    def activate(self, player):
        """
        The action taken when the item is used.

        :param player: The player that the event happend to
        """
        logger.warning(f"event used the default event.trigger, this should not happened.")


class Item(Event):
    def activate(self, player):
        for _ in "_"*self.kwargs["amount"]:
            item = player.game_data.get_item(self.value)
            player.inventory.add_item(item)


class Gold(Event):
    def activate(self, player):
        player.gold += self.value


class HealthTimes(Event):
    def activate(self, player):
        player.health *= self.value
        player.health = min(player.health, 40)


class Nothing(Event):
    def activate(self, player):
        pass


class MagicStone(Event):
    def activate(self, player):
        if player.inventory.count_item(self.kwargs["item"]) >= 1:
            self.message = self.kwargs["new_message"]
            player.gold += self.value


class Command(Event):
    def activate(self, player):
        pass
