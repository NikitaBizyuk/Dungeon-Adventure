import random

class Room:
    def __init__(self, row, col):
        self.row = row
        self.col = col

        # Room contents
        self.has_pit = random.random() < 0.1
        self.has_healing_potion = random.random() < 0.1
        self.has_vision_potion = random.random() < 0.1
        self.has_hero = False
        self.pillar = None  # 'A', 'E', 'I', 'P' or None
        self.is_entrance = False
        self.is_exit = False
        self.visited = False


    def enter(self, hero):
        self.has_hero = True
        print(f"\nYou entered room at ({self.row}, {self.col})")

        if hero is not None:
            if self.has_pit:
                damage = random.randint(1, 20)
                hero.take_damage(damage)
                print(f"You fell into a pit! Took {damage} damage.")
                self.has_pit = False

            if self.has_healing_potion:
                hero.healing_potions += 1
                print("You picked up a healing potion!")
                self.has_healing_potion = False

            if self.has_vision_potion:
                hero.vision_potions += 1
                print("You picked up a vision potion!")
                self.has_vision_potion = False

            if self.pillar:
                hero.pillars_found += 1
                print(f"You found a Pillar of OO: {self.pillar}!")
                self.pillar = None

    def display_center(self):
        if self.has_hero:
            return 'H'
        elif self.is_entrance:
            return 'i'
        elif self.is_exit:
            return 'O'
        elif self.pillar:
            return self.pillar
        elif self.has_pit:
            return 'X'
        elif self.has_healing_potion and self.has_vision_potion:
            return 'M'
        elif self.has_healing_potion:
            return 'C'
        elif self.has_vision_potion:
            return 'V'
        return ' '

    def draw_room(self, screen, width, height):
        import pygame
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(100, 100, width - 200, height - 200))
        pygame.draw.circle(screen, (255, 0, 0), (width // 2, height // 2), 20)
        font = pygame.font.SysFont(None, 36)
        text = font.render("In Room! Press Q to return.", True, (255, 255, 255))
        screen.blit(text, (width // 2 - 120, 60))
