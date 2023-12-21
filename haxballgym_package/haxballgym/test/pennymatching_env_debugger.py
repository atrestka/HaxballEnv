import numpy as np
from haxballgym.environments.loaded_penny_matching_env import PennyMatchingLoadedOpponentEnv


def single_player_debug():
    env = PennyMatchingLoadedOpponentEnv(playing=0)

    n_steps = 100

    for step in range(n_steps):
        env.render()
        move = input("move")
        print(env.step(np.array([move])))


if __name__ == "__main__":
    single_player_debug()
