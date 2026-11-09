"""블록 충돌 감지."""

from config import BOARD_HEIGHT, BOARD_WIDTH


def check_collision(board, shape, x, y):
    """벽, 바닥, 고정된 블록과 겹치면 True를 반환한다."""
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if not cell:
                continue

            board_x = x + col_index
            board_y = y + row_index

            if board_x < 0 or board_x >= BOARD_WIDTH:
                return True

            if board_y >= BOARD_HEIGHT:
                return True

            if board_y >= 0 and board[board_y][board_x] != 0:
                return True

    return False
