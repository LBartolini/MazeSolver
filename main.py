from maze import Maze
import time
import numpy as np
import pickle
from engine import MainLoop


def generate_Q_matrix(maze):

    q = np.zeros(maze.grid.matrix_ai.shape, dtype=np.ndarray)
    
    for r in range(q.shape[0]):
        for c in range(q.shape[1]):
            q[r][c] = np.zeros([1, 4])

    return q

def save_maze(maze, file_name):
    with open(f"saves/{file_name}_maze.pkl", 'wb') as f:
        pickle.dump(maze.grid.matrix_ai, f)

def save_agent(q, file_name):
    with open(f"saves/{file_name}_agent.pkl", 'wb') as f:
        pickle.dump(q, f)

def load_maze(maze, file_name):
    try:
        with open(f"saves/{file_name}_maze.pkl", "rb") as f:
            maze.grid.matrix_ai = pickle.load(f)
    except FileNotFoundError:
        print("File might not exist")

def load_agent(q, file_name):
    try:
        with open(f"saves/{file_name}_agent.pkl", "rb") as f:
            x = pickle.load(f)

    except FileNotFoundError:
        print("File might not exist!\n Exiting...")
        time.sleep(0.5)
        exit()

    return x

load_settings = { # Setting to load the program
        'filename_load' : "astronave",
        'filename_save' : "astronave",

        # SAVE / LOAD MAZE
        'LOAD_MAZE' : False,
        'SAVE_MAZE' : False,

        # SAVE / LOAD AGENT
        'LOAD_AGENT' : False,
        'CLEAR_AGENT_ON_RESTART' : False,
        'SAVE_AGENT' : False,
}

@MainLoop
def main():
    global maze, load_settings, Q

    if maze.running or maze.ready_loading:

        if load_settings['LOAD_MAZE'] and maze.ready_loading:
            load_maze(maze, load_settings['filename_load'])
            maze.grid.updateMatrixWidg(True)

        maze.ready_loading = False

        while not maze.running: time.sleep(0.01) # Waiting till the game starts

        if not load_settings['CLEAR_AGENT_ON_RESTART'] and Q is not None:
            pass
        else:
            if load_settings['LOAD_AGENT']:
                Q = load_agent(load_settings['filename_load'])
            else:
                Q = generate_Q_matrix(maze)

        gamma = 0.7
        CAP = 300
        EPOCHS = 100

        maze.grid.MOVE_PENALTY = -0.2
        maze.grid.VISITED_PENALTY = -0.5

        step_by_step = False
        verbose = False

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

                next_state, reward, done = maze.grid.step(action)

                Q[tuple(state)][0][action] = (reward + (gamma * np.max(Q[tuple(next_state)][0])))
                if verbose: print(f"State: {state}, Next state: {next_state}, Action: {action}, Pool: {Q[tuple(state)][0]} Reward: {reward}")

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
        if load_settings['SAVE_MAZE']:
            save_maze(maze, load_settings['filename_save'])

        if load_settings['SAVE_AGENT']:
            save_agent(Q, load_settings['filename_save'])

        maze.running = False
        load_settings['LOAD_MAZE'] = False

if __name__ == "__main__":
    maze = Maze("MazeSolver", (800, 900))
    maze.window.show_fps = True
    maze.window.fps_perc = 4
    maze.window.FPS_CAP = 60
    maze.start()

    Q = None
    main()


