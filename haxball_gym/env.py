from game_simulator import gamesim, playeraction
from game_displayer import basicdisplayer
from haxball_gym.config import config


import numpy as np


class HaxballEnvironment:
    def __init__(self, step_len=15, max_steps=400, norming=True):
        self.step_len = step_len
        self.max_steps = max_steps

        self.norming = norming

        self.game_sim = gamesim.GameSim(config.NUM_RED_PLAYERS, config.NUM_BLUE_PLAYERS, config.NUM_BALLS)
        self.game_sim.resetMap()

        self.steps_since_reset = 0

        self.display = None

    def getState(self):
        # Returns the state of the game, posToNp flattens it to a np array.
        # That's desired so the state is in an easier to manipulate form.
        return np.array(self.game_sim.log().posToNp("red", 0, self.norming))

    def step(self, action_list):
        # advances the simulator by step_len number of steps. Returns a list of
        # [observation (object), reward (float), done (bool), info (dict)]
        # Actions must be integeres in the range [0, 18)
        self.steps_since_reset += 1

        self.game_sim.giveCommands([playeraction.Action(action) for action in action_list])

        for i in range(self.step_len):
            self.game_sim.step()
            goal = self.goalScored()
            # If a goal is scored return instantly
            if goal == 1:
                return [self.getState(), 1.0, True, {}]
            elif goal == -1:
                return [self.getState(), -1.0, True, {}]

        # If no goal consider it a tie.
        if self.steps_since_reset >= self.max_steps:
            return [self.getState(), 0.0, True, {}]
        else:
            return [self.getState(), 0.0, False, {}]

    def render(self, mode='human'):
        # If the display hasn't been created, create it
        if self.display is None:
            self.display = basicdisplayer.GameWindow(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.display.drawFrame(self.game_sim.log())

        # Support moving and closing the window
        self.display.getInput()
        if self.display.rip:
            self.display.shutdown()

    def reset(self):
        self.steps_since_reset = 0
        self.game_sim.resetMap("random")
        return self.getState()

    def goalScored(self):
        # Checks goals. Returns 1 for red, 0 for none, -1 for blue.
        goals = self.game_sim.checkGoals()
        if goals[0] > 0:
            return 1
        elif goals[1] > 0:
            return -1
        else:
            return 0
