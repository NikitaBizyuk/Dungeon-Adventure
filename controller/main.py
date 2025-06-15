import pygame
import math
from controller.dungeon_adventure import DungeonAdventure
from controller.save_load import save_game, load_game
from model.AnimatedHero  import AnimatedHero
from view.game_view import GameView
from model.Skeleton import Skeleton
from model.Gremlin import Gremlin
from model.Ogre import Ogre
from model.OOPillars import OOPillars
from model.Room import Room

# Hero classes for the selection step
from model.Priestess import Priestess
from model.Warrior import Warrior
from model.Thief import Thief

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
    prev_menu_state = None
    game = None
    hero_screen_x = 0
    hero_screen_y = 0
    typed_name = ""
    typing_name = True
    name_max_length = 12
    confirmed_name = False
    dead_start = None

    pending_difficulty: str | None = None

    while running:
        screen.fill((0, 0, 0))
        if state in ["main_menu", "difficulty_menu", "about_screen", "pause_menu", "hero_menu"]:
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
            if isinstance(game.hero, AnimatedHero):
                mouse_x, _ = pygame.mouse.get_pos()
                game.hero.facing_right = mouse_x >= hero_screen_x
            hero_screen_y = (hero_r - start_r) * CELL_SIZE + CELL_SIZE // 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if state == "about_screen":
                    state = prev_menu_state if prev_menu_state else "main_menu"
                    prev_menu_state = None
                    pause_state = False
                elif state == "difficulty_menu":
                    state = "main_menu"
                elif state == "hero_menu":
                    state = "difficulty_menu"
                elif state == "pause_menu":
                    state = "main_menu"
                    pause_state = False
                elif state == "playing":
                    state = "pause_menu"
                    pause_state = True

            elif state == "main_menu":
                for button in view.menu_buttons:
                    if button.is_clicked(event):
                        if button.text == "PLAY":
                            typed_name = ""
                            typing_name = True
                            confirmed_name = False
                            state = "difficulty_menu"
                        elif button.text == "LOAD":
                            view._draw_transient_message("Loading... Please wait")
                            pygame.time.delay(300)  # Give time for the user to see the message
                            loaded_game = load_game()
                            if loaded_game:
                                loaded_game.attach_view(view)

                                # ✅ Promote to AnimatedHero if needed
                                if not isinstance(loaded_game.hero, AnimatedHero):
                                    prev = loaded_game.hero

                                    # Dynamically create an animated version of the same hero type
                                    if isinstance(prev, Warrior):
                                        new_hero = Warrior(prev.name)
                                    elif isinstance(prev, Priestess):
                                        new_hero = Priestess(prev.name)
                                    elif isinstance(prev, Thief):
                                        new_hero = Thief(prev.name)
                                    else:
                                        new_hero = Warrior(prev.name)  # fallback

                                    # ⛑ Copy essential runtime fields manually
                                    new_hero.health_points = prev.health_points
                                    new_hero.pillars_found = prev.pillars_found
                                    new_hero.chance_to_block = prev.chance_to_block

                                    # ✅ Set animation state defaults
                                    new_hero.current_animation = "idle"
                                    new_hero._last_animation_change = pygame.time.get_ticks()
                                    new_hero._moving = False
                                    new_hero.facing_right = True
                                    new_hero.getting_hit = False

                                    loaded_game._hero = new_hero

                                game = loaded_game
                                state = "playing"
                                view.display_message("Game Loaded!", 2000)
                            else:
                                view.display_message("⚠ No save found or failed to load!", 2000)

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
                        pending_difficulty = difficulty
                        state = "hero_menu"

            elif state == "hero_menu":
                if event.type == pygame.KEYDOWN and typing_name:
                    if event.key == pygame.K_RETURN and typed_name.strip():
                        typing_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        typed_name = typed_name[:-1]
                    elif len(typed_name) < name_max_length:
                        typed_name += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(view, "confirm_rect") and view.confirm_rect.collidepoint(event.pos):
                        if typed_name.strip():
                            confirmed_name = True
                            typing_name = False
                            view.display_message("Name confirmed!", 1500)
                        else:
                            view.display_message("Enter a valid name", 1500)


                    elif hasattr(view, "edit_rect") and view.edit_rect and view.edit_rect.collidepoint(event.pos):
                        typing_name = True
                        confirmed_name = False
                        view.display_message("✏ Edit your name", 1500)

                    elif confirmed_name:
                        for button in view.hero_buttons:
                            if button.is_clicked(event):
                                choice = button.text.upper()
                                hero_cls = {
                                    "WARRIOR": Warrior,
                                    "PRIESTESS": Priestess,
                                    "THIEF": Thief,
                                }[choice]

                                hero_name = typed_name.strip()
                                import time
                                print("⏳ Game init started:", time.time())
                                view._draw_transient_message("Creating game...")
                                pygame.time.delay(300)
                                game = DungeonAdventure(view,hero_cls=hero_cls, hero_name=hero_name)
                                game.attach_view(view)
                                print(f"Started {hero_name} the {choice} on {pending_difficulty.upper()}")
                                state = "playing"
                                print("Game init finished:", time.time())

            elif state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "pause_menu"
                    pause_state = True
                elif not pause_state:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_TAB:
                            view.show_inventory = not view.show_inventory
                        elif event.key == pygame.K_e:
                            game.perform_ranged_attack(CELL_SIZE)
                        elif event.key == pygame.K_SPACE:
                            if game.in_room:
                                special_message = game.perform_special_attack()
                                view.display_message(special_message)
                        elif event.key == pygame.K_h:
                            if game.backpack.healing_cntr > 0:
                                game.backpack.use_healing_potion()
                                game.hero.health_points = min(
                                    game.hero.health_points + 20,
                                    game.hero.max_health_points
                                )
                                view.display_message("Used Health Potion (+20 HP)", 2000)
                        elif event.key == pygame.K_v:
                            if game.backpack.use_vision_potion():
                                game.vision_reveal_start = pygame.time.get_ticks()
                                view.display_message("Vision Potion used! Maze revealed briefly.", 2500)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if isinstance(game.hero, AnimatedHero):
                                if dx != 0 or dy != 0:
                                    game.hero.current_animation = "run_slashing"
                                else:
                                    game.hero.current_animation = "slashing"
                                game.hero._last_animation_change = pygame.time.get_ticks()

                            game.perform_melee_attack()
                            view.show_melee_attack()
                        elif event.button == 3:
                            if isinstance(game.hero, AnimatedHero):
                                if dx != 0 or dy != 0:
                                    game.hero.current_animation = "run_throwing"
                                else:
                                    game.hero.current_animation = "throwing"
                                game.hero._last_animation_change = pygame.time.get_ticks()

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
                            resume_countdown = 180
                            state = "countdown"
                        elif button.text == "SAVE":
                            view._draw_transient_message("💾 Saving...")
                            pygame.time.delay(300)
                            try:
                                save_game(game)
                                view.display_message("✅ Game Saved Successfully!", 2000)
                            except Exception:
                                view.display_message("❌ Failed to Save Game!", 2000)
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
        elif state == "hero_menu":
            view.draw_buttons(view.hero_buttons)
            view.draw_name_input(screen, typed_name, typing_name, confirmed_name)
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

                if isinstance(game.hero, AnimatedHero):
                    game.hero._moving = dx != 0 or dy != 0
                game.move_monsters()
                game.monster_attack_hero()
                game.update_projectiles(view.cell_size)

                if dx != 0 or dy != 0:
                    current_time = pygame.time.get_ticks()
                    if current_time - hero_last_move_time >= hero_move_delay:
                        result = game.move_hero(dx, dy, view)
                        if isinstance(game.hero, AnimatedHero):
                            game.hero._moving = dx != 0 or dy != 0
                        if isinstance(game.hero, AnimatedHero):
                            if dy < 0:  # moving left
                                game.hero.facing_right = False
                            elif dy > 0:  # moving right
                                game.hero.facing_right = True
                        if result == "win":
                            state = "main_menu"
                            continue
                        if isinstance(game.hero, AnimatedHero):
                            if game.hero.current_animation not in ["slashing", "un_slashing", "throwing",
                                                                   "run_throwing"]:
                                game.hero.current_animation = "running" if game.hero._moving else "idle"
                        hero_last_move_time = current_time
                if game.game_over:
                    view.display_message("💀 Game Over: No lives left!", 3000)
                    dead_start = pygame.time.get_ticks()
                    state = "dead"
                    continue

            if game.in_room:
                view.draw_room(game, WIDTH, HEIGHT, game.hero, game.backpack, Ogre, Skeleton, Gremlin,
                               OOPillars.ENCAPSULATION.symbol, OOPillars.POLYMORPHISM.symbol,
                               OOPillars.INHERITANCE.symbol, OOPillars.ABSTRACTION.symbol)
            else:
                view.draw_maze(game, WIDTH, HEIGHT, game.hero, game.backpack)

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

            status = f"Lives: {game.lives_remaining}   |   {status}"
            view.draw_status_bar(screen, status)

        elif state == "dead":
            # draw Game-Over screen
            font_big   = pygame.font.Font(None, 120)
            font_small = pygame.font.Font(None,  50)

            txt = font_big.render("GAME OVER", True, (220, 20, 20))
            sub = font_small.render("Returning to main menu...", True, (255, 255, 255))

            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            screen.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40)))

            # after 3 s, return to main menu
            if dead_start and pygame.time.get_ticks() - dead_start > 3000:
                state = "main_menu"
                pause_state = False
                game = None
                dead_start = None
                view.message = ""  # clear any lingering HUD message

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
