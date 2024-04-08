from haxballgym.environments.env import HaxballGymEnvironmentTemplate
from haxballgym.game_simulator import playeraction
from haxballgym.penny_matching.pennymatching import PennyMatchingGameSim
from haxballgym.config import config
import gymnasium as gym
import numpy as np
from haxballgym.agents.randomagent import RandomAgent


class PennyMatchingLoadedOpponentEnv(HaxballGymEnvironmentTemplate):
    def __init__(self, opponent=None, step_len=15, norming=True,
                 use_discrete_actionspace=False, playing=0):

        self.opponent = opponent
        self.playing_as = playing

        if self.opponent is None:
            self.opponent = RandomAgent()

        gamesim = PennyMatchingGameSim(auto_reset=False)

        HaxballGymEnvironmentTemplate.__init__(self, gamesim, step_len, 200, norming)

        self.use_discrete_actionspace = use_discrete_actionspace
        if use_discrete_actionspace:
            self.action_space = gym.spaces.Discrete(18)

    def getActions(self, action_list):
        if action_list is not list:
            action_list = action_list.astype(int)
        # advances the simulator by step_len number of steps. Returns a list of
        # [observation (object), reward (float), done (bool), info (dict)]
        # Actions must be integeres in the range [0, 18)

        if self.use_discrete_actionspace:
            action_list = [action_list]

        opponent_action = self.opponent.getAction(self.game_sim.log())

        # put opponent action into correct type
        if not isinstance(opponent_action, list):
            opponent_action = [opponent_action]

        if self.playing_as == 0:
            actions = [playeraction.Action(action) for action in action_list] + opponent_action
        else:
            actions = opponent_action + [playeraction.Action(action) for action in action_list]
        return actions

    def load_new_opponent(self, opponent):
        self.opponent = opponent

        if opponent is None:
            self.opponent = RandomAgent()

    def getStepReward(self, scoring_player, ball_touched_red):

        print(self.game_sim.steps)
        print(self.game_sim.max_steps)
        print(self.step_len)

        if self.game_sim.steps >= self.game_sim.max_steps - 1:
            print('ASDASD')
            points = self.game_sim.additionalPointCheck()
            print(points)

            result = config.PENNYMATCHING_FAIL_REWARD

            if self.playing_as == 0:
                if points[0] == 1 and points[1] == 0:
                    result = config.PENNYMATCHING_LOSE_REWARD
                elif points[0] == 0 and points[1] == 1:
                    result = config.PENNYMATCHING_WIN_REWARD

                elif points[0] == 2:
                    result = config.PENNYMATCHING_FAIL_REWARD

                elif points[0] == 0 and points[1] == 2:
                    return config.PENNYMATCHING_WIN_REWARD

            if self.playing_as == 1:
                if points[0] == 1 and points[1] == 0:
                    result = config.PENNYMATCHING_WIN_REWARD
                elif points[0] == 0 and points[1] == 1:
                    result = config.PENNYMATCHING_LOSE_REWARD

                elif points[1] == 2:
                    result = config.PENNYMATCHING_FAIL_REWARD

                elif points[0] == 2 and points[1] == 0:
                    return config.PENNYMATCHING_WIN_REWARD

        else:
            result = 0.
        return result

    def getState(self):
        return np.array(self.game_sim.log().posToNp(0, self.norming, player_ind=[self.playing_as])
                        + [self.game_sim.steps])
