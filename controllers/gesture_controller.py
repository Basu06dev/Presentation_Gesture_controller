class GestureController:
    """
    AI Gesture Recognition Engine
    --------------------------------

    Finger pattern:
        [Thumb, Index, Middle, Ring, Little]
    """

    POINTER = "POINTER"
    DRAW = "DRAW"
    FIST = "FIST"
    OPEN = "OPEN"
    FOUR = "FOUR"

    BRIGHT_UP = "BRIGHT_UP"
    BRIGHT_DOWN = "BRIGHT_DOWN"

    NONE = "NONE"

    def __init__(self, stability_frames=3):

        self.stability_frames = stability_frames

        self.previous_gesture = self.NONE
        self.current_gesture = self.NONE

        self.counter = 0

    # =====================================
    # STABLE GESTURE DETECTION
    # =====================================

    def detect(self, fingers):

        gesture = self._recognize(fingers)

        if gesture == self.previous_gesture:

            self.counter += 1

        else:

            self.counter = 1
            self.previous_gesture = gesture

        if self.counter >= self.stability_frames:

            self.current_gesture = gesture

        return self.current_gesture

    # =====================================
    # FINGER PATTERN RECOGNITION
    # =====================================

    def _recognize(self, fingers):

        if not fingers:
            return self.NONE

        # =================================
        # BRIGHTNESS UP
        # Thumb + Index raised
        # Remaining fingers closed
        # =================================

        if fingers == [1, 0, 0, 0, 0]:

            return self.BRIGHT_UP

        # =================================
        # BRIGHTNESS DOWN
        # Thumb + Index + Middle raised
        # Ring + Little closed
        # =================================

        if fingers == [1, 1, 1, 1, 0]:

            return self.BRIGHT_DOWN

        # =================================
        # POINTER
        # Index only
        # =================================

        if fingers == [0, 1, 0, 0, 0]:

            return self.POINTER

        # =================================
        # DRAW
        # Index only
        # =================================

        if fingers == [0, 1, 1, 0, 0]:

            return self.DRAW

        # =================================
        # ERASE
        # Index + Middle + Ring
        # =================================

        if fingers == [0, 1, 1, 1, 0]:

            return self.FIST

        # =================================
        # FOUR FINGERS
        # Thumb closed
        # =================================

        if fingers == [0, 1, 1, 1, 1]:

            return self.FOUR

        # =================================
        # OPEN HAND
        # =================================

        if fingers == [1, 1, 1, 1, 1]:

            return self.OPEN

        return self.NONE