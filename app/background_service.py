import threading
import time

from core.window_detector import WindowDetector
from core.presentation_state import PresentationState


class BackgroundService:
    """
    ==========================================
        Desktop Background Service
    ==========================================

    Runs continuously in the background.

    Responsibilities
    ----------------

    • Detect active window
    • Detect PowerPoint
    • Detect PDF
    • Detect Google Slides
    • Automatically switch between

        EDITOR MODE
            ↓
        PRESENTATION MODE

    No user interaction required.
    """

    def __init__(self):

        self.detector = WindowDetector()

        self.state = PresentationState()

        self.running = False

        self.thread = None

    # ==========================================
    # Main Loop
    # ==========================================

    def loop(self):

        while self.running:

            if self.detector.is_presentation():

                self.state.start()

            else:

                self.state.stop()

            time.sleep(0.5)

    # ==========================================
    # Start Service
    # ==========================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.loop,
            daemon=True,
        )

        self.thread.start()

        print("Background Service Started")

    # ==========================================
    # Stop Service
    # ==========================================

    def stop(self):

        self.running = False

        print("Background Service Stopped")