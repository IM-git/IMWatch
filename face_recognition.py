import cv2
import win32api
import time


def face_recognition():

    cascade_path = './filters/haarcascade_frontalface_default.xml'

    clf = cv2.CascadeClassifier(cascade_path)
    camera = cv2.VideoCapture(0)

    # Обновление координат каждую секунду
    update_interval = 1
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
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)

            # Получение размеров экрана
            screen_width = win32api.GetSystemMetrics(0)
            screen_height = win32api.GetSystemMetrics(1)

            # Преобразование координат лица относительно экрана
            x_screen = int((x + (width / 2)) * screen_width / frame.shape[1])
            y_screen = int((y + (height / 2)) * screen_height / frame.shape[0])

            # Обновление координат только если прошло достаточно времени
            if current_time - last_update_time >= update_interval:
                last_update_time = current_time
                print("Face position (x, y) relative to screen:", x_screen, y_screen)

        cv2.imshow('Faces', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    face_recognition()
