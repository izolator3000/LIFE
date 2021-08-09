from Button import Button
import pygame
from VidgetMediator import VidgetMediator
from coords_cell import Coords
from mouse import Mouse, MouseEvents

pygame.init()
screen = pygame.display.set_mode((800, 800))
running = True
controller = Mouse()

test = Button(text=("pause", "resume"))
test1 = Button(start=Coords(500, 500))
controller.subscribe(test, (MouseEvents.KEY_PRESSED, MouseEvents.KEY_REALISED, MouseEvents.FOCUS_REALISED,MouseEvents.FOCUS_GET))

LIFE = VidgetMediator(test, test1)

while running:
    events = pygame.event.get()
    controller.update(events)

    screen.fill((0, 0, 0))
    test.draw(screen)
    pygame.display.flip()
