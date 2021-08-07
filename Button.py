import pygame as pg
from coords_cell import Coords, Pair
from mouse import MouseEvents


"""
Code Review: Button
1) Установить дефолтные значения цветам и шрифту
2) Заменить size на height и width
3) update метод странный
"""


class Button:
    def __init__(self, start: Coords, size=Pair(40, 40), text="Button", pressed_color=(50, 100, 200), unpressed_color=(200, 10, 250),
                 font_size=20, font_color=(10, 10, 10)):
        if not pg.font.get_init():
            pg.font.init()
        self.__font = pg.font.Font(None, font_size)  # шрифт и его размер

        if self.__font.size(text)[0] > size.x or self.__font.size(text)[1] > size.y:  # исправить
            raise Exception  # исправить
        self.__text = text
        self.__start = start
        self.__size = size  # (width,height)
        self.__pressed_color = pressed_color
        self.__unpressed_color = unpressed_color
        self.__font_color = font_color
        self.__state = 0

    def __cursor_on_button(self, position) -> bool:
        return self.__start.x < position.x < self.__start.x + self.__size.x and \
               self.__start.y < position.y < self.__start.y + self.__size.y

    def update(self, data: tuple):
        position = data[1]

        if data[0] == MouseEvents.KEY_PRESSED:
            if self.__cursor_on_button(position):
                self.__state = 1

        else:
            if self.__cursor_on_button(position):
                if self.__state == 1:
                    self.click()
            self.__state = 0

    def __calculate_text_position(self) -> Coords:
        text_height, text_width = self.__font.size(self.__text)
        offset_x = (self.__size.x - text_height) // 2
        offset_y = (self.__size.y - text_width) // 2
        return Coords(self.__start.x + offset_x, self.__start.y + offset_y)

    def draw(self, screen: pg.Surface):
        if self.__state == 0:
            active_color = self.__unpressed_color
        else:
            active_color = self.__pressed_color
        button_rect = pg.Rect(self.__start.x, self.__start.y, self.__size.x, self.__size.y)
        text_image = self.__font.render(self.__text, True, self.__font_color)
        text_position = self.__calculate_text_position()
        pg.draw.rect(screen, active_color, button_rect, 0)
        screen.blit(text_image, (text_position.x, text_position.y))

    def click(self):
        print("Clicked")
