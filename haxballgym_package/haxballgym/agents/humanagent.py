from haxballgym.game_simulator import playeraction
from haxballgym.config import config


class HumanAgent():
    def __init__(self, keybindings=None, gui=None, team=None):
        # Keybindings is a list containing the strings of the keybindings

        # Movement keys of the agent in the following order: up, right, down, left
        if keybindings is not None:
            self.movement_keys = keybindings[0:4]

        elif team == "red":
            self.movement_keys = config.DEFAULT_RED_BINDINGS

        elif team == "blue":
            self.movement_keys = config.DEFAULT_BLUE_BINDINGS

        else:
            raise ValueError("you must specify either keybindings or team")

        # Kicking key for the agent
        self.kick = keybindings[4]

        # gui gives the human commands (the pygame gui)
        self.gui = gui

        # this is a human agent
        self.requires_human_input = True

    def getAction(self, frame=None):
        # Ignore frame
        _ = frame
        # Returns raw action of the agent based on the key presses queried from
        # the gui. Returns (dir_idx, kicking_state)
        movements = [self.gui.isKeyPressed(key) for key in self.movement_keys]
        movements[0], movements[2] = movements[2], movements[0]

        raw_action = playeraction.binaryToRaw(*movements, self.gui.isKeyPressed(self.kick))
        action = playeraction.Action(*raw_action)

        return [action]
