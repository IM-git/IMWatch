import cv2


class FaceRecognition:
    """
    Класс для распознавания лиц с использованием каскадов Haar и захвата видео с камеры.
    """

    def __init__(self, cascade_path, screen_width, screen_height):
        """
        Инициализирует объект FaceRecognition.

        :param cascade_path: Путь к XML-файлу каскада Хаара для распознавания лиц.
        :param screen_width: Ширина экрана, на котором будут отображаться координаты.
        :param screen_height: Высота экрана, на котором будут отображаться координаты.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clf = cv2.CascadeClassifier(cascade_path)
        self.camera = cv2.VideoCapture(0)
        self.frame = None

        # Проверка, удалось ли открыть камеру
        if not self.camera.isOpened():
            raise Exception("Camera could not be opened.")

    def detect_faces(self):
        """
        Захватывает кадр с камеры и выполняет распознавание лиц на этом кадре.

        :return: Список координат обнаруженных лиц в формате (x, y, width, height).
        """
        _, frame = self.camera.read()
        self.frame = frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces

    def process_faces(self, faces):
        """
        Обрабатывает координаты обнаруженных лиц для преобразования их в координаты экрана.

        :param faces: Список координат обнаруженных лиц в формате (x, y, width, height).
        :return: Координаты экрана (x_screen, y_screen), соответствующие центру первого обнаруженного лица.
        """
        x_screen = 0
        y_screen = 0

        for (x, y, width, height) in faces:
            x_screen = int((x + (width / 2)) * self.screen_width / self.frame.shape[1])
            y_screen = int((y + (height / 2)) * self.screen_height / self.frame.shape[0])

        return x_screen, y_screen

    def release(self):
        """
        Освобождает ресурсы камеры.
        """
        self.camera.release()
