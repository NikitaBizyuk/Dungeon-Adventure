import pygame

class GameView:
    def __init__(self, screen, cell_size, view_rows, view_cols):
        self.screen = screen
        self.cell_size = cell_size
        self.view_rows = view_rows
        self.view_cols = view_cols

    def draw_maze(self, game):
        dungeon = game.dungeon
        hero_x = dungeon.hero_x
        hero_y = dungeon.hero_y
        aim_dx, aim_dy = game.aim_vector
        view_rows, view_cols = self.view_rows, self.view_cols

        start_r = max(0, min(dungeon.rows - view_rows, hero_x - view_rows // 2))
        start_c = max(0, min(dungeon.cols - view_cols, hero_y - view_cols // 2))
        end_r = min(start_r + view_rows, dungeon.rows)
        end_c = min(start_c + view_cols, dungeon.cols)

        base_colors = {
            "wall": (30, 30, 30),
            "hallway": (220, 220, 220),
            "door": (0, 128, 255),
            "exit": (0, 255, 128)
        }
    #update varianles better
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                cell = dungeon.maze[r][c]
                screen_x = (c - start_c) * self.cell_size
                screen_y = (r - start_r) * self.cell_size
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)

                if not cell.explored:
                    color = (0, 0, 0)
                elif not cell.visible:
                    base = base_colors.get(cell.cell_type, (100, 100, 100))
                    color = tuple(int(x * 0.35) for x in base)
                else:
                    color = base_colors.get(cell.cell_type, (255, 0, 255))

                pygame.draw.rect(self.screen, color, rect)

                if r == hero_x and c == hero_y:
                    pygame.draw.circle(self.screen, (255, 0, 0), rect.center, self.cell_size // 3)


                aim_dx, aim_dy = game.aim_vector
                center_x = (hero_y - start_c) * self.cell_size + self.cell_size // 2
                center_y = (hero_x - start_r) * self.cell_size + self.cell_size // 2
                end_x = int(center_x + aim_dx * 40)
                end_y = int(center_y + aim_dy * 40)
                pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

    def draw_room(self, game, width, height):
        room = game.active_room
        view_rows = self.view_rows
        view_cols = self.view_cols

        hero_r, hero_c = room.get_hero_position()
        start_r = max(0, min(max(0, room.height - view_rows), hero_r - view_rows // 2))
        start_c = max(0, min(max(0, room.width - view_cols), hero_c - view_cols // 2))
        end_r = min(start_r + view_rows, room.height)
        end_c = min(start_c + view_cols, room.width)

        base_colors = {
            "wall": (40, 40, 40),
            "floor": (230, 230, 230),
            "door": (0, 128, 255)
        }

        room_tile_width = end_c - start_c
        room_tile_height = end_r - start_r

        cell_w = width // room_tile_width
        cell_h = height // room_tile_height
        cell_size = min(cell_w, cell_h)  # Make tiles square

        # Draw tiles
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                tile = room.get_tile(r, c)
                screen_x = (c - start_c) * cell_size
                screen_y = (r - start_r) * cell_size
                rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)
                color = base_colors.get(tile, (255, 0, 255))
                pygame.draw.rect(self.screen, color, rect)

        # Draw hero
        center_x = (hero_c - start_c) * cell_size + cell_size // 2
        center_y = (hero_r - start_r) * cell_size + cell_size // 2
        pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), cell_size // 3)

        # Draw aim direction
        aim_dx, aim_dy = game.aim_vector
        end_x = int(center_x + aim_dx * 40)
        end_y = int(center_y + aim_dy * 40)
        pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

