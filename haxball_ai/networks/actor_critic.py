import torch


class ACNetwork(torch.nn.Module):
    def __init__(self, hidden_size=50, norming=False):
        super(ACNetwork, self).__init__()

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
