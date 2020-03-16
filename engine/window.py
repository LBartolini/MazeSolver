import pygame
import threading
import os
import sys
from engine.widgets import *


class Window:
    def __init__(self, title, dim, FPS_CAP=60):
        """
        :param title: Title of the Window
        :param dim: Dimension of the window (example 1920, 1080) as a list/tuple
        :param FPS_CAP: FPS cap of the game
        """

        # Window configuration attributes
        self.window = pygame.display.set_mode(dim)
        self.title = title
        self.dimension = dim
        self.background_color = (0, 0, 0)

        # fps related vars
        self.FPS_CAP = FPS_CAP
        self.clock = pygame.time.Clock()
        self.fps_perc = 7  # edit this to make fps counter bigger or smaller
        self.show_fps = False  # you can modify this in order to show FPS

        # Game attributes
        self.widgets = []
        self.objects = {}

    def drawFPS(self):
        if self.show_fps:
            fps = str(int(self.clock.get_fps()))
            ratio_fps = (self.dimension[1]/100) * self.fps_perc  # 7% default
            px_to_pt = 12/16
            fps_text = pygame.font.SysFont("Arial", int(ratio_fps*px_to_pt)).render(fps, 1, pygame.Color("violet"))
            self.window.blit(fps_text, (3, 3))
    
    def addWidget(self, widget):
        widget.parent = self
        self.widgets.append(widget)

    def addObject(self, obj, identifier):
        self.objects[identifier] = obj

    def start(self):
        th = threading.Thread(target=self.run, daemon=True)
        th.start()

    def drawWidgets(self):
        for widg in self.widgets:
            widg.draw(self.window)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for widg in self.widgets:
                    widg.checkEvent('onClick', pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                for widg in self.widgets:
                    widg.checkEvent('onKeyDown', event.key, pygame.mouse.get_pos())

    def run(self):
        pygame.init()
        pygame.display.set_caption(self.title)
        done = False
        while not done:
            #Clear the screen
            self.window.fill(self.background_color)

            # Draw
            self.drawWidgets()
            self.drawFPS()

            # Events
            self.checkEvents()

            # Screen update and fps cap
            pygame.display.update()
            self.clock.tick(self.FPS_CAP)

        pygame.quit()
