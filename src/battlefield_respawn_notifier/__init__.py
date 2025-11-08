import os
import sys
import time
import threading
import keyboard
from playsound import playsound

HOTKEY = "num 5"
TIMER_DURATION = 3  # seconds
DEFAULT_SOUND_FILENAME = "notification.mp3"


def get_exe_dir():
    """Return the folder where the .exe or .py file is located."""
    if getattr(sys, "frozen", False):
        # When packaged with PyInstaller
        return os.path.dirname(sys.executable)
    else:
        # When run from source
        return os.path.dirname(os.path.abspath(__file__))


def get_sound_path():
    """Look for default .mp3 next to the .exe or script."""
    exe_dir = get_exe_dir()
    sound_path = os.path.join(exe_dir, DEFAULT_SOUND_FILENAME)
    if not os.path.exists(sound_path):
        print(f"[!] Sound file not found: {sound_path}")
        return None
    print(f"[+] Sound file path: {sound_path}")
    return sound_path


def start_timer():
    print(f"Timer started for {TIMER_DURATION} seconds...")
    time.sleep(TIMER_DURATION)
    print("Time’s up!")

    sound = get_sound_path()
    if sound:
        try:
            playsound(sound)
        except Exception as e:
            print(f"[!] Error playing sound: {e}")
    else:
        print("No sound played — file missing.")


def on_hotkey():
    threading.Thread(target=start_timer, daemon=True).start()


if __name__ == "__main__":
    print(f"Listening for hotkey: {HOTKEY}")
    keyboard.add_hotkey(HOTKEY, on_hotkey)
    keyboard.wait()
