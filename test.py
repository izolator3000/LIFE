from Button import Button
import pygame
from VidgetMediator import VidgetMediator
from coords_cell import Coords, Pair
from mouse import Mouse, MouseEvents
from Screen import Screen

pygame.init()
display = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("LIFE")
running = True
controller = Mouse()

screen = Screen(Coords(300, 0), 900, 600, 10)
pause_button = Button(text=("play", "pause"))
clear_button = Button(start=Coords(50, 250), size=Pair(100, 50), text=("Clear", "Clear"),
                      pressed_color=(255, 0, 0, 100),
                      unpressed_color=(255, 255, 255, 255), font_size=15, font_color=(0, 0, 0, 255))
controller.subscribe(pause_button,
                     (MouseEvents.LEFT_KEY_PRESSED, MouseEvents.LEFT_KEY_REALISED, MouseEvents.FOCUS_REALISED))
controller.subscribe(clear_button,
                     (MouseEvents.LEFT_KEY_PRESSED, MouseEvents.LEFT_KEY_REALISED, MouseEvents.FOCUS_REALISED))

controller.subscribe(screen,
                     (MouseEvents.LEFT_KEY_PRESSED, MouseEvents.RIGHT_KEY_PRESSED, MouseEvents.LEFT_KEY_REALISED,
                      MouseEvents.RIGHT_KEY_REALISED, MouseEvents.FOCUS_REALISED, MouseEvents.FOCUS_GET,
                      MouseEvents.POSITION_CHANGED))
LIFE_controller = VidgetMediator(pause_button, clear_button, screen)

while running:
    events = pygame.event.get()
    if any(map(lambda x: x.type == pygame.QUIT, events)):
        running = False
    controller.update(events)

    display.fill((0, 255, 0))
    pause_button.draw(display)
    clear_button.draw(display)
    screen.draw(display)
    pygame.display.flip()

pygame.quit()
quit()
