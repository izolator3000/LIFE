from enum import Enum
from subscriber import Subscriber


class MouseEvents(Enum):
    key_state = 1
    position = 0, 0
    focus = 0


class Mouse(Subscriber):
    focus_on_screen = True
    state = 1
    position = 0, 0
    subscribers = {}
