import pygame


class Ball:

    @staticmethod
    def draw_circle(screen, radius, color, x, y):
        """
        Рисует круг (шар) на экране.
        :param screen: поверхность Pygame для рисования
        :param radius: радиус шара
        :param color: цвет шара
        :param x: координата x шара
        :param y: координата y шара
        """
        pygame.draw.circle(screen, color, (x, y), radius)

    @staticmethod
    def draw_ellipse(screen, color, rect):
        """
        Рисует эллипс на экране.
        :param screen: поверхность Pygame для рисования
        :param color: цвет эллипса
        :param rect: координаты и размеры эллипса
        """
        pygame.draw.ellipse(screen, color, rect)
