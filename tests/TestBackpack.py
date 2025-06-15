from unittest import TestCase
from model.Backpack import BackPack


class TestBackPack(TestCase):
    def setUp(self):
        self.backpack = BackPack()

    def test_initial_state(self):
        self.assertEqual(len(self.backpack.inventory), 0)
        self.assertEqual(self.backpack.healing_cntr, 0)
        self.assertEqual(self.backpack.vision_cntr, 0)
        self.assertEqual(self.backpack.pillar_cntr, 0)

    def test_add_items(self):
        # Test adding regular items
        self.backpack.add("Sword")
        self.assertIn("Sword", self.backpack._inventory())

        # Test adding health potion
        self.backpack.add("Health Potion")
        self.assertEqual(self.backpack.get_healing_cntr(), 1)

        # Test adding vision potion
        self.backpack.add("Vision Potion")
        self.assertEqual(self.backpack.get_vision_cntr(), 1)

        # Test adding OOP pillars
        pillars = ["A", "E", "I", "P"]
        for pillar in pillars:
            self.backpack.add(pillar)
        self.assertEqual(self.backpack.pillar_cntr, 4)

    def test_use_potions(self):
        # Test healing potion usage
        self.backpack.add("Health Potion")
        self.backpack.use_healing_potion()
        self.assertEqual(self.backpack.get_healing_cntr(), 0)

        # Test vision potion usage
        self.backpack.add("Vision Potion")
        self.assertTrue(self.backpack.use_vision_potion())
        self.assertEqual(self.backpack.get_vision_cntr(), 0)
        self.assertFalse(self.backpack.use_vision_potion())  # No more potions

    def test_found_all_pillars(self):
        self.assertFalse(self.backpack.found_all_pillars())
        pillars = ["A", "E", "I", "P"]
        for pillar in pillars:
            self.backpack.add(pillar)
        self.assertTrue(self.backpack.found_all_pillars())

    def test_to_string(self):
        items = ["Sword", "Shield", "Health Potion"]
        for item in items:
            self.backpack.add(item)
        result = self.backpack.to_string()
        for item in items:
            self.assertIn(item, result)


