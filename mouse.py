from enum import Enum
import pygame as pg
from coords_cell import Coords, Pair


class MouseEvents(Enum):
    KEY_PRESSED = 1
    KEY_REALISED = 2
    POSITION_CHANGED = 3
    FOCUS_CHANGED = 4


class Mouse:
    def __init__(self):
        self.mouse_events = MouseEvents
        self.subscribers = set()

    def subscribe(self, widget, mouse_event):
        self.subscribers.add(Pair(widget, mouse_event))
    
    def unsubscribe(self, widget, mouse_event):
        self.subscribers.remove(Pair(widget, mouse_event))
    
    def update(self, subscriber):
        if pg.mouse.get_focused():
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    subscriber.update(self.mouse_events.KEY_PRESSED, Coords(*pg.mouse.get_pos()))
                elif event.type == pg.MOUSEBUTTONUP:
                    subscriber.update(self.mouse_events.KEY_REALISED, Coords(*pg.mouse.get_pos()))
                elif event.type == pg.MOUSEMOTION:
                    subscriber.update(self.mouse_events.POSITION_CHANGED, Coords(*pg.mouse.get_pos()))
        else:
            subscriber.update(self.mouse_events.FOCUS_CHANGED, Coords(*pg.mouse.get_pos()))
