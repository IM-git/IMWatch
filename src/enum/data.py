from enum import Enum


class Data(Enum):
    """List of common data from balls"""

    # Параметры экрана и интервала обновления
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    UPDATE_INTERVAL = 0.1

    # Параметры шара и цвета экрана
    BALL_RADIUS = 30
    BALL_RADIUS_2 = 50

    OVAL_WIDTH = 400  # Увеличен в 2 раза
    OVAL_HEIGHT = 210  # Увеличен в 2 раза

    YELLOW_BALL_RADIUS = OVAL_HEIGHT // 2  # Радиус желтого шара

    YELLOW_COLOR = (255, 255, 0)  # Жёлтый цвет шара
    BLUE_COLOR = (0, 0, 255)  # Синий цвет шара
    BLACK_COLOR = (0, 0, 0)  # Черный цвет шара
    WHITE_COLOR = (255, 255, 255)  # Белый цвет фона
    GRAY_COLOR = (128, 128, 128)  # Серый цвет овала