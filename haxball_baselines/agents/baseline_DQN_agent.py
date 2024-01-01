from haxballgym import TemplateAgent
from stable_baselines3 import DQN


class DQNBaselineAgent(TemplateAgent):

    def __init__(self, model, frames_per_action, env, team=0):
        TemplateAgent.__init__(self, frames_per_action=frames_per_action, myTeam=team)

        self.env = env
        self.model = DQN.load(model, env=env)

    def get_numpy_action(self, state):
        action, _states = self.model.predict(state, deterministic=True)
        return action
