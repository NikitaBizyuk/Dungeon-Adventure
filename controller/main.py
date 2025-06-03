from xml.dom.minidom import ReadOnlySequentialNamedNodeMap

import pygame
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView
from model.room import Room
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre

def main():
    pygame.init()

    # Fullscreen mode
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Adventure")

    FIXED_VIEW_ROWS = 15
    CELL_SIZE = HEIGHT // FIXED_VIEW_ROWS
    FIXED_VIEW_COLS = WIDTH // CELL_SIZE

    clock = pygame.time.Clock()
    game = DungeonAdventure()
    view = GameView(screen, CELL_SIZE, view_rows=FIXED_VIEW_ROWS, view_cols=FIXED_VIEW_COLS)


    last_move_time = 0
    # If you have a lot of tuning values put them in a config file so you can just change it from there
    hero_last_move_time = 0
    hero_move_delay = 150  # ms
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game.in_room:
                if event.key == pygame.K_q:
                    game.exit_room()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.perform_melee_attack()
                    view.show_melee_attack()

        # --- Movement Input ---
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]: dx -= 1
        if keys[pygame.K_s]: dx += 1
        if keys[pygame.K_a]: dy -= 1
        if keys[pygame.K_d]: dy += 1

        if dx != 0 or dy != 0:
            current_time = pygame.time.get_ticks()
            if current_time - hero_last_move_time >= hero_move_delay:
                game.move_hero(dx, dy)
                game.move_monsters()
                hero_last_move_time = current_time

        # --- 📍 Mouse-Aim Vector Update (INSERTED HERE) ---
        if game.in_room:
            hero_r, hero_c = game.active_room.get_hero_position()

            room_height = game.active_room.height
            room_width = game.active_room.width

            start_r = max(0, min(max(0, room_height - FIXED_VIEW_ROWS), hero_r - FIXED_VIEW_ROWS // 2))
            start_c = max(0, min(max(0, room_width - FIXED_VIEW_COLS), hero_c - FIXED_VIEW_COLS // 2))

            hero_screen_x = (hero_c - start_c) * CELL_SIZE + CELL_SIZE // 2
            hero_screen_y = (hero_r - start_r) * CELL_SIZE + CELL_SIZE // 2
        else:
            hero_r = game.dungeon.hero_x
            hero_c = game.dungeon.hero_y

            start_r = max(0, min(game.dungeon.rows - FIXED_VIEW_ROWS, hero_r - FIXED_VIEW_ROWS // 2))
            start_c = max(0, min(game.dungeon.cols - FIXED_VIEW_COLS, hero_c - FIXED_VIEW_COLS // 2))

            hero_screen_x = (hero_c - start_c) * CELL_SIZE + CELL_SIZE // 2
            hero_screen_y = (hero_r - start_r) * CELL_SIZE + CELL_SIZE // 2

        # Mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate aim vector
        aim_dx = mouse_x - hero_screen_x
        aim_dy = mouse_y - hero_screen_y
        length = (aim_dx ** 2 + aim_dy ** 2) ** 0.5
        if length != 0:
            game.aim_vector = (aim_dx / length, aim_dy / length)

        # --- Draw Maze or Room View ---
        if game.in_room:
            ogre = Ogre
            skeleton = Skeleton
            gremlin = Gremlin
            view.draw_room(game, WIDTH, HEIGHT,ogre,skeleton,gremlin)
            room = Room
        else:
            view.draw_maze(game)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()