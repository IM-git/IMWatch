import pyautogui


class PyAutoGUIController:

    def __init__(self):
        pass

    @staticmethod
    def move_mouse(x, y, screen_width):
        pyautogui.moveTo((screen_width - x), y, duration=0.001)

    @staticmethod
    def click():
        pyautogui.click()
        # pyautogui.doubleClick()
