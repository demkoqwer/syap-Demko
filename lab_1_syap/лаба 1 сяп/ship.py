"""Класс космического корабля с физикой инерции."""

import math

import pygame

from constants import (
    COLORS,
    MAX_SPEED,
    ROTATION_SPEED,
    SHIP_MASS,
    SHIP_RADIUS,
    SHIP_START_ALPHA,
    SHIP_START_X,
    SHIP_START_Y,
    THRUST_FORCE,
    WALL_RESTITUTION,
    WINDOW_HEIGHT,
)


class Ship:
    """Корабль: масса, координаты (x, y), угол alpha, вектор скорости (vx, vy)."""

    def __init__(self):
        self.mass = SHIP_MASS
        self.radius = SHIP_RADIUS
        self.x = float(SHIP_START_X)
        self.y = float(SHIP_START_Y)
        self.alpha = SHIP_START_ALPHA   # угол корпуса в радианах
        self.vx = 0.0
        self.vy = 0.0
        self.thrusting = False          # нужен для отрисовки пламени

    @property
    def speed(self):
        """Модуль вектора скорости."""
        return math.hypot(self.vx, self.vy)

    def handle_input(self, keys, dt):
        """Обрабатывает УДЕРЖАНИЕ клавиш: A/D - поворот, W - тяга."""
        if keys[pygame.K_a]:
            self.alpha -= ROTATION_SPEED * dt
        if keys[pygame.K_d]:
            self.alpha += ROTATION_SPEED * dt

        self.thrusting = bool(keys[pygame.K_w])
        if self.thrusting:
            # ускорение a = F / m; импульс тяги направлен по носу корабля:
            # vx += thrust * cos(alpha), vy += thrust * sin(alpha)
            thrust = (THRUST_FORCE / self.mass) * dt
            self.vx += thrust * math.cos(self.alpha)
            self.vy += thrust * math.sin(self.alpha)

    def update(self, dt):
        """Движение по инерции. Трение = 0, поэтому скорость сама не падает."""
        # Ограничиваем модуль скорости (только для играбельности).
        speed = self.speed
        if speed > MAX_SPEED:
            k = MAX_SPEED / speed
            self.vx *= k
            self.vy *= k

        self.x += self.vx * dt
        self.y += self.vy * dt
        self._bounce_off_borders()

    def _bounce_off_borders(self):
        """Упругий (с потерями) отскок от левой, верхней и нижней границ.

        Правой границы нет: справа находится финишная зона.
        """
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx) * WALL_RESTITUTION
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy) * WALL_RESTITUTION
        elif self.y + self.radius > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.radius
            self.vy = -abs(self.vy) * WALL_RESTITUTION

    def draw(self, surface):
        """Рисует корабль-треугольник, повёрнутый на угол alpha."""
        r = self.radius
        # Вершины в локальной системе (нос смотрит вдоль +x), затем поворот.
        local = [(r * 1.3, 0), (-r, -r * 0.8), (-r * 0.5, 0), (-r, r * 0.8)]
        points = [self._to_world(px, py) for px, py in local]

        if self.thrusting:
            flame = [self._to_world(-r * 0.5, -r * 0.35),
                     self._to_world(-r * 1.9, 0),
                     self._to_world(-r * 0.5, r * 0.35)]
            pygame.draw.polygon(surface, COLORS["flame"], flame)

        pygame.draw.polygon(surface, COLORS["ship"], points)
        pygame.draw.polygon(surface, COLORS["ship_outline"], points, 2)

    def _to_world(self, px, py):
        """Поворачивает точку на alpha и сдвигает в позицию корабля."""
        c, s = math.cos(self.alpha), math.sin(self.alpha)
        return (self.x + px * c - py * s, self.y + px * s + py * c)

