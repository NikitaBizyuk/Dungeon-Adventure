import pygame
import os

class SpriteAnimator:
    def __init__(self, folder_path, frame_duration=100):
        self.frames = []
        self.index = 0
        self.timer = 0
        self.frame_duration = frame_duration

        # Load PNG files from folder
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                path = os.path.join(folder_path, filename)
                image = pygame.image.load(path).convert_alpha()
                self.frames.append(image)

        if not self.frames:
            raise ValueError(f"No frames found in {folder_path}")

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.index]
