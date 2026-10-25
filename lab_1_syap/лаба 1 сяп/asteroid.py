"""Астероиды и алгоритм их спавна."""

import math
import random

import pygame

from constants import (
    ASTEROID_ANGLE_JITTER,
    ASTEROID_DESPAWN_MARGIN,
    ASTEROID_INITIAL_COUNT,
    ASTEROID_MAX_COUNT,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MAX_SPEED,
    ASTEROID_MIN_RADIUS,
    ASTEROID_MIN_SPEED,
    ASTEROID_SPAWN_INTERVAL,
    COLORS,
    SAFE_START_DISTANCE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class Asteroid:
    """Круглый астероид, летящий прямолинейно с постоянной скоростью."""

    def __init__(self, x, y, radius, angle, speed):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def is_gone(self):
        """True, если астероид улетел далеко за пределы экрана."""
        m = ASTEROID_DESPAWN_MARGIN
        return (self.x < -m or self.x > WINDOW_WIDTH + m
                or self.y < -m or self.y > WINDOW_HEIGHT + m)

    def draw(self, surface):
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COLORS["asteroid"], pos, self.radius)
        pygame.draw.circle(surface, COLORS["asteroid_outline"], pos, self.radius, 2)


class AsteroidField:
    """Поток астероидов: хранит список и порождает новые."""

    def __init__(self, ship_x, ship_y):
        self.asteroids = []
        self.spawn_timer = 0.0
        # На старте экран уже не пустой, но рядом с кораблём астероидов нет.
        for _ in range(ASTEROID_INITIAL_COUNT):
            self._spawn_inside(ship_x, ship_y)

    def update(self, dt):
        """Двигает астероиды, удаляет улетевшие, по таймеру добавляет новые."""
        for a in self.asteroids:
            a.update(dt)
        # Фильтрация списка: оставляем только те, что ещё в игровой области.
        self.asteroids = [a for a in self.asteroids if not a.is_gone()]

        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and len(self.asteroids) < ASTEROID_MAX_COUNT:
            self._spawn_from_edge()
            # Небольшой случайный разброс, чтобы поток не был «метрономом».
            self.spawn_timer = ASTEROID_SPAWN_INTERVAL * random.uniform(0.6, 1.4)

    def draw(self, surface):
        for a in self.asteroids:
            a.draw(surface)

    # --- внутренние методы ------------------------------------------
    def _spawn_inside(self, ship_x, ship_y):
        """Астероид в случайной точке экрана, подальше от корабля."""
        radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
        while True:
            x = random.uniform(0, WINDOW_WIDTH)
            y = random.uniform(0, WINDOW_HEIGHT)
            if math.hypot(x - ship_x, y - ship_y) > SAFE_START_DISTANCE + radius:
                break
        angle = random.uniform(0, 2 * math.pi)       # случайный угол полёта
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        self.asteroids.append(Asteroid(x, y, radius, angle, speed))

    def _spawn_from_edge(self):
        """Астероид появляется за краем экрана и летит под случайным углом.

        Край выбирается с весами: чаще справа (навстречу кораблю).
        """
        radius = random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS)
        edge = random.choices(["right", "top", "bottom", "left"],
                              weights=[50, 20, 20, 10])[0]
        off = radius + 10   # центр чуть за границей, астероид не «выскакивает»
        if edge == "right":
            x, y = WINDOW_WIDTH + off, random.uniform(0, WINDOW_HEIGHT)
        elif edge == "left":
            x, y = -off, random.uniform(0, WINDOW_HEIGHT)
        elif edge == "top":
            x, y = random.uniform(0, WINDOW_WIDTH), -off
        else:
            x, y = random.uniform(0, WINDOW_WIDTH), WINDOW_HEIGHT + off

        # Целимся в случайную точку экрана и добавляем случайный разброс угла.
        tx = random.uniform(0, WINDOW_WIDTH)
        ty = random.uniform(0, WINDOW_HEIGHT)
        angle = math.atan2(ty - y, tx - x) + random.uniform(
            -ASTEROID_ANGLE_JITTER, ASTEROID_ANGLE_JITTER)
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        self.asteroids.append(Asteroid(x, y, radius, angle, speed))

