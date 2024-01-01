import numpy as np
from haxballgym.environments.single_player_env import SinglePlayerEnvironment


def single_player_debug():
    env = SinglePlayerEnvironment(max_steps=100, use_discrete_actionspace=True)

    n_steps = 100

    for step in range(n_steps):
        env.render()
        move = int(input("move"))
        print(move)
        print(env.step(move))


if __name__ == "__main__":
    single_player_debug()
