import numpy as np
from haxball_gym.environments.single_player_env import SinglePlayerEnvironment
from haxball_gym.environments.loaded_opponent_env import LoadedOpponentEnv
from haxball_gym.agents.randomagent import RandomAgent
from haxball_gym.config import config


#######################################################
#################### TEST SCRIPT ######################
#######################################################
#      checks we can load all game environments

# check we can load and make moves in single_player_env
def test_single_player_env():
    config.NUM_BLUE_PLAYERS = 1
    config.NUM_RED_PLAYERS = 1
    env = SinglePlayerEnvironment()
    env.step(np.array([1, 1]))


# check we can load and make moves in loaded_opponent_env
def test_multi_player_env():
    config.NUM_BLUE_PLAYERS = 1
    config.NUM_RED_PLAYERS = 1
    env = LoadedOpponentEnv(opponent=RandomAgent())
    env.step(np.array([1, 1]))
