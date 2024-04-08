from haxballgym import SinglePlayerEnvironment
import gymnasium as gym
from gymnasium import register

register(
        id='SinglePlayerHaxball-v0',  # Unique identifier for the environment
        entry_point='haxballgym:SinglePlayerEnvironment',  # Adjusted entry point
    )


# print("###############")
# print(env.getState())

# env.reset(46000)
# print(env.getState())

# env.reset(46000)
# print(env.getState())

# env.reset(50000)
# print(env.getState())

# env.reset(50000)
# print(env.getState())


