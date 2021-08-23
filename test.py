from Button import Button
import pygame
from VidgetMediator import VidgetMediator
from coords_cell import Coords, Pair
from mouse import Mouse, MouseEvents
from Screen import Screen

pygame.init()
display = pygame.display.set_mode((1200, 600))
running = True
controller = Mouse()

screen = Screen(Coords(600, 0), 600, 600, 16)
pause_botton = Button(text=("play", "pause"))
next_step_button = Button(text=("next step",), start=Pair(50, 150))
clear_button = Button(text=("clear",), start=Pair(50, 250))
reset_button = Button(text=("reset",), start=Pair(200, 50), turned_on=False)
button_events = (MouseEvents.LEFT_KEY_PRESSED, MouseEvents.LEFT_KEY_REALISED, MouseEvents.FOCUS_REALISED)
controller.subscribe(pause_botton, button_events)
controller.subscribe(next_step_button, button_events)
controller.subscribe(clear_button, button_events)
controller.subscribe(reset_button, button_events)

controller.subscribe(screen,
                     (MouseEvents.LEFT_KEY_PRESSED, MouseEvents.RIGHT_KEY_PRESSED, MouseEvents.LEFT_KEY_REALISED,
                      MouseEvents.RIGHT_KEY_REALISED, MouseEvents.FOCUS_REALISED, MouseEvents.FOCUS_GET,
                      MouseEvents.POSITION_CHANGED, MouseEvents.WHEEL_MOVED_FORWARD, MouseEvents.WHEEL_MOVED_BACKWARD))
LIFE_controller = VidgetMediator(pause_botton, screen, next_step_button, clear_button, reset_button)

while running:
    events = pygame.event.get()
    controller.update(events)

    display.fill((0, 255, 0))
    pause_botton.draw(display)
    next_step_button.draw(display)
    clear_button.draw(display)
    reset_button.draw(display)
    screen.draw(display)
    pygame.display.flip()
