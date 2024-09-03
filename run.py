import time
import pygame
from face_recognition import FaceRecognition
from ball import Ball

# Путь к каскаду Хаара для распознавания лиц
cascade_path = './filters/haarcascade_frontalface_default.xml'

# Параметры экрана и интервала обновления
screen_width = 800
screen_height = 600
update_interval = 0.1

# Параметры шара и цвета экрана
ball_radius = 30
ball_radius_2 = 50

yellow_color = (255, 255, 0)  # Жёлтый цвет шара
blue_color = (0, 0, 255)  # Синий цвет шара
black_color = (0, 0, 0)  # Черный цвет шара
white_color = (255, 255, 255)  # Белый цвет фона
gray_color = (128, 128, 128)  # Серый цвет овала

# Ограничение FPS
FPS = 30

oval_width = 400  # Увеличен в 2 раза
oval_height = 160  # Увеличен в 2 раза

def run():
    """
    Основная функция запуска приложения для отслеживания головы с использованием распознавания лиц.

    Инициализирует экран, создает объекты для распознавания лиц и шара,
    запускает главный цикл, который обрабатывает видео с камеры,
    распознает лица и обновляет положение шара на экране в зависимости от положения лица.
    """
    last_update_time = time.time()
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Head Tracking Ball")

    # Создание объекта Clock для управления FPS
    clock = pygame.time.Clock()

    ball = Ball()
    face_recognition = FaceRecognition(cascade_path, screen_width, screen_height)

    # Определение границ овала
    oval_center_x = screen_width // 2
    oval_center_y = screen_height // 2
    oval_rect = [(screen_width - oval_width) // 2, (screen_height - oval_height) // 2, oval_width, oval_height]

    try:
        while True:
            # Захват и обработка лиц
            faces = face_recognition.detect_faces()
            _screen_coordinates = face_recognition.process_faces(faces)
            x_screen, y_screen = _screen_coordinates

            current_time = time.time()

            # Обновление положения шара только при наличии обнаруженных лиц
            if x_screen is not None and y_screen is not None:
                if current_time - last_update_time >= update_interval:
                    last_update_time = current_time

                    # Ограничение движения шаров в пределах овала
                    x_centered = screen_width - x_screen
                    y_centered = y_screen

                    # Ограничение для синего шара (большего радиуса)
                    max_x_2 = oval_center_x + (oval_width // 2 - ball_radius_2)
                    min_x_2 = oval_center_x - (oval_width // 2 - ball_radius_2)
                    max_y_2 = oval_center_y + (oval_height // 2 - ball_radius_2)
                    min_y_2 = oval_center_y - (oval_height // 2 - ball_radius_2)

                    # Ограничение для черного шара (меньшего радиуса)
                    max_x = oval_center_x + (oval_width // 2 - ball_radius)
                    min_x = oval_center_x - (oval_width // 2 - ball_radius)
                    max_y = oval_center_y + (oval_height // 2 - ball_radius)
                    min_y = oval_center_y - (oval_height // 2 - ball_radius)

                    # Ограничение позиции для черного шара
                    x_black = min(max(x_centered, min_x), max_x)
                    y_black = min(max(y_centered, min_y), max_y)

                    # Ограничение позиции для синего шара
                    x_blue = min(max(x_centered, min_x_2), max_x_2)
                    y_blue = min(max(y_centered, min_y_2), max_y_2)

            # Очистка экрана и рисование шара
            screen.fill(white_color)

            # Рисуем серый овал
            pygame.draw.ellipse(screen, gray_color, oval_rect)

            # Рисуем синий шар
            ball.draw_circle(screen=screen, radius=ball_radius_2, color=blue_color, x=x_blue, y=y_blue)

            # Рисуем черный шар
            ball.draw_circle(screen=screen, radius=ball_radius, color=black_color, x=x_black, y=y_black)

            pygame.display.update()

            # Обработка событий Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Ограничение количества кадров в секунду
            clock.tick(FPS)

    finally:
        # Обязательно освобождаем ресурсы камеры перед выходом
        face_recognition.release()


if __name__ == '__main__':
    run()
