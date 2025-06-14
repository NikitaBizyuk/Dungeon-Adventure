from unittest import TestCase
from unittest.mock import patch, MagicMock
from model.Room import Room
from model.MazeCell import MazeCell
from model.Dungeon import Dungeon

class TestDungeon(TestCase):

    def setUp(self):
        self.dungeon = Dungeon(difficulty="easy")

    def test_initial_dimensions_easy(self):
        self.assertEqual((self.dungeon.rows, self.dungeon.cols), (41, 41))
        self.assertEqual(self.dungeon.room_count, 8)

    def test_initial_dimensions_medium(self):
        dungeon = Dungeon(difficulty="medium")
        self.assertEqual((dungeon.rows, dungeon.cols), (61, 61))
        self.assertEqual(dungeon.room_count, 15)

    def test_initial_dimensions_hard(self):
        dungeon = Dungeon(difficulty="hard")
        self.assertEqual((dungeon.rows, dungeon.cols), (81, 81))
        self.assertEqual(dungeon.room_count, 25)

    def test_can_place_room_returns_boolean(self):
        top, left, h, w = 5, 5, 3, 3
        result = self.dungeon._can_place_room(top, left, h, w)
        self.assertIsInstance(result, bool)

    def test_carve_room_changes_cells(self):
        top, left, h, w = 5, 5, 3, 3
        self.dungeon._carve_room(top, left, h, w)
        for r in range(top, top + h):
            for c in range(left, left + w):
                self.assertEqual(self.dungeon.maze[r][c].cell_type, "hallway")

    def test_place_exit_marks_exit(self):
        self.dungeon._place_exit()
        last_center = self.dungeon.room_centers[-1]
        self.assertEqual(self.dungeon.maze[last_center[0]][last_center[1]].cell_type, "exit")

    def test_hero_moves_into_hallway(self):
        x, y = self.dungeon.hero_x, self.dungeon.hero_y
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.dungeon.rows and 0 <= ny < self.dungeon.cols:
                self.dungeon.maze[nx][ny].cell_type = "hallway"
                self.dungeon.move_hero(dx, dy)
                self.assertEqual((self.dungeon.hero_x, self.dungeon.hero_y), (nx, ny))
                break

    def test_visibility_updated(self):
        self.dungeon.update_visibility()
        visible_cells = sum(cell.visible for row in self.dungeon.maze for cell in row)
        self.assertGreater(visible_cells, 0)

    def test_entering_door_sets_in_room_true(self):
        # Force a door tile next to hero
        x, y = self.dungeon.hero_x, self.dungeon.hero_y
        self.dungeon.maze[x][y + 1].cell_type = "door"
        self.dungeon.maze[x][y + 1].door_id = list(self.dungeon.rooms.keys())[0]
        self.dungeon.move_hero(0, 1)
        self.assertTrue(self.dungeon.in_room)
        self.assertIsNotNone(self.dungeon.active_room)

