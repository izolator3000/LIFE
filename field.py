from coords_cell import Cell


class Field:
    def __init__(self, alive_cells_coords):
        self.__cells = {elem: Cell() for elem in alive_cells_coords}

    def __next_step(self):
        for coord in list(self.__cells.keys()):
            for coord in coord.neighbors():
                try:
                    self.__cells[coord].number_of_neighbors += 1
                except:
                    self.__cells[coord] = Cell(False, 1)

        for coord in list(self.__cells.keys()):
            current_cell = self.__cells[coord]
            if current_cell.is_alive:
                if current_cell.number_of_neighbors < 2 or current_cell.number_of_neighbors > 3:
                    del self.__cells[coord]
                else:
                    self.__cells[coord].reset()
            else:
                if current_cell.number_of_neighbors != 3:
                    del self.__cells[coord]
                else:
                    self.__cells[coord].reset()
        
    def new_generation(self):
        self.__next_step()
        return self.__cells.keys()

    def current_generation(self):
        return self.__cells.keys()
