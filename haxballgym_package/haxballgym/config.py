from dataclasses import dataclass
import numpy as np
import yaml
from pathlib import Path


@dataclass
class Configuration:

    ################################
    ######## GAME SETTINGS #########
    ################################

    # player and ball parameters
    #AGT CHANGES HERE
    TEAM_NUMBERS = [1,1]  # [red (left), blue (right), yellow (top), green (bottom)]
    NUM_BALLS = 1

    # field size parameters
    WINDOW_WIDTH = 840
    WINDOW_HEIGHT = 400
    PITCH_WIDTH = 640
    PITCH_HEIGHT = 260
    GOAL_SIZE = 110

    # length of game
    MAX_SCORE = 1

    # game parameters for the player
    PLAYER_RADIUS = 15
    PLAYER_BOUNCING = 0.5
    PLAYER_INV_MASS = 0.5
    PLAYER_DAMPING = 0.96
    ACCELARATION = 0.1
    KICK_ACCELARATION = 0.07
    KICK_STRENGTH = 5

    # game parameters for the ball
    BALL_RADIUS = 10
    BALL_DAMPING = 0.99
    BALL_INV_MASS = 1
    BALL_BOUNCING = 0.5

    # start position parameters (for when no random start)
    PLAYER_START_POSITIONS = []
    BALL_START_POSITIONS = []

    # parameters for the pitch drawing
    GOALPOST_RADIUS = 8
    GOALPOST_BOUNCING_QUOTIENT = 0.5
    GOALPOST_BORDER_THICKNESS = 2
    GOAL_LINE_THICKNESS = 3
    KICKING_CIRCLE_RADIUS = 15
    KICKING_CIRCLE_THICKNESS = 2

    # reward parameters
    WIN_REWARD = 1000.
    BALL_PROXIMITY_REWARD = 1.
    KICK_REWARD = 1.

    ################################
    ### PENNY MATCHING SETTINGS ####
    ################################

    # defines the map
    CENTRE_WALL_SIZE = 20
    PENNYMATCHING_TERMINAL_STEP = 200
    PENNYMATCHING_FAIL_REWARD = -5
    PENNYMATCHING_LOSE_REWARD = -1
    PENNYMATCHING_WIN_REWARD = 1

    ################################
    ## PYGAME VISUALIZER SETTINGS ##
    ################################

    # defines colors used in drawing the map
    TEAM_COLOURS = [(229, 110, 86), (86, 137, 229), (229, 229, 10), (0, 200, 0)]
    GOALPOST_COLOUR = (150, 150, 150)
    BALL_COLOUR = (0, 0, 0)
    WALL_COLOUR = (50, 50, 50)
    OTHER_RECT_COLOUR = (120, 150, 90)
    OTHER_RECT_ACTIVE_COLOUR = (120, 170, 90)
    GOAL_LINE_COLOUR = (199, 230, 189)
    PITCH_COLOUR = (127, 162, 112)
    BORDER_COLOUR = (113, 140, 90)
    KICKING_CIRCLE_COLOUR = (255, 255, 255)

    # defines centre line properties
    CENTRE_CIRCLE_RADIUS = 70
    CENTRE_CIRCLE_COLOUR = (199, 230, 189)
    CENTRE_CIRCLE_THICKNESS = 3
    CENTRE_LINE_THICKNESS = 3

    # defines text properties
    TEXT_COLOUR = (0, 0, 0)
    TEXT_POSITION = (215, 25)

    DEFAULT_RED_BINDINGS = ('w', 'd', 's', 'a', 'c')
    DEFAULT_BLUE_BINDINGS = ('i', 'l', 'k', 'j', '.')

    ################################
    ###### GAME CALCULATIONS #######
    ################################

    def __init__(self):
        self.calculations()

    def calculations(self):
        # defines relevant pitch coordinates for calculation
        self.PITCH_CORNER_X = int(np.floor((self.WINDOW_WIDTH - self.PITCH_WIDTH) / 2))
        self.PITCH_CORNER_Y = int(np.floor((self.WINDOW_HEIGHT - self.PITCH_HEIGHT) / 2))
        self.GOAL_CORNER_Y = int(np.floor((self.WINDOW_HEIGHT - self.GOAL_SIZE) / 2))

        # I have no idea what this is
        self.y1 = self.PITCH_CORNER_X - 30
        self.z1 = self.PITCH_CORNER_X + self.PITCH_WIDTH
        self.z2 = self.GOAL_CORNER_Y
        self.a1 = self.y1 + 2 * self.BALL_RADIUS
        self.a2 = int(np.floor(self.GOAL_CORNER_Y - self.GOAL_LINE_THICKNESS / 2))
        self.b1 = self.z1
        self.b2 = int(np.floor(self.GOAL_CORNER_Y - self.GOAL_LINE_THICKNESS / 2))

        # defines the movespace of a player
        self.MOVESPACE_X = [self.PLAYER_RADIUS, self.WINDOW_WIDTH - self.PLAYER_RADIUS]
        self.MOVESPACE_Y = [self.PLAYER_RADIUS, self.WINDOW_HEIGHT - self.PLAYER_RADIUS]

        # defines the movespace of a ball
        self.BALLSPACE_X = [self.PITCH_CORNER_X + self.BALL_RADIUS, self.PITCH_CORNER_X + self.PITCH_WIDTH - self.BALL_RADIUS]
        self.BALLSPACE_Y = [self.PITCH_CORNER_Y + self.BALL_RADIUS, self.PITCH_CORNER_Y + self.PITCH_HEIGHT - self.BALL_RADIUS]

        # defines goal width
        self.GOAL_Y = [self.GOAL_CORNER_Y, self.GOAL_CORNER_Y + self.GOAL_SIZE]

        # number of things in the game
        self.NUM_ENTITIES = sum(self.TEAM_NUMBERS) + self.NUM_BALLS
        self.NUM_PLAYERS = sum(self.TEAM_NUMBERS)


# for updating config from individual game yaml config files
def update_config_from_yaml(config, cfg_yaml):
    cfg_yaml = yaml.safe_load(Path(cfg_yaml).read_text())

    for key in dir(config):
        if key[0] != '_':
            if key in dict(cfg_yaml).keys():
                setattr(config, key, cfg_yaml[key])

    config.calculations()


# define the config
config = Configuration()
