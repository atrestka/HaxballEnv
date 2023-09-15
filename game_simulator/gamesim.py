from game_simulator import playeraction, gameparams
from game_simulator.gamesimengine import GameSimEngine
from game_log import log

import numpy as np
import time

class GameSim(GameSimEngine):
    def __init__(self, red_player_count, blue_player_count, ball_count, printDebug = False, printDebugFreq = 600, print_score_update = False, \
                       auto_score = False, enforce_kickoff = False, seed = -1, rand_reset = True, max_steps = -1):
        GameSimEngine.__init__(self, red_player_count, blue_player_count, ball_count, enforce_kickoff, seed, rand_reset = rand_reset)

        # Sets extra information to do with. Probably a convention that I am
        self.rand_reset = rand_reset
        self.printDebug = printDebug
        self.printDebugFreq = printDebugFreq
        self.print_score_update = print_score_update
        self.auto_score = auto_score
        self.max_steps = max_steps

    def getSingeplayerReward(self):
        # Assumes a single red player
        if len(self.reds) + len(self.blues) > 1:
            raise ValueError("Too many players in GameSim!")

        player = self.reds[0]
        ball = self.balls[0]

        goals = self.checkGoals()
        reward = goals[0] - goals[1]

        if player.kick_count > 0:
            reward += 0.125
            if ball.pos[0] > gameparams.pitchcornerx + gameparams.pitchwidth / 2:
                relative = 2 * (ball.pos[0] - gameparams.pitchcornerx - gameparams.pitchwidth / 2) / gameparams.pitchwidth
                reward += 0.25 + 0.25 * relative

        return reward

    def getFeedback(self):
        # Gives feedback about the state of the game
        if self.printDebug:
            # Print some stuff
            print("Frame {}, score R-B: {}-{}".format(self.steps, self.red_score, self.blue_score))
            if self.was_point_scored:
                print("    A point was scored, nice!")
            for obj in self.reds:
                print("    red player at: {:.3f}; {:.3f} with velocity {:.3f}; {:.3f}".format(obj.pos[0], obj.pos[1], obj.vel[0], obj.vel[1]))
            for obj in self.blues:
                print("    blue player at: {:.3f}; {:.3f} with velocity {:.3f}; {:.3f}".format(obj.pos[0], obj.pos[1], obj.vel[0], obj.vel[1]))
            for obj in self.balls:
                print("    ball at: {:.3f}; {:.3f} with velocity {:.3f}; {:.3f}\n".format(obj.pos[0], obj.pos[1], obj.vel[0], obj.vel[1]))
        return

    def log(self):
        return log.Frame(
                blues = [p.log() for p in self.blues],
                reds  = [p.log() for p in self.reds ],
                balls = [b.log() for b in self.balls],
                )

    def giveCommands(self, actions):
        # Gives commands to all the controllable entities in the game in the form of a list pf commands.
        # Each command is a tuple of size 2 specifying direction (18 possible states) and then the kick state.
        # The position of the command in the list determines which entity the command is sent to.
        # TODO: Pls complete this function

        # NOTE: reds come before blues.
        for i in range(len(self.players)):
            self.players[i].current_action = actions[i]

    def printScoreUpdate(self):
        scores = self.checkGoals()
        if scores[0] + scores[1] > 0:
            print("score R-B: {}-{}".format(self.red_score + scores[0], self.blue_score + scores[1]))

    def step(self):
        self.steps += 1
        self.was_point_scored = False
        game_ended = False

        # Update positions
        self.updatePositions()
        # Handle collisions
        self.detectAndResolveCollisions()

        if self.print_score_update:
            self.printScoreUpdate()

        # Update the score of the game
        if self.auto_score:
            if self.rand_reset:
                game_ended = self.updateScore("random")
            else:
                game_ended = self.updateScore("all default")
        if self.max_steps != -1 and self.steps > self.max_steps:
            game_ended = True
            self.resetMap()

        if self.printDebug and self.steps % self.printDebugFreq == 0:
            self.getFeedback()

        return game_ended

    def run(self, disp, agents):
        while True:
            # Query each agent on what commands should be sent to the game simulator
            self.giveCommands([a.getAction(self.log()) for a in agents])

            self.step()

            if disp != None:
                # Update the graphical interface canvas
                disp.drawFrame(self.log())

                disp.getInput()

                if disp.rip:
                    disp.shutdown()
                    break
