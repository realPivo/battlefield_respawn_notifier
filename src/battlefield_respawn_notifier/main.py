import os
import sys
import time
from configparser import ConfigParser
from threading import Thread

import keyboard
from playsound import playsound

ATTACK_HELI_RESPAWN_SECONDS = 90
SOUND_FILE = "notification.mp3"


def get_base_dir():
    """Get directory where script/exe is located."""
    return os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))


def get_sound_path(filename):
    """Get full path to sound file."""
    sound_path = os.path.join(get_base_dir(), filename)

    if not os.path.exists(sound_path):
        print(f"[!] Sound file not found: {sound_path}")
        return None

    return sound_path


def create_default_config(path):
    """Create a default config.ini file."""
    config = ConfigParser()

    config["ATTACKHELICOPTER1"] = {
        "HOTKEY_NAME": "F9",
        "DURATION": ATTACK_HELI_RESPAWN_SECONDS,
        "SOUNDFILENAME": SOUND_FILE,
    }

    config["ATTACKHELICOPTER2"] = {
        "HOTKEY_CODE": "79",
        "DURATION": ATTACK_HELI_RESPAWN_SECONDS,
        "SOUNDFILENAME": SOUND_FILE,
    }

    with open(path, "w") as f:
        f.write("; Keyboard scan codes:\n")
        f.write("; https://www.reddit.com/r/GlobalOffensive/comments/1ato9z8/new_key_bind_scancodes_visualized/\n")
        config.write(f)

    print(f"Created default config at: {path}")


def _parse_hotkey_from_config(config: ConfigParser, section):
    if config.has_option(section, "HOTKEY_CODE"):
        scan_code = config.getint(section, "HOTKEY_CODE")
        return scan_code  # INT
    elif config.has_option(section, "HOTKEY_NAME"):
        name = config.get(section, "HOTKEY_NAME")
        return name  # STR
    else:
        raise ValueError(f"Section {section} must have either HOTKEY_NAME or HOTKEY_CODE")


def load_config():
    """Load timer configurations from config.ini."""
    config_path = os.path.join(get_base_dir(), "config.ini")

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        print("Creating default config.ini...")
        create_default_config(config_path)

    config = ConfigParser()
    config.read(config_path)

    timers = []
    for section in config.sections():
        try:
            timer = {
                "hotkey": _parse_hotkey_from_config(config, section),
                "duration": config.getint(section, "DURATION"),
                "sound": config.get(section, "SOUNDFILENAME"),
            }
            timers.append(timer)
            print(f"Loaded {section}: {timer['hotkey']} -> {timer['duration']}s -> {timer['sound']}")
        except Exception as e:
            print(f"[!] Error loading {section}: {e}")

    return timers


def play_timer(duration, sound_filename):
    """Wait for timer duration then play sound."""
    print(f"Timer started for {duration} seconds...")
    time.sleep(duration)
    print("Time's up!")

    sound_path = get_sound_path(sound_filename)
    if sound_path:
        try:
            playsound(sound_path)
        except Exception as e:
            print(f"[!] Error playing sound: {e}")


def create_hotkey_handler(duration, sound_filename):
    """Create a hotkey handler for specific timer settings."""

    def handler():
        Thread(target=play_timer, args=(duration, sound_filename), daemon=True).start()

    return handler


def on_hotkey():
    Thread(target=play_timer, daemon=True).start()


if __name__ == "__main__":
    timers = load_config()

    if not timers:
        print("[!] No valid timers configured. Exiting.")
        sys.exit(1)

    print("\nRegistering hotkeys...")
    for timer in timers:
        handler = create_hotkey_handler(timer["duration"], timer["sound"])
        keyboard.add_hotkey(timer["hotkey"], handler)
        print(f"    {timer['hotkey']} registered")

    print("\nListening for hotkeys. Press Ctrl+C to exit.")
    print("=" * 50)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n[+] Exiting...")
