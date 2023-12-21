from haxballgym.config import config

import numpy as np


class GameSimEngine():
    def __init__(self, players, balls, goals, walls, other_rectangles, auto_reset=True, seed=-1):
        # Intialise the entities
        self.players = players
        self.balls = balls
        self.goals = goals
        self.walls = walls
        self.other_rectangles = other_rectangles
        self.auto_reset = auto_reset

        self.goals_left = [g for g in self.goals if g.side == "left"]
        self.goals_right = [g for g in self.goals if g.side == "right"]
        self.goals_top = [g for g in self.goals if g.side == "top"]
        self.goals_bottom = [g for g in self.goals if g.side == "bottom"]

        # Create useful groupings
        self.moving_objects = self.players + self.balls

        self.num_teams = len(np.unique([p.team for p in self.players] + [g.team for g in self.goals]))

        # Game state info
        self.team_scores = [0 for _ in range(self.num_teams)]

        # Number of elapsed frames
        self.steps = 0

        # Initialise the random seed iff seed != 1
        if seed != -1:
            np.random.seed(seed)

        # goalposts
        self.goalposts = sum([goal.goalposts for goal in self.goals], [])

    def getRandomPositionInThePlayingField(self):
        return np.array([np.random.random_sample() * 840, np.random.random_sample() * 400]).astype(float)

    def getRandomPositionInThePitch(self):
        return np.array([config.PITCH_CORNER_X + np.random.random_sample() * 580,
                         config.PITCH_CORNER_Y + np.random.random_sample() * 200]).astype(float)

    def bounceInPitch(self, obj, movement_space_x, movement_space_y):

        if obj.pos[0] <= movement_space_x[0]:
            obj.vel[0] = - 0.5 * obj.vel[0]
            obj.pos[0] = movement_space_x[0] + (movement_space_x[0] - obj.pos[0]) / 2

        if obj.pos[0] >= movement_space_x[1]:
            obj.vel[0] = - 0.5 * obj.vel[0]
            obj.pos[0] = movement_space_x[1] + (movement_space_x[1] - obj.pos[0]) / 2

        if obj.pos[1] <= movement_space_y[0]:
            obj.vel[1] = - 0.5 * obj.vel[1]
            obj.pos[1] = movement_space_y[0] + (movement_space_y[0] - obj.pos[1]) / 2

        if obj.pos[1] >= movement_space_y[1]:
            obj.vel[1] = - 0.5 * obj.vel[1]
            obj.pos[1] = movement_space_y[1] + (movement_space_y[1] - obj.pos[1]) / 2

    def keepEntityInMovementSpace(self, obj, is_ball=0):
        # should keep things on the board where the movement happens

        if not is_ball:

            movement_space_x = [obj.radius, config.WINDOW_WIDTH - obj.radius]
            movement_space_y = [obj.radius, config.WINDOW_HEIGHT - obj.radius]

            if obj.pos[0] <= movement_space_x[0] or obj.pos[0] >= movement_space_x[1]:
                obj.vel[0] = 0
                if obj.pos[0] <= movement_space_x[0]:
                    obj.pos[0] = movement_space_x[0]
                if obj.pos[0] >= movement_space_x[1]:
                    obj.pos[0] = movement_space_x[1]
            if obj.pos[1] <= movement_space_y[0] or obj.pos[1] >= movement_space_y[1]:
                obj.vel[1] = 0
                if obj.pos[1] <= movement_space_y[0]:
                    obj.pos[1] = movement_space_y[0]
                if obj.pos[1] >= movement_space_y[1]:
                    obj.pos[1] = movement_space_y[1]

        else:

            movement_space_x = [config.PITCH_CORNER_X + obj.radius, config.WINDOW_WIDTH - config.PITCH_CORNER_X
                                - obj.radius]
            movement_space_y = [config.PITCH_CORNER_Y + obj.radius, config.WINDOW_HEIGHT - config.PITCH_CORNER_Y
                                - obj.radius] 
            nobounce = False

            if obj.pos[0] <= movement_space_x[0]:
                for goal in self.goals_left:
                    if obj.pos[1] >= config.PITCH_CORNER_Y + goal.position and \
                            obj.pos[1] <= config.PITCH_CORNER_Y + goal.position + goal.size:
                        nobounce = True

            if obj.pos[0] >= movement_space_x[1]:
                for goal in self.goals_right:
                    if obj.pos[1] >= config.PITCH_CORNER_Y + goal.position and \
                            obj.pos[1] <= config.PITCH_CORNER_Y + goal.position + goal.size:
                        nobounce = True

            if obj.pos[1] <= movement_space_y[0]:
                for goal in self.goals_top:
                    if obj.pos[0] >= config.PITCH_CORNER_X + goal.position and \
                            obj.pos[0] <= config.PITCH_CORNER_X + goal.position + goal.size:
                        nobounce = True

            if obj.pos[1] >= movement_space_y[1]:
                for goal in self.goals_bottom:
                    if obj.pos[0] >= config.PITCH_CORNER_X + goal.position and \
                            obj.pos[0] <= config.PITCH_CORNER_X + goal.position + goal.size:
                        nobounce = True

            if not nobounce:
                self.bounceInPitch(obj, movement_space_x, movement_space_y)

    def makeEntityHitBall(self, obj, ball):
        # Updates the ball's velocity since a kick call was called from obj to ball
        ball.vel = ball.vel + config.KICK_STRENGTH * ball.inv_mass * obj.getDirectionTo(ball)
        # Update the number of collisions the player has made
        obj.kick_count += 1

        return

    def resolveCollisionBetweenCircles(self, obj1, obj2, is_obj1_static=0):
        # if there is a collision between the two objects, resolve it. Assumes two circles
        # Has flag for the case where obj2 is static and doesn't get any momentum
        direction = (obj1.pos - obj2.pos)
        distance = (np.linalg.norm(direction))

        # if the objects aren't overlapping, don't even bother resolving
        if distance > obj1.radius + obj2.radius:
            return False

        # calculates normal and tangent vectors
        collisionnormal = direction / distance
        collisiontangent = np.array([direction[1], - direction[0]]) / (np.linalg.norm(direction))

        if collisionnormal[0] is np.NaN:
            raise ValueError()

        bouncingq = obj1.bouncingquotient * obj2.bouncingquotient
        if not is_obj1_static:
            centerofmass = (obj1.pos * obj1.mass + obj2.pos * obj2.mass) / (obj1.mass + obj2.mass)

            # updates object components
            obj1normalvelocity = np.dot(np.array(obj1.vel), collisionnormal)
            obj2normalvelocity = np.dot(np.array(obj2.vel), collisionnormal)

            # inelastic collision formula
            obj1newnormalvelocity = (bouncingq * obj2.mass * (obj2normalvelocity - obj1normalvelocity)
                                     + obj1.mass * obj1normalvelocity + obj2.mass * obj2normalvelocity) \
                / (obj1.mass + obj2.mass)
            obj2newnormalvelocity = (bouncingq * obj1.mass * (obj1normalvelocity - obj2normalvelocity)
                                     + obj2.mass * obj2normalvelocity + obj1.mass * obj1normalvelocity) \
                / (obj2.mass + obj1.mass)
            obj1tangentvelocity = np.dot(np.array(obj1.vel), collisiontangent)
            obj2tangentvelocity = np.dot(np.array(obj2.vel), collisiontangent)

            obj1.vel = obj1newnormalvelocity * np.array(collisionnormal) \
                + obj1tangentvelocity * np.array(collisiontangent)
            obj2.vel = obj2newnormalvelocity * np.array(collisionnormal) \
                + obj2tangentvelocity * np.array(collisiontangent)

            obj1.pos = centerofmass + ((obj1.radius + obj2.radius)
                                       + bouncingq * (obj1.radius + obj2.radius - distance)) \
                * collisionnormal * obj2.mass / (obj1.mass + obj2.mass)
            obj2.pos = centerofmass - ((obj1.radius + obj2.radius)
                                       + bouncingq * (obj1.radius + obj2.radius - distance)) \
                * collisionnormal * obj1.mass / (obj1.mass + obj2.mass)
        else:
            # updates obj2 components since that's the only moving part
            obj1normalvelocity = np.dot(np.array(obj1.vel), collisionnormal)
            obj2normalvelocity = np.dot(np.array(obj2.vel), collisionnormal)
            velocityafter = (obj1normalvelocity + obj2normalvelocity) * bouncingq * 2

            obj1tangentvelocity = np.dot(np.array(obj1.vel), collisiontangent)
            obj2tangentvelocity = np.dot(np.array(obj2.vel), collisiontangent)

            obj1.vel = - velocityafter * np.array(collisionnormal) + obj1tangentvelocity * np.array(collisiontangent)
            obj2.vel = velocityafter * np.array(collisionnormal) + obj2tangentvelocity * np.array(collisiontangent)

            obj2.pos = obj1.pos - collisionnormal * (obj1.radius + obj2.radius)

            return True

    def resolveCollisionBetweenCircleAndWall(self, wall, circle):

        # if there is a collision between the two objects, resolve it. Assumes two circles
        # Has flag for the case where obj2 is static and doesn't get any momentum
        direction = wall.getDirectionTo(circle)
        distance = wall.getDistanceTo(circle)
        closestwallpoint = wall.proj_into_rect(circle)

        # if the objects aren't overlapping, don't even bother resolving
        if distance > circle.radius:
            return False

        # calculates normal and tangent vectors
        collisionnormal = direction

        collisiontangent = np.array([direction[1], - direction[0]]) / (np.linalg.norm(direction))

        if collisionnormal[0] is np.NaN:
            raise ValueError()

        bouncingq = circle.bouncingquotient * wall.bouncingquotient

        # updates obj2 components since that's the only moving part
        obj1normalvelocity = np.dot(np.array(circle.vel), collisionnormal)
        obj2normalvelocity = 0
        velocityafter = (obj1normalvelocity + obj2normalvelocity) * bouncingq * 2

        obj1tangentvelocity = np.dot(np.array(circle.vel), collisiontangent)

        circle.vel = - velocityafter * np.array(collisionnormal) + obj1tangentvelocity * np.array(collisiontangent)
        circle.pos = closestwallpoint + collisionnormal * (circle.radius)

        return True

    def resolveCollision(self, obj1, obj2, is_obj1_static=0):
        if obj1.is_circle:
            return self.resolveCollisionBetweenCircles(obj1, obj2, is_obj1_static)
        else:
            return self.resolveCollisionBetweenCircleAndWall(obj1, obj2)

    def detectAndResolveCollisions(self):
        # Handle ALL the collision in the sim, including borders, entities etc.

        # blocks the players that aren't kicking off from entering the centre/other half

        # Keep all the players within the playing field
        for player in self.players:
            self.keepEntityInMovementSpace(player, 0)
        # And same for the balls. Keep in mind they have a different field size
        for ball in self.balls:
            self.keepEntityInMovementSpace(ball, 1)

        # Handle moving object - moving object collisions
        for i in range(len(self.moving_objects)):
            for j in range(i + 1, len(self.moving_objects)):
                self.resolveCollision(self.moving_objects[i], self.moving_objects[j])

        # Handle moving object - goal post collisions
        for thing in self.moving_objects:
            for goalpost in self.goalposts:
                self.resolveCollision(goalpost, thing, 1)

        for wall in self.walls:
            for thing in self.moving_objects:
                self.resolveCollision(wall, thing, 1)

        # Handle ball kicks
        for player in self.players:
            for ball in self.balls:
                if player.getDistanceTo(ball) <= player.radius + ball.radius + 4:

                    if player.current_action.isKicking() and player.can_kick:
                        self.makeEntityHitBall(player, ball)
                        player.can_kick = False

            if not player.current_action.isKicking():
                player.can_kick = True

    def updatePositions(self):
        # Update all the positions of the entities, no collision detection
        for entity in self.moving_objects:
            entity.updatePosition()

    def resetMap(self, reset_type="random"):
        # Reset the positions of the entities in the sim. Possible reset options are:
        # 1) random reset for all moving entities
        # 2) ball spawned in center, players randomly
        # 3) all entities are respawned in default positions TODO: Hasn't been implemented
        self.steps = 0
        if reset_type == "random":
            for obj in self.moving_objects:
                obj.reset("random")
        elif reset_type == "ball center, players random":
            for obj in self.players:
                obj.reset("random")
            for obj in self.balls:
                obj.reset("default")
        elif reset_type == "all default":
            for obj in self.moving_objects:
                obj.reset("default")
        else:
            raise ValueError("Passed a wrong reset type to GameSim")
        return

    def updateScore(self, reset_params="random"):
        # TODO: Fuck this.
        goals = self.checkGoals()
        for i in range(len(self.team_scores)):
            self.team_scores[i] += goals[i]

        if sum(goals) > 0:
            self.was_point_scored = True
            if self.auto_reset:
                self.resetMap(reset_params)
            return True

        add_points = self.additionalPointCheck()
        if sum(add_points) > 0:
            self.was_point_scored = True
            if self.auto_reset:
                self.resetMap(reset_params)
            return True

    def additionalPointCheck(self):
        return [0]

    def resetTrackers(self):
        self.was_point_scored = False
        # Resets trackers about the game at the start of an env step
        self.was_ball_touched_blue = False
        self.was_ball_touched_red = False

    def checkGoals(self):
        goals = [0 for _ in range(len(self.team_scores))]

        movement_space_x = [config.PITCH_CORNER_X + config.BALL_RADIUS, config.WINDOW_WIDTH - config.PITCH_CORNER_X
                            - config.BALL_RADIUS]
        movement_space_y = [config.PITCH_CORNER_Y + config.BALL_RADIUS, config.WINDOW_HEIGHT - config.PITCH_CORNER_Y
                            - config.BALL_RADIUS] 

        for obj in self.balls:
            if obj.pos[0] <= movement_space_x[0]:

                for goal in self.goals_left:
                    if obj.pos[1] >= config.PITCH_CORNER_Y + goal.position and \
                            obj.pos[1] <= config.PITCH_CORNER_Y + goal.position + goal.size:
                        goals[goal.team] = 1

            if obj.pos[0] >= movement_space_x[1]:
                for goal in self.goals_right:
                    if obj.pos[1] >= config.PITCH_CORNER_Y + goal.position and \
                            obj.pos[1] <= config.PITCH_CORNER_Y + goal.position + goal.size:
                        goals[goal.team] = 1

            if obj.pos[1] <= movement_space_y[0]:
                for goal in self.goals_top:
                    if obj.pos[0] >= config.PITCH_CORNER_X + goal.position and \
                            obj.pos[0] <= config.PITCH_CORNER_X + goal.position + goal.size:
                        goals[goal.team] = 1

            if obj.pos[1] >= movement_space_y[1]:
                for goal in self.goals_bottom:
                    if obj.pos[0] >= config.PITCH_CORNER_X + goal.position and \
                            obj.pos[0] <= config.PITCH_CORNER_X + goal.position + goal.size:
                        goals[goal.team] = 1
        return goals

    def updateRectangleActivity(self):
        for rect in self.other_rectangles:
            rect.active = False
            if rect.active_criterion == "player":
                for player in self.players:
                    if rect.checkEntityOnTopOf(player):
                        rect.active = True
