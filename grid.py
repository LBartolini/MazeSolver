from engine import *
import numpy as np


class Grid(Widget):
    def __init__(self, dim, win):
        super().__init__()

        # Window
        self.window = win

        # Cells
        self.cell_dim = 50
        self.cell_maz_size = None
        self.padding = 2

        try:
            self.cells = int((dim[0] / self.cell_dim) - ((dim[0]  % self.cell_dim)/(dim[0]  % self.cell_dim)))
        except ZeroDivisionError:
            self.cells = int((dim[0] / self.cell_dim))

        # Matrix
        self.matrix_widg = None  # Initialized in setup method

        # Environment
        self.matrix_ai = None  # Initialized in setup method
        self.state = None # Initialized in setup method: tuple = (row, col, won/not won)
        self.visited = [] # list containing tuples of coordinates of the cells already visited
        self.WALL_PENALTY = -1
        self.MOVE_PENALTY = 0
        self.VISITED_PENALTY = -0.25
        self.EXIT_FOUND = 10
        self.possible_moves = [0, 1, 2, 3] # 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT

        # Setup is done by maze setup method

    def updateMatrixAi(self):
        for r, row in enumerate(self.matrix_widg):
            for c, cell in enumerate(row):
                if cell.bgcolor == pygame.Color("black"):
                    self.matrix_ai[r][c] = " "
                elif cell.bgcolor == pygame.Color("gray"):
                    self.matrix_ai[r][c] = "*"
                elif cell.bgcolor == pygame.Color("green"):
                    self.matrix_ai[r][c] = "S"
                elif cell.bgcolor == pygame.Color("red"):
                    self.matrix_ai[r][c] = "E"

    def updateMatrixWidg(self):
        for r, row in enumerate(self.matrix_ai):
            for c, cell in enumerate(row):
                if cell == "P": # P stands for Player
                   self.matrix_widg[r][c].bgcolor = pygame.Color("blue")

    def clear(self):
        for row in self.matrix_widg:
            for cell in row:
                cell.setBgColor("black")

    def draw(self, win):
        for row in self.matrix_widg:
            for cell in row:
                cell.draw(win)

    def checkEvent(self, event, *args):
        for row in self.matrix_widg:
            for cell in row:
                cell.checkEvent(event, *args)

    def setup(self):
        # Setup grid size
        if self.cell_maz_size is not None and self.cells > self.cell_maz_size:
            self.cells = self.cell_maz_size

        # Draw maze
        tmp_mat = []
        for cellx in range(self.cells):  # cols
            tmp_row = []
            for celly in range(self.cells):  # rows
                pos_x = (cellx * self.cell_dim) + cellx * self.padding
                pos_y = (celly * self.cell_dim) + celly * self.padding
                rect = Rect((pos_x, pos_y), (self.cell_dim, self.cell_dim))
                rect.parent = self.parent
                rect.text = ""
                rect.setBgColor('black')
                rect.bind('onClick', button_click_function)
                rect.bind('onKeyDown', keyboard_button_function)
                tmp_row.append(rect)

            tmp_mat.append(tmp_row)


        self.matrix_widg = np.asarray(tmp_mat, dtype=Rect)
        self.matrix_widg = np.transpose(self.matrix_widg)  # match the real size 5 rows and 6 cols

        # Init matrix
        self.matrix_ai = np.chararray(self.matrix_widg.shape)
        self.matrix_ai.fill("")

        return cellx, celly

    # ENVIRONMENT METHODS

    def get_valid_actions(self):
        valid = self.possible_moves.copy()

        if self.state[0] == 0 or (self.state[0] > 0 and self.matrix_ai[row - 1][col] == "*"):
            valid.remove(0) # remove UP ACTION

        # TODO remove other actions


def button_click_function(self, window):
    if not window.objects["maze"].running:
        if self.bgcolor == pygame.Color('black'):
            self.bgcolor = pygame.Color('gray')
        else:
            self.bgcolor = pygame.Color('black')
        window.objects["maze"].grid.updateMatrixAi()

def keyboard_button_function(self, window, key): # key is char
    if not window.objects["maze"].running:
        if key == 's':
            self.setBgColor('green')
        elif key == 'e':
            self.setBgColor('red')
        window.objects["maze"].grid.updateMatrixAi()