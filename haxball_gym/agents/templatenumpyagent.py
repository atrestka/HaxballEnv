from abc import abstractmethod, ABC
from haxball_gym.game_simulator import playeraction


class TemplateAgent(ABC):
    # A really clever agent that only returns random commands
    def __init__(self, frames_per_action=1):
        # this is not a human agent
        self.requires_human_input = False
        self.frames_per_action = frames_per_action
        self.current_action = None

    @abstractmethod
    def get_numpy_action(self, state):
        raise NotImplementedError

    def getAction(self, frame=None):
        step = frame.frame
        if step % self.frames_per_action == 0:
            numpy_frame = frame.posToNp(myTeam="red", me=0, normalise=True, pad_to_n_players=0, pad_to_n_balls=0)
            self.current_action = self.get_numpy_action(numpy_frame)

        print(self.current_action)
        self.current_action = self.current_action.astype(int)
        print(self.current_action)
        return [playeraction.Action(action) for action in self.current_action][0]
