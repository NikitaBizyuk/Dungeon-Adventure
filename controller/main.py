import pygame
import math

from controller.dungeon_adventure import DungeonAdventure
from view.game_view import GameView
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.OOPillars import OOPillars
from model.room import Room

# Hero classes for the selection step
from model.Priestess import Priestess
from model.warrior import Warrior
from model.Thief import Thief


def main() -> None:
    pygame.init()

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Adventure")

    FIXED_VIEW_ROWS = 15
    CELL_SIZE = HEIGHT // FIXED_VIEW_ROWS
    FIXED_VIEW_COLS = WIDTH // CELL_SIZE

    clock = pygame.time.Clock()
    view = GameView(
        screen,
        CELL_SIZE,
        view_rows=FIXED_VIEW_ROWS,
        view_cols=FIXED_VIEW_COLS,
    )

    hero_last_move_time = 0
    hero_move_delay = 150

    running = True
    state = "main_menu"
    pause_state = False
    resume_countdown = 0
    prev_menu_state: str | None = None

    game: DungeonAdventure | None = None
    hero_screen_x = 0
    hero_screen_y = 0

    # Difficulty chosen, waiting for hero pick
    pending_difficulty: str | None = None

    # ──────────────────────────────────────────────────────────────
    while running:
        screen.fill((0, 0, 0))

        # Show / hide cursor
        if state in {
            "main_menu",
            "difficulty_menu",
            "hero_menu",
            "about_screen",
            "pause_menu",
        }:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
        else:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True)

        # Center camera on hero
        if game and state == "playing":
            if game.in_room:
                hero_r, hero_c = game.active_room.get_hero_position()
            else:
                hero_r, hero_c = game.dungeon.hero_x, game.dungeon.hero_y

            start_r = max(
                0, min(game.dungeon.rows - FIXED_VIEW_ROWS, hero_r - FIXED_VIEW_ROWS // 2)
            )
            start_c = max(
                0, min(game.dungeon.cols - FIXED_VIEW_COLS, hero_c - FIXED_VIEW_COLS // 2)
            )

            hero_screen_x = (hero_c - start_c) * CELL_SIZE + CELL_SIZE // 2
            hero_screen_y = (hero_r - start_r) * CELL_SIZE + CELL_SIZE // 2

        # ───────────────────────── EVENTS ─────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Main Menu ---------------------------------------------------
            elif state == "main_menu":
                for button in view.menu_buttons:
                    if button.is_clicked(event):
                        if button.text == "PLAY":
                            state = "difficulty_menu"
                        elif button.text == "LOAD":
                            print("LOAD not implemented yet.")
                        elif button.text == "ABOUT":
                            prev_menu_state = "main_menu"
                            state = "about_screen"
                        elif button.text == "QUIT":
                            running = False

            # Difficulty Menu --------------------------------------------
            elif state == "difficulty_menu":
                for button in view.difficulty_buttons:
                    if button.is_clicked(event):
                        difficulty = button.text.lower()
                        Room.set_difficulty(difficulty)
                        pending_difficulty = difficulty
                        state = "hero_menu"

            # Hero Menu --------------------------------------------------
            elif state == "hero_menu":
                for button in view.hero_buttons:
                    if button.is_clicked(event):
                        choice = button.text.upper()
                        hero_cls = {
                            "WARRIOR": Warrior,
                            "PRIESTESS": Priestess,
                            "THIEF": Thief,
                        }[choice]

                        game = DungeonAdventure(hero_cls=hero_cls, hero_name="Rudy")
                        print(f"Started {choice} on {pending_difficulty.upper()}")
                        state = "playing"

            # About Screen ----------------------------------------------
            elif state == "about_screen":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = prev_menu_state or "main_menu"
                    pause_state = state == "pause_menu"
                    prev_menu_state = None

            # Playing ----------------------------------------------------
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
                        elif event.key == pygame.K_SPACE and game.in_room:
                            msg = game.perform_special_attack()
                            view.display_message(msg)
                        elif event.key == pygame.K_h:
                            pack = game.get_backpack()
                            if pack.get_healing_cntr() > 0:
                                pack.use_healing_potion()
                                hero = game.get_hero()
                                hero.health_points = min(
                                    hero.health_points + 20, hero._max_health_points
                                )
                                view.display_message("Used Health Potion (+20 HP)", 2000)
                        elif event.key == pygame.K_v:
                            pack = game.get_backpack()
                            if pack.use_vision_potion():
                                game.vision_reveal_start = pygame.time.get_ticks()
                                view.display_message(
                                    "Vision Potion used! Maze revealed briefly.", 2500
                                )

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
                        if length:
                            raw = pygame.math.Vector2(dx / length, dy / length)
                            smoothed = pygame.math.Vector2(game.aim_vector).lerp(
                                raw, 0.1
                            )
                            game.aim_vector = (smoothed.x, smoothed.y)

                    elif game.get_backpack().found_all_pillars():
                        view.display_message(
                            "🎉 Congrats! You found all 4 Pillars of OOP!", 3000
                        )

            # Pause Menu -------------------------------------------------
            elif state == "pause_menu":
                for button in view.pause_buttons:
                    if button.is_clicked(event):
                        if button.text == "RESUME":
                            resume_countdown = 180  # 3 s @ 60 fps
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

        # ───────────────────────── DRAW ──────────────────────────
        if state == "main_menu":
            view.draw_buttons(view.menu_buttons)

        elif state == "difficulty_menu":
            view.draw_buttons(view.difficulty_buttons)

        elif state == "hero_menu":
            view.draw_buttons(view.hero_buttons)

        elif state == "about_screen":
            view.draw_about_screen()

        elif state == "pause_menu":
            view.draw_buttons(view.pause_buttons)

        elif state == "countdown":
            pause_state = True
            seconds = resume_countdown // 60 + 1
            large_font = pygame.font.Font(None, 200)
            text = large_font.render(str(seconds), True, (255, 255, 255))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, rect)
            resume_countdown -= 1
            if resume_countdown <= 0:
                state = "playing"
                pause_state = False

        elif state == "playing":
            if not pause_state:
                keys = pygame.key.get_pressed()
                dx = dy = 0
                if keys[pygame.K_w]:
                    dx -= 1
                if keys[pygame.K_s]:
                    dx += 1
                if keys[pygame.K_a]:
                    dy -= 1
                if keys[pygame.K_d]:
                    dy += 1

                game.move_monsters()
                game.monster_attack_hero()
                game.update_projectiles(view.cell_size)

                if dx or dy:
                    now = pygame.time.get_ticks()
                    if now - hero_last_move_time >= hero_move_delay:
                        game.move_hero(dx, dy)
                        hero_last_move_time = now

            if game.in_room:
                view.draw_room(
                    game,
                    WIDTH,
                    HEIGHT,
                    game.get_hero(),
                    game.get_backpack(),
                    Ogre,
                    Skeleton,
                    Gremlin,
                    OOPillars.ENCAPSULATION.symbol,
                    OOPillars.POLYMORPHISM.symbol,
                    OOPillars.INHERITANCE.symbol,
                    OOPillars.ABSTRACTION.symbol,
                )
            else:
                view.draw_maze(
                    game, WIDTH, HEIGHT, game.get_hero(), game.get_backpack()
                )

            now = pygame.time.get_ticks()
            if (
                game.special_active
                and now - game.last_special_used > game.special_duration
            ):
                game.special_active = False

            if game.special_active:
                left = (game.special_duration - (now - game.last_special_used)) / 1000
                status = f"Special: Active ({left:.1f}s)"
            elif now - game.last_special_used < game.special_cooldown:
                cd = (game.special_cooldown - (now - game.last_special_used)) / 1000
                status = f"Special: Cooling Down ({cd:.1f}s)"
            else:
                status = "Special: Ready"

            view.draw_status_bar(screen, status)

        # Frame done
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()