import pygame
from collections import namedtuple
from random import randint, randrange

WIDTH, HEIGHT = 800, 800
FPS = 10    # Generation change rate
WHITE = 255, 255, 255   # Colors in RGB
GREEN = 0, 255, 0
BLACK = 0, 0, 0
BLUE = 0, 0, 255
RED = 255, 0, 0

Cell = namedtuple("Cell", "is_alive number_of_living_cells_around")
Coord = namedtuple("Coord", "x y")
living_cells = {Coord(randrange(0, WIDTH, 10), randrange(0, HEIGHT, 10)): Cell(True, 0)
                for _ in range(randint(3000, 5000))}    # Living cells
# living_cells = {Coord(x, y): Cell(True, 0) for x in range(300, 400, 10) for y in range(300, 400, 10)}  # Таракан
# living_cells = {
#     Coord(100, 400): Cell(True, 0),
#     Coord(110, 400): Cell(True, 0),
#     Coord(120, 400): Cell(True, 0),
#     Coord(120, 390): Cell(True, 0),
#     Coord(110, 380): Cell(True, 0),
# }


def new_living_cells(cells: dict):
    old_cells = cells.copy()
    for coord in old_cells:
        for i in (-10, 0, 10):
            for j in (-10, 0, 10):
                if not i == j == 0:
                    new_coord = Coord(coord.x + i, coord.y + j)
                    if new_coord in cells.keys():
                        cells[new_coord] = Cell(cells[new_coord].is_alive,
                                                cells[new_coord].number_of_living_cells_around + 1)
                    else:
                        cells[new_coord] = Cell(False, 1)

    old_cells = cells.copy()
    for cell in old_cells:
        if not old_cells[cell].is_alive and old_cells[cell].number_of_living_cells_around == 3:     # If cell death and there are 3 living cells around
            cells[cell] = Cell(True, 0)
        elif old_cells[cell].is_alive:
            if old_cells[cell].number_of_living_cells_around not in (2, 3):
                cells.pop(cell)
            else:
                cells[cell] = Cell(True, 0)
        elif not old_cells[cell].is_alive and old_cells[cell].number_of_living_cells_around != 3:
            cells.pop(cell)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LIFE")
clock = pygame.time.Clock()
screen.fill(WHITE)
pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # check for closing window
            running = False

    screen.fill(BLACK)
    for cell in living_cells:
        pygame.draw.rect(screen, GREEN, (cell.x, cell.y, 10, 10))
    pygame.display.flip()
    new_living_cells(living_cells)

    clock.tick(FPS)     # Держим цикл на правильной скорости

pygame.quit()
quit()
