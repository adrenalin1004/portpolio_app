"""게임 진행 및 상태 관리."""

import pygame

from board import Board
from config import STATE_GAME_OVER, STATE_PAUSED, STATE_PLAYING, STATE_READY
from input_handler import InputHandler
from renderer import Renderer
from scoring import ScoreManager
from tetromino import Tetromino


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = STATE_READY
        self.board = Board()
        self.score_manager = ScoreManager()
        self.renderer = Renderer(screen)
        self.input_handler = InputHandler()
        self.current_piece = None
        self.next_piece = None
        self.last_fall_time = 0
        self.init_error = None

        try:
            self.reset()
        except Exception as error:
            self.init_error = str(error)
            print(f"[E-008] 게임 초기화 실패: {error}")

    def reset(self):
        """모든 게임 데이터를 초기 상태로 되돌린다."""
        self.board.clear_board()
        self.score_manager.reset_score()
        self.current_piece = None
        self.next_piece = Tetromino()
        self.last_fall_time = pygame.time.get_ticks()
        self.state = STATE_READY

    def start(self):
        if self.init_error:
            return
        self.board.clear_board()
        self.score_manager.reset_score()
        self.next_piece = Tetromino()
        self.state = STATE_PLAYING
        self.last_fall_time = pygame.time.get_ticks()
        self.spawn_piece()

    def pause(self):
        if self.state == STATE_PLAYING:
            self.state = STATE_PAUSED
        elif self.state == STATE_PAUSED:
            self.state = STATE_PLAYING
            self.last_fall_time = pygame.time.get_ticks()

    def game_over(self):
        self.state = STATE_GAME_OVER

    def quit(self):
        self.running = False

    def spawn_piece(self):
        self.current_piece = self.next_piece
        self.current_piece.x = self.current_piece._spawn_x()
        self.current_piece.y = 0
        self.next_piece = Tetromino()

        if not self.board.is_valid_position(
            self.current_piece.shape, self.current_piece.x, self.current_piece.y
        ):
            self.game_over()

    def move_left(self):
        self._try_move(-1, 0)

    def move_right(self):
        self._try_move(1, 0)

    def soft_drop(self):
        if not self._try_move(0, 1):
            self.lock_current_piece()
        else:
            self.last_fall_time = pygame.time.get_ticks()

    def hard_drop(self):
        if self.current_piece is None:
            return
        while self.board.is_valid_position(
            self.current_piece.shape, self.current_piece.x, self.current_piece.y + 1
        ):
            self.current_piece.move_down()
        self.lock_current_piece()

    def rotate(self):
        if self.current_piece is None:
            return
        previous = [row[:] for row in self.current_piece.shape]
        self.current_piece.rotate()
        if not self.board.is_valid_position(
            self.current_piece.shape, self.current_piece.x, self.current_piece.y
        ):
            self.current_piece.shape = previous

    def get_drop_y(self):
        if self.current_piece is None:
            return 0
        y = self.current_piece.y
        while self.board.is_valid_position(
            self.current_piece.shape, self.current_piece.x, y + 1
        ):
            y += 1
        return y

    def lock_current_piece(self):
        if self.current_piece is None:
            return
        self.board.lock_piece(self.current_piece)
        _, cleared = self.board.clear_lines()
        if cleared:
            self.score_manager.add_score(cleared)
            self.score_manager.update_lines(cleared)
        self.current_piece = None
        self.spawn_piece()
        self.last_fall_time = pygame.time.get_ticks()

    def handle_click(self, pos):
        if self.state == STATE_READY and self.renderer.start_button.collidepoint(pos):
            self.start()
        elif self.state == STATE_GAME_OVER and self.renderer.restart_button.collidepoint(
            pos
        ):
            self.reset()
            self.start()

    def update(self):
        if self.state != STATE_PLAYING or self.current_piece is None:
            return

        now = pygame.time.get_ticks()
        interval = self.score_manager.get_fall_interval_ms()
        if now - self.last_fall_time >= interval:
            if not self._try_move(0, 1):
                self.lock_current_piece()
            self.last_fall_time = now

    def draw(self):
        if self.init_error:
            self.screen.fill((20, 20, 30))
            font = pygame.font.SysFont("arial", 24)
            message = font.render(
                f"Initialization failed: {self.init_error}", True, (255, 80, 80)
            )
            self.screen.blit(message, (40, 40))
            return
        self.renderer.draw(self)

    def run(self):
        while self.running:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                self.input_handler.handle_event(event, self)

            self.input_handler.update(self, now)
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def _try_move(self, dx, dy):
        if self.current_piece is None:
            return False
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.board.is_valid_position(
            self.current_piece.shape, self.current_piece.x, self.current_piece.y
        ):
            return True
        self.current_piece.x -= dx
        self.current_piece.y -= dy
        return False
