import unittest
from unittest.mock import Mock
from model.OOPillars import OOPillars
from model.Backpack import BackPack  # adjust the import as needed based on your structure


class TestBackPack(unittest.TestCase):

    def setUp(self):
        self.backpack = BackPack()
        self.mock_view = Mock()

    def test_add_pillars(self):
        self.backpack.add("A", self.mock_view)
        self.assertEqual(self.backpack.abstraction, 1)
        self.assertEqual(self.backpack.pillar_cntr, 1)

        self.backpack.add("E", self.mock_view)
        self.assertEqual(self.backpack.encapsulation, 1)
        self.assertEqual(self.backpack.pillar_cntr, 2)

        self.backpack.add("I", self.mock_view)
        self.assertEqual(self.backpack.inheritance, 1)
        self.assertEqual(self.backpack.pillar_cntr, 3)

        self.backpack.add("P", self.mock_view)
        self.assertEqual(self.backpack.polymorphism, 1)
        self.assertEqual(self.backpack.pillar_cntr, 4)
        self.assertTrue(self.backpack.found_all_pillars())

    def test_add_health_potion(self):
        self.backpack.add("Health Potion", self.mock_view)
        self.assertEqual(self.backpack.healing_cntr, 1)

    def test_add_vision_potion(self):
        self.backpack.add("Vision Potion", self.mock_view)
        self.assertEqual(self.backpack.vision_cntr, 1)

    def test_use_healing_potion(self):
        self.backpack.add("Health Potion")
        self.backpack.use_healing_potion()
        self.assertEqual(self.backpack.healing_cntr, 0)

    def test_use_vision_potion(self):
        self.assertFalse(self.backpack.use_vision_potion())
        self.backpack.add("Vision Potion")
        self.assertTrue(self.backpack.use_vision_potion())
        self.assertEqual(self.backpack.vision_cntr, 0)

    def test_inventory_tracking(self):
        self.backpack.add("A")
        self.backpack.add("Health Potion")
        self.assertIn("A", self.backpack.inventory)
        self.assertIn("Health Potion", self.backpack.inventory)
        self.assertEqual(self.backpack.to_string(), "A, Health Potion")

    def test_view_message_calls(self):
        self.backpack.add("A", self.mock_view)
        self.mock_view.display_message.assert_called_with("You found Pillar 1/4", 2500)

        self.backpack.add("Health Potion", self.mock_view)
        self.mock_view.display_message.assert_called_with("You found a Healing Potion", 2500)

        self.backpack.add("Vision Potion", self.mock_view)
        self.mock_view.display_message.assert_called_with("You found a Vision Potion", 2500)


class TestOOPillarsEnum(unittest.TestCase):

    def test_enum_symbols_and_descriptions(self):
        self.assertEqual(OOPillars.ABSTRACTION.symbol, 'A')
        self.assertTrue("Hides complexity" in OOPillars.ABSTRACTION.description)

        self.assertEqual(OOPillars.ENCAPSULATION.symbol, 'E')
        self.assertTrue("Bundles data" in OOPillars.ENCAPSULATION.description)

        self.assertEqual(OOPillars.INHERITANCE.symbol, 'I')
        self.assertTrue("acquire properties" in OOPillars.INHERITANCE.description)

        self.assertEqual(OOPillars.POLYMORPHISM.symbol, 'P')
        self.assertTrue("many forms" in OOPillars.POLYMORPHISM.description)

    def test_str_method(self):
        self.assertIn("Abstraction (A):", str(OOPillars.ABSTRACTION))


if __name__ == '__main__':
    unittest.main()
