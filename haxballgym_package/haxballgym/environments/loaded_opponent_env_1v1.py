from haxballgym.environments.env import HaxballGymEnvironmentTemplate
from haxballgym.game_simulator import playeraction
from haxballgym.haxball.haxball import TwoTeamHaxballGamesim
from haxballgym.config import config
import gym
from haxballgym.agents.randomagent import RandomAgent


class LoadedOpponentEnv1v1(HaxballGymEnvironmentTemplate):
    def __init__(self, opponent=None, step_len=15, max_steps=400, norming=True, rand_reset=True,
                 use_discrete_actionspace=False):

        self.opponent = opponent

        if self.opponent is None:
            self.opponent = RandomAgent()

        gamesim = TwoTeamHaxballGamesim(
            1,
            1,
            1,
            auto_score=True,
            rand_reset=rand_reset,
            max_steps=max_steps,
            auto_reset=False
        )

        HaxballGymEnvironmentTemplate.__init__(self, gamesim, step_len, max_steps, norming)

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

        actions = [playeraction.Action(action) for action in action_list] + opponent_action
        return actions

    def load_new_opponent(self, opponent):
        self.opponent = opponent

        if opponent is None:
            self.opponent = RandomAgent()

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
