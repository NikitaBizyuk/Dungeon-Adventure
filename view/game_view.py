import pygame
import os
import math

from view.menu_button import Button


class GameView:
    def __init__(self, screen, cell_size, view_rows, view_cols):
        self.screen = screen
        self.cell_size = cell_size
        self.view_rows = view_rows
        self.view_cols = view_cols

        self.last_attack_time = 0
        self.attack_duration = 150

        self.font = pygame.font.Font(None, 60)

        # menus
        self.menu_buttons = self.create_menu_buttons()
        self.difficulty_buttons = self._create_difficulty_buttons()
        self.hero_buttons = self._create_hero_buttons()
        self.pause_buttons = self._create_pause_menu_buttons()

        # inventory pop-up & transient messages
        self.show_inventory = False
        self.message = ""
        self.message_start_time = 0
        self.message_duration = 0

        # menu background
        img_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "DungeonBackground.png"
        )
        self.menu_bg = pygame.transform.scale(
            pygame.image.load(img_path).convert(), self.screen.get_size()
        )

        self.pause_buttons = self._create_pause_menu_buttons()
        self.edit_rect = None

    # ───────────────────────── Button factories ──────────────────────
    def create_menu_buttons(self):
        w, h = self.screen.get_size()
        mk = lambda txt, y: Button(
            txt, pygame.Rect(w // 2 - 100, y, 200, 60),
            self.font, (200, 200, 200), (255, 255, 0)
        )
        return [
            Button(
                "PLAY",
                pygame.Rect(w // 2 - 100, h // 2 - 150, 200, 60),
                self.font,
                (200, 200, 200),
                (255, 255, 0),
            ),
            Button(
                "LOAD",
                pygame.Rect(w // 2 - 100, h // 2 - 50, 200, 60),
                self.font,
                (200, 200, 200),
                (255, 255, 0),
            ),
            Button(
                "ABOUT",
                pygame.Rect(w // 2 - 100, h // 2 + 50, 200, 60),
                self.font,
                (200, 200, 200),
                (255, 255, 0),
            ),
            Button(
                "QUIT",
                pygame.Rect(w // 2 - 100, h // 2 + 150, 200, 60),
                self.font,
                (200, 200, 200),
                (255, 255, 0),
            ),
        ]

    def _create_difficulty_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("EASY", pygame.Rect(w // 2 - 100, h // 2 - 100, 200, 60), self.font, (200, 200, 200), (0, 255, 0)),
            Button("MEDIUM", pygame.Rect(w // 2 - 100, h // 2, 200, 60), self.font, (200, 200, 200), (255, 165, 0)),
            Button("HARD", pygame.Rect(w // 2 - 100, h // 2 + 100, 200, 60), self.font, (200, 200, 200), (255, 0, 0)),
        ]

    def _create_hero_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("WARRIOR", pygame.Rect(w // 2 - 150, h // 2 - 120, 300, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("PRIESTESS", pygame.Rect(w // 2 - 150, h // 2 - 40, 300, 60), self.font, (200, 200, 200), (0, 255, 255)),
            Button("THIEF", pygame.Rect(w // 2 - 150, h // 2 + 40, 300, 60), self.font, (200, 200, 200), (255, 165, 0)),
        ]

    def _create_pause_menu_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("RESUME", pygame.Rect(w // 2 - 100, h // 2 - 150, 200, 60), self.font, (200, 200, 200), (0, 255, 0)),
            Button("SAVE", pygame.Rect(w // 2 - 100, h // 2 - 50, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("ABOUT", pygame.Rect(w // 2 - 100, h // 2 + 50, 200, 60), self.font, (200, 200, 200), (0, 128, 255)),
            Button("BACK", pygame.Rect(w // 2 - 100, h // 2 + 150, 200, 60), self.font, (200, 200, 200), (255, 0, 0)),
        ]

    def draw_name_input(self, screen, typed_name, typing_name, confirmed_name):
        font = pygame.font.Font(None, 48)
        input_rect = pygame.Rect(screen.get_width() // 2 - 200, 150, 400, 60)

        # Draw input box
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

        # Add blinking cursor
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 and typing_name else ""
        text_surface = font.render(typed_name + cursor, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 15))

        # Confirm button
        confirm_font = pygame.font.Font(None, 36)
        confirm_text = confirm_font.render("Confirm", True, (0, 0, 0))
        self.confirm_rect = pygame.Rect(input_rect.right + 20, input_rect.y, 140, 60)
        confirm_color = (180, 255, 180) if confirmed_name else (200, 200, 200)
        pygame.draw.rect(screen, confirm_color, self.confirm_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.confirm_rect, 2)
        screen.blit(confirm_text, (self.confirm_rect.x + 20, self.confirm_rect.y + 15))

        # Edit button (only if confirmed)
        if confirmed_name:
            edit_font = pygame.font.Font(None, 36)
            edit_text = edit_font.render("✏️ Edit", True, (0, 0, 0))
            self.edit_rect = pygame.Rect(input_rect.left - 160, input_rect.y, 140, 60)
            pygame.draw.rect(screen, (255, 255, 200), self.edit_rect)
            pygame.draw.rect(screen, (255, 255, 255), self.edit_rect, 2)
            screen.blit(edit_text, (self.edit_rect.x + 10, self.edit_rect.y + 15))


    # ───────────────────────── Generic helpers ───────────────────────
    def draw_buttons(self, buttons):
        self.screen.blit(self.menu_bg, (0, 0))
        for button in buttons:
            button.draw(self.screen)

    def display_message(self, message: str, duration: int = 2000) -> None:
        self.message = message
        self.message_start_time = pygame.time.get_ticks()
        self.message_duration = duration

    def draw_message(self):
        if self.message and pygame.time.get_ticks() - self.message_start_time < self.message_duration:
            font = pygame.font.SysFont("georgia", 48, bold=True)
            lines = self.message.split('\n')  # Split the message on \n
            line_height = font.get_height() + 10

            total_height = len(lines) * line_height
            start_y = (self.screen.get_height() - total_height) // 2

            # Get the widest line to size the background box
            max_width = max(font.size(line)[0] for line in lines)
            box_width = max_width + 40
            box_height = total_height + 20

            box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            box_surface.fill((0, 0, 0, 180))  # Semi-transparent black
            box_rect = box_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(box_surface, box_rect)

            # Draw each line of text centered
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, (255, 215, 0))  # Gold
                text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, start_y + i * line_height))
                self.screen.blit(text_surface, text_rect)
        else:
            self.message = ""

    def draw_special_status(self, game, x: int = 20, y: int = 20) -> None:
        now = pygame.time.get_ticks()
        font = pygame.font.Font(None, 32)

        if game.special_active and now - game.last_special_used < game.special_duration:
            remaining = (game.special_duration - (now - game.last_special_used)) / 1000
            msg = f"Special: Active ({remaining:.1f}s)"
            color = (0, 255, 0)
        elif now - game.last_special_used < game.special_cooldown:
            remaining = (game.special_cooldown - (now - game.last_special_used)) / 1000
            msg = f"Special: Cooling down ({remaining:.1f}s)"
            color = (255, 0, 0)
        else:
            msg = "Special: Ready"
            color = (255, 255, 255)

        text = font.render(msg, True, color)
        background = pygame.Surface((text.get_width() + 20, text.get_height() + 10))
        background.set_alpha(150)
        background.fill((0, 0, 0))
        self.screen.blit(background, (x, y))
        self.screen.blit(text, (x + 10, y + 5))

    def draw_status_bar(self, screen, status_text: str) -> None:
        font = pygame.font.SysFont("Arial", 28)
        text_surface = font.render(status_text, True, (255, 255, 255))
        rect = pygame.Rect(10, 10, text_surface.get_width() + 20, text_surface.get_height() + 10)

        pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        screen.blit(text_surface, (rect.x + 10, rect.y + 5))

    # ───────────────────────── Maze view ─────────────────────────────
    def draw_maze(self, game, width, height, hero, backpack):
        dungeon = game.dungeon
        hero_x = dungeon.hero_x
        hero_y = dungeon.hero_y
        aim_dx, aim_dy = game.aim_vector

        start_r = max(0, min(dungeon.rows - self.view_rows, hero_x - self.view_rows // 2))
        start_c = max(0, min(dungeon.cols - self.view_cols, hero_y - self.view_cols // 2))
        end_r = min(start_r + self.view_rows, dungeon.rows)
        end_c = min(start_c + self.view_cols, dungeon.cols)

        base_colors = {
            "wall": (30, 30, 30),
            "hallway": (220, 220, 220),
            "door": (0, 128, 255),
            "exit": (0, 255, 128),
        }

        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                cell = dungeon.maze[r][c]
                screen_x = (c - start_c) * self.cell_size
                screen_y = (r - start_r) * self.cell_size
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)

                now = pygame.time.get_ticks()
                vision_active = (
                    game.vision_reveal_start
                    and now - game.vision_reveal_start < game.vision_reveal_duration
                )

                if not cell.explored:
                    color = (0, 0, 0)
                elif vision_active or cell.visible:
                    color = base_colors.get(cell.cell_type, (255, 0, 255))
                else:
                    base = base_colors.get(cell.cell_type, (100, 100, 100))
                    color = tuple(int(x * 0.35) for x in base)

                pygame.draw.rect(self.screen, color, rect)

        # Hero symbol
        hero_rect = pygame.Rect(
            (hero_y - start_c) * self.cell_size,
            (hero_x - start_r) * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
        pygame.draw.circle(self.screen, (255, 0, 0), hero_rect.center, self.cell_size // 3)

        # Aim line
        center_x = hero_rect.centerx
        center_y = hero_rect.centery
        end_x = int(center_x + aim_dx * 40)
        end_y = int(center_y + aim_dy * 40)
        pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

        # Melee arc
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < self.attack_duration:
            style = game.hero.get_melee_style()
            attack_angle = math.atan2(aim_dy, aim_dx)
            color = style["color"]
            arc_width = style["arc_width"]
            reach = style["reach"]
            swings = style.get("swings", 1)
            for i in range(swings):
                offset = (-1 + 2 * i) * (arc_width / 2) if swings > 1 else 0
                angle = attack_angle + offset
                ax = int(center_x + reach * math.cos(angle))
                ay = int(center_y + reach * math.sin(angle))
                pygame.draw.line(self.screen, color, (center_x, center_y), (ax, ay), 4)

        self.health_bar(width, height, hero)
        if self.show_inventory:
            self.draw_inventory(backpack)
        self.draw_message()

    # ───────────────────────── Room view ────────────────────────────
    def draw_room(
        self,
        game,
        width,
        height,
        hero,
        backpack,
        ogre_cls,
        skeleton_cls,
        gremlin_cls,
        pillar_1,
        pillar_2,
        pillar_3,
        pillar_4,
    ):
        room = game.active_room
        hero_r, hero_c = room.get_hero_position()
        monsters = room.get_monsters()

        start_r = max(0, min(max(0, room.height - self.view_rows), hero_r - self.view_rows // 2))
        start_c = max(0, min(max(0, room.width - self.view_cols), hero_c - self.view_cols // 2))
        end_r = min(start_r + self.view_rows, room.height)
        end_c = min(start_c + self.view_cols, room.width)

        room_tile_width = end_c - start_c
        room_tile_height = end_r - start_r
        cell_size = min(width // room_tile_width, height // room_tile_height)

        total_width_used = room_tile_width * cell_size
        total_height_used = room_tile_height * cell_size
        offset_x = (width - total_width_used) // 2
        offset_y = (height - total_height_used) // 2

        base_colors = {
            "wall": (40, 40, 40),
            "floor": (230, 230, 230),
            "door": (0, 128, 255),
            "pit": (0, 0, 0),  # black pits
            pillar_1: (255, 215, 0),
            pillar_2: (255, 215, 0),
            pillar_3: (255, 215, 0),
            pillar_4: (255, 215, 0),
            "Health Potion": (255, 192, 203),
            "Vision Potion": (128, 0, 128),
        }

        # Tiles
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                tile = room.get_tile(r, c)
                screen_x = offset_x + (c - start_c) * cell_size
                screen_y = offset_y + (r - start_r) * cell_size
                rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)
                color = base_colors.get(tile, (255, 0, 255))
                if tile in {"A", "E", "I", "P"}:
                    color = base_colors.get(tile, (255, 215, 0))
                pygame.draw.rect(self.screen, color, rect)

        # Hero
        center_x = offset_x + (hero_c - start_c) * cell_size + cell_size // 2
        center_y = offset_y + (hero_r - start_r) * cell_size + cell_size // 2
        pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), cell_size // 3)

        # Aim line
        aim_dx, aim_dy = game.aim_vector
        end_x = int(center_x + aim_dx * 40)
        end_y = int(center_y + aim_dy * 40)
        pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

        # Monsters
        for monster, (mr, mc) in monsters.items():
            screen_x = offset_x + (mc - start_c) * cell_size
            screen_y = offset_y + (mr - start_r) * cell_size
            pos = (
                screen_x + cell_size // 2,
                screen_y + cell_size // 2,
            )

            if isinstance(monster, ogre_cls):
                base_color = (0, 250, 0)
            elif isinstance(monster, skeleton_cls):
                base_color = (0, 0, 0)
            elif isinstance(monster, gremlin_cls):
                base_color = (0, 0, 250)
            else:
                base_color = (255, 0, 255)

            if hasattr(monster, "is_flashing") and monster.is_flashing():
                pygame.draw.circle(self.screen, (255, 0, 0), pos, cell_size // 2)

            pygame.draw.circle(self.screen, base_color, pos, cell_size // 3)

        # Projectiles
        for projectile in game.projectiles:
            px, py = projectile.position
            draw_x = offset_x + px - (start_c * cell_size)
            draw_y = offset_y + py - (start_r * cell_size)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(draw_x), int(draw_y)), 5)

        # Melee arc
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < self.attack_duration:
            style = game.hero.get_melee_style()
            attack_angle = math.atan2(aim_dy, aim_dx)
            color = style["color"]
            arc_width = style["arc_width"]
            reach = style["reach"]
            swings = style.get("swings", 1)
            for i in range(swings):
                offset = (-1 + 2 * i) * (arc_width / 2) if swings > 1 else 0
                angle = attack_angle + offset
                ax = int(center_x + reach * math.cos(angle))
                ay = int(center_y + reach * math.sin(angle))
                pygame.draw.line(self.screen, color, (center_x, center_y), (ax, ay), 4)

        self.health_bar(width, height, hero)
        if self.show_inventory:
            self.draw_inventory(backpack)
        self.draw_message()

    # ───────────────────────── UI widgets ───────────────────────────
    def health_bar(self, width, height, hero):
        max_bar_width = width - 800
        bar_height = 20
        bar_x = 20
        bar_y = height - bar_height - 10

        hp = hero.health_points
        max_hp = 100
        hp_ratio = max(hp / max_hp, 0)
        hp_bar_width = int(max_bar_width * hp_ratio)
        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            pygame.Rect(bar_x, bar_y, hp_bar_width, bar_height),
        )
        pygame.draw.rect(
            self.screen, (0, 0, 0), pygame.Rect(bar_x, bar_y, max_bar_width, bar_height), 2
        )
        font = pygame.font.Font(None, 30)

        # Display: PlayerName (ClassName)
        name_text = font.render(f"{hero.name} ({hero.__class__.__name__})", True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(bar_x + max_bar_width // 2, bar_y - 20))
        self.screen.blit(name_text, name_rect)

        # HP: current / max
        hp_text = font.render(f"HP: {hp}/{max_hp}", True, (255, 255, 255))
        hp_rect = hp_text.get_rect(center=(bar_x + max_bar_width // 2, bar_y + bar_height // 2))
        self.screen.blit(hp_text, hp_rect)

    def show_melee_attack(self):
        self.last_attack_time = pygame.time.get_ticks()

    def draw_inventory(self, backpack):
        inv_rect = pygame.Rect(100, 100, 400, 300)
        pygame.draw.rect(self.screen, (50, 50, 50), inv_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), inv_rect, 3)
        font = pygame.font.Font(None, 30)

        title = font.render("Inventory", True, (255, 255, 0))
        self.screen.blit(title, (inv_rect.x + 10, inv_rect.y + 10))

        items_to_display = {}
        if backpack.healing_cntr > 0:
            items_to_display["Health Potion"] = backpack.healing_cntr
        if backpack.vision_cntr > 0:
            items_to_display["Vision Potion"] = backpack.vision_cntr

        from collections import Counter

        inv_items = Counter(backpack.inventory)
        for item in inv_items:
            if item in {"A", "E", "I", "P"}:
                items_to_display[item] = inv_items[item]

        for idx, (item, count) in enumerate(items_to_display.items()):
            item_text = font.render(f"- {item}: {count}", True, (255, 255, 255))
            self.screen.blit(item_text, (inv_rect.x + 20, inv_rect.y + 40 + idx * 25))

    def draw_about_screen(self):
        self.screen.fill((15, 15, 15))

        lines = [
            "Dungeon Adventure Game",
            "Version: 1.0 — June 11th, 2025",
            "Authors: Rudolf Arakelyan, Nikita Bizyuk",
            "         Collins Mbugua, Ian Fuhr",
            "",
            "OBJECTIVE:",
            "Find all 4 Pillars of OOP:",
            " - Abstraction (A)",
            " - Encapsulation (E)",
            " - Inheritance (I)",
            " - Polymorphism (P)",
            "",
            "Enter rooms, defeat monsters, use potions,",
            "and escape the dungeon with all 4 pillars!",
            "",
            "CONTROLS:",
            " - Move: W A S D",
            " - Melee Attack: Left Click",
            " - Ranged Attack: Right Click or E",
            " - Special Ability: SPACE",
            " - Exit Room: Q",
            " - Health Potion: H",
            " - Vision Potion: V",
            " - Inventory: TAB",
            " - Pause / Menu / Back: ESC",
            "",
            "Press ESC to return to the previous menu.",
        ]

        screen_height, screen_width = self.screen.get_height(), self.screen.get_width()
        max_content_height = screen_height - 100
        line_height = max_content_height // len(lines)
        font_size = min(32, line_height - 4)

        font = pygame.font.SysFont("georgia", font_size, bold=True)
        bright_brown = (210, 140, 70)

        padding = 20
        box_width = screen_width - 160
        box_height = len(lines) * line_height + padding
        box_x = 80
        box_y = (screen_height - box_height) // 2

        pygame.draw.rect(self.screen, (25, 25, 25), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, bright_brown, (box_x, box_y, box_width, box_height), 4)

        y_offset = box_y + padding // 2
        for line in lines:
            text = font.render(line, True, bright_brown)
            text_rect = text.get_rect(center=(screen_width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += line_height


