import tkinter as tk


class PresentationOverlay:
    """
    ==========================================
        Presentation Drawing Overlay
    ==========================================

    Transparent fullscreen overlay that sits
    above the PPT/PDF presentation.

    Features
    --------
    • Fullscreen overlay
    • Transparent background
    • Always on top
    • Air drawing support
    • Clear drawing
    • Show / hide
    • Safe close
    """

    def __init__(self):

        # ==========================================
        # CREATE OVERLAY WINDOW
        # ==========================================

        self.root = tk.Tk()

        self.root.title(
            "Presentation Drawing Overlay"
        )

        # ==========================================
        # SCREEN SIZE
        # ==========================================

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.root.geometry(
            f"{self.width}x{self.height}+0+0"
        )

        # ==========================================
        # REMOVE WINDOW BORDER
        # ==========================================

        self.root.overrideredirect(True)

        # ==========================================
        # TRANSPARENT BACKGROUND
        # ==========================================

        self.root.configure(
            bg="black"
        )

        self.root.attributes(
            "-transparentcolor",
            "black"
        )

        # ==========================================
        # ALWAYS ON TOP
        # ==========================================

        self.root.attributes(
            "-topmost",
            True
        )

        # ==========================================
        # CANVAS
        # ==========================================

        self.canvas = tk.Canvas(
            self.root,
            bg="black",
            highlightthickness=0,
            bd=0,
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # DRAWING SETTINGS
        # ==========================================

        self.color = "red"

        self.thickness = 5

        self.visible = False

        self.closed = False

        # ==========================================
        # HIDE INITIALLY
        # ==========================================

        self.root.withdraw()

        self.root.update_idletasks()

    # ==========================================
    # SHOW OVERLAY
    # ==========================================

    def show(self):

        if self.closed:
            return

        if not self.visible:

            self.visible = True

            self.root.deiconify()

            self.root.lift()

            self.root.attributes(
                "-topmost",
                True
            )

            self.root.update_idletasks()

    # ==========================================
    # HIDE OVERLAY
    # ==========================================

    def hide(self):

        if self.closed:
            return

        if self.visible:

            self.visible = False

            self.root.withdraw()

    # ==========================================
    # DRAW LINE
    # ==========================================

    def draw_line(
        self,
        x1,
        y1,
        x2,
        y2,
    ):

        if self.closed:
            return

        if not self.visible:
            return

        self.canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=self.color,
            width=self.thickness,
            capstyle=tk.ROUND,
            smooth=True,
        )

    # ==========================================
    # DRAWING CURSOR
    # ==========================================

    def draw_cursor(
        self,
        x,
        y,
        radius=10,
    ):

        if self.closed:
            return

        if not self.visible:
            return

        # Remove previous cursor
        self.canvas.delete("drawing_cursor")

        # Draw new cursor
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            outline="yellow",
            width=2,
            tags="drawing_cursor",
        )

    # ==========================================
    # DRAW CURSOR
    # ==========================================

    def draw_cursor(self, x, y):

        if self.closed:
            return

        if not self.visible:
            return

        # Remove previous cursor
        self.canvas.delete("cursor")

        # Yellow cursor
        radius = 10

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="yellow",
            outline="white",
            width=2,
            tags="cursor",
        )

        # Small center point
        self.canvas.create_oval(
            x - 3,
            y - 3,
            x + 3,
            y + 3,
            fill="white",
            outline="white",
            tags="cursor",
        )

    # ==========================================
    # CLEAR DRAWING
    # ==========================================

    def clear(self):

        if self.closed:
            return

        self.canvas.delete("all")

    # ==========================================
    # UPDATE OVERLAY
    # ==========================================

    def update(self):

        if self.closed:
            return

        try:

            self.root.update_idletasks()

            self.root.update()

        except tk.TclError:

            self.closed = True

    # ==========================================
    # CLOSE OVERLAY
    # ==========================================

    def close(self):

        if self.closed:
            return

        self.closed = True

        try:

            self.root.destroy()

        except tk.TclError:

            pass