from Mediator import Mediator
from Button import Button
from Screen import Screen


class VidgetMediator(Mediator):
    def __init__(self, pause_button: Button, clear_button: Button, live_back_button: Button, screen: Screen):
        self._pause_button = pause_button
        self._pause_button.mediator = self
        self._screen = screen
        self._screen.mediator = self
        self._clear_button = clear_button
        self._clear_button.mediator = self
        self._live_back_button = live_back_button
        self._live_back_button.mediator = self

    def notify(self, component):
        if component == self._pause_button:
            self._screen.change_play_mode()
        elif component == self._clear_button:
            self._screen.reset()
        elif component == self._live_back_button:
            self._screen.reverse_game()
