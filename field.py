from coords_cell import Cell, Coords
from collections import deque


class Field:
    def __init__(self):
        self._cells = {}  # ключи-координаты,значения-клетки
        self._old_generations = deque([self._cells], maxlen=1000)
        self._live_forward = True

    def next_generation(self):
        if self._live_forward:
            return self._new_generation()
        return self._old_generation()

    def _old_generation(self):
        try:
            self._cells = self._old_generations.pop()
        except IndexError:
            self._cells = {Coords(5, 8): Cell(True, 0),
                           Coords(6, 8): Cell(True, 0),
                           Coords(7, 8): Cell(True, 0),
                           Coords(7, 7): Cell(True, 0),
                           Coords(6, 6): Cell(True, 0)}
            self._old_generations.append(self._cells)
        return self._cells

    def _new_generation(self):
        for coord in list(self._cells.keys()):
            for neighbor in coord.neighbors():  # ???
                try:
                    self._cells[neighbor].number_of_neighbors += 1
                except KeyError:
                    self._cells[neighbor] = Cell(False, 1)

        for coord in list(self._cells):
            current_cell = self._cells[coord]
            if current_cell.is_alive:
                if current_cell.number_of_neighbors not in (2, 3):
                    del self._cells[coord]
                else:
                    self._cells[coord].reset()
            else:
                if current_cell.number_of_neighbors != 3:
                    del self._cells[coord]
                else:
                    self._cells[coord].reset()
        self._old_generations.append(self._cells.copy())
        return self._cells

    def add_alive_cell(self, coords: Coords):
        self._cells[coords] = Cell()

    def del_alive_cell(self, coords: Coords):
        try:
            del self._cells[coords]  # добавить пользовательское исключение
        except KeyError:
            pass

    def current_generation(self):
        return self._cells.keys()

    def clear(self):
        self._cells.clear()

    def reverse_game(self):
        self._live_forward = not self._live_forward
