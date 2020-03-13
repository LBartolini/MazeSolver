import pygame


class EventListener:
    def __init__(self):
        # Window pointer
        self.parent = None

        # Event binding need argument self to be used properly
        self.eventsBindings = {
            'onClick': None,
            'onKeyDown': None,
        }

    def bind(self, event, func):
        if callable(func) and event in self.eventsBindings.keys():
            self.eventsBindings[event] = func

    def checkEvent(self, event, *args):
        if event == 'onClick':
            if callable(self.eventsBindings[event]):
                self.eventsBindings[event](self, self.parent)
        elif event == 'onKeyDown':
            if callable(self.eventsBindings[event]):
                self.eventsBindings[event](self, self.parent)

    def draw(self, win):
        # This method is here just for the window code which calls this function on every widget
        pass