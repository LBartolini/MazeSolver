from engine import *


class Maze:
    '''
    Class that will generate the maze
    This is the environment of this program
    Maybe built in PyGame
    '''

    def __init__(self, title, dim):
        self.window = Window(title, dim, FPS_CAP=60)
        self.window.background_color = pygame.Color('white')

        # Cells
        self.cell_dim = 100
        self.padding = 2
        self.cells_rows = int(((dim[0]-self.cell_dim) / self.cell_dim))
        self.cells_cols = int((dim[0] / self.cell_dim))

        # Setup
        self.setup()

    def setup(self):
        # Draw maze
        for cellx in range(self.cells_cols):  # cols
            for celly in range(self.cells_rows):  # rows
                pos_x = (cellx*self.cell_dim) + cellx*self.padding
                pos_y = (celly*self.cell_dim) + celly*self.padding
                rect = Rect((pos_x, pos_y), (self.cell_dim, self.cell_dim))
                rect.text = ""
                rect.setBgColor('black')
                rect.bind('onClick', cell_func)
                self.window.addWidget(rect)

        # Draw Instuctions label
        label = Label((0, (celly*self.cell_dim)+self.cell_dim), (self.window.dimension[1], self.cell_dim), "prova")
        self.window.addWidget(label)

    def start(self):
        self.window.start()


def cell_func(self, window):
    if self.bgcolor == pygame.Color('black'):
        self.bgcolor = pygame.Color('gray')
    else:
        self.bgcolor = pygame.Color('black')
