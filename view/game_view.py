import pygame


class GameView:
    def __init__(self, screen, cell_size, view_rows, view_cols):
        self.screen = screen
        self.cell_size = cell_size
        self.view_rows = view_rows
        self.view_cols = view_cols
       # self.font = pygame.font.SysFont(None, 24)

    def draw_maze(self, dungeon, hero_x, hero_y):
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

    def draw_room(self, room, width, height,ogre,skeleton,gremlin):
        view_rows = self.view_rows
        view_cols = self.view_cols

        hero_r, hero_c = room.get_hero_position()
        monsters = room.get_monsters()
        start_r = max(0, min(max(0, room.height - view_rows), hero_r - view_rows // 2))
        start_c = max(0, min(max(0, room.width - view_cols), hero_c - view_cols // 2))
        end_r = min(start_r + view_rows, room.height)
        end_c = min(start_c + view_cols, room.width)

        base_colors = {
            "wall": (40, 40, 40),
            "floor": (230, 230, 230),
            "door": (0, 128, 255),
            "Encapsulation": (255, 215, 0),
            "Polymorphism": (255, 215, 0),
            "Abstraction": (255, 215, 0),
            "Inheritance": (255, 215, 0),
            "Health Potion": (255, 192, 203),
            "Vision Potion": (255, 192, 203)
        }

        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                tile = room.get_tile(r, c)
                room_tile_width = end_c - start_c
                room_tile_height = end_r - start_r

                cell_w = width // room_tile_width
                cell_h = height // room_tile_height
                cell_size = min(cell_w, cell_h)  # Make tiles square

                screen_x = (c - start_c) * cell_size
                screen_y = (r - start_r) * cell_size
                rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)

                color = base_colors.get(tile, (255, 0, 255))
                pygame.draw.rect(self.screen, color, rect)
        center = ((hero_c - start_c) * self.cell_size + self.cell_size // 2,
                  (hero_r - start_r) * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(self.screen, (250, 0, 0), center, self.cell_size // 3)

        for monster, (mr, mc) in monsters.items():
            screen_x = (mc - start_c) * self.cell_size
            screen_y = (mr - start_r) * self.cell_size
            if isinstance(monster, ogre):
                pygame.draw.circle(self.screen, (0, 250,0),
               (screen_x + self.cell_size // 2, screen_y + self.cell_size // 2), self.cell_size // 3)
            if isinstance(monster, skeleton):
                pygame.draw.circle(self.screen, (0, 0, 0),
               (screen_x + self.cell_size // 2, screen_y + self.cell_size // 2), self.cell_size // 3)
            if isinstance(monster, gremlin):
                pygame.draw.circle(self.screen, (0,0 , 250),
               (screen_x + self.cell_size // 2, screen_y + self.cell_size // 2), self.cell_size // 3)


