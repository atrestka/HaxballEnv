from haxballgym.game_simulator.gamesimengine import GameSimEngine
from haxballgym.game_log import log
import numpy as np


class HaxballGameSim(GameSimEngine):
    def __init__(self, balls, goals, walls, other_rectangles, players, printDebug=False, printDebugFreq=600,
                 print_score_update=False,
                 auto_score=False, rand_reset=True, max_steps=-1,
                 auto_reset=True, seed=None):

        GameSimEngine.__init__(self, players, balls, goals, walls, other_rectangles, auto_reset, seed)

        # Sets extra information to do with. Probably a convention that I am
        self.rand_reset = rand_reset
        self.printDebug = printDebug
        self.printDebugFreq = printDebugFreq
        self.print_score_update = print_score_update
        self.auto_score = auto_score
        self.max_steps = max_steps
        self.players = players
        self.balls = balls
        self.goals = goals
        self.walls = walls
        self.other_recrangles = other_rectangles

        if self.rand_reset:
            self.resetMap()

    def log(self):
        return log.Frame(
            players=[p.log() for p in self.players],
            balls=[b.log() for b in self.balls],
            goalposts=[g.log() for g in self.goalposts],
            rectangles=[r.log() for r in self.walls],
            other_rectangles=[r.log() for r in self.other_rectangles],
            frame=self.steps
        )

    def giveCommands(self, actions):
        # Gives commands to all the controllable entities in the game in the form of a list pf commands.
        # Each command is a tuple of size 2 specifying direction (18 possible states) and then the kick state.
        # The position of the command in the list determines which entity the command is sent to.
        for i in range(len(self.players)):
            self.players[i].current_action = actions[i]

    def printScoreUpdate(self):
        scores = self.checkGoals()
        if sum(scores) > 0:
            print("score R-B: {}-{}".format(self.team_scores[0], self.team_scores[1]))

    def step(self):
        self.steps += 1
        self.resetTrackers()
        game_ended = False

        # Update positions
        self.updatePositions()
        # Handle collisions
        self.detectAndResolveCollisions()
        # update rectangle activity
        self.updateRectangleActivity()

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
        if game_ended is None:
            game_ended = False

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
        if len(self.balls) == 0:
            return 0.
        positions = [p.posToList(normalise=True)[0:2] for p in self.log().players if p.team == team]
        ball_positions = [b.posToList(normalise=True)[0:2] for b in self.log().balls]
        score = np.min([np.linalg.norm(np.array(x).flatten() - np.array(y).flatten())
                        for x in positions for y in ball_positions])
        return score
