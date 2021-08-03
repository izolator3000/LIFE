from enum import Enum
from subscriber import Subscriber


class MouseEvents(Enum):
    key_state = 1   #
    position = 0, 0
    focus = 0


class Mouse(Subscriber):
    focus_on_screen = True
    state = 1
    position = 0, 0
    subscribers = {}

    def update(self):
        """Обновление"""
        pass

    def subscribe(self, subscriber: Subscriber, event: MouseEvents):
        """"""
        pass

    def unsubscribe(self, subscriber: Subscriber, event: MouseEvents):
        """"""
        pass    #return True

    def notify(self, event: MouseEvents, data):
        """"""
        pass

