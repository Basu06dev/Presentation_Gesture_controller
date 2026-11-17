import tkinter as tk
from PIL import Image, ImageTk
import cv2


class FloatingWindow:
    """
    Always-on-top webcam preview window.

    Features:
        • Small webcam preview
        • Always on top
        • Borderless window
        • Draggable
        • Close button
        • Safe Tkinter image handling
    """

    def __init__(self, width=320, height=180):

        self.width = width
        self.height = height

        self.closed = False

        # ==========================================
        # Create Tkinter Window
        # ==========================================

        self.root = tk.Tk()

        self.root.title("AI Gesture Controller")

        # Borderless
        self.root.overrideredirect(True)

        # Always on top
        self.root.attributes("-topmost", True)

        # Fixed size
        self.root.resizable(False, False)

        # Background
        self.root.configure(bg="black")

        # ==========================================
        # Position - Top Right
        # ==========================================

        screen_width = self.root.winfo_screenwidth()

        x = screen_width - self.width - 20
        y = 20

        self.root.geometry(
            f"{self.width}x{self.height}+{x}+{y}"
        )

        # ==========================================
        # Webcam Label
        # ==========================================

        self.label = tk.Label(
            self.root,
            bg="black",
            bd=0,
            highlightthickness=0,
        )

        self.label.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # Close Button
        # ==========================================

        self.close_button = tk.Button(
            self.root,
            text="✕",
            command=self.close,
            bg="#222222",
            fg="white",
            activebackground="#ff3333",
            activeforeground="white",
            bd=0,
            highlightthickness=0,
            font=("Arial", 10, "bold"),
            cursor="hand2",
        )

        self.close_button.place(
            x=self.width - 30,
            y=5,
            width=25,
            height=25,
        )

        # ==========================================
        # Drag Support
        # ==========================================

        self.offset_x = 0
        self.offset_y = 0

        self.label.bind(
            "<ButtonPress-1>",
            self.start_move
        )

        self.label.bind(
            "<B1-Motion>",
            self.move_window
        )

        # ==========================================
        # Close Support
        # ==========================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        # ==========================================
        # Keep Reference To Current Image
        # ==========================================

        self.photo = None

        self.root.update_idletasks()

    # ==========================================
    # START DRAG
    # ==========================================

    def start_move(self, event):

        self.offset_x = event.x
        self.offset_y = event.y

    # ==========================================
    # MOVE WINDOW
    # ==========================================

    def move_window(self, event):

        if self.closed:
            return

        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y

        self.root.geometry(
            f"+{x}+{y}"
        )

    # ==========================================
    # UPDATE WEBCAM
    # ==========================================

    def update(self, frame):

        if self.closed:
            return

        try:

            # --------------------------------------
            # Resize Frame
            # --------------------------------------

            frame = cv2.resize(
                frame,
                (self.width, self.height),
                interpolation=cv2.INTER_AREA,
            )

            # --------------------------------------
            # Convert BGR → RGB
            # --------------------------------------

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB,
            )

            # --------------------------------------
            # Convert OpenCV → PIL
            # --------------------------------------

            image = Image.fromarray(frame)

            # --------------------------------------
            # Create Tkinter Image
            # --------------------------------------

            self.photo = ImageTk.PhotoImage(
                image=image,
                master=self.root,
            )

            # --------------------------------------
            # Update Label
            # --------------------------------------

            self.label.configure(
                image=self.photo
            )

            # Keep reference
            self.label.image = self.photo

            # --------------------------------------
            # Update Tkinter
            # --------------------------------------

            self.root.update_idletasks()
            self.root.update()

        except tk.TclError:

            self.closed = True

    # ==========================================
    # CLOSE WINDOW
    # ==========================================

    def close(self):

        if self.closed:
            return

        self.closed = True

        try:

            self.label.configure(
                image=""
            )

            self.photo = None

            self.root.destroy()

        except tk.TclError:

            pass