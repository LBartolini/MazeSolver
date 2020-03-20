from maze import Maze
import time
import numpy as np
from engine import MainLoop


def generate_Q_matrix(maze):

    q = np.zeros(maze.grid.matrix_ai.shape, dtype=np.ndarray)
    
    for r in range(q.shape[0]):
        for c in range(q.shape[1]):
            q[r][c] = np.zeros([1, 4])

    return q

def save_maze(maze, file_name):
    with open(f"/saves/{file_name}.txt", "wb") as f:
        # TODO save the maze
        pass


@MainLoop
def main():
    global maze

    if maze.running:
        Q = generate_Q_matrix(maze)
        gamma = 0.6
        CAP = 300
        EPOCHS = 100

        step_by_step = False
        verbose = False
        save_on_exit = False

        for episode in range(1, EPOCHS+1):
            time.sleep(0.001)
            print("EPISODE :", episode)

            state, done = (0, 0), False
            counter = 0

            state = maze.grid.reset()
            path = []

            while not done and counter < CAP and maze.running:
                time.sleep(0.001)
                counter += 1
                action = np.argmax(Q[tuple(state)][0]) # 0 = UP, 1 = RIGHT, 2 = DOWN, 3 = LEFT

                if verbose: print(action, Q[tuple(state)][0], np.max(Q[tuple(state)][0]), max(Q[tuple(state)][0]))

                next_state, reward, done = maze.grid.step(action)

                Q[tuple(state)][0][action] = (reward + (gamma * np.max(Q[tuple(next_state)][0])))
                if verbose: print(f"State: {state}, Next state: {next_state}, Action: {action}, Reward: {reward}")

                state = next_state.copy()

                if episode == EPOCHS:
                    path.append(state.copy())

                maze.grid.updateMatrixWidg()

                if step_by_step: input()

            if verbose:
                if done:
                    print("OK")
                else:
                    print("NO")

        maze.grid.display_path(path)
        if save_on_exit: save_maze(maze, "prova")
        maze.running = False

if __name__ == "__main__":
    maze = Maze("MazeSolver", (800, 900))
    maze.window.show_fps = True
    maze.window.fps_perc = 4
    maze.window.FPS_CAP = 60
    maze.start()
    main()


