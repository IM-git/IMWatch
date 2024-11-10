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

    last_update_time = time.time()  # Время последнего обновления положения шара
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))  # Экран для отображения графики
    pygame.display.set_caption("Head Tracking Ball")  # Заголовок окна приложения

    # Создание объекта Clock для управления FPS
    clock = pygame.time.Clock()

    ball = Ball()
    face_recognition = FaceRecognition(cascade_path, screen_width, screen_height)

    # Определение границ овала
    oval_center_x = screen_width // 2  # X-координата центра овала
    oval_center_y = screen_height // 2  # Y-координата центра овала
    # Прямоугольник, задающий овал
    oval_rect = [(screen_width - oval_width) // 2, (screen_height - oval_height) // 2, oval_width, oval_height]

    try:
        x_blue, y_blue = oval_center_x, oval_center_y  # Начальная позиция синего шара
        x_black, y_black = oval_center_x, oval_center_y  # Начальная позиция черного шара

        while True:
            # Захват и обработка лиц
            faces = face_recognition.detect_faces()  # Список обнаруженных лиц
            _screen_coordinates = face_recognition.process_faces(faces)  # Координаты центра первого обнаруженного лица
            x_screen, y_screen = _screen_coordinates

            current_time = time.time()

            # Обновление положения шара только при наличии обнаруженных лиц
            if x_screen is not None and y_screen is not None:

                if current_time - last_update_time >= update_interval:
                    last_update_time = current_time  # Обновление времени последнего перемещения

                    # Ограничение движения шаров в пределах овала
                    x_centered = screen_width - x_screen  # Инвертированная X-координата
                    y_centered = y_screen  # Центрированная Y-координата

                    # Ограничение для синего шара (большего радиуса)
                    max_x_2 = oval_center_x + (oval_width // 2 - ball_radius_2)  # Максимальная X-координата для синего шара
                    min_x_2 = oval_center_x - (oval_width // 2 - ball_radius_2)  # Минимальная X-координата для синего шара
                    max_y_2 = oval_center_y + (oval_height // 2 - ball_radius_2)  # Максимальная Y-координата для синего шара
                    min_y_2 = oval_center_y - (oval_height // 2 - ball_radius_2)  # Минимальная Y-координата для синего шара

                    # Ограничение для черного шара (меньшего радиуса)
                    max_x = oval_center_x + (oval_width // 2 - ball_radius)  # Максимальная X-координата для черного шара
                    min_x = oval_center_x - (oval_width // 2 - ball_radius)  # Минимальная X-координата для черного шара
                    max_y = oval_center_y + (oval_height // 2 - ball_radius)  # Максимальная Y-координата для черного шара
                    min_y = oval_center_y - (oval_height // 2 - ball_radius)  # Минимальная Y-координата для черного шара

                    # Ограничение позиции для синего шара
                    x_blue = min(max(x_centered, min_x_2), max_x_2)
                    y_blue = min(max(y_centered, min_y_2), max_y_2)

                    # Ограничение движения синего шара в пределах овала
                    x_shift_blue = x_centered - oval_center_x  # Смещение синего шара относительно центра овала
                    y_shift_blue = y_centered - oval_center_y  # Смещение синего шара относительно центра овала

                    # Черный шар будет смещаться в 5.5 раза меньше, чем синий шар
                    x_shift_black = x_shift_blue / 5.5  # Смещение черного шара
                    y_shift_black = y_shift_blue / 5.5  # Смещение черного шара

                    # Вычисляем позицию черного шара относительно центра синего шара
                    x_black = x_blue + x_shift_black  # Позиция черного шара по оси X
                    y_black = y_blue + y_shift_black  # Позиция черного шара по оси Y

            # Очистка экрана и рисование шара
            screen.fill(white_color)  # Заполнение фона белым цветом

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
