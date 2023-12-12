from haxballgym import TemplateAgent
from stable_baselines3 import PPO


class PPOBaselineAgent(TemplateAgent):

    def __init__(self, model, frames_per_action, env):
        TemplateAgent.__init__(self, frames_per_action=frames_per_action)

        self.env = env
        self.model = PPO.load(model, env=env)

    def get_numpy_action(self, state):
        action, _states = self.model.predict(state, deterministic=True)
        return [action]
