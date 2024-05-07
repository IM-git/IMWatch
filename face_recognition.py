import cv2
import pygame
import numpy as np  # noqa
import time

# Initializing Pygame
pygame.init()

# Setting screen sizes
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Head Tracking Ball")

# Colors
WHITE = (255, 255, 255)
BLUE = (255, 255, 0)

BALL_X = screen_width // 2
BALL_Y = screen_height // 2

# The radius and initial coordinates of the ball
ball_radius = 20


# Function for drawing a ball
def draw_ball(x, y):
    pygame.draw.circle(screen, BLUE, (x, y), ball_radius)


def face_recognition():
    cascade_path = './filters/haarcascade_frontalface_default.xml'

    ball_x = 0
    ball_y = 0

    clf = cv2.CascadeClassifier(cascade_path)
    camera = cv2.VideoCapture(0)

    # Coordinates update every 0.1 second
    update_interval = 0.1
    last_update_time = time.time()

    while True:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        current_time = time.time()

        for (x, y, width, height) in faces:

            # Converting face coordinates relative to the screen
            x_screen = int((x + (width / 2)) * screen_width / frame.shape[1])
            y_screen = int((y + (height / 2)) * screen_height / frame.shape[0])

            # Updating coordinates only if enough time has passed
            if current_time - last_update_time >= update_interval:
                last_update_time = current_time
                print("Face position (x, y) relative to screen:", x_screen, y_screen)
                ball_x = screen_width - x_screen
                ball_y = y_screen

        # drawing a ball
        screen.fill(WHITE)
        draw_ball(ball_x, ball_y)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == '__main__':
    face_recognition()
