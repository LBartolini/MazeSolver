import pygame


class Label:
    def __init__(self, coor, dim, text):
        self.bgcolor = pygame.Color("white")
        self.to_display = pygame.Rect(coor, dim)
        self.dimension = dim
        self.display = True
        self.parent = None

        # Text
        self.text = "Label"
        self.textColor = pygame.Color("black")
        self.text_percentage = 100  # percentage of the button rectangle height
        self.text_size = None

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
            if self.text_size is not None and type(self.text_size == int):
                button_text = pygame.font.SysFont("Arial", self.text_size).render(self.text, 1, self.textColor)
            else:
                ratio = (self.dimension[1] / 100) * self.text_percentage
                px_to_pt = 12 / 16
                button_text = pygame.font.SysFont("Arial", int(ratio * px_to_pt)).render(self.text, 1, self.textColor)
            win.blit(button_text, (self.to_display.x, self.to_display.y))

    def checkEvent(self, event, *args):
        pass
