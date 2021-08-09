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
        for event in mouse_event:
            self.subscribers.add(Pair(widget, event))

    def unsubscribe(self, widget, mouse_event):
        self.subscribers.remove(Pair(widget, mouse_event))

    def update(self, event_queue):  # спорно
        for event in event_queue:
            if event.type == pg.ACTIVEEVENT:
                if not event.gain:
                    self._notify(MouseEvents.FOCUS_REALISED, Coords(-1, -1))
                else:
                    self._notify(MouseEvents.FOCUS_GET, Coords(-1, -1))
            if event.type == pg.MOUSEBUTTONDOWN:
                self._notify(MouseEvents.KEY_PRESSED, Coords(*event.pos))
            if event.type == pg.MOUSEBUTTONUP:
                self._notify(MouseEvents.KEY_REALISED, Coords(*event.pos))
            if event.type == pg.MOUSEMOTION:
                self._notify(MouseEvents.POSITION_CHANGED, Coords(*event.pos))

    def _notify(self, mouse_event: MouseEvents, position: Coords):
        data = (mouse_event, position)
        for subscriber in self.subscribers:
            if subscriber.y == mouse_event:
                subscriber.x.update(data)
