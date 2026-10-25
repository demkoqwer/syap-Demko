"""Интерфейс: фон, финишная зона, HUD, меню и экраны завершения."""

import math
import random

import pygame

from constants import (
    COLORS,
    FINISH_WIDTH,
    FINISH_X,
    SHIP_START_X,
    STAR_COUNT,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


def make_stars():
    """Список случайных звёзд (x, y, размер) для фона."""
    return [(random.randrange(WINDOW_WIDTH), random.randrange(WINDOW_HEIGHT),
             random.choice([1, 1, 2])) for _ in range(STAR_COUNT)]


def draw_background(surface, stars):
    surface.fill(COLORS["bg"])
    for x, y, size in stars:
        pygame.draw.circle(surface, COLORS["star"], (x, y), size)


def draw_finish_zone(surface):
    """Полупрозрачная зелёная полоса у правого края + надпись."""
    overlay = pygame.Surface((FINISH_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*COLORS["finish"], 70))
    surface.blit(overlay, (FINISH_X, 0))
    pygame.draw.line(surface, COLORS["finish"], (FINISH_X, 0), (FINISH_X, WINDOW_HEIGHT), 2)


def _center_text(surface, font, text, y, color):
    img = font.render(text, True, color)
    surface.blit(img, img.get_rect(center=(WINDOW_WIDTH // 2, y)))


def draw_hud(surface, font, ship, elapsed):
    """Скорость, угол, время и прогресс до финиша."""
    angle_deg = math.degrees(ship.alpha) % 360
    lines = [
        f"Скорость: {ship.speed:6.1f} px/с",
        f"Угол: {angle_deg:5.0f}°",
        f"Время: {elapsed:5.1f} с",
    ]
    for i, line in enumerate(lines):
        surface.blit(font.render(line, True, COLORS["text"]), (10, 8 + i * 22))

    # Полоска прогресса по оси X: от старта до финишной линии.
    progress = (ship.x - SHIP_START_X) / (FINISH_X - SHIP_START_X)
    progress = max(0.0, min(1.0, progress))
    bar = pygame.Rect(WINDOW_WIDTH - 210, 12, 190, 12)
    pygame.draw.rect(surface, COLORS["text_dim"], bar, 1)
    pygame.draw.rect(surface, COLORS["finish"],
                     (bar.x + 1, bar.y + 1, int((bar.w - 2) * progress), bar.h - 2))
    label = font.render("До финиша", True, COLORS["text_dim"])
    surface.blit(label, (bar.x, bar.bottom + 4))


def draw_menu(surface, big_font, font):
    _center_text(surface, big_font, "ASTEROID ESCAPE", 190, COLORS["ship"])
    _center_text(surface, font, "Космический лабиринт", 235, COLORS["text_dim"])
    help_lines = [
        "A / D - поворот корабля",
        "W - тяга (корабль движется по инерции, трения нет)",
        "Долети до зелёной зоны справа и не сталкивайся с астероидами",
    ]
    for i, line in enumerate(help_lines):
        _center_text(surface, font, line, 310 + i * 28, COLORS["text"])
    _center_text(surface, font, "Нажми ENTER или ПРОБЕЛ, чтобы начать", 450, COLORS["win"])
    _center_text(surface, font, "ESC - выход", 480, COLORS["text_dim"])


def _draw_overlay(surface):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill(COLORS["overlay"])
    surface.blit(overlay, (0, 0))


def draw_game_over(surface, big_font, font, elapsed):
    _draw_overlay(surface)
    _center_text(surface, big_font, "GAME OVER", 240, COLORS["danger"])
    _center_text(surface, font, f"Корабль разбит астероидом через {elapsed:.1f} с", 290, COLORS["text"])
    _center_text(surface, font, "R - заново    ESC - в меню", 350, COLORS["text_dim"])


def draw_win(surface, big_font, font, elapsed):
    _draw_overlay(surface)
    _center_text(surface, big_font, "ФИНИШ!", 240, COLORS["win"])
    _center_text(surface, font, f"Ты выбрался из поля астероидов за {elapsed:.1f} с", 290, COLORS["text"])
    _center_text(surface, font, "R - заново    ESC - в меню", 350, COLORS["text_dim"])

