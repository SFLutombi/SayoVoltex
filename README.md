# SayoVoltex

Welcome to **SayoVoltex**.

This is a small rhythm game and chart editor I built with **Python** and **Pygame**. The repo includes the game client, the chart editor, the shared UI/gameplay systems, and a few sample song folders so you can boot it up and start testing right away.

If your main question is **"how do I get this running on my machine quickly?"**, start here:

## Quick setup

### macOS / Linux

```bash
./setup.sh
```

That script will:

- create a virtual environment in `.venv`
- install the Python dependencies from `requirements.txt`
- warn you about optional editor dependencies like FFmpeg
- help with the `assets/Skin` vs `assets/skin` path issue on case-sensitive systems

After that, run:

```bash
source .venv/bin/activate
python main.py
```

### Windows (PowerShell)

```powershell
./setup.ps1
```

After that, run:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

If you do not want to use the helper scripts, the manual setup instructions are below.

---

## What you need installed

To run SayoVoltex locally, you need:

- **Python 3**
- **pip**
- a machine with a normal **desktop GUI environment**
- working **audio output**, since the game initializes the mixer at startup

Python packages used by the project are listed in `requirements.txt`.

### Optional but recommended

- **FFmpeg** if you want to use the editor to import/convert audio files
- **Tkinter**, which is used for native file/folder pickers in the editor
  - this is usually bundled with Python
  - on some Linux installs, it may need to be installed separately

## Manual setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd SayoVoltex
```

### 2. Create a virtual environment

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the game

```bash
python main.py
```

## Important platform note

The code currently loads several files from `assets/skin/...`, while the repository directory is named `assets/Skin/...`.

- On **Windows**, this usually works because the filesystem is case-insensitive.
- On **Linux** and some **macOS** setups, this can fail.

The setup script tries to handle that for you automatically on Unix-like systems. If you are setting things up manually and run into missing asset errors, fix it by renaming the folder:

```bash
mv assets/Skin assets/skin
```

## Running the game

Always run the game from the repository root:

```bash
python main.py
```

The project uses relative paths like `assets/...` and `song_folder/...`, so running it from some other directory will break asset and song loading.

## Running the editor

The editor is part of the normal application flow.

From the main menu, you can go into the editor setup flow and either:

- create a new song/chart folder
- load an existing song folder

A few notes about the editor:

- it uses **Tkinter** for file and folder dialogs
- it uses **Mutagen** to read audio file metadata
- it calls **FFmpeg** through `subprocess` when converting/importing audio into both `.wav` and `.ogg`
- some window-focus logic uses `ctypes.windll`, so the editor path is most comfortable on Windows right now

If you only want to play the included sample songs, you do **not** need FFmpeg.

## Project structure

This is the rough layout of the repo:

```text
SayoVoltex/
├── main.py
├── requirements.txt
├── setup.sh
├── setup.ps1
├── assets/
│   ├── Skin/
│   ├── backgrounds/
│   ├── font/
│   └── images/
├── game/
│   ├── screen_main.py
│   ├── screen_play.py
│   ├── screen_map.py
│   ├── screen_editor_initialize.py
│   ├── screen_editor.py
│   ├── settings.py
│   ├── states.py
│   ├── utils.py
│   └── ...
└── song_folder/
    └── <song directories>/
```

## How the program is organized

### `main.py`

`main.py` is the entry point.

It does the following:

- initializes `pygame`
- initializes the mixer
- loads saved settings from `game/settings.json`
- creates the game window
- enters the main state loop
- switches between menu/game/editor screens using values from `game/states.py`

If you are trying to understand the flow of the project, this is the best place to start.

### `game/`

The `game/` directory contains the actual systems that make the project work.

#### Screen modules

These are the top-level screens and flows:

- `screen_main.py` — main menu
- `screen_options.py` — options menu
- `screen_set_keybinds.py` — keybind setup
- `screen_set_resolution.py` — resolution/fullscreen settings
- `screen_audio_settings.py` — volume and audio delay settings
- `screen_play.py` — song select screen
- `screen_map.py` — gameplay screen for a selected chart
- `screen_map_complete.py` — result screen
- `screen_editor_initialize.py` — editor setup/import screen
- `screen_editor.py` — the chart editor itself

#### Shared systems

Some of the more important shared files are:

- `settings.py` — loads/saves persistent settings
- `states.py` — app state constants
- `constants.py` — project-wide constants and mutable shared values
- `utils.py` — helper functions for scaling, asset loading, chart parsing, etc.
- `music_player.py` — audio playback wrapper
- `game_objects.py` — note and laser object models
- `note_tool.py` — chart editing logic for placing notes/lasers
- `timeline.py` — editor timeline UI
- `button.py`, `dropdown.py`, `slider.py`, `textfield.py` — reusable UI controls

## Songs and charts

The game looks for content inside `song_folder/`.

Each song folder typically contains:

- a chart `.txt` file
- audio files such as `.wav` and/or `.ogg`
- a song image or cover image
- optionally extra helper files used while editing

The repository already includes sample folders you can use immediately:

- `song_folder/Brain Power-Extreme-Crogo/`
- `song_folder/Gary Come Home Punk Cover-Easy-Corgo/`
- `song_folder/Kyoufuu All Back-Easy-Corgo/`

So if you just want to verify that the project boots and can load songs, you do not need to prepare your own content first.

## Settings

User settings are stored in:

```text
game/settings.json
```

If that file does not exist, the project falls back to the defaults defined in `game/settings.py`.

Settings include:

- music volume
- SFX volume
- audio delay
- scroll speed
- resolution
- fullscreen
- keybindings
- whether instructions should be shown on launch

## Troubleshooting

### `ModuleNotFoundError`

Make sure your virtual environment is activated and that you installed dependencies:

```bash
pip install -r requirements.txt
```

### Assets are not loading

Make sure:

- you launched the game from the repo root
- the `assets/Skin` vs `assets/skin` issue has been fixed on case-sensitive filesystems

### The editor cannot import audio

Check that FFmpeg is installed and available on your `PATH`:

```bash
ffmpeg -version
```

### Tkinter errors

Your Python installation may not include Tk support. Install a Python build that includes Tkinter, or install the OS package that provides it.

### Audio init errors on startup

The game calls `pygame.mixer.init(...)` immediately on launch. If your system has no working audio device/configuration, startup can fail early.

## Recommended workflow for contributors

If you plan to work on the project, I recommend this flow:

1. run the setup script
2. activate `.venv`
3. launch with `python main.py`
4. test the included songs first
5. install FFmpeg before doing editor-heavy work

That should give you the smoothest path to getting started.
