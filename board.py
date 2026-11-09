"""게임 보드 생성, 블록 고정, 줄 제거."""

from collision import check_collision
from config import BOARD_HEIGHT, BOARD_WIDTH


class Board:
    def __init__(self):
        self.grid = self.create_board()

    def create_board(self):
        return [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    def clear_board(self):
        self.grid = self.create_board()

    def is_valid_position(self, shape, x, y):
        return not check_collision(self.grid, shape, x, y)

    def lock_piece(self, piece):
        """현재 블록을 보드에 고정한다."""
        for row_index, row in enumerate(piece.shape):
            for col_index, cell in enumerate(row):
                if not cell:
                    continue
                board_x = piece.x + col_index
                board_y = piece.y + row_index
                if 0 <= board_y < BOARD_HEIGHT and 0 <= board_x < BOARD_WIDTH:
                    self.grid[board_y][board_x] = piece.color_id

    def clear_lines(self):
        """완성된 가로줄을 제거하고 (새 보드, 제거한 줄 수)를 반환한다."""
        new_board = [row for row in self.grid if not all(cell != 0 for cell in row)]
        cleared = BOARD_HEIGHT - len(new_board)

        for _ in range(cleared):
            new_board.insert(0, [0] * BOARD_WIDTH)

        self.grid = new_board
        return self.grid, cleared
