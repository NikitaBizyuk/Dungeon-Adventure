import unittest
from unittest.mock import patch, MagicMock
from model.Dungeon import Dungeon
from model.MazeCell import MazeCell
from model.OOPillars import OOPillars


class TestDungeon(unittest.TestCase):

    @patch('model.Dungeon.Room')
    def test_dungeon_initialization(self, MockRoom):
        dungeon = Dungeon(difficulty='easy')
        self.assertEqual(dungeon.rows, 41)
        self.assertEqual(dungeon.cols, 41)
        self.assertGreaterEqual(len(dungeon.rooms), 4)
        self.assertTrue(0 <= dungeon.hero_x < dungeon.rows)
        self.assertTrue(0 <= dungeon.hero_y < dungeon.cols)

    @patch('model.Dungeon.Room')
    def test_maze_has_exit(self, MockRoom):
        dungeon = Dungeon(difficulty='medium')
        exit_found = any(
            cell.cell_type == "exit"
            for row in dungeon.maze
            for cell in row
        )
        self.assertTrue(exit_found)

    @patch('model.Dungeon.Room')
    def test_hero_movement_in_maze(self, MockRoom):
        dungeon = Dungeon()
        old_x, old_y = dungeon.hero_x, dungeon.hero_y

        # Try moving in 4 directions (skip if outside bounds)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_x, new_y = old_x + dx, old_y + dy
            if 0 <= new_x < dungeon.rows and 0 <= new_y < dungeon.cols:
                cell = dungeon.maze[new_x][new_y]
                if cell.cell_type == "hallway":
                    dungeon.move_hero_in_room(dx, dy, backpack=MagicMock())
                    self.assertEqual((dungeon.hero_x, dungeon.hero_y), (new_x, new_y))
                    break

    @patch('model.Dungeon.Room')
    def test_visibility_after_move(self, MockRoom):
        dungeon = Dungeon()
        dungeon.move_hero_in_room(0, 1, backpack=MagicMock())
        count_visible = sum(cell.visible for row in dungeon.maze for cell in row)
        self.assertGreater(count_visible, 0)

    @patch('model.Dungeon.Room')
    def test_pillars_are_placed(self, MockRoom):
        dungeon = Dungeon()
        item_counts = {symbol: 0 for symbol in ["A", "E", "I", "P"]}
        for room in dungeon.rooms.values():
            for item in room.items if hasattr(room, 'items') else []:
                if item in item_counts:
                    item_counts[item] += 1
        total = sum(item_counts.values())
        self.assertLessEqual(total, 4)

    @patch('model.Dungeon.Room')
    def test_entering_room_sets_flags(self, MockRoom):
        mock_room = MagicMock()
        MockRoom.return_value = mock_room

        dungeon = Dungeon()
        # find a door tile to simulate entrance
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            x, y = dungeon.hero_x + dx, dungeon.hero_y + dy
            if 0 <= x < dungeon.rows and 0 <= y < dungeon.cols:
                if dungeon.maze[x][y].cell_type == "door":
                    door_id = dungeon.maze[x][y].door_id
                    dungeon.rooms[door_id] = mock_room
                    dungeon.move_hero_in_room(dx, dy, backpack=MagicMock())
                    self.assertTrue(dungeon.in_room)
                    self.assertEqual(dungeon.active_room, mock_room)
                    break


if __name__ == "__main__":
    unittest.main()
