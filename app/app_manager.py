from app.system_tray import SystemTray
from app.startup_manager import StartupManager
from app.background_service import BackgroundService


class AppManager:
    """
    ==========================================
        AI Gesture Presentation Controller
              Application Manager
    ==========================================

    Responsible for:

    • Starting the application
    • Starting background services
    • Starting System Tray
    • Stopping the application
    """

    def __init__(self):

        self.running = False

        self.tray = SystemTray()
        self.startup = StartupManager()
        self.background = BackgroundService()

    # ==========================================
    # START APPLICATION
    # ==========================================

    def start(self):

        print("=" * 50)
        print("AI Gesture Presentation Controller")
        print("Application Started")
        print("=" * 50)

        self.running = True
        import sys

        if getattr(sys, "frozen", False):

            self.startup.enable(sys.executable)

        # Start tray in background
        self.tray.start()
        self.background.start()

    # ==========================================
    # STOP APPLICATION
    # ==========================================

    def stop(self):

        print("=" * 50)
        print("Application Closed")
        print("=" * 50)

        self.background.stop()
        self.tray.stop()

        self.running = False

    # ==========================================
    # CHECK STATUS
    # ==========================================

    def is_running(self):

        return self.running

    