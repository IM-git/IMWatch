import pygame


class Ball:

    def __init__(self):
        self.x = 0
        self.y = 0

    def update_position(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw_circle(self, screen, radius, color) -> None:
        pygame.draw.circle(screen, color, (self.x, self.y), radius)

    def draw_ellipse(self, screen, color, rect) -> None:
        pygame.draw.ellipse(screen, color, rect)
