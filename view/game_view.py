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
        self.menu_buttons = self.create_menu_buttons()
        self.difficulty_buttons = self.create_difficulty_buttons()
        self.show_inventory = False
        self.message = ""
        self.message_start_time = 0
        self.message_duration = 0
        image_path = os.path.join(os.path.dirname(__file__), "..", "assets", "DungeonBackground.png")
        self.menu_bg = pygame.image.load(image_path).convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, self.screen.get_size())

    def create_menu_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("PLAY", pygame.Rect(w // 2 - 100, h // 2 - 150, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("LOAD", pygame.Rect(w // 2 - 100, h // 2 - 50, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("ABOUT", pygame.Rect(w // 2 - 100, h // 2 + 50, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
            Button("QUIT", pygame.Rect(w // 2 - 100, h // 2 + 150, 200, 60), self.font, (200, 200, 200), (255, 255, 0)),
        ]

    def create_difficulty_buttons(self):
        w, h = self.screen.get_size()
        return [
            Button("EASY", pygame.Rect(w // 2 - 100, h // 2 - 100, 200, 60), self.font, (200, 200, 200), (0, 255, 0)),
            Button("MEDIUM", pygame.Rect(w // 2 - 100, h // 2, 200, 60), self.font, (200, 200, 200), (255, 165, 0)),
            Button("HARD", pygame.Rect(w // 2 - 100, h // 2 + 100, 200, 60), self.font, (200, 200, 200), (255, 0, 0)),
        ]

    def draw_buttons(self, buttons):
        self.screen.blit(self.menu_bg, (0, 0))
        for button in buttons:
            button.draw(self.screen)

    def display_message(self, message, duration=2000):
        self.message = message
        self.message_start_time = pygame.time.get_ticks()

        self.message_duration = duration

    def draw_message(self):
        if self.message and pygame.time.get_ticks() - self.message_start_time < self.message_duration:
            font = pygame.font.Font(None, 36)
            rendered = font.render(self.message, True, (255, 255, 0))
            self.screen.blit(rendered, (30, 60))  # adjust position as needed
        else:
            self.message = ""

    def draw_special_status(self, game, x=20, y=20):
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
        background.set_alpha(150)  # optional transparency
        background.fill((0, 0, 0))
        self.screen.blit(background, (x, y))
        self.screen.blit(text, (x + 10, y + 5))

    def draw_status_bar(self, screen, status_text):
        font = pygame.font.SysFont("Arial", 28)
        text_surface = font.render(status_text, True, (255, 255, 255))
        background_rect = pygame.Rect(10, 10, text_surface.get_width() + 20, text_surface.get_height() + 10)

        pygame.draw.rect(screen, (0, 0, 0), background_rect)  # black background
        pygame.draw.rect(screen, (255, 255, 255), background_rect, 2)  # white border
        screen.blit(text_surface, (background_rect.x + 10, background_rect.y + 5))

    def draw_maze(self, game,width, height,hero,backpack):
        dungeon = game.dungeon
        hero_x = dungeon.hero_x
        hero_y = dungeon.hero_y
        aim_dx, aim_dy = game.aim_vector
        view_rows, view_cols = self.view_rows, self.view_cols

        start_r = max(0, min(dungeon.rows - view_rows, hero_x - view_rows // 2))
        start_c = max(0, min(dungeon.cols - view_cols, hero_y - view_cols // 2))
        end_r = min(start_r + view_rows, dungeon.rows)
        end_c = min(start_c + view_cols, dungeon.cols)

        base_colors = {
            "wall": (30, 30, 30),
            "hallway": (220, 220, 220),
            "door": (0, 128, 255),
            "exit": (0, 255, 128)
        }
    #update variables better
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                cell = dungeon.maze[r][c]
                screen_x = (c - start_c) * self.cell_size
                screen_y = (r - start_r) * self.cell_size
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)

                now = pygame.time.get_ticks()
                vision_active = game.vision_reveal_start and now - game.vision_reveal_start < game.vision_reveal_duration
                if not cell.explored:
                    color = (0, 0, 0)
                elif vision_active or cell.visible:
                    color = base_colors.get(cell.cell_type, (255, 0, 255))
                else:
                    base = base_colors.get(cell.cell_type, (100, 100, 100))
                    color = tuple(int(x * 0.35) for x in base)

                pygame.draw.rect(self.screen, color, rect)

                if r == hero_x and c == hero_y:
                    pygame.draw.circle(self.screen, (255, 0, 0), rect.center, self.cell_size // 3)


                aim_dx, aim_dy = game.aim_vector
                center_x = (hero_y - start_c) * self.cell_size + self.cell_size // 2
                center_y = (hero_x - start_r) * self.cell_size + self.cell_size // 2
                end_x = int(center_x + aim_dx * 40)
                end_y = int(center_y + aim_dy * 40)
                pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

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


    def draw_room(self, game, width, height,hero,backpack,ogre,skeleton,gremlin,
                  pillar_1,pillar_2,pillar_3,pillar_4):
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

        # ✅ Compute screen offsets to center the room
        total_width_used = room_tile_width * cell_size
        total_height_used = room_tile_height * cell_size
        offset_x = (width - total_width_used) // 2
        offset_y = (height - total_height_used) // 2

        base_colors = {
            "wall": (40, 40, 40),
            "floor": (230, 230, 230),
            "door": (0, 128, 255),
            pillar_1: (255, 215, 0), #gold
            pillar_2: (255, 215, 0), #gold
            pillar_3: (255, 215, 0), #gold
            pillar_4: (255, 215, 0), #gold
            "Health Potion": (255, 192, 203), #pink for health
            "Vision Potion": (128, 0, 128) #purple for vision
        }

        # ─── Draw tiles ───
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                tile = room.get_tile(r, c)
                screen_x = offset_x + (c - start_c) * cell_size
                screen_y = offset_y + (r - start_r) * cell_size
                rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)
                color = base_colors.get(tile, (255, 0, 255))
               ## If tile is a pillar, make gold
                if (tile == "A" or tile == "E" or
                    tile == "I" or tile == "P"):
                    color = base_colors.get(tile,(255,215,0))
                pygame.draw.rect(self.screen, color, rect)

        # ─── Draw Hero ───
        center_x = offset_x + (hero_c - start_c) * cell_size + cell_size // 2
        center_y = offset_y + (hero_r - start_r) * cell_size + cell_size // 2
        pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), cell_size // 3)

        # ─── Aim direction ───
        aim_dx, aim_dy = game.aim_vector
        end_x = int(center_x + aim_dx * 40)
        end_y = int(center_y + aim_dy * 40)
        pygame.draw.line(self.screen, (255, 255, 0), (center_x, center_y), (end_x, end_y), 2)

        # ─── Draw Monsters ───
        for monster, (mr, mc) in monsters.items():
            screen_x = offset_x + (mc - start_c) * cell_size
            screen_y = offset_y + (mr - start_r) * cell_size

            if isinstance(monster, ogre):
                base_color = (0, 250, 0)
            elif isinstance(monster, skeleton):
                base_color = (0, 0, 0)
            elif isinstance(monster, gremlin):
                base_color = (0, 0, 250)
            else:
                base_color = (255, 0, 255)

            pos = (screen_x + cell_size // 2, screen_y + cell_size // 2)
            if hasattr(monster, "is_flashing") and monster.is_flashing():
                pygame.draw.circle(self.screen, (255, 0, 0), pos, cell_size // 2)

            pygame.draw.circle(self.screen, base_color, pos, cell_size // 3)

        # ─── Draw Projectiles ───
        for projectile in game.projectiles:
            px, py = projectile.get_position()
            draw_x = offset_x + px - (start_c * cell_size)
            draw_y = offset_y + py - (start_r * cell_size)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(draw_x), int(draw_y)), 5)

        # ─── Draw Melee Arc ───
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
        self.health_bar(width,height,hero)
        if self.show_inventory:
            self.draw_inventory(backpack)

        self.draw_message()


    def health_bar(self,width,height,hero):
        max_bar_width = width - 800
        bar_height = 20
        bar_x = 20
        bar_y = height - bar_height - 10

        hp = hero.health_points
        max_hp = 100
        hp_ratio = max(hp / max_hp, 0)  # prevent negative
        # Green portion (actual HP)
        hp_bar_width = int(max_bar_width * hp_ratio)
        hp_bar_rect = pygame.Rect(bar_x, bar_y, hp_bar_width, bar_height)
        pygame.draw.rect(self.screen, (0, 255, 0), hp_bar_rect)
        # Bar outline
        border_rect = pygame.Rect(bar_x, bar_y, max_bar_width, bar_height)
        pygame.draw.rect(self.screen, (0, 0, 0), border_rect, 2)
        # Optional: Add HP text
        font = pygame.font.Font(None, 30)
        hp_text = font.render(f"HP: {hp}/{max_hp}", True, (255, 255, 255))
        text_rect = hp_text.get_rect(center=(bar_x + max_bar_width // 2, bar_y + bar_height // 2))
        self.screen.blit(hp_text, text_rect)

    def show_melee_attack(self):
        self.last_attack_time = pygame.time.get_ticks()

    def draw_inventory(self, backpack):
        # Simple overlay box
        inv_rect = pygame.Rect(100, 100, 400, 300)
        pygame.draw.rect(self.screen, (50, 50, 50), inv_rect)  # background
        pygame.draw.rect(self.screen, (255, 255, 255), inv_rect, 3)  # border
        font = pygame.font.Font(None, 30)

        title = font.render("Inventory", True, (255, 255, 0))
        self.screen.blit(title, (inv_rect.x + 10, inv_rect.y + 10))

        items_to_display = {}

        # Static potions (tracked by counters)
        if backpack.get_healing_cntr() > 0:
            items_to_display["Health Potion"] = backpack.get_healing_cntr()
        if backpack.get_vision_cntr() > 0:
            items_to_display["Vision Potion"] = backpack.get_vision_cntr()

        # Pillars (tracked by symbol in inventory list)
        from collections import Counter
        inv_items = Counter(backpack.get_inventory())
        for item in inv_items:
            if item in {"A", "E", "I", "P"}:
                items_to_display[item] = inv_items[item]

        # Draw each item
        for idx, (item, count) in enumerate(items_to_display.items()):
            item_text = font.render(f"- {item}: {count}", True, (255, 255, 255))
            self.screen.blit(item_text, (inv_rect.x + 20, inv_rect.y + 40 + idx * 25))

    def draw_about_screen(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        lines = [
            "Dungeon Adventure Game",
            "Version: 1.0 June 11th 2025",
            "Authors: Rudolf Arakelyan, Nikita Bizyuk",
            "         Collins Mbugua, Ian Fuhr",
            "",
            "OBJECTIVE:",
            "Find all 4 Pillars of OOP:",
            "- Abstraction (A)",
            "- Encapsulation (E)",
            "- Inheritance (I)",
            "- Polymorphism (P)",
            "",
            "Enter a room fight and defeat monsters.",
            "Use potions to survive.",
            "Reach the exit with all 4 pillars to win!",
            "",
            "Press ESC to return to the main menu."
        ]

        font = pygame.font.SysFont('georgia', 36, bold = True)
        y_offset = 80
        bright_brown = (210, 140, 70)

        # ─── Add a background box ───
        box_width = self.screen.get_width() - 200
        box_height = len(lines) * 45 + 40
        box_x = 100
        box_y = y_offset - 30

        # Draw background box and border
        pygame.draw.rect(self.screen, (30, 30, 30), (box_x, box_y, box_width, box_height))  # dark gray bg
        pygame.draw.rect(self.screen, bright_brown, (box_x, box_y, box_width, box_height), 4)  # brown border

        for line in lines:
            text = font.render(line, True, bright_brown)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 45
