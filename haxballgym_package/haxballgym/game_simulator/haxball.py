from haxballgym.config import config
from haxballgym.game_simulator.entities.circle_entities import Player, Ball
from haxballgym.game_simulator.entities.goals import Goal
# from game_simulator.entities.rectangle_entities import RectangleEntity
import numpy as np
from haxballgym.game_simulator.haxballsim import HaxballGameSim


class TwoTeamHaxballGamesim(HaxballGameSim):
    def __init__(self, red_player_count, blue_player_count, ball_count, printDebug=False, printDebugFreq=600,
                 print_score_update=False, auto_score=False,
                 rand_reset=True, max_steps=-1):

        self.reds = [Player(0, np.zeros(2)) for _ in range(red_player_count)]
        self.blues = [Player(1, np.zeros(2)) for _ in range(blue_player_count)]

        players = self.reds + self.blues

        balls = [Ball(np.zeros(2)) for _ in range(ball_count)]

        goals = [
            Goal("left", config.PITCH_HEIGHT // 2 - config.GOAL_SIZE // 2, 0, config.GOAL_SIZE),
            Goal("right", config.PITCH_HEIGHT // 2 - config.GOAL_SIZE // 2, 1, config.GOAL_SIZE),
        ]

        other_rectangles = []

        HaxballGameSim.__init__(self, balls, goals, [], other_rectangles, players, printDebug, printDebugFreq,
                                print_score_update, auto_score, rand_reset, max_steps)


class FourTeamHaxballGameSim(HaxballGameSim):
    def __init__(self, red_player_count, blue_player_count, orange_player_count, green_player_count,
                 ball_count, printDebug=False, printDebugFreq=600,
                 print_score_update=False, auto_score=False,
                 rand_reset=True, max_steps=-1):

        self.reds = [Player(0, np.zeros(2)) for _ in range(red_player_count)]
        self.blues = [Player(1, np.zeros(2)) for _ in range(blue_player_count)]
        self.oranges = [Player(2, np.zeros(2)) for _ in range(orange_player_count)]
        self.greens = [Player(3, np.zeros(2)) for _ in range(green_player_count)]

        players = self.reds + self.blues + self.oranges + self.greens

        balls = [Ball(np.zeros(2)) for _ in range(ball_count)]

        goals = [
            Goal("left", config.PITCH_HEIGHT // 2 - config.GOAL_SIZE // 2, 0, config.GOAL_SIZE),
            Goal("right", config.PITCH_HEIGHT // 2 - config.GOAL_SIZE // 2, 1, config.GOAL_SIZE),
            Goal("top", config.PITCH_WIDTH // 2 - config.GOAL_SIZE // 2, 2, config.GOAL_SIZE),
            Goal("bottom", config.PITCH_WIDTH // 2 - config.GOAL_SIZE // 2, 3, config.GOAL_SIZE),
        ]

        other_rectangles = []

        HaxballGameSim.__init__(self, balls, goals, [], other_rectangles, players, printDebug, printDebugFreq,
                                print_score_update, auto_score, rand_reset, max_steps)

