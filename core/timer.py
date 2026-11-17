import time


class GestureTimer:
    """
    Gesture Timer
    --------------------------
    Used for holding gestures.

    Examples:
        • Start Presentation (2 sec)
        • Exit Presentation (2 sec)
        • Clear Drawing (2 sec)
    """

    def __init__(self):

        self.start_time = None

    # ==================================
    # START TIMER
    # ==================================

    def start(self):

        if self.start_time is None:

            self.start_time = time.time()

    # ==================================
    # RESET TIMER
    # ==================================

    def reset(self):

        self.start_time = None

    # ==================================
    # ELAPSED TIME
    # ==================================

    def elapsed(self):

        if self.start_time is None:

            return 0

        return time.time() - self.start_time

    # ==================================
    # TIMER COMPLETED
    # ==================================

    def completed(self, seconds=2):

        if self.start_time is None:

            return False

        return self.elapsed() >= seconds