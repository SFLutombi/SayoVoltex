# SayoVoltex

SayoVoltex is a Python/Pygame rhythm game project with three main parts:

- a **main menu and settings flow**
- a **song selection + gameplay flow**
- an **in-game chart editor**

This README focuses on the practical question: **what do you need on your machine to run it, and how is the repo organized?**

## What this project expects

From reading the codebase, the game is started directly with `python main.py`, and it expects to be run from the repository root so relative asset paths like `assets/...` and `song_folder/...` resolve correctly.

Core runtime expectations from the code:

- **Python 3**
- **Pygame** for the window, rendering, audio, input, and clipboard handling
- **Mutagen** for reading audio metadata in the editor
- **Tkinter** for native file dialogs in the editor
- **A desktop/GUI environment** because this is not a headless CLI app
- **Audio support** for `pygame.mixer`
- **The `song_folder/` directory** with playable song folders inside it

Optional-but-important dependency:

- **FFmpeg** is needed if you use the editor to import/convert audio files. The editor calls `ffmpeg` directly through `subprocess` when it needs to create `.wav` and `.ogg` versions of a track.

## Quick start

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd SayoVoltex
```

### 2. Create and activate a virtual environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

There is currently no `requirements.txt`, so install the packages used by the repo manually:

```bash
pip install pygame mutagen numpy
```

Notes:

- `numpy` is only referenced by `game/debugging_module.py`, but installing it is harmless and helps avoid missing-module surprises if that module is used later.
- `tkinter` is imported by the editor, but it is usually provided by your Python installation rather than installed with `pip`.

### 4. Install FFmpeg if you want to use the editor fully

The game can be played without FFmpeg if you only use existing song folders. However, the editor uses FFmpeg to convert audio into both `.wav` and `.ogg` files.

Check whether it is already installed:

```bash
ffmpeg -version
```

If that command fails, install FFmpeg using your OS package manager or from the official FFmpeg distribution for your platform.

### 5. Verify the asset folder name on case-sensitive systems

The code references `assets/skin/...`, but the repository currently contains `assets/Skin/...`.

That usually works on Windows, but it can fail on Linux and other case-sensitive filesystems. If your machine is case-sensitive, rename the folder so the on-disk name matches what the code loads:

```bash
mv assets/Skin assets/skin
```

If you are on Windows, you may not need to do anything here.

### 6. Run the game

From the repository root:

```bash
python main.py
```

Or, on systems where `python` points to Python 2:

```bash
python3 main.py
```

## Platform notes

### Windows

Windows is likely the smoothest platform for the current codebase because:

- the editor contains `ctypes.windll.user32...` calls to refocus the game window after opening a folder picker
- case-insensitive filesystems hide the `Skin` vs `skin` path mismatch

### Linux / macOS

These platforms should still be able to run the project, but be aware of:

- **case-sensitive paths**: you may need to rename `assets/Skin` to `assets/skin`
- **Tkinter availability**: some Python installs do not include it by default
- **FFmpeg availability**: may need separate installation
- **GUI/audio requirements**: running from a headless shell or remote session without display/audio support may fail

Also note that the Windows-specific `ctypes.windll` logic in the editor may not behave correctly outside Windows if that exact path is exercised.

## Repo structure

Here is the high-level structure of the repository:

```text
SayoVoltex/
├── main.py
├── assets/
│   ├── Skin/              # note: code currently expects assets/skin/
│   ├── backgrounds/
│   ├── font/
│   └── images/
├── game/
│   ├── screen_*.py        # menu/game/editor screens
│   ├── settings.py        # load/save persistent settings
│   ├── settings.json      # current saved settings
│   ├── states.py          # application state names
│   ├── music_player.py    # playback wrapper
│   ├── game_objects.py    # note/laser data models
│   ├── note_tool.py       # editor note placement logic
│   ├── timeline.py        # editor timeline UI
│   └── utils.py           # shared helpers
└── song_folder/
    └── <song directories>/
