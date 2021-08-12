from coords_cell import Cell, Coords


class Field:
    def __init__(self):
        self.__cells = {}  # ключи-координаты,значения-клетки

    def new_generation(self):
        for coord in list(self.__cells.keys()):
            for coord in coord.neighbors():  # ???
                try:
                    self.__cells[coord].number_of_neighbors += 1
                except:
                    self.__cells[coord] = Cell(False, 1)

        for coord in list(self.__cells.keys()):
            current_cell = self.__cells[coord]
            if current_cell.is_alive:
                if current_cell.number_of_neighbors not in (2, 3):
                    del self.__cells[coord]
                else:
                    self.__cells[coord].reset()
            else:
                if current_cell.number_of_neighbors != 3:
                    del self.__cells[coord]
                else:
                    self.__cells[coord].reset()
        return self.__cells.keys()

    def add_alive_cell(self, coords: Coords):
        self.__cells[coords] = Cell()

    def del_alive_cell(self, coords: Coords):
        try:
            del self.__cells[coords]  # добавить пользовательское исключение
        except:
            pass

    def current_generation(self):
        return self.__cells.keys()
