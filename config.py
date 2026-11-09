"""게임 설정 및 상수 (화면, 보드, 색상, 점수, 레벨)."""

# 화면
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60
WINDOW_TITLE = "Python Tetris"

# 보드
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30
BOARD_PIXEL_WIDTH = BOARD_WIDTH * CELL_SIZE  # 300
BOARD_PIXEL_HEIGHT = BOARD_HEIGHT * CELL_SIZE  # 600

# 보드 위치 (좌측)
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 50

# 우측 정보 패널
PANEL_X = 400
PANEL_WIDTH = 350

# 게임 초기값
INITIAL_LEVEL = 1
INITIAL_SCORE = 0
MAX_LEVEL = 10
LINES_PER_LEVEL = 10

# 게임 상태
STATE_READY = "READY"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"

# 색상
COLOR_BACKGROUND = (20, 20, 30)
COLOR_BOARD_BG = (12, 12, 22)
COLOR_GRID = (45, 45, 65)
COLOR_BORDER = (90, 90, 130)
COLOR_TEXT = (230, 230, 240)
COLOR_TEXT_DIM = (160, 160, 180)
COLOR_ACCENT = (80, 180, 255)
COLOR_BUTTON = (50, 120, 220)
COLOR_BUTTON_HOVER = (70, 150, 255)
COLOR_OVERLAY = (0, 0, 0, 160)
COLOR_GHOST = (80, 80, 100)

# 블록 색상 (1~7)
COLORS = {
    0: COLOR_BOARD_BG,
    1: (0, 255, 255),      # I 하늘색
    2: (255, 255, 0),      # O 노란색
    3: (160, 0, 255),      # T 보라색
    4: (0, 255, 0),        # S 초록색
    5: (255, 0, 0),        # Z 빨간색
    6: (0, 0, 255),        # J 파란색
    7: (255, 165, 0),      # L 주황색
}

SHAPE_IDS = {
    "I": 1,
    "O": 2,
    "T": 3,
    "S": 4,
    "Z": 5,
    "J": 6,
    "L": 7,
}

SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [
        [1, 1],
        [1, 1],
    ],
    "T": [
        [0, 1, 0],
        [1, 1, 1],
    ],
    "S": [
        [0, 1, 1],
        [1, 1, 0],
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 1],
    ],
    "J": [
        [1, 0, 0],
        [1, 1, 1],
    ],
    "L": [
        [0, 0, 1],
        [1, 1, 1],
    ],
}

SHAPE_NAMES = list(SHAPES.keys())

# 점수: 제거한 줄 수 -> 기본 점수 (최종 점수 = 기본 점수 * 레벨)
SCORE_TABLE = {
    1: 100,
    2: 300,
    3: 500,
    4: 800,
}

# 레벨별 자동 하강 간격 (밀리초)
FALL_INTERVALS_MS = {
    1: 1000,
    2: 800,
    3: 600,
    4: 500,
    5: 400,
    6: 300,
    7: 250,
    8: 200,
    9: 150,
    10: 100,
}

# 키 반복 (좌우/소프트 드롭)
KEY_REPEAT_DELAY_MS = 180
KEY_REPEAT_INTERVAL_MS = 50
