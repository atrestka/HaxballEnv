from abc import abstractmethod, ABC
from haxballgym.game_simulator import playeraction
import numpy as np


class TemplateAgent(ABC):
    # A really clever agent that only returns random commands
    def __init__(self, frames_per_action=1, myTeam=0):
        # this is not a human agent
        self.requires_human_input = False
        self.frames_per_action = frames_per_action
        self.current_action = None
        self.team = myTeam

    @abstractmethod
    def get_numpy_action(self, state):
        raise NotImplementedError

    def getAction(self, frame=None):
        step = frame.frame
        if step % self.frames_per_action == 0:
            numpy_frame = frame.posToNp(flip_dir=self.team, normalise=True, pad_to_n_players=0, pad_to_n_balls=0)
            self.current_action = self.get_numpy_action(numpy_frame)

        self.current_action = np.block(self.current_action).flatten().astype(int)
        if self.team == 0:
            return [playeraction.Action(action) for action in self.current_action]
        elif self.team == 1:
            return [playeraction.Action(action).flipped() for action in self.current_action]
        else:
            raise ValueError("team is invalid!")
