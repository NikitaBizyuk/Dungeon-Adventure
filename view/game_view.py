import pygame
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
        for button in buttons:
            button.draw(self.screen)

    def draw_maze(self, game):
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
    #update varianles better
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                cell = dungeon.maze[r][c]
                screen_x = (c - start_c) * self.cell_size
                screen_y = (r - start_r) * self.cell_size
                rect = pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)

                if not cell.explored:
                    color = (0, 0, 0)
                elif not cell.visible:
                    base = base_colors.get(cell.cell_type, (100, 100, 100))
                    color = tuple(int(x * 0.35) for x in base)
                else:
                    color = base_colors.get(cell.cell_type, (255, 0, 255))

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

    def draw_room(self, game, width, height, ogre, skeleton, gremlin):
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
            "Encapsulation": (255, 215, 0),
            "Polymorphism": (255, 215, 0),
            "Abstraction": (255, 215, 0),
            "Inheritance": (255, 215, 0),
            "Health Potion": (255, 192, 203),
            "Vision Potion": (255, 192, 203)
        }

        # ─── Draw tiles ───
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                tile = room.get_tile(r, c)
                screen_x = offset_x + (c - start_c) * cell_size
                screen_y = offset_y + (r - start_r) * cell_size
                rect = pygame.Rect(screen_x, screen_y, cell_size, cell_size)
                color = base_colors.get(tile, (255, 0, 255))
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

    def show_melee_attack(self):
        self.last_attack_time = pygame.time.get_ticks()

