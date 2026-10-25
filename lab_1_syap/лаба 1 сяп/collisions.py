"""Проверка столкновений окружностей."""

import math


def circles_collide(x1, y1, r1, x2, y2, r2):
    """Две окружности пересекаются, если расстояние между центрами
    не больше суммы радиусов: sqrt((x2-x1)^2 + (y2-y1)^2) <= r1 + r2.
    """
    distance = math.hypot(x2 - x1, y2 - y1)
    return distance <= r1 + r2


def ship_hits_any_asteroid(ship, asteroids):
    """True, если корабль столкнулся хотя бы с одним астероидом."""
    for a in asteroids:
        if circles_collide(ship.x, ship.y, ship.radius, a.x, a.y, a.radius):
            return True
    return False
