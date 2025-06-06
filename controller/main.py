import pygame
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView
from view.menu_button import Button
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre

def main():
    a=5
    print(a.__abs__())
    pygame.init()

    # Fullscreen mode
    info = pygame.display.Info()
    WIDTH = info.current_w - 70
    HEIGHT = info.current_h - 100

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dungeon Adventure")

    FIXED_VIEW_ROWS = 15
    CELL_SIZE = HEIGHT // FIXED_VIEW_ROWS
    FIXED_VIEW_COLS = WIDTH // CELL_SIZE

    clock = pygame.time.Clock()
    game = DungeonAdventure()
    view = GameView(screen, CELL_SIZE, view_rows=FIXED_VIEW_ROWS, view_cols=FIXED_VIEW_COLS)

    hero_last_move_time = 0
    hero_move_delay = 150
    running = True
    state = "main_menu" 
    game = None

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == "main_menu":
                for button in view.menu_buttons:
                    if button.is_clicked(event):
                        if button.text == "PLAY":
                            state = "difficulty_menu"
                        elif button.text == "LOAD":
                            print("NOT IMPLEMENTED YET")
                        elif button.text == "ABOUT":
                            print("Dungeon Adventures VERSION 1.0")
                        elif button.text == "QUIT":
                            running = False

            elif state == "difficulty_menu":
                for button in view.difficulty_buttons:
                    if button.is_clicked(event):
                        difficulty = button.text.lower()
                        from model.room import Room
                        Room.set_difficulty(difficulty)
                        game = DungeonAdventure()
                        if hasattr(game, "set_difficulty"):
                            game.set_difficulty(difficulty)
                        print(f"Started game on {difficulty.upper()}")
                        state = "playing"

            elif state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = "main_menu"
                    elif game.in_room and event.key == pygame.K_q:
                        game.exit_room()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.perform_melee_attack()
                    view.show_melee_attack()

        if state == "main_menu":
            view.draw_buttons(view.menu_buttons)
        elif state == "difficulty_menu":
            view.draw_buttons(view.difficulty_buttons)
        elif state == "playing":
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_w]: dx -= 1
            if keys[pygame.K_s]: dx += 1
            if keys[pygame.K_a]: dy -= 1
            if keys[pygame.K_d]: dy += 1

            game.move_monsters()
            if dx != 0 or dy != 0:
                current_time = pygame.time.get_ticks()
                if current_time - hero_last_move_time >= hero_move_delay:
                    game.move_hero(dx, dy)
                    hero_last_move_time = current_time

            if game.in_room:
                hero_r, hero_c = game.active_room.get_hero_position()
                room = game.active_room
            else:
                hero_r = game.dungeon.hero_x
                hero_c = game.dungeon.hero_y

            start_r = max(0, min(game.dungeon.rows - FIXED_VIEW_ROWS, hero_r - FIXED_VIEW_ROWS // 2))
            start_c = max(0, min(game.dungeon.cols - FIXED_VIEW_COLS, hero_c - FIXED_VIEW_COLS // 2))
            hero_screen_x = (hero_c - start_c) * CELL_SIZE + CELL_SIZE // 2
            hero_screen_y = (hero_r - start_r) * CELL_SIZE + CELL_SIZE // 2

            mouse_x, mouse_y = pygame.mouse.get_pos()
            aim_dx = mouse_x - hero_screen_x
            aim_dy = mouse_y - hero_screen_y
            length = (aim_dx ** 2 + aim_dy ** 2) ** 0.5
            if length != 0:
                game.aim_vector = (aim_dx / length, aim_dy / length)

            if game.in_room:
                view.draw_room(game, WIDTH, HEIGHT, Ogre, Skeleton, Gremlin)
            else:
                view.draw_maze(game)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
