from haxballgym.config import config
from haxballgym.game_simulator.gamesimengine import GameSimEngine
from haxballgym.game_log import log
import numpy as np


class GameSim(GameSimEngine):
    def __init__(self, red_player_count, blue_player_count, ball_count, printDebug=False, printDebugFreq=600,
                 print_score_update=False, auto_score=False, enforce_kickoff=False, seed=-1,
                 rand_reset=True, max_steps=-1):
        GameSimEngine.__init__(self, red_player_count, blue_player_count, ball_count, enforce_kickoff, seed,
                               rand_reset=rand_reset)

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
            if ball.pos[0] > config.PITCH_CORNER_X + config.PITCH_WIDTH / 2:
                relative = 2 * (ball.pos[0] - config.PITCH_CORNER_X - config.PITCH_WIDTH / 2) / config.PITCH_WIDTH
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
                print("    red player at: {:.3f}; {:.3f} with velocity {:.3f}; {:.3f}".format(obj.pos[0], obj.pos[1],
                                                                                              obj.vel[0], obj.vel[1]))
            for obj in self.blues:
                print("    blue player at: {:.3f}; {:.3f} with velocity {:.3f}; {:.3f}".format(obj.pos[0], obj.pos[1],
                                                                                               obj.vel[0], obj.vel[1]))
            for obj in self.balls:
                print("    ball at: {:.3f}; {:.3f} with velocity {:.3f}; {:.3f}\n".format(obj.pos[0], obj.pos[1],
                                                                                          obj.vel[0], obj.vel[1]))
        return

    def log(self):
        return log.Frame(
            blues=[p.log() for p in self.blues],
            reds=[p.log() for p in self.reds],
            balls=[b.log() for b in self.balls],
            frame=self.steps
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
        self.resetTrackers()
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

            if disp is not None:
                # Update the graphical interface canvas
                disp.drawFrame(self.log())

                disp.getInput()

                if disp.rip:
                    disp.shutdown()
                    break

    def cloneGameState(self, other_gamesim):
        pass

    def getBallProximityScore(self, team):
        # gets the minimum distance from the players on a given team to a ball
        if team == "red":
            positions = [self.log().posToNp(myTeam="red", me=0)[2 * i: 2 * i + 2]
                         for i in range(config.NUM_RED_PLAYERS)]
            ball_positions = [b.posToList(myTeam="red", normalise=True)[0:2]
                              for b in self.log().balls]
        elif team == "blue":
            positions = [self.log().posToNp(myTeam="blue", me=0)[4 * i: 4 * i + 2]
                         for i in range(config.NUM_BLUE_PLAYERS)]
            ball_positions = [b.posToList(myTeam="blue", normalise=True)[0:2]
                              for b in self.log().balls]
        score = np.min([np.linalg.norm(np.array(x).flatten() - np.array(y).flatten())
                        for x in positions for y in ball_positions])
        return score