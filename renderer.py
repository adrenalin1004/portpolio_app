"""게임 화면 렌더링."""

import pygame

from config import (
    BOARD_HEIGHT,
    BOARD_OFFSET_X,
    BOARD_OFFSET_Y,
    BOARD_PIXEL_HEIGHT,
    BOARD_PIXEL_WIDTH,
    BOARD_WIDTH,
    CELL_SIZE,
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_BOARD_BG,
    COLOR_BORDER,
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_GRID,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    COLORS,
    PANEL_WIDTH,
    PANEL_X,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATE_GAME_OVER,
    STATE_PAUSED,
    STATE_READY,
)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 36, bold=True)
        self.font_large = pygame.font.SysFont("arial", 28, bold=True)
        self.font = pygame.font.SysFont("arial", 22)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.start_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 50, 180, 48
        )
        self.restart_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 + 70, 180, 48
        )

    def draw(self, game):
        self.screen.fill(COLOR_BACKGROUND)
        self.draw_board(game.board)
        if game.current_piece is not None and game.state != STATE_READY:
            self.draw_ghost(game)
            self.draw_piece(game.current_piece)
        self.draw_panel(game)

        if game.state == STATE_READY:
            self.draw_ready()
        elif game.state == STATE_PAUSED:
            self.draw_paused()
        elif game.state == STATE_GAME_OVER:
            self.draw_game_over(game)

    def draw_board(self, board):
        board_rect = pygame.Rect(
            BOARD_OFFSET_X,
            BOARD_OFFSET_Y,
            BOARD_PIXEL_WIDTH,
            BOARD_PIXEL_HEIGHT,
        )
        pygame.draw.rect(self.screen, COLOR_BOARD_BG, board_rect)
        pygame.draw.rect(self.screen, COLOR_BORDER, board_rect, 3)

        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                cell = board.grid[y][x]
                if cell:
                    self._draw_cell(x, y, COLORS[cell])

        for x in range(BOARD_WIDTH + 1):
            px = BOARD_OFFSET_X + x * CELL_SIZE
            pygame.draw.line(
                self.screen,
                COLOR_GRID,
                (px, BOARD_OFFSET_Y),
                (px, BOARD_OFFSET_Y + BOARD_PIXEL_HEIGHT),
            )
        for y in range(BOARD_HEIGHT + 1):
            py = BOARD_OFFSET_Y + y * CELL_SIZE
            pygame.draw.line(
                self.screen,
                COLOR_GRID,
                (BOARD_OFFSET_X, py),
                (BOARD_OFFSET_X + BOARD_PIXEL_WIDTH, py),
            )

    def draw_piece(self, piece):
        self._draw_shape(piece.shape, piece.x, piece.y, COLORS[piece.color_id])

    def draw_ghost(self, game):
        ghost_y = game.get_drop_y()
        if ghost_y == game.current_piece.y:
            return
        color = COLORS[game.current_piece.color_id]
        faint = tuple(max(30, c // 4) for c in color)
        self._draw_shape(
            game.current_piece.shape,
            game.current_piece.x,
            ghost_y,
            faint,
            border_only=True,
        )

    def draw_next_piece(self, piece, box):
        title = self.font.render("NEXT BLOCK", True, COLOR_ACCENT)
        self.screen.blit(title, (box.x + 16, box.y + 12))

        if piece is None:
            return

        shape = piece.shape
        rows = len(shape)
        cols = len(shape[0])
        size = 24
        total_w = cols * size
        total_h = rows * size
        start_x = box.x + (box.width - total_w) // 2
        start_y = box.y + 50 + (box.height - 70 - total_h) // 2

        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if not cell:
                    continue
                rect = pygame.Rect(
                    start_x + col_index * size,
                    start_y + row_index * size,
                    size - 2,
                    size - 2,
                )
                pygame.draw.rect(self.screen, COLORS[piece.color_id], rect, border_radius=3)

    def draw_score(self, score, box):
        self._draw_stat_box(box, "SCORE", str(score))

    def draw_level(self, level, box):
        self._draw_stat_box(box, "LEVEL", str(level))

    def draw_lines(self, lines, box):
        self._draw_stat_box(box, "LINES", str(lines))

    def draw_game_over(self, game):
        self._draw_overlay()
        title = self.font_title.render("GAME OVER", True, (255, 90, 90))
        score = self.font_large.render(
            f"SCORE  {game.score_manager.score}", True, COLOR_TEXT
        )
        hint = self.font_small.render("Press R to restart", True, COLOR_TEXT_DIM)

        self._blit_center(title, SCREEN_HEIGHT // 2 - 70)
        self._blit_center(score, SCREEN_HEIGHT // 2 - 20)
        self._blit_center(hint, SCREEN_HEIGHT // 2 + 20)
        self._draw_button(self.restart_button, "RESTART")

    def draw_paused(self):
        self._draw_overlay()
        title = self.font_title.render("PAUSED", True, COLOR_TEXT)
        hint = self.font_small.render("Press P to resume", True, COLOR_TEXT_DIM)
        self._blit_center(title, SCREEN_HEIGHT // 2 - 24)
        self._blit_center(hint, SCREEN_HEIGHT // 2 + 24)

    def draw_ready(self):
        self._draw_overlay()
        title = self.font_title.render("PYTHON TETRIS", True, COLOR_ACCENT)
        hint = self.font_small.render(
            "Click START or press Enter", True, COLOR_TEXT_DIM
        )
        self._blit_center(title, SCREEN_HEIGHT // 2 - 140)
        self._blit_center(hint, SCREEN_HEIGHT // 2 - 90)
        self._draw_button(self.start_button, "START")

        controls = [
            "Left / Right : Move",
            "Up : Rotate",
            "Down : Soft Drop",
            "Space : Hard Drop",
            "P : Pause    R : Restart    ESC : Quit",
        ]
        y = SCREEN_HEIGHT // 2 + 20
        for line in controls:
            text = self.font_small.render(line, True, COLOR_TEXT_DIM)
            self._blit_center(text, y)
            y += 24

    def draw_panel(self, game):
        next_box = pygame.Rect(PANEL_X, 50, PANEL_WIDTH - 50, 160)
        score_box = pygame.Rect(PANEL_X, 230, PANEL_WIDTH - 50, 80)
        level_box = pygame.Rect(PANEL_X, 325, PANEL_WIDTH - 50, 80)
        lines_box = pygame.Rect(PANEL_X, 420, PANEL_WIDTH - 50, 80)

        for box in (next_box, score_box, level_box, lines_box):
            pygame.draw.rect(self.screen, (28, 28, 42), box, border_radius=10)
            pygame.draw.rect(self.screen, COLOR_BORDER, box, 2, border_radius=10)

        self.draw_next_piece(game.next_piece, next_box)
        self.draw_score(game.score_manager.score, score_box)
        self.draw_level(game.score_manager.level, level_box)
        self.draw_lines(game.score_manager.lines, lines_box)

        help_text = self.font_small.render(
            "P pause  |  R restart  |  ESC quit", True, COLOR_TEXT_DIM
        )
        self.screen.blit(help_text, (PANEL_X, 520))

    def _draw_stat_box(self, box, label, value):
        title = self.font.render(label, True, COLOR_ACCENT)
        number = self.font_large.render(value, True, COLOR_TEXT)
        self.screen.blit(title, (box.x + 16, box.y + 10))
        self.screen.blit(number, (box.x + 16, box.y + 38))

    def _draw_shape(self, shape, origin_x, origin_y, color, border_only=False):
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if not cell:
                    continue
                x = origin_x + col_index
                y = origin_y + row_index
                if y < 0:
                    continue
                self._draw_cell(x, y, color, border_only=border_only)

    def _draw_cell(self, grid_x, grid_y, color, border_only=False):
        rect = pygame.Rect(
            BOARD_OFFSET_X + grid_x * CELL_SIZE + 1,
            BOARD_OFFSET_Y + grid_y * CELL_SIZE + 1,
            CELL_SIZE - 2,
            CELL_SIZE - 2,
        )
        if border_only:
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=3)
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=3)
            highlight = tuple(min(255, c + 40) for c in color)
            pygame.draw.line(
                self.screen,
                highlight,
                (rect.left + 2, rect.top + 2),
                (rect.right - 3, rect.top + 2),
                2,
            )

    def _draw_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

    def _draw_button(self, rect, label):
        mouse = pygame.mouse.get_pos()
        color = COLOR_BUTTON_HOVER if rect.collidepoint(mouse) else COLOR_BUTTON
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        text = self.font.render(label, True, COLOR_TEXT)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def _blit_center(self, surface, y):
        x = (SCREEN_WIDTH - surface.get_width()) // 2
        self.screen.blit(surface, (x, y))
