from engine import *
import numpy as np


class Grid(Widget):
    def __init__(self, dim, win):
        super().__init__()

        # Window
        self.window = win

        # Cells
        self.cell_dim = 100
        self.padding = 2
        self.cells_rows = int(((dim[0] - self.cell_dim) / self.cell_dim))
        self.cells_cols = int((dim[0] / self.cell_dim))

        # Matrix
        self.matrix_widg = None  # Initialized in setup method
        self.matrix_ai = None  # Initialized in setup method

        # Setup is done by maze setup method

    def updateMatrix(self):
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
        # Draw maze
        tmp_mat = []
        for cellx in range(self.cells_cols):  # cols
            tmp_row = []
            for celly in range(self.cells_rows):  # rows
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


def button_click_function(self, window):
    if self.bgcolor == pygame.Color('black'):
        self.bgcolor = pygame.Color('gray')
    else:
        self.bgcolor = pygame.Color('black')
    window.objects["maze"].grid.updateMatrix()

def keyboard_button_function(self, window, key): # key is char
    if key == 's':
        self.setBgColor('green')
    elif key == 'e':
        self.setBgColor('red')
    window.objects["maze"].grid.updateMatrix()