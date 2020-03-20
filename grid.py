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
        self.state = None # Initialized in setup method: list = (row, col)
        self.start_point = None # Initialized when sim starts
        self.end_point = None   # Initialized when sim starts
        self.finish = False
        self.visited = [] # list containing tuples of coordinates of the cells already visited
        self.WALL_PENALTY = -2
        self.MOVE_PENALTY = 0.05
        self.VISITED_PENALTY = -0.05
        self.EXIT_FOUND = 20
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
                    self.state = [r, c]
                    self.start_point = [r, c]
                elif cell.bgcolor == pygame.Color("red"):
                    self.matrix_ai[r][c] = "E"
                    self.end_point = [r, c]

    def updateMatrixWidg(self):
        if self.window.objects["maze"].running:
            for r, row in enumerate(self.matrix_ai):
                for c, cell in enumerate(row):
                    if [r, c] == self.state:
                        self.matrix_widg[r][c].bgcolor = pygame.Color("blue")
                    else:
                        if cell == b'*':
                            self.matrix_widg[r][c].bgcolor = pygame.Color("gray")
                        elif cell == b'E':
                            self.matrix_widg[r][c].bgcolor = pygame.Color("red")
                        elif cell == b'S':
                            self.matrix_widg[r][c].bgcolor = pygame.Color("green")
                        else:
                            self.matrix_widg[r][c].bgcolor = pygame.Color("black")

    def clear(self):
        for row in self.matrix_widg:
            for cell in row:
                cell.setBgColor("black")

    def draw(self, win):
        self.updateMatrixWidg()
        for row in self.matrix_widg:
            for cell in row:
                cell.draw(win)

    def checkEvent(self, event, *args):
        for row in self.matrix_widg:
            for cell in row:
                cell.checkEvent(event, *args)

    def display_path(self, path):
        for r, row in enumerate(self.matrix_widg):
            for c, cell in enumerate(row):
                if self.matrix_ai[r][c] == b'E':
                    cell.bgcolor = pygame.Color("red")
                if [r, c] in path and self.matrix_ai[r][c] != b'S' and self.matrix_ai[r][c] != b'E':
                    cell.bgcolor = pygame.Color("blue")

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

    #
    #
    #
    # ENVIRONMENT METHODS ###################################
    #
    #
    #

    def reset(self):
        self.finish = False
        self.state = self.start_point.copy()
        self.visited = []

        return self.state.copy()

    def perform_action(self, action):

        if action == 0: # UP
            self.state[0] -= 1
        elif action == 1: # RIGHT
            self.state[1] += 1
        elif action == 2: # DOWN
            self.state[0] += 1
        elif action == 3: # LEFT
            self.state[1] -= 1

        return self.state

    def step(self, action):
        next_state, reward = self.state, self.MOVE_PENALTY # Initial values, need to be modified
        valid_actions = self.get_valid_actions()

        if action not in valid_actions:
            # Has been chosen an invalid action
            reward = self.WALL_PENALTY
        else:
            # PERFORM ACTION
            next_state = self.perform_action(action)

            if next_state == self.end_point:
                self.finish = True
                reward = self.EXIT_FOUND
            elif next_state in self.visited:
                reward = self.VISITED_PENALTY

            self.visited.append(next_state.copy())

        return next_state, reward, self.finish # next_state, reward, done(wheter the agent found the exit)

    def exist_start_point(self):
        for row in self.matrix_widg:
            for cell in row:
                if cell.bgcolor == pygame.Color("green"):
                    return True

        return False

    def exist_end_point(self):
        for row in self.matrix_widg:
            for cell in row:
                if cell.bgcolor == pygame.Color("red"):
                    return True

        return False

    def get_valid_actions(self):
        valid = self.possible_moves.copy()

        row = self.state[0]
        col = self.state[1]

        nrows = self.matrix_ai.shape[0]
        ncols = self.matrix_ai.shape[0]

        if row == 0 or (self.state[0] > 0 and self.matrix_ai[row - 1][col] == b"*"):
            valid.remove(0) # remove UP ACTION

        if row == nrows - 1 or (row < nrows - 1 and self.matrix_ai[row + 1, col] == b"*"):
            valid.remove(2) # remove DOWN ACTION

        if col == 0 or (col > 0 and self.matrix_ai[row, col - 1] == b"*"):
            valid.remove(3) # remove LEFT ACTION

        if col == ncols - 1 or (col < ncols - 1 and self.matrix_ai[row, col + 1] == b"*"):
            valid.remove(1) # remove RIGHT ACTION

        return valid


def button_click_function(self, window):
    if not window.objects["maze"].running:
        if self.bgcolor == pygame.Color('black'):
            self.bgcolor = pygame.Color('gray')
        else:
            self.bgcolor = pygame.Color('black')
        window.objects["maze"].grid.updateMatrixAi()

def keyboard_button_function(self, window, key): # key is char
    if not window.objects["maze"].running:
        if key == 's' and not window.objects["maze"].grid.exist_start_point():
            self.setBgColor('green')
        elif key == 'e' and not window.objects["maze"].grid.exist_end_point():
            self.setBgColor('red')
        window.objects["maze"].grid.updateMatrixAi()