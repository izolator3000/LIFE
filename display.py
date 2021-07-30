from coords_cell import Coords
import pygame


class Display:
    def __init__(self, field, width, height, cell_size, fps):
        self.field = field
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.one_frame_delay = int(1000 / fps)
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
        bound_width = int(self.width / 15)
        bound_height = int(self.height / 15)
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
