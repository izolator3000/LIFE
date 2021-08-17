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
controller.subscribe(pause_botton,
                     (MouseEvents.LEFT_KEY_PRESSED, MouseEvents.LEFT_KEY_REALISED, MouseEvents.FOCUS_REALISED))

controller.subscribe(screen,
                     (MouseEvents.LEFT_KEY_PRESSED, MouseEvents.RIGHT_KEY_PRESSED, MouseEvents.LEFT_KEY_REALISED,
                      MouseEvents.RIGHT_KEY_REALISED, MouseEvents.FOCUS_REALISED, MouseEvents.FOCUS_GET,
                      MouseEvents.POSITION_CHANGED,MouseEvents.WHEEL_MOVED_FORWARD,MouseEvents.WHEEL_MOVED_BACKWARD))
LIFE_controller = VidgetMediator(pause_botton, screen)

while running:
    events = pygame.event.get()
    controller.update(events)

    display.fill((0, 255, 0))
    pause_botton.draw(display)
    screen.draw(display)
    pygame.display.flip()
