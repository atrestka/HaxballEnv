import torch
import torch.nn.functional as F

"""
A collection of neural network models for learning to play Haxball. The input dimension should be 12 (pos, vel of both players and ball)
and the outpt dimension should be 10 (up, down, left, right, nothing and all of the previous plus kick)
"""


class Policy(torch.nn.Module):
    def __init__(self, D_in = 12, D_hid = 50, D_out = 10, norming = False):
        super(Policy, self).__init__()
        self.norming = norming

        self.affine1 = torch.nn.Linear(D_in, D_hid)
        self.move_head = torch.nn.Linear(D_hid, D_out - 1)
        self.kick_head = torch.nn.Linear(D_hid, 1)
        self.value_head = torch.nn.Linear(D_hid, 1)

    def forward(self, x):
        y = F.relu(self.affine1(x))
        moveprobs = F.softmax(self.move_head(y), dim=-1)
        kickprob = torch.nn.Sigmoid()(self.kick_head(y))
        winprob = torch.nn.Sigmoid()(self.value_head(y))
        return moveprobs, kickprob, winprob


class GregPolicy(torch.nn.Module):
    def __init__(self, D_hid = 80, norming = False):
        super(GregPolicy, self).__init__()
        self.norming = norming

        self.affine_actor_1 = torch.nn.Linear(12, D_hid)
        self.affine_actor_2 = torch.nn.Linear(D_hid, D_hid)
        self.affine_critic = torch.nn.Linear(12, D_hid)
        self.move_head = torch.nn.Linear(D_hid, 9)
        self.kick_head = torch.nn.Linear(D_hid, 1)
        self.value_head = torch.nn.Linear(D_hid, 1)

    def forward(self, x):
        y_actor_1 = F.relu(self.affine_actor_1(x))
        y_actor_2 = F.relu(self.affine_actor_2(y_actor_1))
        y_critic = F.relu(self.affine_critic(x))
        moveprobs = F.softmax(self.move_head(y_actor_2), dim=-1)
        kickprob = torch.nn.Sigmoid()(self.kick_head(y_actor_2))
        winprob = self.value_head(y_critic)
        return moveprobs, kickprob, winprob


class GregPolicy2(torch.nn.Module):
    def __init__(self, D_hid = 50, norming = False):
        super(GregPolicy2, self).__init__()
        self.norming = norming

        self.affine_actor_1 = torch.nn.Linear(12, D_hid)
        self.affine_actor_2 = torch.nn.Linear(D_hid, D_hid)
        self.affine_critic_1 = torch.nn.Linear(12, D_hid)
        self.affine_critic_2 = torch.nn.Linear(D_hid, D_hid)
        self.move_head = torch.nn.Linear(D_hid, 9)
        self.kick_head = torch.nn.Linear(D_hid, 1)
        self.value_head = torch.nn.Linear(D_hid, 1)

    def forward(self, x):
        y_actor_1 = F.relu(self.affine_actor_1(x))
        y_actor_2 = F.relu(self.affine_actor_2(y_actor_1))
        y_critic_1 = F.relu(self.affine_critic_1(x))
        y_critic_2 = F.relu(self.affine_critic_2(y_critic_1))
        moveprobs = F.softmax(self.move_head(y_actor_2), dim=-1)
        kickprob = torch.nn.Sigmoid()(self.kick_head(y_actor_2))
        winprob = self.value_head(y_critic_2)
        return moveprobs, kickprob, winprob


class SebPolicy(torch.nn.Module):
    def __init__(self, hidden_size = 50, norming = False):
        super(SebPolicy, self).__init__()

        # Just a flag to allow for easily finding if a model is supposed
        # to use normalised data.
        self.norming = norming

        self.critic = torch.nn.Sequential(
            torch.nn.Linear(12, hidden_size),
            torch.torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, hidden_size),
            torch.torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, 1)
        )

        self.actor = torch.nn.Sequential(
            torch.nn.Linear(12, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, hidden_size),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_size, 18)
        )


    def forward(self, x):
        value = self.critic(x)
        move  = F.softmax(self.actor(x),dim = -1)
        return move, value
