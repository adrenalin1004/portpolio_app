"""점수, 레벨, 제거 줄 수 관리."""

from config import (
    FALL_INTERVALS_MS,
    INITIAL_LEVEL,
    INITIAL_SCORE,
    LINES_PER_LEVEL,
    MAX_LEVEL,
    SCORE_TABLE,
)


class ScoreManager:
    def __init__(self):
        self.reset_score()

    def reset_score(self):
        self.score = INITIAL_SCORE
        self.level = INITIAL_LEVEL
        self.lines = 0

    def add_score(self, cleared_lines):
        """제거한 줄 수와 현재 레벨로 점수를 더한다."""
        if cleared_lines <= 0:
            return self.score

        try:
            base = SCORE_TABLE.get(cleared_lines, 0)
            self.score += base * self.level
        except Exception as error:
            print(f"[E-007] 점수 계산 오류: {error}")

        return self.score

    def update_lines(self, cleared_lines):
        self.lines += cleared_lines
        self.update_level()
        return self.lines

    def update_level(self):
        new_level = self.lines // LINES_PER_LEVEL + INITIAL_LEVEL
        self.level = min(new_level, MAX_LEVEL)
        return self.level

    def get_fall_interval_ms(self):
        return FALL_INTERVALS_MS.get(self.level, FALL_INTERVALS_MS[MAX_LEVEL])
