# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose, AgedBrie, BackstagePass, Sulfuras, RegularItem


class ItemTest(unittest.TestCase):

    def test_increase_quality(self):
        item = Item("Test Item", 10, 10)
        item.increase_quality()
        self.assertEqual(item.quality, 11)
        item.increase_quality()
        self.assertEqual(item.quality, 12)
        item = Item("Test max", 10, 49)
        item.increase_quality()
        self.assertEqual(item.quality, 50)
        item.increase_quality()
        self.assertEqual(item.quality, 50)

    def test_decrease_quality(self):
        item = Item("Test Item", 10, 10)
        item.decrease_quality()
        self.assertEqual(item.quality, 9)
        item.decrease_quality()
        self.assertEqual(item.quality, 8)
        item = Item("Test min", 10, 1)
        item.decrease_quality()
        self.assertEqual(item.quality, 0)
        item.decrease_quality()
        self.assertEqual(item.quality, 0)

    def test_decrease_sell_in(self):
        item = Item("Test Item", 10, 10)
        item.decrease_sell_in()
        self.assertEqual(item.sell_in, 9)

    def test_is_expired(self):
        item = Item("Test Item", -1, 10)
        self.assertTrue(item.is_expired())
        item.sell_in = 0
        self.assertFalse(item.is_expired())
        item.sell_in = 10
        self.assertFalse(item.is_expired())

    def test_update_not_implemented(self):
        item = Item("Test Item", 10, 10)
        with self.assertRaises(NotImplementedError):
            item.update()

class AgedBrieTest(unittest.TestCase):
    def test_update(self):
        item = AgedBrie("Aged Brie", 5, 10)
        item.update()
        self.assertEqual(item.sell_in, 4)
        self.assertEqual(item.quality, 11)

    def test_update_after_expiry(self):
        item = AgedBrie("Aged Brie", 0, 10)
        item.update()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 12)


class BackstagePassTest(unittest.TestCase):
    def test_update(self):
        item = BackstagePass("Backstage passes to a TAFKAL80ETC concert", 15, 10)
        item.update()
        self.assertEqual(item.sell_in, 14)
        self.assertEqual(item.quality, 11)

    def test_update_close_to_event(self):
        item = BackstagePass("Backstage passes to a TAFKAL80ETC concert", 10, 10)
        item.update()
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 12)

    def test_update_very_close_to_event(self):
        item = BackstagePass("Backstage passes to a TAFKAL80ETC concert", 5, 10)
        item.update()
        self.assertEqual(item.sell_in, 4)
        self.assertEqual(item.quality, 13)

    def test_update_expired(self):
        item = BackstagePass("Backstage passes to a TAFKAL80ETC concert", 0, 10)
        item.update()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 0)


class SulfurasTest(unittest.TestCase):
    def test_update(self):
        item = Sulfuras("Sulfuras, Hand of Ragnaros", 10, 80)
        item.update()  # Sulfuras should not change
        self.assertEqual(item.sell_in, 10)
        self.assertEqual(item.quality, 80)


class RegularItemTest(unittest.TestCase):
    def test_update(self):
        item = RegularItem("Regular Item", 5, 10)
        item.update()
        self.assertEqual(item.sell_in, 4)
        self.assertEqual(item.quality, 9)

    def test_update_after_expiry(self):
        item = RegularItem("Regular Item", 0, 10)
        item.update()
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 8)
        

class GildedRoseTest(unittest.TestCase):
    def test_update_quality(self):
        # Test to ensure update_quality method calls update on correct subclasses
        
        # Mock list of items with their respective types 
        # and expected quality after update
        items = {
            Item("Aged Brie", 5, 10): 11,
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 10): 13,
            Item("Sulfuras, Hand of Ragnaros", 0, 80): 80,
            Item("Regular Item", 5, 10): 9
        }
        
        gilded_rose = GildedRose(list(items.keys()))
        
        # Run the update
        gilded_rose.update_quality()

        for item, expected_quality in items.items():
            with self.subTest(item=item.name):
                self.assertEqual(item.quality, expected_quality)


    def test_update_quality_multiple_times(self):
        # Mock list of items with their respective types 
        # and expected quality after update
        items = {
            Item("Aged Brie",  2, 10): 14,
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 10): 19,
            Item("Sulfuras, Hand of Ragnaros", 0, 80): 80,
            Item("Regular Item", 5, 10): 7
        }
        
        gilded_rose = GildedRose(list(items.keys()))
        
        # Run update multiple times
        for _ in range(3): 
            gilded_rose.update_quality() 

        # Test for Aged Brie: It should have increased in quality over time
        for item, expected_quality in items.items():
            with self.subTest(item=item.name):
                self.assertEqual(item.quality, expected_quality)

    def test_update_quality_max_min_values(self):
        # Mock list of items with their respective types 
        # and expected quality after update
        items = {
            # Aged Brie should not increase above 50
            Item("Aged Brie", 5, 50): 50,  
            # Regular item should not decrease below 0
            Item("Regular Item", 5, 0): 0,
            # Backstage passes should not exceed 50
            Item("Backstage passes to a TAFKAL80ETC concert", 5, 49): 50,  
        }
        
        gilded_rose = GildedRose(list(items.keys()))
        
        # Run update
        gilded_rose.update_quality()
        
        for item, expected_quality in items.items():
            with self.subTest(item=item.name):
                self.assertEqual(item.quality, expected_quality)

    def test_update_quality_expired_items(self):
        # Mock list of items with their respective types 
        # and expected quality after update
        items = {
            # Regular item should degrade by 2 after expiry
            Item("Regular Item", 0, 10): 8,
            # Aged Brie should increase by 2 after expiry
            Item("Aged Brie", 0, 10): 12,
            # Backstage passes should have its quality drop to 0 after expiry
            Item("Backstage passes to a TAFKAL80ETC concert", 0, 10): 0,
        }
        
        gilded_rose = GildedRose(list(items.keys()))
        
        # Run update
        gilded_rose.update_quality()

        for item, expected_quality in items.items():
            with self.subTest(item=item.name):
                self.assertEqual(item.quality, expected_quality)
        
if __name__ == '__main__':
    unittest.main()
