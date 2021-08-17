from coords_cell import Coords, Pair
from Component import Component
from Subscriber import Subscriber
from mouse import MouseEvents
import pygame


# добавить возможность включать и отключать кнопки


class Button(Component, Subscriber):
    def __init__(self, start=Coords(50, 50), size=Pair(100, 50), text=("Button"), pressed_color=(255, 0, 0, 100),
                 unpressed_color=(255, 255, 255, 255), font_size=15, font_color=(0, 0, 0, 255)):

        super().__init__()
        if not pygame.font.get_init():
            pygame.font.init()
        self._font = pygame.font.Font(None, font_size)  # шрифт и его размер

        for title in text:
            if self._font.size(title)[0] > size.x or self._font.size(title)[1] > size.y:  # исправить
                raise Exception  # исправить

        self._text = text
        self._text_index = 0
        self._start = start
        self._size = size  # (width,height)
        self._pressed_color = pressed_color
        self._unpressed_color = unpressed_color
        self._font_color = font_color
        self._state = 0

    def _cursor_on_button(self, position):
        if position.x < self._start.x or position.x > self._start.x + self._size.x:
            return False
        if position.y < self._start.y or position.y > self._start.y + self._size.y:
            return False
        return True

    def turn_off(self):

        pass

    def turn_on(self):
        pass

    def update(self, data: tuple): #левая кнопка мыши нажата/отпущена,фокус потерян
        if data[0] == MouseEvents.FOCUS_REALISED:
            self._state = 0
            return

        position = data[1]  # первый элемент-тип события,второй элемент-пара координат

        if data[0] == MouseEvents.LEFT_KEY_PRESSED:
            if self._cursor_on_button(position):
                self._state = 1
        else:
            if self._cursor_on_button(position):
                if self._state == 1:
                    self.click()
                    self._text_index += 1
                    if self._text_index > len(self._text) - 1:
                        self._text_index = 0
            self._state = 0

    def _calculate_text_position(self):
        text_size = self._font.size(self._text[self._text_index])
        offset_x = int((self._size.x - text_size[0]) / 2)
        offset_y = int((self._size.y - text_size[1]) / 2)
        return Coords(self._start.x + offset_x, self._start.y + offset_y)

    def draw(self, screen: pygame.Surface):
        if self._state == 0:
            active_color = self._unpressed_color
        else:
            active_color = self._pressed_color
        button_rect = pygame.Rect(self._start.x, self._start.y, self._size.x, self._size.y)
        text_image = self._font.render(self._text[self._text_index], True, self._font_color)
        text_position = self._calculate_text_position()
        pygame.draw.rect(screen, active_color, button_rect, 0)
        screen.blit(text_image, (text_position.x, text_position.y))

    def click(self):

        self.mediator.notify(self)
