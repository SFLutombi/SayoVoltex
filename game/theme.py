import json
import math
from pathlib import Path

import pygame

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


def load_image(name, size=None, convert_alpha=True):
    asset_ref = get_asset(name)

    if asset_ref.startswith("generated:"):
        surface = _build_generated_surface(asset_ref.split(":", 1)[1], size)
    else:
        surface = pygame.image.load(asset_ref)
        if size is not None:
            surface = pygame.transform.smoothscale(surface, size)

    if convert_alpha:
        return surface.convert_alpha()
    return surface.convert()


def _build_generated_surface(kind, size):
    if size is None:
        defaults = {
            "main_menu_background": (1280, 720),
            "options_background": (1280, 720),
            "play_background": (1280, 720),
            "logo": (520, 520),
            "song_tile_cover": (225, 75),
            "map_details_panel": (400, 250),
        }
        size = defaults[kind]

    builders = {
        "main_menu_background": _build_main_menu_background,
        "options_background": _build_options_background,
        "play_background": _build_play_background,
        "logo": _build_logo,
        "song_tile_cover": _build_song_tile_cover,
        "map_details_panel": _build_map_details_panel,
    }
    return builders[kind](size)


def _vertical_gradient(size, top_color, bottom_color):
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)
    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(int(top_color[i] + (bottom_color[i] - top_color[i]) * t) for i in range(3))
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface


def _draw_soft_glow(surface, center, radius, color, alpha):
    for step in range(5, 0, -1):
        glow_radius = int(radius * (step / 5))
        glow_alpha = max(10, int(alpha * (step / 5) ** 2))
        glow_color = (*color, glow_alpha)
        pygame.draw.circle(surface, glow_color, center, glow_radius)


