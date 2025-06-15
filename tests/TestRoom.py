import unittest
from model.Room import Room
from unittest.mock import MagicMock, patch

class TestRoom(unittest.TestCase):

    def setUp(self):
        Room.set_difficulty("easy")  # Use a controlled difficulty for testing
        self.room = Room(door_r=14, door_c=12)

    def test_room_initialization(self):
        self.assertEqual(self.room.get_dimensions(), (15, 25))
        self.assertIsNotNone(self.room.get_tile(14, 12))  # Door
        self.assertEqual(self.room.get_tile(self.room._hero_r, self.room._hero_c), "floor")

    def test_hero_positioning(self):
        r, c = self.room.get_hero_position()
        self.assertTrue(0 <= r < self.room.height)
        self.assertTrue(0 <= c < self.room.width)

    def test_monsters_spawn(self):
        monsters = self.room.get_monsters()
        self.assertTrue(1 <= len(monsters) <= 3)
        for pos in monsters.values():
            self.assertTrue(1 <= pos[0] < self.room.height - 1)
            self.assertTrue(1 <= pos[1] < self.room.width - 1)

    def test_place_item(self):
        self.room.place_item("TestItem")
        found = any("TestItem" in row for row in self.room._grid)
        self.assertTrue(found)

    def test_place_random_loot(self):
        self.room.place_random_loot()
        found = any(cell in ["Health Potion", "Vision Potion"] for row in self.room._grid for cell in row)
        self.assertTrue(found)

    def test_move_hero_on_floor(self):
        start_r, start_c = self.room.get_hero_position()
        result = self.room.move_hero_in_room(0, -1, backpack=MagicMock())
        self.assertIn(result, [None, "pit"])

    @patch('model.MonsterFactory.MonsterFactory.create_random_monster')
    def test_monster_mocking(self, mock_factory):
        mock_monster = MagicMock()
        mock_factory.return_value = mock_monster
        test_room = Room(door_r=14, door_c=12)
        self.assertIn(mock_monster, test_room.get_monsters())