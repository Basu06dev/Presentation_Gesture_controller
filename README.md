✋ Presentation Gesture Controller

Control your slideshow with hand gestures. No keyboard, mouse or clicker needed. The app uses your webcam to track your hand in real time, recognises gestures from the fingers you raise, and turns them into presentation actions such as next slide, previous slide, drawing on slides and brightness control.

Built with Python, MediaPipe, OpenCV and PyAutoGUI.

✨ Features
Action	Gesture	Notes
Start presentation	Open hand (all fingers up)	Hold ~2 seconds in editor mode
Exit presentation	Four fingers up	Hold ~2 seconds in presentation mode
Next slide	Touch thumb + index finger together	Pinch distance < 35 px
Previous slide	Touch thumb + middle finger together	Pinch distance < 35 px
Draw on slide	Drawing gesture (index finger)	Draws on a transparent overlay
Clear drawing	Fist	Hold ~2 seconds
Brightness up	Thumb + index finger raised	Presentation mode only
Brightness down	Thumb + index + middle finger raised	Presentation mode only
Quit the app	Press q or close the floating window	

The 2-second hold on start, exit and clear prevents accidental triggers.

The app has two modes:

EDITOR: the app is idle until you start the presentation.
PRESENTATION: slide navigation, drawing and brightness gestures are active.

A small floating webcam window shows the live feed, the detected gesture, the hand (left or right), the finger states, the current mode and the FPS.

🗂️ Project Structure
Presentation_Gesture_controller/
├── main.py                  # Entry point: camera loop and gesture-to-action logic
├── app.py                   # Application setup
├── config.py                # Configuration values
├── requirements.txt         # Python dependencies
├── app/                     # Application modules
├── core/
│   ├── hand_tracker.py          # MediaPipe hand detection and finger states
│   ├── timer.py                 # GestureTimer: "hold for N seconds" logic
│   ├── presentation_state.py    # Editor / presentation mode state
│   ├── floating_window.py       # Small floating webcam window
│   └── presentation_overlay.py  # Transparent overlay used for drawing
├── controllers/
│   ├── gesture_controller.py        # Classifies finger patterns into gestures
│   ├── drawing_controller.py        # Drawing and clearing logic
│   └── presentation_controller.py   # Sends slide, start/end and brightness commands
└── ui/
    └── status_overlay.py    # Mode, gesture and FPS overlay on the video feed
⚙️ How It Works
Capture: OpenCV reads frames from the webcam (1280×720) and mirrors them.
Detect: HandTracker uses MediaPipe to find 21 hand landmarks (detection confidence 0.8, tracking confidence 0.9).
Classify: GestureController turns the raised-finger pattern into a named gesture (open, four, fist, draw, brightness up/down).
Act: PresentationController triggers keyboard and system actions through PyAutoGUI, and DrawingController draws on the overlay.
Display: StatusOverlay and FloatingWindow show live feedback.
🚀 Getting Started
Prerequisites
Python 3.9 – 3.11 (MediaPipe 0.10.14 does not support newer versions)
A working webcam
A presentation app (PowerPoint, LibreOffice Impress, Google Slides in a browser, etc.)
Installation
bash
# 1. Clone the repository
git clone https://github.com/Basu06dev/Presentation_Gesture_controller.git
cd Presentation_Gesture_controller

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
Run
bash
python main.py
Open your slideshow file first.
Run the app and show your hand to the camera.
Hold an open hand for 2 seconds to start the presentation.
Use the gestures from the table above.
Press q to quit.
💡 Tips for Best Results
Use good, even lighting and a plain background.
Keep your hand about 40–80 cm from the camera, fully inside the frame.
Make gestures clearly, with fingers fully extended or fully folded.
Keep the presentation window focused so keyboard commands reach it.
🛠️ Troubleshooting
Problem	Fix
Cannot open webcam	Close other apps using the camera, or change the camera index in cv2.VideoCapture(0).
Gestures are flickery	Improve lighting, or raise the detection and tracking confidence in main.py.
Slides don't change	Make sure the slideshow window is focused.
Brightness doesn't change	Brightness control depends on your OS and hardware. Laptop displays usually work best.
Install errors	Check you are on a supported Python version (3.9–3.11).
🔭 Future Improvements
Custom gesture mapping through config.py
Laser-pointer mode
Zoom in / out gestures
Two-hand gestures
Multi-camera support
🤝 Contributing

Contributions are welcome. Fork the repo, create a feature branch, and open a pull request.

📄 License

Distributed under the license in the LICENSE file.

👤 Author

Basu06dev: github.com/Basu06dev
