import time
import pygame
import numpy as np

from face_recognition import FaceRecognition
from ball import Ball
from src import Data

# Путь к каскаду Хаара для распознавания лиц
cascade_path = './filters/haarcascade_frontalface_default.xml'

# Параметры экрана и интервала обновления
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# UPDATE_INTERVAL = 0.1
#
# # Параметры шара и цвета экрана
# BALL_RADIUS = 30
# BALL_RADIUS_2 = 50
#
# OVAL_WIDTH = 400  # Увеличен в 2 раза
# OVAL_HEIGHT = 210  # Увеличен в 2 раза
#
# YELLOW_BALL_RADIUS = OVAL_HEIGHT // 2  # Радиус желтого шара
#
# YELLOW_COLOR = (255, 255, 0)  # Жёлтый цвет шара
# BLUE_COLOR = (0, 0, 255)  # Синий цвет шара
# BLACK_COLOR = (0, 0, 0)  # Черный цвет шара
# WHITE_COLOR = (255, 255, 255)  # Белый цвет фона
# GRAY_COLOR = (128, 128, 128)  # Серый цвет овала

# Ограничение FPS
FPS = 60

data = Data

def update_ball_positions(x_yellow, y_yellow, x_screen, y_screen, last_update_time, x_blue, y_blue, x_black, y_black):
    """Обновление позиции шаров в зависимости от положения лица."""

    current_time = time.time()
    if current_time - last_update_time >= Data.UPDATE_INTERVAL.value:
        last_update_time = current_time
        x_centered = Data.SCREEN_WIDTH.value - x_screen  # Инвертированная X-координата
        y_centered = y_screen  # Центрированная Y-координата

        # Смещение синего шара относительно желтого
        x_shift_blue = x_centered - x_yellow
        y_shift_blue = y_centered - y_yellow

        # Ограничение для синего шара
        max_x_2 = x_yellow + (Data.YELLOW_BALL_RADIUS.value - Data.BALL_RADIUS_2.value)
        min_x_2 = x_yellow - (Data.YELLOW_BALL_RADIUS.value - Data.BALL_RADIUS_2.value)
        max_y_2 = y_yellow + (Data.YELLOW_BALL_RADIUS.value - Data.BALL_RADIUS_2.value)
        min_y_2 = y_yellow - (Data.YELLOW_BALL_RADIUS.value - Data.BALL_RADIUS_2.value)

        # Обновление позиции для синего шара
        x_blue = min(max(x_centered, min_x_2), max_x_2)
        y_blue = min(max(y_centered, min_y_2), max_y_2)

        # Черный шар будет смещаться в 5.5 раза меньше, чем синий
        x_shift_black = x_shift_blue / 5.5
        y_shift_black = y_shift_blue / 5.5

        # Вычисляем позицию черного шара относительно центра синего шара
        x_black = x_blue + x_shift_black
        y_black = y_blue + y_shift_black

        return x_blue, y_blue, x_black, y_black, last_update_time

    return x_blue, y_blue, x_black, y_black, last_update_time


def run():
    """
        Основная функция запуска приложения для отслеживания головы с использованием распознавания лиц.

        Инициализирует экран, создает объекты для распознавания лиц и шара,
        запускает главный цикл, который обрабатывает видео с камеры,
        распознает лица и обновляет положение шара на экране в зависимости от положения лица.
    """

    last_update_time = time.time()  # Время последнего обновления положения шара
    pygame.init()
    screen = pygame.display.set_mode((Data.SCREEN_WIDTH.value, Data.SCREEN_HEIGHT.value))  # Экран для отображения графики
    pygame.display.set_caption("Head Tracking Ball")  # Заголовок окна приложения

    # Создание объекта Clock для управления FPS
    clock = pygame.time.Clock()

    ball = Ball()
    with FaceRecognition(cascade_path, Data.SCREEN_WIDTH.value, Data.SCREEN_HEIGHT.value) as face_recognition:

        # Определение границ овала
        oval_center_x = Data.SCREEN_WIDTH.value // 2  # X-координата центра овала
        oval_center_y = Data.SCREEN_HEIGHT.value // 2  # Y-координата центра овала

        # Прямоугольник, задающий овал
        oval_rect = [(Data.SCREEN_WIDTH.value - Data.OVAL_WIDTH.value) // 2,
                     (Data.SCREEN_HEIGHT.value - Data.OVAL_HEIGHT.value) // 2,
                     Data.OVAL_WIDTH.value, Data.OVAL_HEIGHT.value]

        try:

            x_yellow, y_yellow = oval_center_x, oval_center_y  # Начальная позиция желтого шара
            x_blue, y_blue = oval_center_x, oval_center_y  # Начальная позиция синего шара
            x_black, y_black = oval_center_x, oval_center_y  # Начальная позиция черного шара

            while True:
                # Захват и обработка лиц
                faces = face_recognition.detect_faces()  # Список обнаруженных лиц

                # Проверка, если faces - это numpy.ndarray и в нем есть лица
                if isinstance(faces, np.ndarray) and faces.size > 0:

                    # Координаты центра первого обнаруженного лица
                    x_screen, y_screen = face_recognition.process_faces(faces)

                    current_time = time.time()

                    # Обновление положения шара только при наличии обнаруженных лиц
                    if x_screen is not None and y_screen is not None:

                        x_blue, y_blue, x_black, y_black, last_update_time = update_ball_positions(x_yellow,
                                                                                                   y_yellow,
                                                                                                   x_screen,
                                                                                                   y_screen,
                                                                                                   last_update_time,
                                                                                                   x_blue,
                                                                                                   y_blue,
                                                                                                   x_black,
                                                                                                   y_black)

                    # Очистка экрана и рисование шара
                    screen.fill(Data.WHITE_COLOR.value)  # Заполнение фона белым цветом

                    # Рисуем серый овал
                    ball.draw_ellipse(screen, Data.GRAY_COLOR.value, oval_rect)

                    ball.draw_circle(screen=screen, radius=Data.YELLOW_BALL_RADIUS.value,
                                     color=Data.YELLOW_COLOR.value, x=x_yellow, y=y_yellow)

                    # Рисуем синий шар
                    ball.draw_circle(screen=screen, radius=Data.BALL_RADIUS_2.value,
                                     color=Data.BLUE_COLOR.value, x=x_blue, y=y_blue)

                    # Рисуем черный шар
                    ball.draw_circle(screen=screen, radius=Data.BALL_RADIUS.value, color=Data.BLACK_COLOR.value,
                                     x=x_black, y=y_black)

                    pygame.display.update()

                    # Обработка событий Pygame
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return

                    # Ограничение количества кадров в секунду
                    clock.tick(FPS)
                # Ускорение: Переходите к следующему кадру, если лица не обнаружены
                else:
                    continue

        finally:
            # Обязательно освобождаем ресурсы камеры перед выходом
            face_recognition.release()


if __name__ == '__main__':
    run()
