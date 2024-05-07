import pygame


class Ball:

    def __init__(self, radius, color):
        self.x = 0
        self.y = 0
        self.radius = radius
        self.color = color

    def update_position(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
