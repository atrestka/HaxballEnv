from haxballgym.environments.env import HaxballGymEnvironment
from haxballgym.game_simulator import playeraction
from haxballgym.config import config


class SinglePlayerEnvironment(HaxballGymEnvironment):
    def __init__(self, step_len=15, max_steps=400, norming=True, rand_reset=True):

        config.NUM_BLUE_PLAYERS = 0
        config.NUM_RED_PLAYERS = 1
        HaxballGymEnvironment.__init__(self, step_len, max_steps, norming, rand_reset)

    def getActions(self, action_list):
        if action_list is not list:
            action_list = action_list.astype(int)
        # advances the simulator by step_len number of steps. Returns a list of
        # [observation (object), reward (float), done (bool), info (dict)]
        # Actions must be integeres in the range [0, 18)

        actions = [playeraction.Action(action) for action in action_list]
        return actions
