from haxball_gym.environments.env import HaxballGymEnvironment
from haxball_gym.game_simulator import playeraction


class LoadedOpponentEnv(HaxballGymEnvironment):
    def __init__(self, opponent, step_len=15, max_steps=400, norming=True, rand_reset=True):

        self.opponent = opponent
        print(opponent)

        HaxballGymEnvironment.__init__(self, step_len, max_steps, norming, rand_reset)

    def getActions(self, action_list):
        if action_list is not list:
            action_list = action_list.astype(int)
        # advances the simulator by step_len number of steps. Returns a list of
        # [observation (object), reward (float), done (bool), info (dict)]
        # Actions must be integeres in the range [0, 18)

        print(self.opponent)
        opponent_action = self.opponent.getAction(self.game_sim.log())

        # put opponent action into correct type
        if opponent_action is not list:
            opponent_action = [opponent_action]

        actions = [playeraction.Action(action) for action in action_list] + opponent_action
        return actions
