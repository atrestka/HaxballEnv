from haxballgym.environments.env import HaxballGymEnvironmentTemplate
from haxballgym.haxball.haxball import TwoTeamHaxballGamesim
from haxballgym.game_simulator import playeraction
from haxballgym.config import config
import gymnasium as gym


class SinglePlayerEnvironment(HaxballGymEnvironmentTemplate):
    def __init__(self, step_len=15, max_steps=400, norming=True, rand_reset=True, use_discrete_actionspace=True, seed=None):

        config.TEAM_NUMBERS = [1]

        gamesim = TwoTeamHaxballGamesim(
            1,
            0,
            1,
            auto_score=True,
            rand_reset=rand_reset,
            max_steps=max_steps * step_len,
            auto_reset=False,
            seed = seed
        )

        HaxballGymEnvironmentTemplate.__init__(self, gamesim, step_len, max_steps, norming)
        self.seed(seed)

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
            return [playeraction.Action(action_list)]

        actions = [playeraction.Action(action) for action in action_list]
        return actions

    def getStepReward(self, scoring_player, ball_touched_red):
        if scoring_player == 1:
            return 1.0 * config.WIN_REWARD
        elif scoring_player == -1:
            return -1.0 * config.WIN_REWARD

        if self.steps_since_reset >= self.max_steps:
            result = ball_touched_red * config.KICK_REWARD \
                - (self.game_sim.getBallProximityScore(0) - self.last_ballprox) \
                * config.BALL_PROXIMITY_REWARD
        else:
            result = ball_touched_red * config.KICK_REWARD \
                - (self.game_sim.getBallProximityScore(0) - self.last_ballprox) \
                * config.BALL_PROXIMITY_REWARD
        return result
