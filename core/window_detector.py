import pygetwindow as gw


class WindowDetector:
    """
    Detects the currently active window on Windows.
    """

    def __init__(self):
        pass

    # ==========================================
    # Get Active Window Title
    # ==========================================

    def get_active_window(self):

        try:

            window = gw.getActiveWindow()

            if window:
                return window.title

        except Exception:
            pass

        return ""

    # ==========================================
    # Check Presentation
    # ==========================================

    def is_presentation(self):

        title = self.get_active_window()

        # Debug (you can remove this later)
        print("Active Window:", title)

        title = title.lower()

        keywords = [

            # Microsoft PowerPoint
            "powerpoint",
            "microsoft powerpoint",

            # Google Slides
            "google slides",
            "slides",

            # General Presentation
            "presentation",
            "presenter",

            # PDF Files
            ".pdf",
            "pdf",

            # PDF Readers
            "adobe",
            "acrobat",
            "foxit",

            # Browsers (PDF opened inside)
            "microsoft edge",
            "edge",
            "chrome",

            # Office Suites
            "wps",
            "impress",
            "libreoffice",

        ]

        return any(keyword in title for keyword in keywords)