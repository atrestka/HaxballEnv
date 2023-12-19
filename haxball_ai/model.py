import torch
import torch.nn as nn
import torch.nn.functional as F
from haxballgym import TemplateAgent, SinglePlayerEnvironment
from haxball_ai.settings import settings
from haxball_ai.envs import get_2p_env


def normalized_columns_initializer(weights, std=1.0):
    out = torch.randn(weights.size())
    out *= std / torch.sqrt(out.pow(2).sum(1, keepdim=True))
    return out


class ActorCritic(torch.nn.Module):
    def __init__(self, num_inputs, action_space):
        super(ActorCritic, self).__init__()
        self.linear1 = nn.Linear(num_inputs, settings.hidden_dimension)

        self.lstm = nn.LSTMCell(settings.hidden_dimension, settings.hidden_dimension)

        self.actor_hidden = [nn.Linear(settings.hidden_dimension, settings.hidden_dimension) for _ in range(settings.num_hidden)]
        self.critic_hidden = [nn.Linear(settings.hidden_dimension, settings.hidden_dimension) for _ in range(settings.num_hidden)]

        num_outputs = action_space.n
        self.critic_linear = nn.Linear(settings.hidden_dimension, 1)
        self.actor_linear = nn.Linear(settings.hidden_dimension, num_outputs)

    def forward(self, inputs):
        inputs, (hx, cx) = inputs
        inputs = inputs.float()
        hx = hx.float()
        cx = cx.float()
        x = F.elu(self.linear1(inputs))

        x = x.view(-1, settings.hidden_dimension)
        hx, cx = self.lstm(x, (hx, cx))
        x = hx

        return self.critic_linear(x), self.actor_linear(x), (hx, cx)

    def save(self, save_name):
        torch.save(self.state_dict(), '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_ai/saves/' + save_name)


class ActorCriticAgent(TemplateAgent):
    def __init__(self, model, frames_per_action, env, team):
        TemplateAgent.__init__(self, frames_per_action=frames_per_action, myTeam=team)

        self.env = env
        self.model = ActorCritic(get_2p_env().observation_space.shape[0], get_2p_env().action_space)

        if model is not None:
            self.model.load_state_dict(torch.load(model))

        self.cx = torch.zeros(1, 256)
        self.hx = torch.zeros(1, 256)

    def get_numpy_action(self, state):
        critic_val, action, (hx, cx) = self.model((torch.from_numpy(state).unsqueeze(0), (self.hx, self.cx)))
        self.hx = hx
        self.cx = cx
        return [int(torch.argmax(action))]
