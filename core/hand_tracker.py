import time
import math
import cv2
import mediapipe as mp


class HandTracker:
    """
    Hand Tracking Module
    ====================

    Features:
        • Hand detection
        • Landmark detection
        • Left / right hand detection
        • Finger state detection
        • Finger distance calculation
        • Stable FPS calculation
    """

    TIP_IDS = [4, 8, 12, 16, 20]

    def __init__(
        self,
        mode=False,
        max_hands=1,
        detection_confidence=0.65,
        tracking_confidence=0.70,
    ):

        # ==========================================
        # Basic Settings
        # ==========================================

        self.mode = mode
        self.max_hands = max_hands

        # ==========================================
        # MediaPipe
        # ==========================================

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

        # ==========================================
        # Results
        # ==========================================

        self.results = None

        # ==========================================
        # FPS
        # ==========================================

        self.previous_time = time.time()
        self.fps = 0.0

        # FPS smoothing factor
        self.fps_smoothing = 0.10

    # ==========================================
    # HAND DETECTION
    # ==========================================

    def find_hands(self, frame, draw=True):
        """
        Detect hands and optionally draw landmarks.
        """

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:

            for hand_landmarks in self.results.multi_hand_landmarks:

                if draw:

                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                    )

        return frame

    # ==========================================
    # LANDMARK POSITIONS
    # ==========================================

    def find_position(
        self,
        frame,
        hand_no=0,
        draw=True,
    ):
        """
        Return landmark coordinates and hand type.
        """

        landmark_list = []
        hand_type = None

        if (
            self.results
            and self.results.multi_hand_landmarks
        ):

            # Safety check
            if hand_no >= len(
                self.results.multi_hand_landmarks
            ):
                return landmark_list, hand_type

            hand = (
                self.results
                .multi_hand_landmarks[hand_no]
            )

            # --------------------------------------
            # Hand Type
            # --------------------------------------

            if self.results.multi_handedness:

                hand_type = (
                    self.results
                    .multi_handedness[hand_no]
                    .classification[0]
                    .label
                )

            # --------------------------------------
            # Frame Dimensions
            # --------------------------------------

            height, width, _ = frame.shape

            # --------------------------------------
            # Landmarks
            # --------------------------------------

            for idx, landmark in enumerate(
                hand.landmark
            ):

                cx = int(
                    landmark.x * width
                )

                cy = int(
                    landmark.y * height
                )

                landmark_list.append(
                    [idx, cx, cy]
                )

                # ----------------------------------
                # Draw Landmark Points
                # ----------------------------------

                if draw:

                    cv2.circle(
                        frame,
                        (cx, cy),
                        4,
                        (255, 0, 255),
                        cv2.FILLED,
                    )

        return landmark_list, hand_type

    # ==========================================
    # FINGER STATES
    # ==========================================

    def fingers_up(
        self,
        landmark_list,
        hand_type,
    ):
        """
        Return finger states:

        [Thumb, Index, Middle, Ring, Pinky]

        1 = Up
        0 = Down
        """

        if not landmark_list:
            return []

        fingers = []

        # ======================================
        # THUMB
        # ======================================

        if hand_type == "Right":

            fingers.append(
                1
                if landmark_list[4][1]
                < landmark_list[2][1]
                else 0
            )

        else:

            fingers.append(
                1
                if landmark_list[4][1]
                > landmark_list[2][1]
                else 0
            )

        # ======================================
        # INDEX, MIDDLE, RING, PINKY
        # ======================================

        for tip in [8, 12, 16, 20]:

            fingers.append(
                1
                if landmark_list[tip][2]
                < landmark_list[tip - 2][2]
                else 0
            )

        return fingers

    # ==========================================
    # DISTANCE BETWEEN LANDMARKS
    # ==========================================

    def finger_distance(
        self,
        landmark_list,
        point1,
        point2,
    ):
        """
        Calculate Euclidean distance
        between two landmarks.
        """

        if not landmark_list:
            return 0

        x1 = landmark_list[point1][1]
        y1 = landmark_list[point1][2]

        x2 = landmark_list[point2][1]
        y2 = landmark_list[point2][2]

        return math.hypot(
            x2 - x1,
            y2 - y1,
        )

    # ==========================================
    # FPS CALCULATION
    # ==========================================

    def get_fps(self):
        """
        Calculate and return smoothed FPS.
        """

        current_time = time.time()

        elapsed = (
            current_time
            - self.previous_time
        )

        if elapsed > 0:

            current_fps = 1.0 / elapsed

            # ----------------------------------
            # Smooth FPS
            # ----------------------------------

            self.fps = (
                self.fps
                * (1 - self.fps_smoothing)
                +
                current_fps
                * self.fps_smoothing
            )

        self.previous_time = current_time

        return int(self.fps)

    # ==========================================
    # DRAW FPS
    # ==========================================

    def draw_fps(self, frame):
        """
        Draw FPS directly on the frame.
        """

        fps = self.get_fps()

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (20, 220),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        return frame

    # ==========================================
    # RELEASE
    # ==========================================

    def close(self):
        """
        Release MediaPipe resources.
        """

        try:

            self.hands.close()

        except Exception:

            pass