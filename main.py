"""Python Tetris — 프로그램 시작 및 메인 루프."""

import sys

import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE
from game import Game


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game = Game(screen)
    game.run()
    sys.exit()


if __name__ == "__main__":
    main()
