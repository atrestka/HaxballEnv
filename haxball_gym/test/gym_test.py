from haxball_gym.env import HaxballEnvironment
from haxball_gym.config import config


def test_env():
    config.NUM_BLUE_PLAYERS = 1
    config.NUM_RED_PLAYERS = 1
    env = HaxballEnvironment()
    env.step([1, 1])
