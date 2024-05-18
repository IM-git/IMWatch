import pyautogui


class PyAutoGUIController:

    def __init__(self):
        pass

    @staticmethod
    def move_mouse(x, y, screen_width):
        pyautogui.moveTo((screen_width - x), y)

    @staticmethod
    def click():
        pyautogui.click()
        # pyautogui.doubleClick()

    @staticmethod
    def get_cursor_position():
        try:
            # Getting the current cursor coordinates
            x, y = pyautogui.position()
            # print(f"Current cursor position: (X: {x}, Y: {y})")
            return x, y
        except KeyboardInterrupt:
            print("Program terminated.")
