import pyautogui


class PcActions:

    def __init__(self):
        self.x = 0
        self.y = 0

    def update_position(self, x, y) -> None:
        self.x = x
        self.y = y

    def moving_cursor(self):
        print("Face position (x, y) relative to screen:", self.x, self.y)

        # Moving the mouse according to the coordinates of the face
        pyautogui.moveTo(self.x, self.y, duration=0.25)
