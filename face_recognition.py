import cv2  # Импортируем модуль OpenCV для обработки видеопотока
import win32api  # Импортируем модуль win32api для получения информации о размерах экрана
import pygame  # Импортируем модуль pygame для отображения графики
import multiprocessing  # Импортируем модуль multiprocessing для работы с процессами
import time  # Импортируем модуль time для работы со временем


def face_capture(face_position_x, face_position_y):
    cascade_path = './filters/haarcascade_frontalface_default.xml'  # Путь к каскадному классификатору для определения лиц

    clf = cv2.CascadeClassifier(cascade_path)  # Создаем объект классификатора лиц
    camera = cv2.VideoCapture(0)  # Получаем доступ к видеопотоку с веб-камеры

    update_interval = 1  # Обновление координат каждую секунду
    last_update_time = time.time()  # Время последнего обновления координат

    while True:
        _, frame = camera.read()  # Считываем кадр из видеопотока
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Преобразуем изображение в оттенки серого

        faces = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )  # Обнаруживаем лица на кадре

        current_time = time.time()  # Получаем текущее время

        if len(faces) > 0:
            x, y, width, height = faces[0]
            screen_width = win32api.GetSystemMetrics(0)  # Получаем ширину экрана
            screen_height = win32api.GetSystemMetrics(1)  # Получаем высоту экрана
            x_screen = int((x + (width / 2)) * screen_width / frame.shape[1])  # Пересчитываем координату x
            y_screen = int((y + (height / 2)) * screen_height / frame.shape[0])  # Пересчитываем координату y
            face_position_x.value = x_screen  # Устанавливаем значение x координаты лица
            face_position_y.value = y_screen  # Устанавливаем значение y координаты лица
        else:
            face_position_x.value = -1  # Используйте значение по умолчанию, чтобы показать отсутствие лица
            face_position_y.value = -1

        # Обновление координат только если прошло достаточно времени
        if current_time - last_update_time >= update_interval:
            last_update_time = current_time

    camera.release()  # Освобождаем ресурсы камеры



def show_ball(ball_position_x, ball_position_y):
    pygame.init()  # Инициализируем библиотеку pygame

    screen_width = 800  # Ширина окна
    screen_height = 600  # Высота окна

    screen = pygame.display.set_mode((screen_width, screen_height))  # Создаем окно с заданными размерами
    pygame.display.set_caption('Moving Ball')  # Устанавливаем заголовок окна

    ball_color = (255, 0, 0)  # Цвет шарика
    ball_radius = 20  # Радиус шарика

    clock = pygame.time.Clock()  # Создаем объект Clock для ограничения частоты кадров

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Заполняем экран черным цветом

        if ball_position_x.value != -1 and ball_position_y.value != -1:  # Проверяем, что у нас есть корректные координаты шарика
            x = ball_position_x.value  # Получаем x-координату шарика
            y = ball_position_y.value  # Получаем y-координату шарика
            pygame.draw.circle(screen, ball_color, (x, y), ball_radius)  # Рисуем шарик на экране

        pygame.display.flip()  # Обновляем экран

        clock.tick(60)  # Ограничиваем частоту кадров

    pygame.quit()  # Завершаем работу pygame


if __name__ == '__main__':
    ball_position_x = multiprocessing.Value('i', -1, lock=True)  # Создаем объект Value для хранения x-координаты шарика
    ball_position_y = multiprocessing.Value('i', -1, lock=True)  # Создаем объект Value для хранения y-координаты шарика

    face_position_x = multiprocessing.Value('i', -1, lock=True)  # Создаем объект Value для хранения x-координаты лица
    face_position_y = multiprocessing.Value('i', -1, lock=True)  # Создаем объект Value для хранения y-координаты лица

    face_process = multiprocessing.Process(target=face_capture, args=(face_position_x, face_position_y))  # Создаем процесс для обнаружения лица
    ball_process = multiprocessing.Process(target=show_ball, args=(ball_position_x, ball_position_y))  # Создаем процесс для отображения шарика

    face_process.start()  # Запускаем процесс обнаружения лица
    ball_process.start()  # Запускаем процесс отображения шарика

    face_process.join()  # Ждем завершения процесса обнаружения лица
    ball_process.join()  # Ждем завершения процесса отображения шарика
