import cv2

from face_recognition import FaceRecognition


PATH = './filters/haarcascade_frontalface_default.xml'


class FaceControlsCursor:

    def __init__(self):
        self.face_recognition = FaceRecognition(cascade_path=PATH, open_cv2=cv2)

    def run(self):
        while True:
            _, frame = self.face_recognition.camera.read()
            if frame is None:
                break
            faces = self.face_recognition.detect_faces(frame)
            self.face_recognition.process_faces(faces, frame)
            cv2.imshow('Faces', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        self.face_recognition.camera.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':

    face_controls_cursor = FaceControlsCursor()
    face_controls_cursor.run()

