import cv2

from win32api import GetSystemMetrics

from pc_action import PyAutoGUIController
from object_recognition import ObjectRecognition


class HandControlsCursor:

    def __init__(self):
        self.gui_controller = PyAutoGUIController()
        self.cap = cv2.VideoCapture(0)  # Initialize webcam capture
        self.detector = ObjectRecognition()  # Initialize hand detector object
        self.x_screen = 1000
        self.y_screen = 1000
        self.old_x_screen = 1000
        self.old_y_screen = 1000

    def get_differences(self, new_position):

        x_new_position = new_position[1]
        y_new_position = new_position[2]

        # x_differences =
        # y_differences =
        #
        # x_old_position =
        # y_old_position =

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

                if length < 20:
                    # self.gui_controller.click()
                    # print("Click")

                    finger_tip = find_position[4]
                    screen_width = GetSystemMetrics(0)
                    screen_height = GetSystemMetrics(1)

                    x_screen = screen_width - (finger_tip[1] * screen_width / img.shape[1])
                    y_screen = finger_tip[2] * screen_height / img.shape[0]

                    # print(f"x:{x_screen}, y:{y_screen}")

                    if abs(self.old_x_screen - x_screen) > 15:

                        if self.old_x_screen < x_screen:
                            self.x_screen += 30
                        if self.old_x_screen > x_screen:
                            self.x_screen -= 30

                    if abs(self.old_y_screen - y_screen) > 15:

                        if self.old_y_screen < y_screen:
                            self.y_screen += 30
                        if self.old_y_screen > y_screen:
                            self.y_screen -= 30

                    if self.x_screen > 1920:
                        self.x_screen = 1920
                    if self.x_screen <= 0:
                        self.x_screen = 0

                    if self.y_screen > 1080:
                        self.y_screen = 1080
                    if self.y_screen <= 0:
                        self.y_screen = 0

                    self.gui_controller.move_mouse(self.x_screen, self.y_screen, screen_width)

                    self.old_x_screen = x_screen
                    self.old_y_screen = y_screen


if __name__ == '__main__':

    hand_controls_cursor = HandControlsCursor()
    hand_controls_cursor.run()
