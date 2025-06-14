import unittest
from unittest.mock import patch, MagicMock
from model.Room import Room


class MockBackPack:
    def __init__(self):
        self.items = set()
    def add(self, item):
        self.items.add(item)
    def to_string(self):
        return ", ".join(sorted(self.items))


class TestRoom(unittest.TestCase):

    @patch("model.Room.MonsterFactory.create_random_monster")
    def test_room_initialization_default(self, mock_create_monster):
        mock_create_monster.side_effect = lambda: MagicMock(name="Monster")
        Room.set_difficulty("easy")
        room = Room(14, 12)

        self.assertEqual(room.get_dimensions(), (15, 25))
        self.assertEqual(room.get_tile(room.door_r, room.door_c), "door")
        self.assertEqual(room.get_tile(room.hero_r, room.hero_c), "floor")
        self.assertTrue(all(tile in ["floor", "wall", "door", "A", "E", "I", "P", "Health Potion", "Vision Potion"]
                            for row in room.grid for tile in row))

    @patch("model.Room.MonsterFactory.create_random_monster")
    def test_move_hero_valid_and_loot_pickup(self, mock_create_monster):
        mock_create_monster.side_effect = lambda: MagicMock(name="Monster")
        Room.set_difficulty("easy")
        room = Room(14, 12)
        backpack = MockBackPack()

        loot_r, loot_c = room.hero_r - 1, room.hero_c
        room.grid[loot_r][loot_c] = "Health Potion"
        result = room.move_hero_in_room(-1, 0, backpack)

        self.assertIsNone(result)
        self.assertIn("Health Potion", backpack.items)
        self.assertEqual(room.get_tile(loot_r, loot_c), "floor")

    @patch("model.Room.MonsterFactory.create_random_monster")
    def test_move_hero_into_door_returns_exit(self, mock_create_monster):
        mock_create_monster.side_effect = lambda: MagicMock(name="Monster")
        room = Room(14, 12)
        backpack = MockBackPack()
        door_r, door_c = room.door_r, room.door_c
        room.hero_r, room.hero_c = door_r - 1, door_c
        room.grid[door_r][door_c] = "door"

        result = room.move_hero_in_room(1, 0, backpack)
        self.assertEqual(result, "exit")

    @patch("model.Room.MonsterFactory.create_random_monster")
    def test_monster_movement_no_overlap_with_hero(self, mock_create_monster):
        mock_create_monster.side_effect = lambda: MagicMock(name="Monster")
        room = Room(14, 12)

        original_positions = set(room.monsters.values())
        room.move_monsters()
        new_positions = set(room.monsters.values())

        self.assertEqual(len(original_positions), len(new_positions))
        self.assertNotIn((room.hero_r, room.hero_c), new_positions)

    def test_set_difficulty_invalid_defaults_to_medium(self):
        Room.set_difficulty("insane")
        self.assertEqual(Room._current_difficulty, "medium")

    @patch("model.Room.MonsterFactory.create_random_monster")
    def test_get_monster_at_specific_position(self, mock_create_monster):
        mock_monster = MagicMock(name="Monster")
        mock_create_monster.return_value = mock_monster
        room = Room(14, 12)

        for m, (r, c) in room.get_monsters().items():
            self.assertEqual(room.get_monster_at(r, c), m)
            break

    def test_get_hero_position_accessor(self):
        room = Room(14, 12)
        self.assertEqual(room.get_hero_position(), (room.hero_r, room.hero_c))

