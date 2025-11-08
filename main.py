import keyboard
import time
from playsound import playsound
import threading

# === SETTINGS ===
HOTKEY = "num 5"  # You can change this to any key or combo
TIMER_DURATION = 3  # Seconds before playing sound
SOUND_FILE = "vert.mp3"  # Replace with your sound file path


def start_timer():
    print("Timer started!")
    time.sleep(TIMER_DURATION)
    print("Time’s up! Playing sound...")
    playsound(SOUND_FILE)


def on_hotkey():
    # Run the timer in a separate thread so the listener doesn’t freeze
    threading.Thread(target=start_timer, daemon=True).start()


print(f"Listening for hotkey: {HOTKEY}")
keyboard.add_hotkey(HOTKEY, on_hotkey)

# Keep the script running in the background
keyboard.wait()  # waits forever
