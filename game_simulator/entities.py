from game_simulator.config import config
from game_simulator import playeraction
from game_log import log

import numpy as np


# Base class for any entity, stores position, velocity, acceleration.
class Entity:
    def __init__(self, initial_position, initial_velocity, initial_acceleration, radius, bouncingquotient):
        self.pos = np.array(initial_position)
        self.vel = np.array(initial_velocity)

        self.radius = radius
        self.bouncingquotient = bouncingquotient

    # Get the Euclidian distance from self to obj
    def getDistanceTo(self, obj):
        return np.linalg.norm(obj.pos - self.pos)

    # Get the normalised vector pointing from self to obj
    def getDirectionTo(self, obj):
        return (obj.pos - self.pos) / self.getDistanceTo(obj)


class Player(Entity):
    def __init__(self, team, initial_position, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        Entity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                        config.PLAYER_RADIUS, config.PLAYER_BOUNCING)

        # Set the not random reset position
        self.default_position = initial_position

        # Initialise current action + can_kick which presents kick-spamming
        self.current_action = playeraction.Action()
        self.can_kick = True

        # Records the number of kicks the ball has made, used for reward shaping
        self.kick_count = 0

        # player properties
        self.team = team
        self.mass = 1 / config.PLAYER_INV_MASS

    def updatePosition(self):
        # Updates the position of the player while taking the player input into account
        # Damping effect when trying to kick the ball
        if self.current_action.isKicking() and self.can_kick:
            self.vel += self.current_action.getDirection() * config.KICK_ACCELARATION
        else:
            self.vel += self.current_action.getDirection() * config.ACCELARATION

        self.vel *= config.PLAYER_DAMPING
        self.pos += self.vel

    def reset(self, reset_type):
        if reset_type == "random":
        # positional parameters
            self.pos = np.array([config.PITCH_CORNER_X + (np.random.random_sample()) * 580,
                                 config.PITCH_CORNER_Y + (np.random.random_sample()) * 200]).astype(float)
        elif reset_type == "default":
            self.pos = self.default_position
        else:
            raise ValueError("Passed a wrong reset type to a player")

        self.vel = np.zeros(2)

        self.kick_count = 0

        # Set the action to default action state
        self.current_action = playeraction.Action()

    def log(self):
        return log.PlayerState(*self.pos, *self.vel, self.current_action)


class Ball(Entity):
    def __init__(self, initial_position, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        Entity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                        config.BALL_RADIUS, config.BALL_BOUNCING)

        # ball properties
        self.mass = 1 / config.BALL_INV_MASS
        self.inv_mass = config.BALL_INV_MASS

    def updatePosition(self):
        # Updates the position of the entity. Doesn't include any step duration for
        # whatever reason. God help us all
        self.vel *= config.BALL_DAMPING
        self.pos += self.vel

    def reset(self, reset_type):
        if reset_type == "random":
			# positional parameters
            self.pos = np.array([config.PITCH_CORNER_X + (np.random.random_sample()) * 580,
                                 config.PITCH_CORNER_Y + (np.random.random_sample()) * 200]).astype(float)
        elif reset_type == "default":
            self.pos = np.array([config.PITCH_CORNER_X + config.PITCH_WIDTH / 2,
                                 config.PITCH_CORNER_Y + config.PITCH_HEIGHT / 2])
        else:
            raise ValueError("Passed a wrong reset type to a ball")
        self.vel = np.zeros(2)

    def log(self):
        return log.BallState(self.pos[0], self.pos[1], self.vel[0], self.vel[1])


class GoalPost(Entity):
    def __init__(self, initial_position, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        Entity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                        config.GOALPOST_RADIUS, config.GOALPOST_BOUNCING_QUOTIENT)


class CentreCircleBlock(Entity):
    def __init__(self, initial_position, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        Entity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                        config.CENTRE_CIRCLE_RADIUS, 0)
