import time

from face_recognition import FaceRecognition
from pc_action import PcActions

cascade_path = './filters/haarcascade_frontalface_default.xml'

screen_width = 800
screen_height = 600

update_interval = 0.1

ball_radius = 20

ball_color = (255, 255, 0)
screen_color = (255, 255, 255)


def run():

    last_update_time = time.time()
    ball = PcActions()
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

        ball.moving_cursor()


if __name__ == '__main__':
    run()
