from Mediator import Mediator
from Button import Button
from Screen import Screen


class VidgetMediator(Mediator):
    def __init__(self, pause_button: Button, screen: Screen, next_step_button: Button, clear_button: Button,
                 reset_button: Button):
        self._pause_button = pause_button
        self._pause_button.mediator = self
        self._screen = screen
        self._screen.mediator = self
        self._next_step_button = next_step_button
        self._next_step_button.mediator = self
        self._clear_button = clear_button
        self._clear_button.mediator = self
        self._reset_button = reset_button
        self._reset_button.mediator = self

    def notify(self, component):
        if component == self._pause_button:
            self._screen.change_play_mode()
            self._next_step_button.change_mode()
            self._clear_button.change_mode()
            self._reset_button.change_mode()

        if component == self._next_step_button:
            self._screen.get_new_step()

        if component == self._clear_button:
            self._screen.clear_screen()

        if component == self._reset_button:
            self._screen.set_start_generation()
