import math

import pygame
from pygame import Surface
from pygame.time import Clock

from game import Game

WIDTH = 600
HEIGHT = 600

ROWS = 30
COLS = 30
STARTING = 300

RECT_W = int(WIDTH / ROWS)
RECT_H = int(HEIGHT / COLS)


def main():
    game = Game(ROWS, COLS, STARTING)

    pygame.init()

    pygame.display.set_caption("Conway's Game of Life")
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = Clock()

    looping = True
    updating = True
    while looping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    looping = False
                elif event.key == pygame.K_p:
                    updating = not updating
                elif event.key == pygame.K_r:
                    game.reset()
                    updating = True

        if updating:
            for r, _ in enumerate(game.board):
                for c, _ in enumerate(game.board[r]):
                    draw_cell(screen, game, r, c)
            game.update()

        pygame.display.flip()
        clock.tick(5)

    pygame.quit()


def draw_cell(screen: Surface, game: Game, r: int, c: int):
    cell = game.cell_at(r, c)
    if cell.is_alive():
        v = max(50, 200 - int(255 * math.pow(0.5, cell.age())))
        color = (v, v, v)
    else:
        color = (255, 255, 255)

    pygame.draw.rect(screen, color,
                     (r * RECT_W, c * RECT_H, RECT_W, RECT_H))


if __name__ == '__main__':
    main()
