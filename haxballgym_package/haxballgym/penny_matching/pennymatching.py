from haxballgym.config import config, update_config_from_yaml
from haxballgym.game_simulator.entities.circle_entities import Player
from haxballgym.game_simulator.entities.rectangle_entities import RectangleEntity
import numpy as np
from haxballgym.game_simulator.haxballsim import HaxballGameSim


class PennyMatchingGameSim(HaxballGameSim):
    def __init__(self, auto_reset=True):

        update_config_from_yaml(config, 'haxballgym_package/haxballgym/penny_matching/penny_matching_config.yaml')

        printDebug = False
        printDebugFreq = 600
        print_score_update = False
        auto_score = True
        rand_reset = False
        max_steps = config.PENNYMATCHING_TERMINAL_STEP

        self.reds = [Player(0, np.array([config.WINDOW_WIDTH // 4, config.WINDOW_HEIGHT // 2]).astype(float))]
        self.blues = [Player(1, np.array([3 * config.WINDOW_WIDTH // 4, config.WINDOW_HEIGHT // 2]).astype(float))]
        players = self.reds + self.blues
        balls = []
        goals = []

        other_rectangles = [
            RectangleEntity(np.array([config.WINDOW_WIDTH // 4 + 100, config.WINDOW_HEIGHT // 2 - 100]), 50, 50,
                            config.GOALPOST_BOUNCING_QUOTIENT, False),
            RectangleEntity(np.array([config.WINDOW_WIDTH // 4 + 100, config.WINDOW_HEIGHT // 2 + 50]), 50, 50,
                            config.GOALPOST_BOUNCING_QUOTIENT, False),
            RectangleEntity(np.array([3 * config.WINDOW_WIDTH // 4 - 150, config.WINDOW_HEIGHT // 2 - 100]), 50, 50,
                            config.GOALPOST_BOUNCING_QUOTIENT, False),
            RectangleEntity(np.array([3 * config.WINDOW_WIDTH // 4 - 150, config.WINDOW_HEIGHT // 2 + 50]), 50, 50,
                            config.GOALPOST_BOUNCING_QUOTIENT, False),
        ]

        walls = [RectangleEntity(np.array([config.WINDOW_WIDTH // 2 - config.CENTRE_WALL_SIZE // 2, 0]),
                                 config.CENTRE_WALL_SIZE, config.WINDOW_HEIGHT, config.GOALPOST_BOUNCING_QUOTIENT,
                                 True)]

        HaxballGameSim.__init__(self, balls, goals, walls, other_rectangles, players, printDebug, printDebugFreq,
                                print_score_update, auto_score, rand_reset=rand_reset, max_steps=max_steps,
                                auto_reset=auto_reset)

    def additionalPointCheck(self):
        if self.steps >= config.PENNYMATCHING_TERMINAL_STEP - 1:

            if self.other_recrangles[0].active and self.other_recrangles[2].active:
                return [1, 0]
            if self.other_recrangles[1].active and self.other_recrangles[3].active:
                return [1, 0]
            if self.other_recrangles[0].active and self.other_recrangles[3].active:
                return [0, 1]
            if self.other_recrangles[1].active and self.other_recrangles[2].active:
                return [0, 1]

            if self.other_recrangles[0].active or self.other_recrangles[1].active:
                return [0, 2]

            if self.other_recrangles[2].active or self.other_recrangles[3].active:
                return [2, 0]

            return [2, 2]
        else:
            return [0, 0]
