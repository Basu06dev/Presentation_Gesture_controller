import time
import pyautogui
import screen_brightness_control as sbc


class PresentationController:
    """
    Presentation Controller
    ---------------------------------

    Supported Functions:
        • Next Slide
        • Previous Slide
        • Start Presentation
        • Exit Presentation
        • Black Screen
        • White Screen
        • Brightness Increase
        • Brightness Decrease
    """

    def __init__(self):

        pyautogui.FAILSAFE = False

        # Gesture cooldown
        self.cooldown = 0.8
        self.last_action = 0

        # Brightness step
        self.brightness_step = 10

    # ==================================
    # COOLDOWN CHECK
    # ==================================

    def ready(self):

        current_time = time.time()

        if current_time - self.last_action > self.cooldown:

            self.last_action = current_time
            return True

        return False

    # ==================================
    # NEXT SLIDE
    # ==================================

    def next_slide(self):

        if self.ready():
            pyautogui.press("right")

    # ==================================
    # PREVIOUS SLIDE
    # ==================================

    def previous_slide(self):

        if self.ready():
            pyautogui.press("left")

    # ==================================
    # START PRESENTATION
    # ==================================

    def start_presentation(self):

        if self.ready():
            pyautogui.press("f5")

    # ==================================
    # EXIT PRESENTATION
    # ==================================

    def end_presentation(self):

        if self.ready():
            pyautogui.press("esc")

    # ==================================
    # BLACK SCREEN
    # ==================================

    def black_screen(self):

        if self.ready():
            pyautogui.press("b")

    # ==================================
    # WHITE SCREEN
    # ==================================

    def white_screen(self):

        if self.ready():
            pyautogui.press("w")

    # ==================================
    # BRIGHTNESS UP
    # ==================================

    def brightness_up(self):

        if not self.ready():
            return

        try:

            current = sbc.get_brightness()

            if isinstance(current, list):
                current = current[0]

            current = int(current)

            new_brightness = min(
                100,
                current + self.brightness_step
            )

            sbc.set_brightness(new_brightness)

            print(
                f"Brightness increased: {new_brightness}%"
            )

        except Exception as error:

            print(
                f"Brightness control error: {error}"
            )

    # ==================================
    # BRIGHTNESS DOWN
    # ==================================

    def brightness_down(self):

        if not self.ready():
            return

        try:

            current = sbc.get_brightness()

            if isinstance(current, list):
                current = current[0]

            current = int(current)

            new_brightness = max(
                0,
                current - self.brightness_step
            )

            sbc.set_brightness(new_brightness)

            print(
                f"Brightness decreased: {new_brightness}%"
            )

        except Exception as error:

            print(
                f"Brightness control error: {error}"
            )

    # ==================================
    # SET BRIGHTNESS
    # ==================================

    def set_brightness(self, value):

        try:

            value = max(
                0,
                min(100, int(value))
            )

            sbc.set_brightness(value)

            print(
                f"Brightness: {value}%"
            )

        except Exception as error:

            print(
                f"Brightness control error: {error}"
            )