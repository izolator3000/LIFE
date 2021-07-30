from coords_cell import Coords
from field import Field
from display import Display

first = Field([Coords(5, 5), Coords(6, 5), Coords(7, 5), Coords(7, 6), Coords(6, 7)])
second = Display(first, 700, 700, 10, 10)
second.draw()
