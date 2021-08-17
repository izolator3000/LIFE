from Component import Component
from Mediator import Mediator


class Bar(Component, Subscriber):
    def __init__(self, start=Coords(50, 450), height=100, weight=50, text="Bar"):
        super().__init__()
        self.font = pygame.font.Font(None, 18)
        self.label = font.render(text, 30, (0, 0, 250))

    def draw(self):
        display.blit(label, (100, 100))

    def update(self):
        pass
