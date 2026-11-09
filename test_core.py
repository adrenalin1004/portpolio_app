"""보드, 충돌, 점수, 회전 핵심 로직 검증."""

from board import Board
from collision import check_collision
from config import BOARD_HEIGHT, BOARD_WIDTH
from scoring import ScoreManager
from tetromino import rotate_shape


def test_collision_walls_and_floor():
    board = Board().grid
    shape = [[1, 1], [1, 1]]
    assert check_collision(board, shape, -1, 0) is True
    assert check_collision(board, shape, BOARD_WIDTH - 1, 0) is True
    assert check_collision(board, shape, 0, BOARD_HEIGHT - 1) is True
    assert check_collision(board, shape, 4, 0) is False


def test_collision_with_locked_block():
    board = Board()
    board.grid[0][4] = 1
    shape = [[1]]
    assert check_collision(board.grid, shape, 4, 0) is True
    assert check_collision(board.grid, shape, 5, 0) is False


def test_clear_one_line_and_gravity():
    board = Board()
    board.grid[18] = [1] * BOARD_WIDTH
    board.grid[19] = [2] + [0] * (BOARD_WIDTH - 1)
    _, cleared = board.clear_lines()
    assert cleared == 1
    assert board.grid[0] == [0] * BOARD_WIDTH
    assert board.grid[19][0] == 2
    assert all(cell == 0 for cell in board.grid[19][1:])


def test_scoring_and_level():
    scores = ScoreManager()
    scores.add_score(1)
    assert scores.score == 100
    scores.update_lines(10)
    assert scores.level == 2
    scores.add_score(1)
    assert scores.score == 300


def test_rotate_clockwise():
    t_shape = [
        [0, 1, 0],
        [1, 1, 1],
    ]
    rotated = rotate_shape(t_shape)
    assert rotated == [
        [1, 0],
        [1, 1],
        [1, 0],
    ]


if __name__ == "__main__":
    tests = [
        test_collision_walls_and_floor,
        test_collision_with_locked_block,
        test_clear_one_line_and_gravity,
        test_scoring_and_level,
        test_rotate_clockwise,
    ]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print("All core tests passed.")
