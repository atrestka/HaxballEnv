import numpy as np
from haxballgym.game_log import log


# Base class for any CircleCircleEntity, stores position, velocity, acceleration.
class RectangleEntity:
    def __init__(self, top_left_pos, width, height, bouncingquotient, wall=True, active_criterion="player"):

        self.top_left_pos = top_left_pos
        self.width = width
        self.height = height
        self.bouncingquotient = bouncingquotient
        self.is_circle = False

        self.vertices = np.array([[top_left_pos[0], top_left_pos[1]],
                                  [top_left_pos[0], top_left_pos[1] + height],
                                  [top_left_pos[0] + height, top_left_pos[1]],
                                  [top_left_pos[0] + height, top_left_pos[1] + height]])

        self.radius = 0
        self.wall = wall
        self.active = False
        self.active_criterion = active_criterion

        if active_criterion != "player":
            raise ValueError("not implemented other active criteria yet!")

    # Get the Euclidian distance from self to obj
    def getDistanceTo(self, obj):
        closest_rect_point = self.proj_into_rect(obj)
        return np.linalg.norm(obj.pos - closest_rect_point)

    def proj_into_rect(self, obj):
        closest_rect_point = np.array([np.clip(obj.pos[0],
                                       self.top_left_pos[0],
                                       self.top_left_pos[0] + self.width),
                                       np.clip(obj.pos[1],
                                       self.top_left_pos[1],
                                       self.top_left_pos[1] + self.height)])
        return closest_rect_point.reshape((obj.pos.shape))

    # Get the normalised vector pointing from self to obj
    def getDirectionTo(self, obj):
        closest_rect_point = self.proj_into_rect(obj)
        return (obj.pos - closest_rect_point) / self.getDistanceTo(obj)

    def log(self):
        return log.RectangleState(self.top_left_pos[0], self.top_left_pos[1], self.width, self.height, self.active)

    def checkEntityOnTopOf(self, obj):
        closest_point = self.proj_into_rect(obj)
        if np.linalg.norm(closest_point - obj.pos) < 1e-6:
            return True
        return False

