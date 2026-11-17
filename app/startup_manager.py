import os
import shutil


class StartupManager:
    """
    ==========================================
           Windows Startup Manager
    ==========================================

    Adds or removes the application from

        Windows Startup Folder

    """

    def __init__(self):

        self.startup_folder = os.path.join(

            os.environ["APPDATA"],
            r"Microsoft\Windows\Start Menu\Programs\Startup"

        )

    # ==========================================
    # Enable Startup
    # ==========================================

    def enable(self, exe_path):

        destination = os.path.join(

            self.startup_folder,

            os.path.basename(exe_path)

        )

        if not os.path.exists(destination):

            shutil.copy(exe_path, destination)

            print("Startup Enabled")

    # ==========================================
    # Disable Startup
    # ==========================================

    def disable(self, exe_path):

        destination = os.path.join(

            self.startup_folder,

            os.path.basename(exe_path)

        )

        if os.path.exists(destination):

            os.remove(destination)

            print("Startup Disabled")

    # ==========================================
    # Check
    # ==========================================

    def enabled(self, exe_path):

        destination = os.path.join(

            self.startup_folder,

            os.path.basename(exe_path)

        )

        return os.path.exists(destination)