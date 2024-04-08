from haxballgym.config import config
from haxballgym.game_simulator import playeraction
from haxballgym.game_log import log
import copy
import numpy as np


# Base class for any CircleCircleEntity, stores position, velocity, acceleration.
class CircleEntity:
    def __init__(self, initial_position, initial_velocity, initial_acceleration, radius, bouncingquotient):
        self.pos = np.array(initial_position)
        self.vel = np.array(initial_velocity)

        self.radius = radius
        self.bouncingquotient = bouncingquotient
        self.is_circle = True

    # Get the Euclidian distance from self to obj
    def getDistanceTo(self, obj):
        return np.linalg.norm(obj.pos - self.pos)

    # Get the normalised vector pointing from self to obj
    def getDirectionTo(self, obj):
        return (obj.pos - self.pos) / self.getDistanceTo(obj)


class Player(CircleEntity):
    def __init__(self, team, initial_position, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        CircleEntity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                              config.PLAYER_RADIUS, config.PLAYER_BOUNCING)

        # Set the not random reset position
        self.default_position = copy.deepcopy(initial_position)

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
    
    #define method for obtaining global seed
    def get_seed(self):
        from haxballgym.environments.env import global_rng
        return global_rng
    
    #define method for accessing global seed and creating a random uniform sample with PCG64 algorithm random number generator
    def uniPCG64(self, low_bound, high_bound): 
        uniGlobal = self.get_seed()
        x = uniGlobal.uniform(low = float(low_bound), high = float(high_bound))
        return x

    def reset(self, reset_type):
        if reset_type == "random":  # positional parameters
            self.pos = np.array([config.PITCH_CORNER_X + self.uniPCG64(0,580),
                                 config.PITCH_CORNER_Y + self.uniPCG64(0,200)]).astype(float)

        elif reset_type == "default":
            self.pos = copy.copy(self.default_position)
        else:
            raise ValueError("Passed a wrong reset type to a player")

        self.vel = np.zeros(2)

        self.kick_count = 0

        # Set the action to default action state
        self.current_action = playeraction.Action()

    def log(self):
        return log.PlayerState(*self.pos, *self.vel, self.current_action, team=self.team)


class Ball(CircleEntity):
    def __init__(self, initial_position, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        CircleEntity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                              config.BALL_RADIUS, config.BALL_BOUNCING)

        # ball properties
        self.mass = 1 / config.BALL_INV_MASS
        self.inv_mass = config.BALL_INV_MASS

    def updatePosition(self):
        # Updates the position of the CircleEntity. Doesn't include any step duration for
        # whatever reason. God help us all
        self.vel *= config.BALL_DAMPING
        self.pos += self.vel
        #define method for obtaining global seed
    
    def get_seed(self):
        from haxballgym.environments.env import global_rng
        return global_rng
    
    #define method for accessing global seed and creating a random uniform sample with PCG64 algorithm random number generator
    def uniPCG64(self, low_bound, high_bound): 
        uniGlobal = self.get_seed()
        x = uniGlobal.uniform(low = float(low_bound), high = float(high_bound))
        return x

    def reset(self, reset_type):
        if reset_type == "random":  # positional parameters
            self.pos = np.array([config.PITCH_CORNER_X + self.uniPCG64(0,580),
                                 config.PITCH_CORNER_Y + self.uniPCG64(0,200)]).astype(float)

        elif reset_type == "default":
            self.pos = np.array([config.PITCH_CORNER_X + config.PITCH_WIDTH / 2,
                                 config.PITCH_CORNER_Y + config.PITCH_HEIGHT / 2])
        else:
            raise ValueError("Passed a wrong reset type to a ball")
        self.vel = np.zeros(2)

    def log(self):
        return log.BallState(self.pos[0], self.pos[1], self.vel[0], self.vel[1])


class GoalPost(CircleEntity):
    def __init__(self, initial_position, team, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        CircleEntity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                              config.GOALPOST_RADIUS, config.GOALPOST_BOUNCING_QUOTIENT)
        self.team = team

    def log(self):
        return log.GoalpostState(self.pos[0], self.pos[1], self.team)


class CentreCircleBlock(CircleEntity):
    def __init__(self, initial_position, initial_velocity=np.zeros(2), initial_acceleration=np.zeros(2)):
        # Initialise positional parameters, basic properties of the object
        CircleEntity.__init__(self, initial_position, initial_velocity, initial_acceleration,
                              config.CENTRE_CIRCLE_RADIUS, 0)
