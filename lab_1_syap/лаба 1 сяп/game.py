"""Главный класс игры: окно, игровой цикл, переключение состояний."""

import sys

import pygame

from asteroid import AsteroidField
from collisions import ship_hits_any_asteroid
from constants import (
    COLORS,
    FINISH_X,
    FPS,
    STATE_GAME_OVER,
    STATE_MENU,
    STATE_PLAY,
    STATE_WIN,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)
from ship import Ship
import ui


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        # SysFont с запасным вариантом: стандартный шрифт pygame не знает кириллицу.
        self.font = pygame.font.SysFont("arial,dejavusans,verdana", 20)
        self.big_font = pygame.font.SysFont("arial,dejavusans,verdana", 56, bold=True)

        self.stars = ui.make_stars()
        self.state = STATE_MENU
        self.reset()

    def reset(self):
        """Создаёт новый корабль и поле астероидов."""
        self.ship = Ship()
        self.field = AsteroidField(self.ship.x, self.ship.y)
        self.elapsed = 0.0

    # --- события ----------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type != pygame.KEYDOWN:
                continue

            # if/elif вместо match/case - так код работает и на Python 3.9.
            if self.state == STATE_MENU:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.reset()
                    self.state = STATE_PLAY
                elif event.key == pygame.K_ESCAPE:
                    self.quit()
            elif self.state == STATE_PLAY:
                if event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU
            elif self.state in (STATE_GAME_OVER, STATE_WIN):
                if event.key == pygame.K_r:
                    self.reset()
                    self.state = STATE_PLAY
                elif event.key == pygame.K_ESCAPE:
                    self.state = STATE_MENU

    # --- обновление -------------------------------------------------
    def update(self, dt):
        if self.state != STATE_PLAY:
            return

        self.ship.handle_input(pygame.key.get_pressed(), dt)
        self.ship.update(dt)
        self.field.update(dt)
        self.elapsed += dt

        if ship_hits_any_asteroid(self.ship, self.field.asteroids):
            self.state = STATE_GAME_OVER
        elif self.ship.x >= FINISH_X:
            self.state = STATE_WIN

    # --- отрисовка --------------------------------------------------
    def draw(self):
        ui.draw_background(self.screen, self.stars)

        if self.state == STATE_MENU:
            ui.draw_menu(self.screen, self.big_font, self.font)
        else:
            ui.draw_finish_zone(self.screen)
            self.field.draw(self.screen)
            self.ship.draw(self.screen)
            ui.draw_hud(self.screen, self.font, self.ship, self.elapsed)
            if self.state == STATE_GAME_OVER:
                ui.draw_game_over(self.screen, self.big_font, self.font, self.elapsed)
            elif self.state == STATE_WIN:
                ui.draw_win(self.screen, self.big_font, self.font, self.elapsed)

        pygame.display.flip()

    # --- главный цикл -----------------------------------------------
    def run(self):
        while True:
            # dt - время кадра в секундах; физика не зависит от FPS.
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()
