import numpy as np
import haxballgym
from haxballgym.environments.single_player_env import SinglePlayerEnvironment

env = SinglePlayerEnvironment()

n_steps = 100

for step in range(n_steps):
    env.render()
    move = input("move")
    print(env.step(np.array([move])))
