import pygame
from abc import abstractmethod


class Component:
    def __init__(self):
        self._mediator = None

    @property
    def mediator(self):
        if self._mediator is None:
            raise Exception
        return self._mediator

    @mediator.setter
    def mediator(self, value):
        self._mediator = value

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
