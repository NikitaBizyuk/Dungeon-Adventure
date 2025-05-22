
import pygame
import sys
class View:

    pygame.init()

# Set up the screen
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
    pygame.display.set_caption("Move the Rectangle")

    # Define colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    # Define rectangle properties
    rect_width, rect_height = 60, 40
    rect_x, rect_y = WIDTH // 2, HEIGHT // 2
    rect_speed = 8

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rect_x -= rect_speed
        if keys[pygame.K_RIGHT]:
            rect_x += rect_speed
        if keys[pygame.K_UP]:
            rect_y -= rect_speed
        if keys[pygame.K_DOWN]:
            rect_y += rect_speed

        # Draw everything
        screen.fill(WHITE)  # Clear the screen
        pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height))  # Draw the rectangle
        pygame.display.flip()  # Update the display

        # Control the frame rate
        pygame.time.Clock().tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()
    def __init__(self,controller):
        self.controller = controller

    def main(self):
        #Call this method in controllers main method to initialize GUI.
        print("This is main method for GUI")
