from game_simulator import gamesim, gameparams, playeraction
from game_displayer import basicdisplayer

from gym import core, spaces
import numpy as np
import torch

class SingleplayerGym(core.Env):
    def __init__(self, config):
        if "step_length" in config:
            self.step_len = config["step_length"]
        else:
            self.step_len = 7

        if "max_steps" in config:
            self.max_steps = config["max_steps"]
        else:
            self.max_steps = 400

        self.game_sim = gamesim.GameSim(1, 0, 1)
        self.game_sim.resetMap("ball center, players random")

        win_w = gameparams.windowwidth
        win_h = gameparams.windowheight

        self.action_space = spaces.Discrete(18)
        self.observation_space = spaces.Box(
           low = np.array([0.0, 0.0, -15.0, -15.0, 0.0, 0.0,
                          -15.0, -15.0]),
           high = np.array([win_w, win_h, 15.0, 15.0, win_w, win_h,
                            15.0, 15.0]),
            dtype = np.float32
           )

        self.steps_since_reset = 0

        self.display = None

    def getState(self):
        # Returns the state of the game, posToNp flattens it to a np array.
        # That's desired so the state is in an easier to manipulate form.
        return np.array(self.game_sim.log().posToNp("red"))

    def step(self, action_single):
        # advances the simulator by step_len number of steps. Returns a list of
        # [observation (object), reward (float), done (bool), info (dict)]
        # Actions must be integeres in the range [0, 18)
        self.steps_since_reset += 1

        self.game_sim.giveCommands([playeraction.Action(action_single)])

        for i in range(self.step_len):
            self.game_sim.step()
            goal = self.goalScored()
            # If a goal is scored return instantly
            if goal != 0:
                return [self.getState(), self.game_sim.getSingeplayerReward(), True, {}]

        # If no goal consider it a tie.
        if self.steps_since_reset >= self.max_steps:
            return [self.getState(), self.game_sim.getSingeplayerReward(), True, {}]
        else:
            return [self.getState(), 0.0, False, {}]

    def render(self, mode='human'):
        # If the display hasn't been created, create it
        if self.display == None:
            self.display = basicdisplayer.GameWindow(gameparams.windowwidth, gameparams.windowheight)

        self.display.drawFrame(self.game_sim.log())

        # Support moving and closing the window
        self.display.getInput()
        if self.display.rip:
            self.display.shutdown()

    def reset(self):
        self.steps_since_reset = 0
        self.game_sim.resetMap("ball center, players random")
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
