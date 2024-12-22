# -*- coding: utf-8 -*-

MAX_QUALITY = 50
MIN_QUALITY = 0

class Item:
    def __init__(self, name, sell_in, quality): 
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"

    def update(self):
        # This method must be overridden by subclasses to define specific update behavior.
        raise NotImplementedError("Subclasses must override this method")

    def increase_quality(self):
        # Increase the quality of the item, ensuring it does not exceed MAX_QUALITY.
        self.quality = min(self.quality + 1, MAX_QUALITY)

    def decrease_quality(self):
        # Decrease the quality of the item, ensuring it does not go below MIN_QUALITY.
        self.quality = max(self.quality - 1, MIN_QUALITY)

    def decrease_sell_in(self):
        # Decrease the sell_in value by 1.
        self.sell_in -= 1

    def is_expired(self):
        # Check if the item is expired (sell_in is less than 0).
        return self.sell_in < 0


class AgedBrie(Item):
    # Aged Brie increases in quality over time, and more after expiration.
    def update(self):
        self.increase_quality()
        self.decrease_sell_in()
        if self.is_expired():
            self.increase_quality()


class BackstagePass(Item):
    # Backstage passes increase in quality as the event approaches,
    # with additional increases when sell_in is below 10 and 5.
    # Quality drops to 0 after expiration.
    def update(self):
        self.increase_quality()
        if self.sell_in < 11:
            self.increase_quality()
        if self.sell_in < 6:
            self.increase_quality()
        self.decrease_sell_in()
        if self.is_expired():
            self.quality = 0


class Sulfuras(Item):
    # Sulfuras is a legendary item whose quality and sell_in never change.
    def update(self):
        pass  # Sulfuras doesn't change


class RegularItem(Item):
    # Regular items decrease in quality over time, and decrease faster after expiration.
    def update(self):
        self.decrease_quality()
        self.decrease_sell_in()
        if self.is_expired():
            self.decrease_quality()


class GildedRose:
    def __init__(self, items):
        self.items = items
        self.item_types = {
            "Aged Brie": AgedBrie,
            "Backstage passes to a TAFKAL80ETC concert": BackstagePass,
            "Sulfuras, Hand of Ragnaros": Sulfuras,
        }

    def update_quality(self):
        # Update the quality of all items in the shop.
        for item in self.items:
            # Dispatching logic: instantiate the correct item type using the dictionary
            item_type = self.item_types.get(item.name, RegularItem)
            specific_item = item_type(item.name, item.sell_in, item.quality)

            # Update the item
            specific_item.update()

            # Reflect the updated values in the original item
            item.sell_in = specific_item.sell_in
            item.quality = specific_item.quality
