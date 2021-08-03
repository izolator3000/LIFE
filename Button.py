import pygame
from coords_cell import Coords,Pair
from enum import Enum


class Mouse_events(Enum):  # временно
    KEY_PRESSED = 1
    KEY_REALISED = 2
    POSITION_CHANGED = 3
    FOCUS_CHANGED = 4


class Button:
    def __init__(self, start: Coords, size: Pair, text: str, pressed_color: tuple, unpressed_color: tuple,
                 font_size: int, font_color: tuple):
        if not pygame.font.get_init():
            pygame.font.init()
        self.__font = pygame.font.Font(None, font_size)  # шрифт и его размер

        if self.__font.size(text)[0] > size.x or self.__font.size(text)[1] > size.y:  # исправить
            raise Exception  # исправить
        self.__text = text
        self.__start = start
        self.__size = size  # (width,height)
        self.__pressed_color = pressed_color
        self.__unpressed_color = unpressed_color
        self.__font_color = font_color
        self.__state = 0

    def __cursor_on_botton(self, position):
        if position.x < self.__start.x or position.x > self.__start.x + self.__size.x:
            return False
        if position.y < self.__start.y or position.y > self.__start.y + self.__size.y:
            return False
        return True

    def update(self, data: tuple):
        position = data[1]

        if data[0] == Mouse_events.KEY_PRESSED:
            if self.__cursor_on_botton(position):
                self.__state = 1

        else:
            if self.__cursor_on_botton(position):
                if self.__state == 1:
                    self.click()
            self.__state = 0

    def __calculate_text_position(self):
        text_size = self.__font.size(self.__text)
        offset_x = int((self.__size.x - text_size[0]) / 2)
        offset_y = int((self.__size.y - text_size[1]) / 2)
        return Coords(self.__start.x + offset_x, self.__start.y + offset_y)

    def draw(self, screen: pygame.Surface):
        if self.__state == 0:
            active_color = self.__unpressed_color
        else:
            active_color = self.__pressed_color
        button_rect = pygame.Rect(self.__start.x, self.__start.y, self.__size.x, self.__size.y)
        text_image = self.__font.render(self.__text, True, self.__font_color)
        text_position = self.__calculate_text_position()
        pygame.draw.rect(screen, active_color, button_rect, 0)
        screen.blit(text_image, (text_position.x, text_position.y))

        pass

    def click(self):
        print("Clicked")
        pass


pass
