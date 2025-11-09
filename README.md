# Battlefield Respawn Notifier

The recent release of Battlefield 6 takes up all my free time (I'm quite happy with that).


I spend most of my time as a attack helicopter pilot, where I sometimes have a problem: when I destroy an enemy helicopter, it respawns after a while and can kill me from behind.

To solve this, I measured the respawn of helicopters and wrote a simple program that registers hotkey presses and plays a notification when the respawn timer ends.

This is definetely total over-engineering, when it could be done using AutoHotKey, but I don't care.

## Usage

- Download or build yourself an `.exe` file and put `.mp3` file next to it.
- On the first startup it will create a base `config.ini`.
- Modify `config.ini` to your needs: sound filename, timer duration and hotkey / [key scan code](https://www.reddit.com/r/GlobalOffensive/comments/1ato9z8/new_key_bind_scancodes_visualized/)


## Build
```bash
uv run pyinstaller --onefile --name 'Battlefield Respawn Notifier' src/battlefield_respawn_notifier/main.py
```