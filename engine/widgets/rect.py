import pygame


class Rect:
    def __init__(self, coor, dim):
        self.bgcolor = pygame.Color("white")
        self.to_display = pygame.Rect(coor, dim)
        self.dimension = dim
        self.display = True
        self.parent = None

        # Text
        self.text = "Button"
        self.textColor = pygame.Color("black")
        self.text_size = 100  # percentage of the button rectangle height

        # Event binding need argument self to be used properly
        self.eventsBindings = {
                'onClick': None
                }

    def setBgColor(self, color):
        # color is a pygame.Color instance or a tuple containing RGB values
        if type(color) == pygame.Color:
            self.bgcolor = color
        else:
            self.bgcolor = pygame.Color(color)

    def setTextColor(self, color):
        # color is a pygame.Color instance or a tuple containing RGB values
        if type(color) == pygame.Color:
            self.textColor = color
        else:
            self.textColor = pygame.Color(color)

    def draw(self, win):  # window instance
        if self.display:
            pygame.draw.rect(win, self.bgcolor, self.to_display)
            ratio = (self.dimension[1] / 100) * self.text_size
            px_to_pt = 12 / 16
            button_text = pygame.font.SysFont("Arial", int(ratio * px_to_pt)).render(self.text, 1, self.textColor)
            win.blit(button_text, (self.to_display.x, self.to_display.y))

    def bind(self, event, func):
        if callable(func) and event in self.eventsBindings.keys():
            self.eventsBindings[event] = func

    def checkEvent(self, event, *args):
        if event == 'onClick' and self.to_display.collidepoint(args):
            if callable(self.eventsBindings[event]):
                self.eventsBindings[event](self, self.parent)


