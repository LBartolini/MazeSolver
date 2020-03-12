import pygame


class Button:
    def __init__(self, coor, dim):
        self.color = pygame.Color(255, 255, 255)
        self.to_display = pygame.Rect(coor, dim)
        self.dimension = dim

        # Text
        self.text = "Button"
        self.text_size = 100  # percentage of the button rectangle height

        self.eventsBindings = {
                'onClick': None
                              }

    def setColor(self, color):
        # color is a pygame.Color instance or a tuple containing RGB values
        if type(color) == pygame.Color:
            self.color = color
        else:
            self.color = pygame.Color(color)

    def draw(self, win):  # window instance
        pygame.draw.rect(win, self.color, self.to_display)
        ratio = (self.dimension[1] / 100) * self.text_size
        px_to_pt = 12 / 16
        button_text = pygame.font.SysFont("Arial", int(ratio * px_to_pt)).render(self.text, 1, pygame.Color("black"))
        win.blit(button_text, (self.to_display.x, self.to_display.y))
        # self.to_display = self.to_display.move(5, 5)

    def bind(self, event, func):
        if callable(func) and event in self.eventsBindings.keys():
            self.eventsBindings[event] = func

    def checkEvent(self, event, *args):
        if event == 'onClick' and self.to_display.collidepoint(args):
            if callable(self.eventsBindings[event]):
                self.eventsBindings[event]()


