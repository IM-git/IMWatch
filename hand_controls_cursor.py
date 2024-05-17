import cv2

from win32api import GetSystemMetrics

from pc_action import PyAutoGUIController
from object_recognition import ObjectRecognition


class HandControlsCursor:

    def __init__(self):
        self.gui_controller = PyAutoGUIController()
        self.cap = cv2.VideoCapture(0)  # Initialize webcam capture
        self.detector = ObjectRecognition()  # Initialize hand detector object

    def run(self):

        while True:
            success, img = self.cap.read()  # Read frame from webcam

            if cv2.waitKey(1) == ord('q'):
                break

            img = self.detector.find_object(img)  # Detect hands in the frame
            cv2.imshow("Hand Tracking", img)  # Display the annotated image
            find_position = self.detector.find_position(img)

            if len(find_position) != 0:
                # print(f"find_position: {find_position[4]}")
                length, _, _ = self.detector.find_distance(8, 12, img, draw=False)
                # print(f"length: {length}")

                if length < 30:
                    # self.gui_controller.click()
                    print("Click")

                finger_tip = find_position[4]
                screen_width = GetSystemMetrics(0)
                screen_height = GetSystemMetrics(1)

                x_screen = screen_width - (finger_tip[1] * screen_width / img.shape[1])
                y_screen = finger_tip[2] * screen_height / img.shape[0]

                self.gui_controller.move_mouse(x_screen, y_screen, screen_width)


if __name__ == '__main__':

    hand_controls_cursor = HandControlsCursor()
    hand_controls_cursor.run()
