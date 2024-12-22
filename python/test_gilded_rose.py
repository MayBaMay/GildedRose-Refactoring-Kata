# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


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

        
if __name__ == '__main__':
    unittest.main()
