import threading

import pystray

from PIL import Image, ImageDraw


class SystemTray:

    def __init__(self):

        self.icon = None

    # =====================================
    # Create Tray Icon
    # =====================================

    def create_icon(self):

        image = Image.new("RGB", (64, 64), (40, 40, 40))

        draw = ImageDraw.Draw(image)

        draw.ellipse((12, 12, 52, 52), fill=(0, 255, 0))

        draw.ellipse((22, 22, 42, 42), fill=(255, 255, 255))

        return image

    # =====================================
    # Exit
    # =====================================

    def on_exit(self, icon, item):

        icon.stop()

    # =====================================
    # Run Tray
    # =====================================

    def run(self):

        self.icon = pystray.Icon(

            "GestureController",

            self.create_icon(),

            "AI Gesture Presentation Controller",

            menu=pystray.Menu(

                pystray.MenuItem(
                    "Exit",
                    self.on_exit,
                )

            )

        )

        self.icon.run()

    # =====================================
    # Start Tray
    # =====================================

    def start(self):

        threading.Thread(

            target=self.run,

            daemon=True

        ).start()

    # =====================================
    # Stop Tray
    # =====================================

    def stop(self):

        if self.icon:

            self.icon.stop()