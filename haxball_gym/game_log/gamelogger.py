import haxball_gym.game_simulator.gamesim as gs
from haxball_gym.config import config
from haxball_gym.game_displayer import basicdisplayer
from haxball_gym.agents import humanagent
from haxball_gym.game_log import log
import pygame


def recordPlayerGames(dest, games_to_play=10):
    disp = basicdisplayer.GameWindow(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    blue_agent = humanagent.HumanAgent(('w', 'd', 's', 'a', 'LSHIFT'), disp)
    red_agent = humanagent.HumanAgent(('UP', 'RIGHT', 'DOWN', 'LEFT', 'RCTRL'), disp)
    pygame.init()

    for game_number in range(games_to_play):
        sim = gs.GameSim(1, 1, 1)
        game_done = False
        game_log = log.Game()
        while not game_done:
            disp.updateKeys()
            red_move = red_agent.getAction()
            blue_move = blue_agent.getAction()

            sim.giveCommands([red_move, blue_move])
            sim.step()

            game_log.append(sim.log())

            disp.drawFrame(sim.log())

            goals = sim.checkGoals()
            if sum(goals) > 0:
                game_done = True
                game_log.red_goals = goals[0]
                game_log.blue_goals = goals[1]

            disp.getInput()
            if disp.rip:
                return
        game_log.save(f"{dest}/{game_number}")
