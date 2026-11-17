class DrawingController:
    """
    Presentation Drawing Controller
    ================================

    Features:
        • Smooth air drawing
        • Yellow drawing cursor
        • Remembers last drawing position
        • New drawing continues from last endpoint
        • Prevents unwanted line when starting a new drawing
        • Clear drawing
    """

    def __init__(self):

        # ==========================================
        # LAST DRAWING POSITION
        # ==========================================

        self.previous_x = None
        self.previous_y = None

        # ==========================================
        # SMOOTHED HAND POSITION
        # ==========================================

        self.smooth_x = None
        self.smooth_y = None

        # ==========================================
        # CURRENT CURSOR POSITION
        # ==========================================

        self.cursor_x = None
        self.cursor_y = None

        # ==========================================
        # DRAWING SETTINGS
        # ==========================================

        self.thickness = 5

        # Lower value = smoother movement
        self.smoothing = 0.25

    # ==========================================
    # DRAW
    # ==========================================

    def draw(
        self,
        overlay,
        landmark_list,
        frame_width,
        frame_height,
    ):
        """
        Draw using the index finger.

        The previous drawing endpoint is preserved
        when drawing stops.
        """

        if not landmark_list:
            return

        # ==========================================
        # INDEX FINGER
        # ==========================================

        x = landmark_list[8][1]
        y = landmark_list[8][2]

        # ==========================================
        # CAMERA → SCREEN COORDINATES
        # ==========================================

        target_x = (
            x / frame_width
        ) * overlay.width

        target_y = (
            y / frame_height
        ) * overlay.height

        # ==========================================
        # LIMIT TO SCREEN
        # ==========================================

        target_x = max(
            0,
            min(
                target_x,
                overlay.width - 1
            )
        )

        target_y = max(
            0,
            min(
                target_y,
                overlay.height - 1
            )
        )

        # ==========================================
        # INITIAL SMOOTH POSITION
        # ==========================================

        if self.smooth_x is None:

            self.smooth_x = target_x
            self.smooth_y = target_y

        # ==========================================
        # SMOOTH MOVEMENT
        # ==========================================

        self.smooth_x += (
            target_x - self.smooth_x
        ) * self.smoothing

        self.smooth_y += (
            target_y - self.smooth_y
        ) * self.smoothing

        # ==========================================
        # CURRENT CURSOR POSITION
        # ==========================================

        self.cursor_x = int(
            self.smooth_x
        )

        self.cursor_y = int(
            self.smooth_y
        )

        # ==========================================
        # SHOW YELLOW CURSOR
        # ==========================================

        overlay.draw_cursor(
            self.cursor_x,
            self.cursor_y,
        )

        # ==========================================
        # FIRST DRAWING POINT
        # ==========================================

        if self.previous_x is None:

            self.previous_x = self.cursor_x
            self.previous_y = self.cursor_y

            return

        # ==========================================
        # DISTANCE FROM LAST DRAWING POINT
        # ==========================================

        dx = (
            self.cursor_x
            - self.previous_x
        )

        dy = (
            self.cursor_y
            - self.previous_y
        )

        distance = (
            dx * dx +
            dy * dy
        ) ** 0.5

        # ==========================================
        # IGNORE VERY SMALL MOVEMENT
        # ==========================================

        if distance < 2:

            return

        # ==========================================
        # DRAW LINE
        # ==========================================

        overlay.draw_line(
            self.previous_x,
            self.previous_y,
            self.cursor_x,
            self.cursor_y,
        )

        # ==========================================
        # SAVE CURRENT ENDPOINT
        # ==========================================

        self.previous_x = self.cursor_x
        self.previous_y = self.cursor_y

    # ==========================================
    # SHOW LAST CURSOR
    # ==========================================

    def show_cursor(self, overlay):
        """
        Keep the yellow cursor visible even when
        the hand is not currently drawing.
        """

        if self.cursor_x is None:
            return

        overlay.draw_cursor(
            self.cursor_x,
            self.cursor_y,
        )

    # ==========================================
    # RESET DRAWING MOVEMENT
    # ==========================================

    def reset(self):
        """
        Stop the current drawing movement.

        IMPORTANT:
        The last drawing position is preserved.

        Therefore, when drawing starts again,
        the new line continues from the previous
        drawing endpoint.
        """

        self.smooth_x = None
        self.smooth_y = None

    # ==========================================
    # CLEAR EVERYTHING
    # ==========================================

    def clear(self, overlay=None):
        """
        Completely clear the drawing and forget
        the previous drawing position.
        """

        if overlay is not None:

            overlay.clear()

        self.previous_x = None
        self.previous_y = None

        self.cursor_x = None
        self.cursor_y = None

        self.smooth_x = None
        self.smooth_y = None