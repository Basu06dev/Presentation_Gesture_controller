import time
import screen_brightness_control as sbc


class BrightnessController:
    """
    Screen Brightness Controller
    ----------------------------

    Thumb + Index pinch:
        Increase brightness

    Thumb + Index + Middle pinch:
        Decrease brightness
    """

    def __init__(self):

        self.cooldown = 0.8
        self.last_action = 0

        # Brightness step
        self.step = 10

    # ==========================================
    # COOLDOWN
    # ==========================================

    def ready(self):

        current_time = time.time()

        if current_time - self.last_action >= self.cooldown:

            self.last_action = current_time

            return True

        return False

    # ==========================================
    # GET CURRENT BRIGHTNESS
    # ==========================================

    def get_brightness(self):

        try:

            brightness = sbc.get_brightness()

            if isinstance(brightness, list):

                brightness = brightness[0]

            return int(brightness)

        except Exception:

            return None

    # ==========================================
    # INCREASE BRIGHTNESS
    # ==========================================

    def increase(self):

        if not self.ready():
            return

        current = self.get_brightness()

        if current is None:
            return

        new_value = min(
            100,
            current + self.step
        )

        try:

            sbc.set_brightness(new_value)

            print(
                f"Brightness increased: {new_value}%"
            )

        except Exception as error:

            print(
                "Brightness increase error:",
                error
            )

    # ==========================================
    # DECREASE BRIGHTNESS
    # ==========================================

    def decrease(self):

        if not self.ready():
            return

        current = self.get_brightness()

        if current is None:
            return

        new_value = max(
            0,
            current - self.step
        )

        try:

            sbc.set_brightness(new_value)

            print(
                f"Brightness decreased: {new_value}%"
            )

        except Exception as error:

            print(
                "Brightness decrease error:",
                error
            )