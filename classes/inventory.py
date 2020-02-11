import logging
from collections import Counter
from typing import List, Optional, Dict
from operator import attrgetter

from classes.item import Item

logger = logging.getLogger(__name__)


class Inventory(object):
    def __init__(self):
        self.__items: List = []

    def __str__(self):
        counter = Counter(list(map(attrgetter("name"), self.__items)))
        strings = []
        for item, amount in dict(counter).items():
            strings.append(f"{item} x {amount}")
        return "; ".join(strings)

    def get_item(self, item_name: str) -> Optional[Item]:
        """
        Get a item from the inventory

        :param item_name: The name of the item to get
        :return: Get's the item, if not found return None
        """
        for item in self.__items:
            if item.name == item_name:
                return item
        else:
            return None

    def remove_item(self, item: Item) -> None:
        """
        Remove item from the inventory

        :param item: The item to remove
        :return: None
        """
        self.__items.remove(item)

    def add_item(self, item: Item) -> None:
        """
        Add item to the inventory

        :param item: add a item to the inventory
        :return: None
        """
        self.__items.append(item)

    def count_item(self, item_name: str) -> int:
        count = 0
        for item in self.__items:
            count += item.name == item_name
        return count

    def as_dict(self) -> List[Dict[str, any]]:
        as_dict = []
        for item in self.__items:
            as_dict.append(item.name)
        return as_dict
    
    def load_from_dict(self, dict_data: List[Dict[str, any]], game_data) -> None:
        self.__items = []
        for item_name in dict_data:
            self.__items.append(game_data.get_item(item_name))