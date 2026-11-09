"""키보드 및 마우스 입력 처리."""

import pygame

from config import (
    KEY_REPEAT_DELAY_MS,
    KEY_REPEAT_INTERVAL_MS,
    STATE_GAME_OVER,
    STATE_PAUSED,
    STATE_PLAYING,
    STATE_READY,
)


class InputHandler:
    """상태에 따라 입력을 Game 액션으로 변환한다."""

    def __init__(self):
        self._held = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_DOWN: False,
        }
        self._hold_start = {key: 0 for key in self._held}
        self._last_repeat = {key: 0 for key in self._held}

    def handle_event(self, event, game):
        if event.type == pygame.QUIT:
            game.quit()
            return

        if event.type == pygame.KEYDOWN:
            self._on_keydown(event.key, game)
        elif event.type == pygame.KEYUP:
            if event.key in self._held:
                self._held[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.handle_click(event.pos)

    def update(self, game, now_ms):
        """키를 누르고 있는 동안 좌우/소프트 드롭을 반복한다."""
        if game.state != STATE_PLAYING:
            return

        for key, held in self._held.items():
            if not held:
                continue
            elapsed = now_ms - self._hold_start[key]
            if elapsed < KEY_REPEAT_DELAY_MS:
                continue
            if now_ms - self._last_repeat[key] < KEY_REPEAT_INTERVAL_MS:
                continue
            self._last_repeat[key] = now_ms
            self._apply_hold_action(key, game)

    def _on_keydown(self, key, game):
        if key == pygame.K_ESCAPE:
            game.quit()
            return

        if game.state == STATE_READY:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                game.start()
            return

        if game.state == STATE_GAME_OVER:
            if key == pygame.K_r:
                game.reset()
                game.start()
            return

        if key == pygame.K_p:
            game.pause()
            return

        if key == pygame.K_r:
            game.reset()
            game.start()
            return

        if game.state != STATE_PLAYING:
            return

        if key in self._held:
            self._held[key] = True
            self._hold_start[key] = pygame.time.get_ticks()
            self._last_repeat[key] = pygame.time.get_ticks()

        if key == pygame.K_LEFT:
            game.move_left()
        elif key == pygame.K_RIGHT:
            game.move_right()
        elif key == pygame.K_DOWN:
            game.soft_drop()
        elif key == pygame.K_UP:
            game.rotate()
        elif key == pygame.K_SPACE:
            game.hard_drop()

    def _apply_hold_action(self, key, game):
        if game.state == STATE_PAUSED:
            return
        if key == pygame.K_LEFT:
            game.move_left()
        elif key == pygame.K_RIGHT:
            game.move_right()
        elif key == pygame.K_DOWN:
            game.soft_drop()
