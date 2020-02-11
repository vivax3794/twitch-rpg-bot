import logging
from typing import Dict


logger = logging.getLogger(__name__)


def new_item(item_data: Dict[str, any]) -> "Item":
    if item_data["type"] == "health":
        return Health(item_data)
    elif item_data["type"] == "dmg":
        return Dmg(item_data)
    elif item_data["type"] == "nothing":
        return Nothing(item_data)
    elif item_data["type"] == "air":
        return Air(item_data)
    elif item_data["type"] == "health potion":
        return HealthPotion(item_data)
    elif item_data["type"] == "bow":
        return Bow(item_data)
    else:
        raise ValueError("Item missing type filed.")


class Item(object):
    """
    Represents a item.
    """
    def __init__(self, item_data: Dict[str, any]):
        logger.info(f"Item made: {item_data['name']}")
        logger.debug(str(item_data))
        self.name = item_data["name"]
        self.value = item_data["value"]
        self.type = item_data["type"]
        self.description = item_data["description"]
        self.used = item_data["used"]
        self.cant_use = item_data["cant use"]

        self.kwargs = item_data["kwargs"]

    def use(self, player, monster) -> bool:
        """
        The action taken when the item is used.

        :param player: The player that used the item
        :param monster: A possible monster it was used on, might be none
        :return: If the item could be used.
        """
        pass


class Nothing(Item):
    def use(self, player, monster) -> bool:
        return True


class Health(Item):
    def use(self, player, monster) -> bool:
        logger.debug(f'item {self.name} being used.')
        if player.health >= self.kwargs["min_health"]:
            player.health += self.value
            player.health = min(player.health, 40)
            player.inventory.remove_item(self)
            return True
        else:
            return False


class Dmg(Item):
    def __init__(self, *args):
        super().__init__(*args)
        self.org_used = self.used

    def use(self, player, monster) -> bool:
        self.used = self.org_used
        logger.debug(f'item {self.name} being used.')

        if self.kwargs["can die"]:
            died = player.take_dmg(self.value)
            if died:
                player.used = self.kwargs["died"]
        else:
            dmg = player.health - 1 if player.health - self.value <= 0 else self.value
            player.take_dmg(dmg)
        player.inventory.remove_item(self)
        return True


# Special items, classes for 1 item and not a type
class Air(Item):
    def use(self, player, monster) -> bool:
        player.inventory.remove_item(self)

        if player.inventory.count_item("air") == 0:
            player.take_dmg(40)
            self.used = self.kwargs["when_used_up"]
            for _ in "_"*10:
                item = player.game_data.get_item("air")
                player.inventory.add_item(item)

        return True


class HealthPotion(Health):
    def use(self, player, monster) -> bool:
        super().use(player, monster)
        if "health potions drunken" not in player.item_data.keys():
            player.item_data["health potions drunken"] = 0

        player.item_data["health potions drunken"] += 1
        if player.item_data["health potions drunken"] == self.kwargs["to black out"]:
            self.used = self.kwargs["black out"]
            player.item_data["health potions drunken"] = 0
            player.gold //= 2
            player.xp //= 2

        return True


class Bow(Item):
    def use(self, player, monster) -> bool:
        if monster is None:
            self.cant_use = "Monster not found"
            return False

        if player.inventory.count_item(self.kwargs["arrow"]) == 0:
            self.cant_use = f"Arrow not found ({self.kwargs['arrow']})"
            return False

        arrow = player.inventory.get_item(self.kwargs["arrow"])
        dmg = arrow.value * self.value

        died = monster.take_dmg(dmg)
        player.inventory.remove_item(arrow)

        if not died:
            self.used = (
                f"You fire the bow at {monster.name}, it took {dmg} dmg. "
                f"{monster.name} hp: {monster.health}. "
            )
        else:
            self.used = (
                f"You fire the bow at {monster.name}, it took {dmg} dmg. "
                f"{monster.name} hp: {monster.health}. "
                f"{monster.name} died, you get {monster.reward['gold']} and "
                f"{monster.reward['xp']} xp!"
            )

        return True