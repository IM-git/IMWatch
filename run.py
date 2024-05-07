import time

import pygame

from face_recognition import FaceRecognition
from ball import Ball

cascade_path = './filters/haarcascade_frontalface_default.xml'

screen_width = 800
screen_height = 600

update_interval = 0.1

ball_radius = 20

ball_color = (255, 255, 0)
screen_color = (255, 255, 255)


def run():

    last_update_time = time.time()

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Head Tracking Ball")

    ball = Ball(ball_radius, ball_color)
    face_recognition = FaceRecognition(cascade_path, screen_width, screen_height)

    while True:

        faces = face_recognition.detect_faces()

        _screen_coordinates = face_recognition.process_faces(faces)
        x_screen = _screen_coordinates[0]
        y_screen = _screen_coordinates[1]

        current_time = time.time()

        if current_time - last_update_time >= update_interval:
            last_update_time = current_time
            ball.update_position(screen_width - x_screen, y_screen)

        screen.fill(screen_color)
        ball.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == '__main__':
    run()
