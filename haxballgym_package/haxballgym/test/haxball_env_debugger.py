import numpy as np
from haxballgym.environments.single_player_env import SinglePlayerEnvironment


def single_player_debug():
    env = SinglePlayerEnvironment()

    n_steps = 100

    for step in range(n_steps):
        env.render()
        move = input("move")
        print(env.step(np.array([move])))


if __name__ == "__main__":
    single_player_debug()
