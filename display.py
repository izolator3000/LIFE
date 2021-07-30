import pygame
from coords_cell import Coords


class Display:
    def __init__(self, field, width, height, cell_size, fps):
        self.field = field
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.fps = fps
        self.background_color = 0, 0, 0
        self.cell_color = 30, 0, 255

    def __coords_for_drawing(self, coords):
        for coord in coords:
            yield Coords(self.width/2 + coord.x*self.cell_size, self.height/2 - coord.y*self.cell_size)

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("LIFE")
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(self.background_color)
            for coord in self.__coords_for_drawing(self.field.new_generation()):  # оптимизировать?
                rect = coord.x, coord.y, self.cell_size, self.cell_size
                pygame.draw.rect(screen, self.cell_color, rect)
            pygame.display.flip()
