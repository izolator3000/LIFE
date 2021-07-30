

import pygame


class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({str(self.x)}, {str(self.y)})"

    def get_neighbors(self):
        x, y = self.x, self.y
        return (Coords(x - 1, y + 1), Coords(x, y + 1), Coords(x + 1, y + 1), Coords(x + 1, y), Coords(x + 1, y - 1),
                Coords(x, y - 1), Coords(x - 1, y - 1), Coords(x - 1, y))


class Cell:

    def __init__(self, is_alive, alive_neighbors_count):
        self.is_alive = is_alive
        self.alive_neighbors_count = alive_neighbors_count

    def __repr__(self):
        return str(self.is_alive) + ' ' + str(self.alive_neighbors_count)


class Field:
    # словарь белых клеток
    def __init__(self, alive_cells_coords):
        self.__cells = {}
        for elem in alive_cells_coords:
            self.__cells[elem] = Cell(True, 0)

    def __next_step(self):
        alive_cells_coords = list(self.__cells.keys())
        for coord in alive_cells_coords:
            neighbors = coord.get_neighbors()
            for coord in neighbors:
                try:
                    self.__cells[coord].alive_neighbors_count += 1
                except:
                    self.__cells[coord] = Cell(False, 1)

        all_cells = list(self.__cells.keys())
        for coord in all_cells:
            current_cell = self.__cells[coord]
            if current_cell.is_alive:

                if current_cell.alive_neighbors_count < 2 or current_cell.alive_neighbors_count > 3:
                    del self.__cells[coord]
                else:
                    self.__cells[coord].alive_neighbors_count = 0
            else:
                if current_cell.alive_neighbors_count != 3:
                    del self.__cells[coord]
                else:
                    self.__cells[coord].is_alive = True
                    self.__cells[coord].alive_neighbors_count = 0

    def get_new_generation(self):
        self.__next_step()
        return self.__cells.keys()


class DField:

    def __init__(self, field, width, height, cell_size, fps):
        self.field = field
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.fps = fps
        self.background_color = (0, 0, 0)
        self.cell_color = (0, 0, 255)

    def __transform_coords(self, coords):
        outptut = []
        for coord in coords:
            outptut.append(
                Coords(coord.x * self.cell_size + self.width / 2, self.height / 2 - (coord.y * self.cell_size)))
        return outptut

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            screen.fill(self.background_color)
            for coord in self.__transform_coords(self.field.get_new_generation()):  # оптимизировать?
                rect = pygame.Rect(coord.x, coord.y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.cell_color, rect, 0)
            pygame.display.flip()


first = Field([Coords(5, 5), Coords(6, 5), Coords(7, 5),Coords(7,6),Coords(6,7)])
second=DField(first,700,700,10,10)
second.draw()
