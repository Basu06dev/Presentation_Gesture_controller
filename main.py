import cv2
from core.hand_tracker import HandTracker
from core.timer import GestureTimer
from core.presentation_state import PresentationState
from core.floating_window import FloatingWindow
from core.presentation_overlay import PresentationOverlay

from ui.status_overlay import StatusOverlay

from controllers.gesture_controller import GestureController
from controllers.drawing_controller import DrawingController
from controllers.presentation_controller import PresentationController



def main():

    # ==========================================
    # Initialize Camera
    # ==========================================

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("❌ Cannot open webcam.")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # ==========================================
    # Initialize Controllers
    # ==========================================

    tracker = HandTracker(
        detection_confidence=0.8,
        tracking_confidence=0.9,
    )
    gesture = GestureController()
    drawing = DrawingController()
    presentation = PresentationController()
    state = PresentationState()
    presentation_overlay = PresentationOverlay()
    overlay = StatusOverlay()

    floating = FloatingWindow(
        width=320,
        height=180,
    )

    # ----------------------------------
    # Timers
    # ----------------------------------

    start_timer = GestureTimer()

    exit_timer = GestureTimer()

    clear_timer = GestureTimer()

    # ==========================================
    # Main Loop
    # ==========================================

    while True:

        gesture_name = GestureController.NONE
        success, frame = camera.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)


        # --------------------------------------
        # Hand Detection
        # --------------------------------------

        tracker.find_hands(frame)

        landmark_list, hand_type = tracker.find_position(frame)

        if landmark_list:

            fingers = tracker.fingers_up(
                landmark_list,
                hand_type,
            )

            gesture_name = gesture.detect(fingers)


            # ===================================
            # START PRESENTATION
            # ===================================

            if gesture_name == GestureController.OPEN:

                if state.is_editor():

                    start_timer.start()

                    if start_timer.completed(2):

                        presentation.start_presentation()

                        state.start()

                        presentation_overlay.hide()

                        start_timer.reset()

                        gesture.previous_gesture = GestureController.NONE
                        gesture.current_gesture = GestureController.NONE
                        gesture.counter = 0

            else:

                start_timer.reset()



            # ===================================
            # EXIT PRESENTATION
            # ===================================

            if gesture_name == GestureController.FOUR:

                if state.is_presentation():

                    exit_timer.start()

                    if exit_timer.completed(2):

                        presentation.end_presentation()

                        state.stop()

                        presentation_overlay.hide()
                        drawing.reset()

                        exit_timer.reset()

                        gesture.previous_gesture = GestureController.NONE
                        gesture.current_gesture = GestureController.NONE
                        gesture.counter = 0

            else:

                exit_timer.reset()



            # ===================================
            # CLEAR DRAWING
            # ===================================

            if gesture_name == GestureController.FIST:

                clear_timer.start()

                if clear_timer.completed(2):

                    drawing.clear(presentation_overlay)

                    clear_timer.reset()

                    gesture.previous_gesture = GestureController.NONE
                    gesture.current_gesture = GestureController.NONE
                    gesture.counter = 0

            else:

                clear_timer.reset()

            # ================================
            # Finger Distances
            #================================

            thumb_index = tracker.finger_distance(
                landmark_list,
                4,
                8,
            )

            thumb_middle = tracker.finger_distance(
                landmark_list,
                4,
                12,
            )

            # =====================================
            # Presentation Control
            # =====================================

            if ( state.is_presentation()
                and gesture_name == GestureController.NONE):

                if thumb_index < 35:

                    presentation.next_slide()

                    cv2.putText(
                        frame,
                        "NEXT SLIDE",
                        (420,60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        3,
                    )


                elif thumb_middle < 35:

                    presentation.previous_slide()

                    cv2.putText(
                        frame,
                        "PREVIOUS SLIDE",
                        (320,60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,255,0),
                        3,
                    )

            # ==========================================
            # BRIGHTNESS CONTROL
            # ==========================================

            if state.is_presentation():

                # ------------------------------
                # BRIGHTNESS UP
                # Thumb + Index raised
                # ------------------------------

                if gesture_name == GestureController.BRIGHT_UP:

                    presentation.brightness_up()

                    cv2.putText(
                        frame,
                        "BRIGHTNESS UP",
                        (400, 110),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 255),
                        3,
                    )

                # ------------------------------
                # BRIGHTNESS DOWN
                # Thumb + Index + Middle raised
                # ------------------------------

                elif gesture_name == GestureController.BRIGHT_DOWN:

                    presentation.brightness_down()

                    cv2.putText(
                        frame,
                        "BRIGHTNESS DOWN",
                        (400, 110),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 255, 255),
                        3,
                    )

            # =====================================
            # Drawing
            # =====================================

            if (
                gesture_name == GestureController.DRAW
                and state.is_presentation()
            ):

                presentation_overlay.show()

                drawing.draw(
                    presentation_overlay,
                    landmark_list,
                    frame.shape[1],
                    frame.shape[0],
                )

            else:

                drawing.reset()

            # =====================================
            # Reset Auto Start
            # =====================================

            if state.is_presentation():

                presentation_started = False

            # =====================================
            # Information Panel
            # =====================================

            cv2.putText(
                frame,
                f"Gesture : {gesture_name}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                f"Hand : {hand_type}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Fingers : {fingers}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
            )

        # -----------------------------------
        # Presentation Mode
        # -----------------------------------

        mode = "EDITOR"

        if state.is_presentation():

            mode = "PRESENTATION"


        cv2.putText(
            frame,
            f"MODE : {mode}",
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 200, 0),
            2,
        )

        # =====================================
        # FPS
        # =====================================

        fps = tracker.get_fps()

        frame = overlay.draw(
            frame,
            mode,
            gesture_name,
            fps,
        )

        # =====================================
        # Display
        # =====================================

        floating.update(frame)

        if floating.closed:
            break

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    # ==========================================
    # Cleanup
    # ==========================================

    camera.release()
    cv2.destroyAllWindows()
    presentation_overlay.close()


if __name__ == "__main__":
    main()