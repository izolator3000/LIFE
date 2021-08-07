from coords_cell import Cell


class Field:
    def __init__(self, alive_cells_coords):
        self.__cells = {elem: Cell() for elem in alive_cells_coords}

    def new_generation(self):
        for coord in list(self.__cells.keys()):
            for neighbor in coord.neighbors():
                try:
                    self.__cells[neighbor].number_of_neighbors += 1
                except:
                    self.__cells[neighbor] = Cell(False, 1)

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

    def current_generation(self):
        return self.__cells.keys()
