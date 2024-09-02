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
ball_radius = 20
ball_color = (255, 255, 0)  # Жёлтый цвет шара
screen_color = (255, 255, 255)  # Белый цвет фона

# Ограничение FPS
FPS = 30

oval_width = 200  # Увеличен в 2 раза
oval_height = 80  # Увеличен в 2 раза
oval_color = (128, 128, 128)  # Gray


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
                    ball.update_position(screen_width - x_screen, y_screen)

            # Очистка экрана и рисование шара
            screen.fill(screen_color)

            oval_rect = [(screen_width - oval_width) // 2, (screen_height - oval_height) // 2, oval_width, oval_height]

            ball.draw_ellipse(screen, oval_color, oval_rect)

            ball.draw_circle(screen=screen, radius=ball_radius, color=ball_color)
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
