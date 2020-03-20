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
        self.ready_loading = False

        # Grid
        self.grid = Grid(dim, self.window)

        # Event handler
        self.eventListener = EventListener()

        # Setup
        self.setup()

    def setup(self):
        # Grid setup
        self.window.addWidget(self.grid)
        self.grid.cell_maz_size = 15
        cellx, celly = self.grid.setup()

        # Draw Instuctions labels
        label1 = Label((0, (celly*self.grid.cell_dim)+100),
                       (self.window.dimension[1], self.grid.cell_dim),
                       "S start point, E end point,SPACE start simulation")
        label1.text_size = 25
        self.window.addWidget(label1)

        label2 = Label((0, (celly * self.grid.cell_dim) + 150),
                       (self.window.dimension[1], self.grid.cell_dim),
                       "C to clear the grid, M_Sx to build walls, L to load")
        label2.text_size = 25
        self.window.addWidget(label2)

        # Add event listener
        self.eventListener.bind('onKeyDown', function)
        self.window.addWidget(self.eventListener)

        # Add maze to objects
        self.window.addObject(self, self.id)

    def start(self):
        self.window.start()

# Function event listener

def function(self, win, key):
    if key == ' ' and not win.objects["maze"].running and win.objects["maze"].grid.exist_start_point() and win.objects["maze"].grid.exist_end_point():
        win.objects["maze"].grid.updateMatrixWidg()
        win.objects["maze"].running = True
    elif key == ' ' and win.objects["maze"].running:
        win.objects["maze"].grid.updateMatrixWidg()
        win.objects["maze"].running = False
    elif key == 'c' and not win.objects["maze"].running:
        win.objects["maze"].grid.clear()
        win.objects["maze"].grid.updateMatrixAi()
    elif key == 'l':
        win.objects["maze"].ready_loading = not win.objects["maze"].ready_loading



