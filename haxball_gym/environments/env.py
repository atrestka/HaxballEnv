from gym import Env
import gym
from haxball_gym.game_simulator import gamesim
from haxball_gym.game_displayer import basicdisplayer
from haxball_gym.config import config

import numpy as np


class HaxballGymEnvironment(Env):
    def __init__(self, step_len=15, max_steps=400, norming=True, rand_reset=True):
        self.step_len = step_len
        self.max_steps = max_steps
        self.norming = norming

        self.game_sim = gamesim.GameSim(config.NUM_RED_PLAYERS, config.NUM_BLUE_PLAYERS, config.NUM_BALLS,
                                        rand_reset=rand_reset)
        self.game_sim.resetMap()
        self.steps_since_reset = 0
        self.display = None

        # define gym spaces
        self.action_space = gym.spaces.MultiDiscrete([18 for _ in
                                                      range(config.NUM_BLUE_PLAYERS + config.NUM_RED_PLAYERS)])
        self.observation_space = get_observation_space()

    def getState(self):
        # Returns the state of the game, posToNp flattens it to a np array.
        # That's desired so the state is in an easier to manipulate form.
        return np.array(self.game_sim.log().posToNp("red", 0, self.norming))

    def getActions(self, action_list):
        raise NotImplementedError

    def step(self, action_list):
        
        self.steps_since_reset += 1
        actions = self.getActions(action_list)

        self.game_sim.giveCommands(actions)

        ball_touched = False
        for i in range(self.step_len):
            self.game_sim.step()
            ball_touched = ball_touched or self.game_sim.was_ball_touched
            goal = self.goalScored()
            # If a goal is scored return instantly
            if goal == 1:
                return [self.getState(), 1.0 * config.WIN_REWARD, True, {}]
            elif goal == -1:
                return [self.getState(), -1.0 * config.WIN_REWARD, True, {}]

        # If no goal consider it a tie.
        if self.steps_since_reset >= self.max_steps:
            return [self.getState(), self.game_sim.was_ball_touched * config.BALL_PROXIMITY_REWARD, True, {}]
        else:
            print(self.game_sim.was_ball_touched * config.BALL_PROXIMITY_REWARD)
            return [self.getState(), self.game_sim.was_ball_touched * config.BALL_PROXIMITY_REWARD, False, {}]

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


def get_observation_space():
    max_player_vals = [config.WINDOW_WIDTH, config.WINDOW_HEIGHT, 100, 100]
    min_player_vals = [0, 0, -100, -100]
    min_vals = sum([min_player_vals for _ in range(config.NUM_ENTITIES)], [])
    max_vals = sum([max_player_vals for _ in range(config.NUM_ENTITIES)], [])

    low = np.array(min_vals).astype(float)
    high = np.array(max_vals).astype(float)
    shape = (len(low),)
    return gym.spaces.Box(np.float32(low), np.float32(high), shape)