from zope.interface import Interface


class Subscriber(Interface):
    def update(self):
        pass
