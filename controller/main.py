import pygame
import random
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView


def main():
    pygame.init()

    # Fullscreen mode
    screen_info = pygame.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Adventure")

    CELL_SIZE = 48  # zoomed in
    VIEW_COLS = WIDTH // CELL_SIZE
    VIEW_ROWS = HEIGHT // CELL_SIZE

    clock = pygame.time.Clock()
    game = DungeonAdventure(view_rows=VIEW_ROWS, view_cols=VIEW_COLS)
    view = GameView(screen, CELL_SIZE, VIEW_ROWS, VIEW_COLS)

    last_move_time = 0
    move_delay = 150  # ms
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game.in_room and event.key == pygame.K_q:
                    game.exit_room()

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]: dx = -1
        if keys[pygame.K_s]: dx = 1
        if keys[pygame.K_a]: dy = -1
        if keys[pygame.K_d]: dy = 1

        if dx or dy:
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