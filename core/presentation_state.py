class PresentationState:
    """
    Controls the current mode of the project.

    Modes:
    --------------------------
    False -> EDITOR MODE
    True  -> PRESENTATION MODE
    """

    def __init__(self):

        self.active = False

    # ==================================
    # START PRESENTATION
    # ==================================

    def start(self):

        self.active = True

    # ==================================
    # EXIT PRESENTATION
    # ==================================

    def stop(self):

        self.active = False

    # ==================================
    # PRESENTATION MODE
    # ==================================

    def is_presentation(self):

        return self.active

    # ==================================
    # EDITOR MODE
    # ==================================

    def is_editor(self):

        return not self.active