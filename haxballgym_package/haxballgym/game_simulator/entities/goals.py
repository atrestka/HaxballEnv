from haxballgym.game_simulator.entities.circle_entities import GoalPost
from haxballgym.config import config
import numpy as np


class Goal:
    def __init__(self, side, position, team, size):
        self.side = side
        self.team = team
        self.size = size
        self.position = position

        if side == "left":
            self.goalposts = [GoalPost(np.array([config.PITCH_CORNER_X, self.position + config.PITCH_CORNER_Y]),
                                       team=self.team),
                              GoalPost(np.array([config.PITCH_CORNER_X, self.position +
                                                 self.size + config.PITCH_CORNER_Y]), team=self.team)]
        elif side == "right":
            self.goalposts = [GoalPost(np.array([config.PITCH_CORNER_X + config.PITCH_WIDTH,
                                                 self.position + config.PITCH_CORNER_Y]), team=self.team),
                              GoalPost(np.array([config.PITCH_CORNER_X + config.PITCH_WIDTH,
                                                 self.position + self.size + config.PITCH_CORNER_Y]), team=self.team)]
        elif side == "top":
            self.goalposts = [GoalPost(np.array([self.position + config.PITCH_CORNER_X, config.PITCH_CORNER_Y]),
                                       team=self.team),
                              GoalPost(np.array([self.position + self.size + config.PITCH_CORNER_X,
                                                 config.PITCH_CORNER_Y]), team=self.team)]
        elif side == "bottom":
            self.goalposts = [GoalPost(np.array([self.position + config.PITCH_CORNER_X,
                                                 config.PITCH_CORNER_Y + config.PITCH_HEIGHT]), team=self.team),
                              GoalPost(np.array([self.position + self.size + config.PITCH_CORNER_X,
                                                 config.PITCH_CORNER_Y + config.PITCH_HEIGHT]), team=self.team)]
        else:
            raise ValueError("invalid side")
