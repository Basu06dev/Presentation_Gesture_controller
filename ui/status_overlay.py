import cv2


class StatusOverlay:

    def __init__(self):
        pass

    def draw(self, frame, mode, gesture, fps):

        cv2.rectangle(frame, (10, 10), (330, 130), (35, 35, 35), -1)

        cv2.putText(
            frame,
            "AI Gesture Controller",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Mode : {mode}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Gesture : {gesture}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        return frame