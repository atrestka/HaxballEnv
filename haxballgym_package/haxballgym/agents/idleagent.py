from haxballgym.game_simulator import playeraction


class IdleAgent():
    # A really clever agent that only returns random commands
    def __init__(self):
        # this is not a human agent
        self.requires_human_input = False

    def getAction(self, frame=None):
        # Ignore frame
        _ = frame
        # Returns raw action of the agent based on the key presses queried from
        # the gui. Returns (dir_idx, kicking_state)
        return [playeraction.Action(0)]
