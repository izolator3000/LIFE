from enum import Enum
import pygame as pg
from subscriber import Subscriber
from coords_cell import Coords


class MouseEvents(Enum):
    KEY_PRESSED = 1
    KEY_REALISED = 2
    POSITION_CHANGED = 3
    FOCUS_CHANGED = 4





class Mouse:
    def __init__(self):
        self.position = pg.mouse.get_pos()
        self.focus_on_screen = False
        self.event = MouseEvents
        self.position = 0, 0
        self.subscriber = Subscriber()
        self.events = pg.event

        self.width, self.height = 1, 2      # КАК ЭТИ ПАРАМЕТРЫ ЗДЕСЬ ПОЛУЧИТЬ?
    
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.subscriber.update("QUIT")  # Пусть останавливает игру
            elif event.type in (pg.MOUSEBUTTONDOWN, event.type == pg.MOUSEBUTTONUP):
                self.subscriber.update(event.type, Coords(*pg.mouse.get_pos()))     # Нажата. Пусть кнопка изменит цвет
            elif event.type == pg.MOUSEMOTION:
                x, y, result = *pg.mouse.get_pos(), Coords(0, 0)
                bound_width = self.width // 15
                bound_height = self.height // 15
                if x > self.width - bound_width:
                    result.x = -1
                elif x < bound_width:
                    result.x = 1
                if y < bound_height:
                    result.y = -1
                elif y > self.height - bound_height:
                    result.y = 1
                self.subscriber.update(event.type, result)












    def events(self):
        while 1:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    break
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.position = pg.mouse.get_pos()

                    if event.button == 1:  # Нажата ЛКМ
                        self.subscriber.update()
                    elif event.button == 2:  # Нажата ПКМ
                        pass
                    elif event.button == 4:  # Колёсико крутится вперёд
                        pass
                    elif event.button == 5:  # Колёсико крутится назад
                        pass
                    pg.display.update()
