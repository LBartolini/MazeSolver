from engine import *


class Maze:
    '''
    Class that will generate the maze
    This is the environment of this program
    Maybe built in PyGame
    '''

    def __init__(self, title, dim):
        self.window = Window(title, dim, FPS_CAP=500)
        button = Button((100, 100), (110, 50))
        self.window.addWidget(button)

    def start(self):
        self.window.start()
