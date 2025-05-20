import pygame
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView

def main():
    pygame.init()

    CELL_SIZE = 40
    ROWS, COLS = 11, 11
    WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dungeon Adventure")

    clock = pygame.time.Clock()
    game = DungeonAdventure()
    view = GameView(screen, CELL_SIZE)

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if not game.in_room:
                    if event.key == pygame.K_w:
                        game.move_hero(-1, 0)
                    elif event.key == pygame.K_s:
                        game.move_hero(1, 0)
                    elif event.key == pygame.K_a:
                        game.move_hero(0, -1)
                    elif event.key == pygame.K_d:
                        game.move_hero(0, 1)
                elif event.key == pygame.K_q:
                    game.exit_room()

        if game.in_room:
            view.draw_room(game.active_room, WIDTH, HEIGHT)
        else:
            view.draw_maze(game.dungeon, game.dungeon.hero_x, game.dungeon.hero_y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
