import pygame

class GameView:
    def __init__(self, screen, cell_size, view_rows, view_cols):
        self.screen = screen
        self.cell_size = cell_size
        self.view_rows = view_rows
        self.view_cols = view_cols

    def draw_maze(self, dungeon, hero_x, hero_y):
        view_rows, view_cols = self.view_rows, self.view_cols

        start_r = max(0, min(dungeon.rows - view_rows, hero_x - view_rows // 2))
        start_c = max(0, min(dungeon.cols - view_cols, hero_y - view_cols // 2))
        end_r = start_r + view_rows
        end_c = start_c + view_cols

        base_colors = {
            "wall": (30, 30, 30),
            "hallway": (220, 220, 220),
            "door": (15, 128, 255),
            "exit": (0, 255, 128)
        }

        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                cell = dungeon.maze[r][c]
                screen_x = (c - start_c) * self.cell_size
                screen_y = (r - start_r) * self.cell_size
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)

                if not cell.explored:
                    color = (0, 0, 0)  # unseen
                elif not cell.visible:
                    base = base_colors.get(cell.cell_type, (100, 100, 100))
                    color = tuple(int(x * 0.35) for x in base)  # darkened explored
                else:
                    color = base_colors.get(cell.cell_type, (255, 0, 255))

                pygame.draw.rect(self.screen, color, rect)

                if r == hero_x and c == hero_y:
                    pygame.draw.circle(self.screen, (255, 0, 0), rect.center, self.cell_size // 3)

    def draw_room(self, room, width, height):
        self.screen.fill((30, 30, 30))
        pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(100, 100, width - 200, height - 200))
        pygame.draw.circle(self.screen, (255, 0, 0), (width // 2, height // 2), 20)
        font = pygame.font.SysFont(None, 36)
        text = font.render("In Room! Press Q to return.", True, (255, 255, 255))
        self.screen.blit(text, (width // 2 - 120, 60))