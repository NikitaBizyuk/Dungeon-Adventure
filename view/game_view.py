# view/game_view.py
import pygame

class GameView:
    def __init__(self, screen, cell_size):
        self.screen = screen
        self.cell_size = cell_size

    def draw_maze(self, dungeon, hero_x, hero_y):
        colors = {
            "wall": (40, 40, 40),
            "hallway": (200, 200, 200),
            "door": (0, 128, 255)
        }
        for r in range(dungeon.rows):
            for c in range(dungeon.cols):
                rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
                cell = dungeon.maze[r][c]
                pygame.draw.rect(self.screen, colors[cell.cell_type], rect)
                if r == hero_x and c == hero_y:
                    pygame.draw.circle(self.screen, (255, 0, 0), rect.center, self.cell_size // 3)

    def draw_room(self, room, width, height):
        self.screen.fill((30, 30, 30))
        pygame.draw.rect(self.screen, (200, 200, 200), pygame.Rect(100, 100, width - 200, height - 200))
        pygame.draw.circle(self.screen, (255, 0, 0), (width // 2, height // 2), 20)
        font = pygame.font.SysFont(None, 36)
        text = font.render("In Room! Press Q to return.", True, (255, 255, 255))
        self.screen.blit(text, (width // 2 - 120, 60))
