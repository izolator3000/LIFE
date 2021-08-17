import sys
from enum import Enum

import pygame
import pygame as pg
from coords_cell import Coords, Pair


class MouseEvents(Enum):
    LEFT_KEY_PRESSED = 1
    RIGHT_KEY_PRESSED = 3
    WHEEL_MOVED_FORWARD = 4
    WHEEL_MOVED_BACKWARD = 5
    FOCUS_GET = 10
    FOCUS_REALISED = 7
    LEFT_KEY_REALISED = 6
    RIGHT_KEY_REALISED = 8
    POSITION_CHANGED = 9


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
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pg.ACTIVEEVENT:
                coords = Coords(*pg.mouse.get_pos())
                if not event.gain:
                    self._notify(MouseEvents.FOCUS_REALISED, coords)
                else:
                    self._notify(MouseEvents.FOCUS_GET, coords)
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button < 6:
                    self._notify(MouseEvents(event.button), Coords(*event.pos))
            if event.type == pg.MOUSEBUTTONUP:
                if event.button < 4:
                    self._notify(MouseEvents(event.button + 5), Coords(*event.pos))
            if event.type == pg.MOUSEMOTION:
                self._notify(MouseEvents.POSITION_CHANGED, Coords(*event.pos))

    def _notify(self, mouse_event: MouseEvents, position: Coords):
        data = (mouse_event, position)
        for subscriber in self.subscribers:
            if subscriber.y == mouse_event:
                subscriber.x.update(data)
