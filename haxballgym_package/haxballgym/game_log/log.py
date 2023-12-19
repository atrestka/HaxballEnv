from haxballgym.game_simulator import playeraction
from haxballgym.config import config
from dataclasses import dataclass, field
from typing import List
import pickle
import numpy as np


@dataclass
class BallState:
    x: float
    y: float
    vx: float
    vy: float

    def posToList(self, rotation=0, normalise=True):
        if rotation == 0:
            l = [self.x, self.y, self.vx, self.vy]
        elif rotation == 1:
            l = [config.WINDOW_HEIGHT - self.y, self.x, -self.vy, self.vx]
        elif rotation == 2:
            l = [config.WINDOW_WIDTH - self.x, config.WINDOW_HEIGHT - self.y, -self.vx, -self.vy]
        elif rotation == 3:
            l = [self.y, config.WINDOW_WIDTH - self.x, self.vy, -self.vx]
        if normalise:
            v_max = config.ACCELARATION * config.PLAYER_DAMPING / (1 - config.PLAYER_DAMPING)
            l = [l[0] / config.WINDOW_WIDTH, l[1] / config.WINDOW_HEIGHT, l[2] / v_max, l[3] / v_max]
        return l


@dataclass
class GoalpostState:
    x: float
    y: float
    team: int


@dataclass
class RectangleState:
    x: float
    y: float
    width: float
    height: float


@dataclass
class PlayerState(BallState):
    action: playeraction.Action
    team: int

    def actToList(self, flip=0):
        if flip == 0:
            return self.action.singleAction()
        elif flip == 1:
            return self.action.rotated_90().singleAction()
        elif flip == 2:
            return self.action.flipped().singleAction()
        elif flip == 3:
            return self.action.rotated_270().singleAction()


@dataclass
class Frame:
    players: List[PlayerState]
    balls: List[BallState]
    goalposts: List[GoalpostState]
    rectangles: List[RectangleState]
    frame: int = 0

    def posToNp(self, flip_dir=0, pad_to_n_players=0, pad_to_n_balls=0, my_team=None, normalise=True):
        example_player = self.players[0]

        if my_team is None:
            return np.array(
                [x for p in self.players for x in p.posToList(flip_dir, normalise)]
                + [x * 0 for x in example_player.posToList(flip_dir, normalise)
                    for _ in range(max(0, pad_to_n_players - len(self.players)))]
                + [x for b in self.balls for x in b.posToList(flip_dir, normalise)]
                + [x * 0 for x in example_player.posToList(flip_dir, normalise)
                    for _ in range(max(0, pad_to_n_balls - len(self.balls)))]
            )
        else:
            raise ValueError("I have not implemented this yet :(")

    def singleActToNp(self, me, flip=0):
        return np.array(self.players[me].actToList(flip))


@dataclass
class Game:
    red_goals: int = 0
    blue_goals: int = 0
    frames: List[Frame] = field(default_factory=list)

    def append(self, frame):
        self.frames.append(frame)

    def toNp(self, myTeam, me, normalise=True):
        return np.array([f.posToNp(myTeam, me, normalise) for f in self.frames]), \
            np.array([f.singleActToNp(myTeam, me) for f in self.frames])

    @staticmethod
    def load(filename):
        f = open(filename, "rb")
        return pickle.load(f)

    def save(self, filename):
        f = open(filename, "w+b")
        pickle.dump(self, f)
