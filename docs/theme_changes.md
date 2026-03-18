# Theme change log

This pass only moves presentation decisions out of the screen code. It does **not** change gameplay flow, state transitions, input handling, chart parsing, or audio logic.

## What changed

1. Added `assets/theme/default.json` as the first centralized theme file.
   - This holds font path, shared colors, and UI asset paths.
   - The goal is to make future visual swaps happen in one place instead of across multiple screens.

2. Added `game/theme.py`.
   - This is a tiny loader for the theme JSON.
   - Screens can now ask for `theme.get_asset(...)`, `theme.get_color(...)`, and `theme.get_font_path()`.

3. Updated shared font loading.
   - `utils.get_font()` now reads the font path from the theme instead of hardcoding `assets/font/font.ttf`.

4. Updated the menu, options, play screen, and map-details panel to read presentation values from the theme.
   - Background image paths moved into the theme.
   - Button colors moved into the theme.
   - A soft overlay was added on menu-like screens to improve contrast without changing layout or interaction logic.

5. Updated default song texture lookup.
   - `song_tile.py` now gets the fallback texture path from the theme.

## What did not change

- state machine behavior
- event handling
- gameplay timing
- chart parsing
- song loading behavior
- editor logic
- button hit detection/layout behavior

## Why this is a good first step

This creates a clean seam between visuals and behavior. If new assets are added later, most of the visual swaps can happen in the theme file instead of forcing another sweep through every screen module.
