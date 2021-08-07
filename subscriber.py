from zope.interface import Interface


class Subscriber(Interface):
    def __init__(self, *args):
        self.widget = {}

    def update(self, event, data):
        pass
