import cv2

import time
from win32api import GetSystemMetrics

from pc_action import PyAutoGUIController


class FaceRecognition:

    def __init__(self, cascade_path, gui_controller):
        self.cascade_path = cascade_path
        self.clf = cv2.CascadeClassifier(self.cascade_path)
        self.camera = cv2.VideoCapture(0)
        self.update_interval = 1
        self.last_update_time = time.time()
        self.gui_controller = gui_controller
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces

    def process_faces(self, faces, frame):
        current_time = time.time()
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)
            x_screen = int((x + (width / 2)) * self.screen_width / frame.shape[1])
            y_screen = int((y + (height / 2)) * self.screen_height / frame.shape[0])
            if current_time - self.last_update_time >= self.update_interval:
                self.last_update_time = current_time
                print("Face position (x, y) relative to screen:", x_screen, y_screen)
                self.gui_controller.move_mouse(x_screen, y_screen, self.screen_width)

    def run(self):
        while True:
            _, frame = self.camera.read()
            if frame is None:
                break
            faces = self.detect_faces(frame)
            self.process_faces(faces, frame)
            cv2.imshow('Faces', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':

    path = './filters/haarcascade_frontalface_default.xml'
    py_auto_gui_controller = PyAutoGUIController()
    face_recognition = FaceRecognition(cascade_path=path, gui_controller=py_auto_gui_controller)
    face_recognition.run()
