from enum import Enum
import pygame as pg
from coords_cell import Coords, Pair


class MouseEvents(Enum):
    KEY_PRESSED = 1
    KEY_REALISED = 2
    POSITION_CHANGED = 3
    FOCUS_GET = 4
    FOCUS_REALISED = 5


class Mouse:
    def __init__(self):
        self.subscribers = set()

    def subscribe(self, widget, mouse_event):
        self.subscribers.add(Pair(widget, mouse_event))
    
    def unsubscribe(self, widget, mouse_event):
        self.subscribers.remove(Pair(widget, mouse_event))
    
    def update(self, subscriber):
        if pg.mouse.get_focused():
            self.notify(MouseEvents.FOCUS_GET, Coords(*pg.mouse.get_pos()))
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:    #
                    self.notify(MouseEvents.KEY_PRESSED, Coords(*event.__dict__["pos"]))
                elif event.type == pg.MOUSEBUTTONUP:
                    self.notify(MouseEvents.KEY_REALISED, Coords(*event.__dict__["pos"]))
                elif event.type == pg.MOUSEMOTION:
                    self.notify(MouseEvents.POSITION_CHANGED, Coords(*event.__dict__["pos"]))
        else:
            self.notify(MouseEvents.FOCUS_REALISED, Coords(*pg.mouse.get_pos()))

    def notify(self, mouse_event: MouseEvents, position: Coords):
        for subscriber in self.subscribers:
            if subscriber.y == mouse_event:
                subscriber.update(position)

