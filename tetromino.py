"""테트리스 블록 생성, 이동, 회전."""

import random

from config import BOARD_WIDTH, SHAPE_IDS, SHAPE_NAMES, SHAPES


def rotate_shape(shape):
    """시계 방향으로 90도 회전한 새 모양을 반환한다."""
    return [list(row) for row in zip(*shape[::-1])]


class Tetromino:
    """하나의 테트로미노(현재 블록 또는 다음 블록)."""

    def __init__(self, name=None):
        self.create_piece(name)

    def create_piece(self, name=None):
        """7가지 블록 중 하나를 무작위로 생성한다."""
        self.name = name if name in SHAPES else random.choice(SHAPE_NAMES)
        self.shape = [row[:] for row in SHAPES[self.name]]
        self.color_id = SHAPE_IDS[self.name]
        self.x = self._spawn_x()
        self.y = 0
        return self

    def _spawn_x(self):
        width = len(self.shape[0])
        return (BOARD_WIDTH - width) // 2

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1

    def rotate(self):
        """모양을 시계 방향으로 90도 회전한다. O 블록은 모양이 같다."""
        self.shape = rotate_shape(self.shape)

    def copy(self):
        piece = Tetromino.__new__(Tetromino)
        piece.name = self.name
        piece.shape = [row[:] for row in self.shape]
        piece.color_id = self.color_id
        piece.x = self.x
        piece.y = self.y
        return piece
