import cv2


class FaceRecognition:

    def __init__(self, cascade_path, screen_width, screen_height):

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clf = cv2.CascadeClassifier(cascade_path)
        self.camera = cv2.VideoCapture(0)
        self.frame = None

    def detect_faces(self):
        _, frame = self.camera.read()
        self.frame = frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.clf.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
        return faces

    def process_faces(self, faces):

        x_screen = 0
        y_screen = 0

        for (x, y, width, height) in faces:
            x_screen = int((x + (width / 2)) * self.screen_width / self.frame.shape[1])
            y_screen = int((y + (height / 2)) * self.screen_height / self.frame.shape[0])

        return x_screen, y_screen
