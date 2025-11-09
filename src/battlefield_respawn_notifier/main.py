import os
import sys
import time
from threading import Thread

import keyboard
from playsound import playsound

HOTKEY = "num 5"
TIMER_DURATION = 3
SOUND_FILE = "notification.mp3"


def get_sound_path():
    """Get path to sound file in same directory as script/exe."""
    base_dir = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
    sound_path = os.path.join(base_dir, SOUND_FILE)

    if os.path.exists(sound_path):
        print(f"Sound file: {sound_path}")
        return sound_path

    print(f"[!] Sound file not found: {sound_path}")
    return None


def play_timer():
    """Wait for timer duration then play sound."""
    print(f"Timer started for {TIMER_DURATION} seconds...")
    time.sleep(TIMER_DURATION)
    print("Time's up!")

    sound_path = get_sound_path()
    if sound_path:
        try:
            playsound(sound_path)
        except Exception as e:
            print(f"[!] Error playing sound: {e}")


def on_hotkey():
    Thread(target=play_timer, daemon=True).start()


if __name__ == "__main__":
    print(f"Listening for hotkey: {HOTKEY}")
    keyboard.add_hotkey(HOTKEY, on_hotkey)
    keyboard.wait()
