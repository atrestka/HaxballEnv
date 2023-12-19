from dataclasses import dataclass
import numpy as np


@dataclass
class Configuration:

    ################################
    ######## GAME SETTINGS #########
    ################################

    # player and ball parameters
    TEAM_NUMBERS = [1]  # [red (left), blue (right), yellow (top), green (bottom)]
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
    ## PYGAME VISUALIZER SETTINGS ##
    ################################

    # defines colors used in drawing the map
    TEAM_COLOURS = [(229, 110, 86), (86, 137, 229), (229, 229, 10), (0, 200, 0)]
    GOALPOST_COLOUR = (150, 150, 150)
    BALL_COLOUR = (0, 0, 0)
    WALL_COLOUR = (50, 50, 50)
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

    # defines relevant pitch coordinates for calculation
    PITCH_CORNER_X = int(np.floor((WINDOW_WIDTH - PITCH_WIDTH) / 2))
    PITCH_CORNER_Y = int(np.floor((WINDOW_HEIGHT - PITCH_HEIGHT) / 2))
    GOAL_CORNER_Y = int(np.floor((WINDOW_HEIGHT - GOAL_SIZE) / 2))

    # I have no idea what this is
    y1 = PITCH_CORNER_X - 30
    z1 = PITCH_CORNER_X + PITCH_WIDTH
    z2 = GOAL_CORNER_Y
    a1 = y1 + 2 * BALL_RADIUS
    a2 = int(np.floor(GOAL_CORNER_Y - GOAL_LINE_THICKNESS / 2))
    b1 = z1
    b2 = int(np.floor(GOAL_CORNER_Y - GOAL_LINE_THICKNESS / 2))

    # defines the movespace of a player
    MOVESPACE_X = [PLAYER_RADIUS, WINDOW_WIDTH - PLAYER_RADIUS]
    MOVESPACE_Y = [PLAYER_RADIUS, WINDOW_HEIGHT - PLAYER_RADIUS]

    # defines the movespace of a ball
    BALLSPACE_X = [PITCH_CORNER_X + BALL_RADIUS, PITCH_CORNER_X + PITCH_WIDTH - BALL_RADIUS]
    BALLSPACE_Y = [PITCH_CORNER_Y + BALL_RADIUS, PITCH_CORNER_Y + PITCH_HEIGHT - BALL_RADIUS]

    # defines goal width
    GOAL_Y = [GOAL_CORNER_Y, GOAL_CORNER_Y + GOAL_SIZE]

    # number of things in the game
    NUM_ENTITIES = sum(TEAM_NUMBERS) + NUM_BALLS
    NUM_PLAYERS = sum(TEAM_NUMBERS)


# define the config
config = Configuration()
