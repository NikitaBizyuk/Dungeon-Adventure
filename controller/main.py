import pygame
import math
from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.OOPillars import OOPillars
from model.room import Room


def main():
    pygame.init()

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Adventure")

    FIXED_VIEW_ROWS = 15
    CELL_SIZE = HEIGHT // FIXED_VIEW_ROWS
    FIXED_VIEW_COLS = WIDTH // CELL_SIZE

    clock = pygame.time.Clock()
    view = GameView(screen, CELL_SIZE, view_rows=FIXED_VIEW_ROWS, view_cols=FIXED_VIEW_COLS)

    hero_last_move_time = 0
    hero_move_delay = 150
    running = True
    state = "main_menu"
    pause_state = False
    resume_countdown = 0
    prev_menu_state = None  # <--- Added
    game = None
    hero_screen_x = 0
    hero_screen_y = 0

    while running:
        screen.fill((0, 0, 0))
        if state in ["main_menu", "difficulty_menu", "about_screen", "pause_menu"]:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
        else:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

        if game and state == "playing":
            if game.in_room:
                hero_r, hero_c = game.active_room.get_hero_position()
            else:
                hero_r, hero_c = game.dungeon.hero_x, game.dungeon.hero_y

            start_r = max(0, min(game.dungeon.rows - FIXED_VIEW_ROWS, hero_r - FIXED_VIEW_ROWS // 2))
            start_c = max(0, min(game.dungeon.cols - FIXED_VIEW_COLS, hero_c - FIXED_VIEW_COLS // 2))
            hero_screen_x = (hero_c - start_c) * CELL_SIZE + CELL_SIZE // 2
            hero_screen_y = (hero_r - start_r) * CELL_SIZE + CELL_SIZE // 2

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
                            prev_menu_state = "main_menu"
                            state = "about_screen"
                        elif button.text == "QUIT":
                            running = False

            elif state == "difficulty_menu":
                for button in view.difficulty_buttons:
                    if button.is_clicked(event):
                        difficulty = button.text.lower()
                        Room.set_difficulty(difficulty)
                        game = DungeonAdventure()
                        print(f"Started game on {difficulty.upper()}")
                        state = "playing"

            elif state == "about_screen":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if prev_menu_state == "pause_menu":
                        state = "pause_menu"
                    else:
                        state = "main_menu"
                        pause_state = False
                    prev_menu_state = None

            elif state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "pause_menu"
                    pause_state = True
                elif not pause_state:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            view.show_inventory = not view.show_inventory
                        elif game.in_room and event.key == pygame.K_q:
                            game.exit_room()
                        elif event.key == pygame.K_e:
                            game.perform_ranged_attack(CELL_SIZE)
                        elif event.key == pygame.K_SPACE:
                            if game.in_room:
                                special_message = game.perform_special_attack()
                                view.display_message(special_message)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            game.perform_melee_attack()
                            view.show_melee_attack()
                        elif event.button == 3:
                            game.perform_ranged_attack(CELL_SIZE)
                    elif event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        dx = mouse_x - hero_screen_x
                        dy = mouse_y - hero_screen_y
                        length = math.hypot(dx, dy)
                        if length != 0:
                            raw_vector = pygame.math.Vector2(dx / length, dy / length)
                            smoothed = pygame.math.Vector2(game.aim_vector).lerp(raw_vector, 0.1)
                            game.aim_vector = (smoothed.x, smoothed.y)

            elif state == "pause_menu":
                for button in view.pause_buttons:
                    if button.is_clicked(event):
                        if button.text == "RESUME":
                            resume_countdown = 180  # 3 sec @ 60 fps
                            state = "countdown"
                        elif button.text == "SAVE":
                            print("SAVE not implemented yet.")
                        elif button.text == "ABOUT":
                            prev_menu_state = "pause_menu"
                            state = "about_screen"
                        elif button.text == "BACK":
                            game = None
                            state = "main_menu"
                            pause_state = False

        if state == "main_menu":
            view.draw_buttons(view.menu_buttons)
        elif state == "difficulty_menu":
            view.draw_buttons(view.difficulty_buttons)
        elif state == "about_screen":
            view.draw_about_screen()
        elif state == "pause_menu":
            view.draw_buttons(view.pause_buttons)
        elif state == "countdown":
            pause_state = True
            seconds = resume_countdown // 60 + 1
            font = pygame.font.Font(None, 200)
            text = font.render(str(seconds), True, (255, 255, 255))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)
            resume_countdown -= 1
            if resume_countdown <= 0:
                state = "playing"
                pause_state = False
        elif state == "playing":
            if not pause_state:
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                if keys[pygame.K_w]: dx -= 1
                if keys[pygame.K_s]: dx += 1
                if keys[pygame.K_a]: dy -= 1
                if keys[pygame.K_d]: dy += 1

                game.move_monsters()
                game.monster_attack_hero()
                game.update_projectiles(view.cell_size)

                if dx != 0 or dy != 0:
                    current_time = pygame.time.get_ticks()
                    if current_time - hero_last_move_time >= hero_move_delay:
                        game.move_hero(dx, dy)
                        hero_last_move_time = current_time

            if game.in_room:
                view.draw_room(game, WIDTH, HEIGHT, game.get_hero(), game.get_backpack(), Ogre, Skeleton, Gremlin,
                               OOPillars.ENCAPSULATION.symbol, OOPillars.POLYMORPHISM.symbol,
                               OOPillars.INHERITANCE.symbol, OOPillars.ABSTRACTION.symbol)
            else:
                view.draw_maze(game, WIDTH, HEIGHT, game.get_hero(), game.get_backpack())

            now = pygame.time.get_ticks()
            if game.special_active and now - game.last_special_used > game.special_duration:
                game.special_active = False

            if game.special_active:
                time_left = (game.special_duration - (now - game.last_special_used)) / 1000
                status = f"Special: Active ({time_left:.1f}s)"
            elif now - game.last_special_used < game.special_cooldown:
                cd_left = (game.special_cooldown - (now - game.last_special_used)) / 1000
                status = f"Special: Cooling Down ({cd_left:.1f}s)"
            else:
                status = "Special: Ready"

            view.draw_status_bar(screen, status)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



if __name__ == "__main__":
    main()

