import json
from pathlib import Path

_THEME_PATH = Path("assets/theme/default.json")
_THEME_CACHE = None


def _load_theme():
    global _THEME_CACHE
    if _THEME_CACHE is None:
        with _THEME_PATH.open("r", encoding="utf-8") as theme_file:
            _THEME_CACHE = json.load(theme_file)
    return _THEME_CACHE


def reload_theme():
    global _THEME_CACHE
    _THEME_CACHE = None
    return _load_theme()


def get_font_path():
    return _load_theme()["font_path"]


def get_color(name):
    return _load_theme()["colors"][name]


def get_asset(name):
    return _load_theme()["assets"][name]
