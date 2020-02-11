import logging

logger = logging.getLogger(__name__)

# TODO: make an amount argument


class Shop():
    def __init__(self):
        self.shops = {
            "candy": {},
            "potion": {},
            "amulet": {},
            "bow": {}
        }

    def load_shop(self, item_data_list):
        for item in item_data_list:
            if item["shop"] is not None:
                item_name = item["name"]
                item_cost = item["cost"]
                item_description = item["description"]
                shop = item["shop"]

                if shop not in self.shops.keys():
                    logger.warning(f"Item {item_name} has an invalid shop name: {shop}, skipping")
                    continue

                self.shops[shop][item_name] = {
                    "name": item_name,
                    "cost": item_cost,
                    "description": item_description
                }

    @property
    def main_shop_string(self) -> str:
        return "Shops: " + ", ".join(self.shops.keys())

    def shop_string(self, shop_name) -> str:
        if shop_name in self.shops.keys():
            return f"{shop_name} shop items: " + ", ".join(f"{item['name']} {item['cost']}G" for item in self.shops[shop_name].values())
        else:
            return f"shop {shop_name} not found."

    def item_dec(self, shop_name, item_name):
        if shop_name in self.shops.keys():
            item = self.shops[shop_name].get(item_name)
            if item is None:
                return f"Item {item_name} not found in shop {shop_name}"
            else:
                return item['description']
        else:
            return f"shop {shop_name} not found."

    def buy(self, player, shop_name, item_name):
        if shop_name in self.shops.keys():
            item = self.shops[shop_name].get(item_name)
            if item is None:
                return f"Item {item_name} not found in shop {shop_name}"
            else:
                if player.gold < item["cost"]:
                    return f"Sorry you need {item['cost'] - player.gold}G more to bye this item"
                else:
                    # bye item

                    item_object = player.game_data.get_item(item_name)
                    logger.debug(f"On buy item object: {item_object}")
                    player.inventory.add_item(item_object)
                    player.gold -= item["cost"]
                    return f"you bought {item['name']} for {item['cost']}G, you know have {player.gold}G left."
        else:
            return f"shop {shop_name} not found."