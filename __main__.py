from mouse import *
from Button import Button
from coords_cell import Coords, Cell
import pygame


class Display:
    def __init__(self, field, width, height, cell_size, fps):
        self.field = field
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.one_frame_delay = 1000 // fps
        self.background_color = (0, 0, 0)
        self.cell_color = (0, 0, 255)
        self.__timer = 0
        self.__offset = Coords(0, 0)
        self.__offset_direction = [False, Coords(0, 0)]
        self.__offset_speed = 0.4

    def __transform_coords(self, coords):
        for coord in coords:
            yield Coords(coord.x * self.cell_size + self.width / 2 + self.__offset.x,
                         self.height / 2 - (coord.y * self.cell_size) - self.__offset.y)

    def __current_frame_cells(self, clock):
        self.__timer += clock.tick()
        if self.__timer < self.one_frame_delay:
            coords = self.field.current_generation()
        else:
            coords = self.field.new_generation()
            self.__timer = 0
        return coords

    def __offset_check(self):
        bound_width = self.width // 15
        bound_height = self.height // 15
        coord = Coords(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        res = Coords(0, 0)
        if coord.x > self.width - bound_width:
            res.x = -1
        elif coord.x < bound_width:
            res.x = 1
        if coord.y < bound_height:
            res.y = -1
        elif coord.y > self.height - bound_height:
            res.y = 1
        if self.__offset_direction[0] and res == self.__offset_direction[1]:
            self.__offset_direction[0] = False
        else:
            self.__offset_direction = [True, res]

    def __calculate_offset(self, offset_clock):
        if self.__offset_direction[1] == Coords(0, 0):
            return
        if self.__offset_direction[0]:
            offset_clock.tick()
        else:
            distance = offset_clock.tick() * self.__offset_speed
            self.__offset.x += distance * self.__offset_direction[1].x
            self.__offset.y += distance * self.__offset_direction[1].y

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        update_clock = pygame.time.Clock()
        pygame.display.set_caption("LIFE")
        offset_clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(self.background_color)
            self.__offset_check()
            self.__calculate_offset(offset_clock)
            coords = self.__current_frame_cells(update_clock)

            for coord in self.__transform_coords(coords):  # оптимизировать?
                rect = pygame.Rect(coord.x, coord.y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.cell_color, rect, 0)
            pygame.display.flip()


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


button = Button(Coords(5, 5), (30, 39), "Dimina buttonka")
subscriber = Subscriber()

start_points = Coords(5, 5), Coords(6, 5), Coords(7, 5), Coords(7, 6), Coords(6, 7)
second = Display(Field(start_points), 700, 700, 10, 10)
second.draw()
