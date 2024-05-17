import cv2
import math
import mediapipe as mp
from win32api import GetSystemMetrics


class ObjectRecognition:

    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.modelComplex = model_complexity
        self.detectionCon = detection_con
        self.trackCon = track_con
        self.results = None

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_object(self, img, draw=True):
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_lms, self.mpHands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_no=0, draw=True):

        self.lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]

            for id, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return self.lm_list

    def find_distance(self, p1, p2, img, draw=True):
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)  # Initialize webcam capture
    detector = ObjectRecognition()  # Initialize hand detector object

    while True:
        success, img = cap.read()  # Read frame from webcam
        if cv2.waitKey(1) == ord('q'):
            break

        img = detector.find_object(img)  # Detect hands in the frame
        cv2.imshow("Hand Tracking", img)  # Display the annotated image

        find_position = detector.find_position(img)

        if len(find_position) != 0:
            # print(f"find_position: {find_position[4]}")

            finger_tip = find_position[4]

            screen_width = GetSystemMetrics(0)
            screen_height = GetSystemMetrics(1)

            x_screen = screen_width - (finger_tip[1] * screen_width / img.shape[1])
            y_screen = finger_tip[2] * screen_height / img.shape[0]

