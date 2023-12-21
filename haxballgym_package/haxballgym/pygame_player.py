import os

from haxballgym.game_displayer import basicdisplayer
from haxballgym.config import config
from haxballgym.haxball import haxball
from haxballgym.penny_matching import pennymatching
from haxballgym.game_log import log


def game_visualizer(
        gamesim,
        agents,
        max_games=2147483648,
        save_dir=None,
        save_master_dir='',
        save_step_length=1,
        suppress_display=False,
        step_length=1
):

    if not suppress_display:
        display = basicdisplayer.GameWindow(config.WINDOW_WIDTH + 2 * 256, config.WINDOW_HEIGHT)
    else:
        display = None

    for agent in agents:
        if suppress_display and agent.requires_human_input:
            raise ValueError("Human players need display to function")
        if agent.requires_human_input and agent.gui is None:
            agent.gui = display

    game = gamesim

    red_wins = 0
    blue_wins = 0

    # Run the game
    for game_number in range(max_games):
        exit_loop = False
        # Initialise the game logger if needed
        if save_dir is not None:
            game_logger = log.Game()
            if save_step_length == -1:
                save_step_length = step_length
            save_counter = 0

            if not os.path.exists(f"{save_master_dir}"):
                os.makedirs(f"{save_master_dir}")

        while True:
            game_ended = False

            # Query each agent on what commands should be sent to the game simulator
            if display is not None:
                display.getInput()
            game.giveCommands(sum([a.getAction(game.log()) for a in agents], []))

            for i in range(step_length):
                game_ended = game_ended or game.step()

                # Append a frame to the game_logger if enabled
                if save_dir is not None:
                    save_counter += 1
                    if save_counter == save_step_length:
                        save_counter = 0
                        game_logger.append(game.log())

                if game_ended:
                    # save winner
                    if game.red_score > game.blue_score:
                        red_wins += 1
                    elif game.blue_score > game.red_score:
                        blue_wins += 1

                    # Save the game logger data if enabled
                    if save_dir is not None:
                        if not os.path.exists(f"{save_master_dir}/{save_dir}"):
                            os.makedirs(f"{save_master_dir}/{save_dir}")
                        game_logger.save(f"{save_master_dir}/{save_dir}/{game_number}")
                    break

            if game_ended:
                break

            if display is not None:
                # Update the graphical interface canvas
                display.drawFrame(game.log())

                if display.rip:
                    display.shutdown()
                    exit_loop = True
                    break
        if exit_loop:
            break

    return red_wins, blue_wins


def play_visual_games_2team(
        red_agents,
        blue_agents,
        print_debug=None,
        auto_score=True,
        rand_reset=True,
        max_steps=2147483648,
        max_games=2147483648,
        save_dir=None,
        save_master_dir='',
        save_step_length=1,
        suppress_display=False,
        suppress_scorekeeping=False,
        step_length=1
):

    agents = red_agents + blue_agents

    config.TEAM_NUMBERS = [len(red_agents), len(blue_agents)]

    game = haxball.TwoTeamHaxballGamesim(len(red_agents), len(blue_agents),
                                         config.NUM_BALLS, printDebug=print_debug,
                                         print_score_update=not suppress_scorekeeping,
                                         auto_score=auto_score,
                                         rand_reset=rand_reset,
                                         max_steps=max_steps)

    game_visualizer(
        game,
        agents,
        max_games,
        save_dir,
        save_master_dir,
        save_step_length,
        suppress_display,
        step_length
    )


def play_visual_games_4team(
        red_agents,
        blue_agents,
        orange_agents,
        green_agents,
        print_debug=None,
        auto_score=True,
        rand_reset=True,
        max_steps=2147483648,
        max_games=2147483648,
        save_dir=None,
        save_master_dir='',
        save_step_length=1,
        suppress_display=False,
        suppress_scorekeeping=False,
        step_length=1
):

    agents = red_agents + blue_agents + orange_agents + green_agents

    config.TEAM_NUMBERS = [len(red_agents), len(blue_agents), len(orange_agents), len(green_agents)]

    game = haxball.FourTeamHaxballGameSim(len(red_agents), len(blue_agents),
                                          len(orange_agents), len(green_agents),
                                          config.NUM_BALLS, printDebug=print_debug,
                                          print_score_update=not suppress_scorekeeping,
                                          auto_score=auto_score,
                                          rand_reset=rand_reset,
                                          max_steps=max_steps)

    game_visualizer(
        game,
        agents,
        max_games,
        save_dir,
        save_master_dir,
        save_step_length,
        suppress_display,
        step_length
    )


def play_visual_games_pennymatching(
        red_agents,
        blue_agents,
        print_debug=None,
        auto_score=True,
        rand_reset=True,
        max_steps=2147483648,
        max_games=2147483648,
        save_dir=None,
        save_master_dir='',
        save_step_length=1,
        suppress_display=False,
        suppress_scorekeeping=False,
        step_length=1
):

    agents = red_agents + blue_agents

    config.TEAM_NUMBERS = [len(red_agents), len(blue_agents)]

    game = pennymatching.PennyMatchingGameSim()

    game_visualizer(
        game,
        agents,
        max_games,
        save_dir,
        save_master_dir,
        save_step_length,
        suppress_display,
        step_length
    )