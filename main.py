from maze import Maze
from solver import Solver
import time
from engine import MainLoop

@MainLoop
def example():
    # PUT YOUR CODE HERE
    for r in range(5):
        for c in range(6):
            maze.grid.matrix_widg[r][c].setBgColor("blue")
    time.sleep(0.1)
    for r in range(5):
        for c in range(6):
            maze.grid.matrix_widg[r][c].setBgColor("green")
    time.sleep(0.1)

@MainLoop
def main():
    pass

if __name__ == "__main__":
    maze = Maze("MazeSolver", (600, 600))
    maze.start()
    maze.window.show_fps = True
    maze.window.FPS_CAP = 60
    main()