def _draw_triangles(surface, color, alpha, triangles):
    for center_x, center_y, size in triangles:
        height = int(size * 0.85)
        points = [
            (center_x, center_y - height // 2),
            (center_x - size // 2, center_y + height // 2),
            (center_x + size // 2, center_y + height // 2),
        ]
        pygame.draw.polygon(surface, (*color, alpha), points, width=2)


def _draw_stripes(surface, color, alpha, spacing, slope):
    width, height = surface.get_size()
    stripe_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for offset in range(-height, width, spacing):
        start = (offset, 0)
        end = (offset + int(height * slope), height)
        pygame.draw.line(stripe_surface, (*color, alpha), start, end, 2)
    surface.blit(stripe_surface, (0, 0))


def _build_main_menu_background(size):
    surface = _vertical_gradient(size, (58, 112, 235), (133, 82, 205))
    glow_layer = pygame.Surface(size, pygame.SRCALPHA)
    _draw_soft_glow(glow_layer, (size[0] // 4, size[1] // 5), size[1] // 3, (94, 231, 255), 105)
    _draw_soft_glow(glow_layer, (int(size[0] * 0.82), size[1] // 4), size[1] // 3, (255, 125, 206), 90)
    _draw_soft_glow(glow_layer, (int(size[0] * 0.66), int(size[1] * 0.78)), size[1] // 3, (152, 110, 255), 70)
    surface.blit(glow_layer, (0, 0))
    _draw_stripes(surface, (255, 255, 255), 16, 44, 0.65)
    _draw_triangles(surface, (255, 193, 80), 95, [
        (180, 120, 180), (360, 260, 210), (220, 540, 250),
        (1020, 150, 170), (1120, 430, 260), (910, 560, 170), (720, 300, 220)
    ])
    vignette = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(vignette, (10, 12, 24, 40), vignette.get_rect(), border_radius=0)
    surface.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return surface


def _build_options_background(size):
    surface = _vertical_gradient(size, (44, 76, 172), (98, 56, 132))
    glow_layer = pygame.Surface(size, pygame.SRCALPHA)
    _draw_soft_glow(glow_layer, (size[0] // 5, size[1] // 4), size[1] // 4, (90, 222, 255), 80)
    _draw_soft_glow(glow_layer, (int(size[0] * 0.8), int(size[1] * 0.72)), size[1] // 3, (255, 108, 192), 55)
    surface.blit(glow_layer, (0, 0))
    _draw_stripes(surface, (255, 255, 255), 12, 56, 0.75)
    _draw_triangles(surface, (255, 182, 70), 70, [
        (250, 190, 170), (410, 420, 220), (810, 170, 160),
        (980, 330, 210), (1120, 150, 140), (1080, 590, 180)
    ])
    return surface


def _build_play_background(size):
    surface = _vertical_gradient(size, (22, 24, 30), (42, 24, 42))
    glow_layer = pygame.Surface(size, pygame.SRCALPHA)
    points = [
        (140, 140, (255, 114, 190)), (260, 440, (96, 224, 255)),
        (500, 220, (255, 188, 70)), (820, 620, (152, 110, 255)),
        (980, 180, (255, 104, 196)), (1120, 420, (90, 222, 255))
    ]
    for x, y, color in points:
        _draw_soft_glow(glow_layer, (x, y), size[1] // 5, color, 45)
    surface.blit(glow_layer, (0, 0))

    panel_layer = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(panel_layer, (10, 12, 18, 150), pygame.Rect(0, 0, 560, size[1]))
    pygame.draw.rect(panel_layer, (10, 12, 18, 110), pygame.Rect(size[0] - 440, 0, 440, size[1]))
    surface.blit(panel_layer, (0, 0))
    _draw_stripes(surface, (255, 255, 255), 12, 18, 0.85)
    return surface


def _build_logo(size):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (size[0] // 2, size[1] // 2)
    outer_radius = min(size) // 2 - 20
    inner_radius = outer_radius - 32

    _draw_soft_glow(surface, center, outer_radius + 35, (255, 255, 255), 36)
    _draw_soft_glow(surface, center, outer_radius + 22, (255, 110, 196), 26)

    ray_layer = pygame.Surface(size, pygame.SRCALPHA)
    for angle in range(0, 360, 15):
        radians = math.radians(angle)
        start = (
            int(center[0] + math.cos(radians) * (inner_radius + 8)),
            int(center[1] + math.sin(radians) * (inner_radius + 8)),
        )
        end = (
            int(center[0] + math.cos(radians) * (outer_radius + 28)),
            int(center[1] + math.sin(radians) * (outer_radius + 28)),
        )
        pygame.draw.line(ray_layer, (255, 255, 255, 120), start, end, 4)
    surface.blit(ray_layer, (0, 0))

    pygame.draw.circle(surface, (255, 255, 255, 255), center, outer_radius)
    pygame.draw.circle(surface, (255, 235, 246, 255), center, outer_radius - 8)
    pygame.draw.circle(surface, (241, 87, 170, 255), center, inner_radius)
    highlight = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.circle(highlight, (255, 130, 200, 70), (center[0], center[1] - inner_radius // 3), inner_radius - 14)
    surface.blit(highlight, (0, 0))
    return surface


def _build_song_tile_cover(size):
    surface = _vertical_gradient(size, (18, 20, 26), (34, 34, 40))
    accent_width = max(10, size[0] // 18)
    cyan_width = max(5, accent_width // 2)
    pygame.draw.rect(surface, (255, 100, 188), pygame.Rect(0, 0, accent_width, size[1]))
    pygame.draw.rect(surface, (96, 224, 255), pygame.Rect(accent_width, 0, cyan_width, size[1]))
    pygame.draw.rect(surface, (245, 245, 245), pygame.Rect(accent_width + cyan_width + 4, 4, size[0] - accent_width - cyan_width - 8, 3))
    return surface


def _build_map_details_panel(size):
    surface = _vertical_gradient(size, (16, 18, 24), (34, 24, 42))
    pygame.draw.rect(surface, (96, 224, 255), pygame.Rect(0, 0, 8, size[1]))
    pygame.draw.rect(surface, (255, 100, 188), pygame.Rect(0, 0, size[0], 6))
    detail_layer = pygame.Surface(size, pygame.SRCALPHA)
    _draw_soft_glow(detail_layer, (int(size[0] * 0.8), int(size[1] * 0.28)), 75, (255, 114, 190), 36)
    _draw_soft_glow(detail_layer, (int(size[0] * 0.88), int(size[1] * 0.72)), 62, (96, 224, 255), 26)
    surface.blit(detail_layer, (0, 0))
    return surface
