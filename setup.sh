#!/usr/bin/env bash
set -e

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Could not find $PYTHON_BIN. Install Python 3 and try again."
  exit 1
fi

echo "Creating virtual environment..."
"$PYTHON_BIN" -m venv .venv

# shellcheck disable=SC1091
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -d assets/skin ] && [ -d assets/Skin ]; then
  echo "Detected assets/Skin without assets/skin."
  if ln -s Skin assets/skin 2>/dev/null; then
    echo "Created assets/skin symlink for case-sensitive filesystems."
  else
    echo "Could not create symlink automatically."
    echo "If assets fail to load, run: mv assets/Skin assets/skin"
  fi
fi

if command -v ffmpeg >/dev/null 2>&1; then
  echo "FFmpeg detected. Editor audio import/conversion should work."
else
  echo "FFmpeg not found. That is okay if you only want to play included songs."
  echo "Install FFmpeg later if you want to import audio in the editor."
fi

echo
echo "Setup complete."
echo "Next steps:"
echo "  source .venv/bin/activate"
echo "  python main.py"
