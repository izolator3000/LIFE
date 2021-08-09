from Mediator import Mediator
from Button import Button
from enum import Enum


class HightEvents(Enum):
    Paused_botton = 1


class VidgetMediator(Mediator):
    def __init__(self, pause_button: Button, next_sptep: Button):
        self._vidgets = (pause_button, next_sptep)
        for elem in self._vidgets:
            elem.mediator = self

    def notify(self, component):
        index = self._vidgets.index(component)
        print(index)
