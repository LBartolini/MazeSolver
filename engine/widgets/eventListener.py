import pygame
from engine.widgets.widget import Widget


class EventListener(Widget):
    def __init__(self):
        super().__init__()
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
                self.eventsBindings[event](self, self.parent, chr(args[0]))
