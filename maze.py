from engine import *
from grid import Grid


class Maze:
    '''
    Class that will generate the maze
    This is the environment of this program
    Maybe built in PyGame
    '''

    def __init__(self, title, dim):
        self.window = Window(title, dim, FPS_CAP=60)
        self.window.background_color = pygame.Color('white')
        self.id = "maze"
        self.running = False

        # Grid
        self.grid = Grid(dim, self.window)

        # Event handler
        self.eventListener = EventListener()

        # Setup
        self.setup()

    def setup(self):
        # Grid setup
        self.window.addWidget(self.grid)
        cellx, celly = self.grid.setup()

        # Draw Instuctions labels
        label1 = Label((0, (celly*self.grid.cell_dim)+self.grid.cell_dim),
                       (self.window.dimension[1], self.grid.cell_dim),
                       "S start point, E end point,SPACE start simulation")
        label1.text_size = 25
        self.window.addWidget(label1)

        label2 = Label((0, (celly * self.grid.cell_dim) + self.grid.cell_dim + 30),
                       (self.window.dimension[1], self.grid.cell_dim),
                       "C to clear the grid")
        label2.text_size = 25
        self.window.addWidget(label2)

        # Add event listener
        self.eventListener.bind('onKeyDown', function)
        self.window.addWidget(self.eventListener)

        # Add maze to objects
        self.window.addObject(self, self.id)

    def start(self):
        self.window.start()


def function(self, win, key):
    if key == ' ' and not win.objects["maze"].running:
        win.objects["maze"].running = True
    elif key == ' ' and win.objects["maze"].running:
        win.objects["maze"].running = False
    elif key == 'c':
        win.objects["maze"].grid.clear()


