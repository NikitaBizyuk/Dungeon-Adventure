import pygame
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView


def main():


    pygame.init()

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Adventure")

    # Compute tile size so that the visible tiles stretch to fit the screen completely
    FIXED_VIEW_ROWS = 15
    CELL_SIZE = HEIGHT // FIXED_VIEW_ROWS
    FIXED_VIEW_COLS = WIDTH // CELL_SIZE

    clock = pygame.time.Clock()
    game = DungeonAdventure()
    view = GameView(screen, CELL_SIZE, view_rows=FIXED_VIEW_ROWS, view_cols=FIXED_VIEW_COLS)

    last_move_time = 0
    move_delay = 140  # milliseconds
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game.in_room:
                if event.key == pygame.K_q:
                    game.exit_room()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dx -= 1
        if keys[pygame.K_s]:
            dx += 1
        if keys[pygame.K_a]:
            dy -= 1
        if keys[pygame.K_d]:
            dy += 1

        if dx != 0 or dy != 0:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= move_delay:
                game.move_hero(dx, dy)
                last_move_time = current_time

        if game.in_room:
            view.draw_room(game.active_room, WIDTH, HEIGHT)
        else:
            view.draw_maze(game.dungeon, game.dungeon.hero_x, game.dungeon.hero_y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
