import numpy as np
from haxballgym.environments.single_player_env import SinglePlayerEnvironment
from haxballgym.environments.loaded_opponent_env_1v1 import LoadedOpponentEnv1v1
from haxballgym.agents.randomagent import RandomAgent
from haxballgym.config import config


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
    env = LoadedOpponentEnv1v1(opponent=RandomAgent())
    env.step(np.array([1, 1]))