```

## How the app flows

### `main.py`

`main.py` is the entry point. It:

- initializes `pygame`
- initializes the mixer
- loads saved settings
- creates the display window
- enters the main state loop
- dispatches to the correct screen module based on the current state

If you are trying to understand where to start debugging, this is the best first file to read.

### `game/`

The `game/` package holds nearly all application logic.

#### Screen modules

These files represent top-level screens or workflows:

- `screen_main.py` — main menu
- `screen_options.py` — options menu
- `screen_set_keybinds.py` — keybinding configuration
- `screen_set_resolution.py` — display settings
- `screen_audio_settings.py` — audio settings
- `screen_play.py` — song selection screen
- `screen_map.py` — gameplay for a selected chart
- `screen_map_complete.py` — result / completion screen
- `screen_editor_initialize.py` — editor setup/import flow
- `screen_editor.py` — chart editor itself

#### Shared systems

Some important supporting modules:

- `constants.py` — shared constants and mutable globals used across screens
- `utils.py` — asset loading, parsing helpers, scaling helpers, etc.
- `settings.py` — default settings plus JSON load/save
- `states.py` — string constants for app state transitions
- `music_player.py` — playback controls used in menus/editor/gameplay
- `get_game_objects.py` / `game_objects.py` — chart object parsing and data containers
- `map_counters.py`, `map_details.py`, `song_tile.py` — gameplay and song-select UI data/presentation
- `dropdown.py`, `button.py`, `slider.py`, `textfield.py`, `timeline.py` — reusable UI widgets
- `note_tool.py`, `laser_cursor.py`, `metronome.py`, `rhythm_stabalizer.py` — editor/gameplay helpers

## How songs are organized

The game expects songs inside `song_folder/`, one folder per song/chart set.

Each song folder typically contains:

- a chart text file (`.txt`)
- audio files (`.wav` and/or `.ogg`)
- a cover/background image
- sometimes helper files used while editing

Example folders already included in the repo:

- `song_folder/Brain Power-Extreme-Crogo/`
- `song_folder/Gary Come Home Punk Cover-Easy-Corgo/`
- `song_folder/Kyoufuu All Back-Easy-Corgo/`

If you only want to test the game locally, these sample song folders should be enough to get started.

## Settings and save behavior

User settings are stored in:

```text
game/settings.json
```

If that file is missing, the code falls back to defaults from `game/settings.py`.

Current settings include things like:

- music volume
- SFX volume
- audio delay
- scroll speed
- resolution
- fullscreen mode
- keybindings
- whether to show instructions on launch

## Common run issues

### `ModuleNotFoundError: No module named 'pygame'` or `'mutagen'`

Install the missing package into your virtual environment:

```bash
pip install pygame mutagen numpy
```

### The window opens but assets fail to load

Make sure you:

- launched the game from the repo root
- fixed the `assets/Skin` vs `assets/skin` mismatch if your filesystem is case-sensitive

### The editor fails when importing audio

You probably need FFmpeg on your `PATH`:

```bash
ffmpeg -version
```

### Tkinter-related errors

Your Python install may not include Tkinter. Install a Python distribution that includes it, or add the OS package that provides Tk support.

### Audio initialization fails

This project calls `pygame.mixer.init(...)` immediately at startup, so machines without working audio output/configuration may fail early.

## Suggested development workflow

If you want to work on the project locally:

1. create a virtual environment
2. install `pygame`, `mutagen`, and `numpy`
3. make sure FFmpeg is installed if you will use the editor
4. verify the `assets/skin` path issue on case-sensitive systems
5. run `python main.py` from the repo root

## Future improvements worth adding

The repository would be easier for contributors to use if it also added:

- a `requirements.txt` or `pyproject.toml`
- a short supported-platform note
- a fix for the `Skin` vs `skin` mismatch
- a note on whether the editor is officially Windows-only or cross-platform
- a formal chart/song-folder format description
