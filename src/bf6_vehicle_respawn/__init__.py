import keyboard
import time
from playsound import playsound
import threading
import os


# === SETTINGS ===
HOTKEY = "num 5"  # You can change this to any key or combo
TIMER_DURATION = 3  # Seconds before playing sound

# Get the directory where the script is located and build the sound file path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_FILE_PATH = os.path.join(SCRIPT_DIR, "vert.mp3")


def start_timer():
    print("Timer started!")
    time.sleep(TIMER_DURATION)
    print("Time’s up! Playing sound...")
    playsound(SOUND_FILE_PATH)


def main() -> None:
    def on_hotkey():
        # Run the timer in a separate thread so the listener doesn’t freeze
        threading.Thread(target=start_timer, daemon=True).start()

    print(f"Sound file path: {SOUND_FILE_PATH}")
    print(f"Listening for hotkey: {HOTKEY}")
    keyboard.add_hotkey(HOTKEY, on_hotkey)

    # Keep the script running in the background
    keyboard.wait()  # waits forever
