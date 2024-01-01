from gym import Env
import gym
from haxballgym.game_displayer import basicdisplayer
from haxballgym.config import config

import numpy as np


class HaxballGymEnvironmentTemplate(Env):
    def __init__(self, game_sim, step_len=15, max_steps=400, norming=True):
        self.step_len = step_len
        self.max_steps = max_steps
        self.norming = norming

        self.game_sim = game_sim
        if self.game_sim.rand_reset:
            self.game_sim.resetMap()
        else:
            self.game_sim.resetMap("all default")
        self.steps_since_reset = 0
        self.display = None
        self.last_ballprox = self.game_sim.getBallProximityScore(0)

        # define gym spaces
        self.action_space = gym.spaces.MultiDiscrete([18 for _ in
                                                      range(config.NUM_PLAYERS)])
        self.observation_space = get_observation_space()

    def getState(self):
        # Returns the state of the game, posToNp flattens it to a np array.
        # That's desired so the state is in an easier to manipulate form.
        return np.array(self.game_sim.log().posToNp(0, self.norming))

    def getActions(self, action_list):
        raise NotImplementedError

    def getStepReward(self, scoring_player, ball_touched_red):
        raise NotImplementedError()

    def step(self, action_list):

        if isinstance(action_list, int):
            action_list = np.array([action_list])

        self.steps_since_reset += 1
        actions = self.getActions(action_list)

        self.game_sim.giveCommands(actions)
        ball_touched_red = False

        for i in range(self.step_len):
            game_ended = self.game_sim.step()
            goal = self.goalScored()
            ball_touched_red = ball_touched_red or self.game_sim.was_ball_touched_red
            # If a goal is scored return instantly
            if goal != 0 or game_ended:
                result = [self.getState(), self.getStepReward(goal, ball_touched_red), True, {}]
                return result

        # If no goal consider it a tie.
        if self.steps_since_reset >= self.max_steps:
            result = [self.getState(), self.getStepReward(goal, ball_touched_red), True, {}]
        else:
            result = [self.getState(), self.getStepReward(goal, ball_touched_red), False, {}]

        self.last_ballprox = self.game_sim.getBallProximityScore(0)

        return result

    def render(self, mode='human'):
        # If the display hasn't been created, create it
        if self.display is None:
            self.display = basicdisplayer.GameWindow(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

        self.display.drawFrame(self.game_sim.log(), hold=1)

        # Support moving and closing the window
        self.display.getInput()
        if self.display.rip:
            self.display.shutdown()

    def reset(self):
        self.steps_since_reset = 0
        if self.game_sim.rand_reset:
            self.game_sim.resetMap()
        else:
            self.game_sim.resetMap("all default")
        return self.getState()

    def goalScored(self):
        # Checks goals. Returns 1 for red, 0 for none, -1 for blue.
        goals = self.game_sim.checkGoals()
        if goals[0] > 0:
            return -1
        elif sum(goals) == 0:
            return 0
        else:
            return 1


def get_observation_space():
    max_player_vals = [config.WINDOW_WIDTH, config.WINDOW_HEIGHT, 100, 100]
    min_player_vals = [0, 0, -100, -100]
    min_vals = sum([min_player_vals for _ in range(config.NUM_ENTITIES)], [])
    max_vals = sum([max_player_vals for _ in range(config.NUM_ENTITIES)], [])

    low = np.array(min_vals).astype(float)
    high = np.array(max_vals).astype(float)
    shape = (len(low),)
    return gym.spaces.Box(np.float32(low), np.float32(high), shape)