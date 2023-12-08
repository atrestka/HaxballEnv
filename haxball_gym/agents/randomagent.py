from haxball_gym.game_simulator import playeraction


class RandomAgent():
    # A really clever agent that only returns random commands
    def __init__(self, frames_per_action=1):
        # this is not a human agent
        self.requires_human_input = False
        self.frames_per_action = frames_per_action
        self.current_action = None

    def getAction(self, frame=None):
        # Ignore frame
        step = frame.frame
        # Returns raw action of the agent based on the key presses queried from
        # the gui. Returns (dir_idx, kicking_state)

        if step % self.frames_per_action == 0:
            self.current_action = playeraction.Action.randomAction()

        return self.current_action
