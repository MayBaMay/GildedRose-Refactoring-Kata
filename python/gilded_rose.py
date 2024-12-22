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


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1

