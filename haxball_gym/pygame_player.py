import os

from haxball_gym.game_displayer import basicdisplayer
from haxball_gym.config import config
from haxball_gym.game_simulator import gamesim
from haxball_gym.game_log import log
from haxball_gym.game_displayer import movedisplayer


def play_visual_games(
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

    red_debug_surf = movedisplayer.DebugSurf()
    blue_debug_surf = movedisplayer.DebugSurf()

    if not suppress_display:
        display = basicdisplayer.GameWindow(config.WINDOW_WIDTH + 2 * 256, config.WINDOW_HEIGHT,
                                            debug_surfs=[red_debug_surf.surf, blue_debug_surf.surf])
    else:
        display = None

    agents = red_agents + blue_agents
    for agent in agents:
        if suppress_display and agent.requires_human_input:
            raise ValueError("Human players need display to function")
        if agent.requires_human_input and agent.gui is None:
            agent.gui = display

    config.NUM_RED_PLAYERS = len(red_agents)
    config.NUM_BLUE_PLAYERS = len(blue_agents)

    game = gamesim.GameSim(config.NUM_RED_PLAYERS, config.NUM_BLUE_PLAYERS,
                           config.NUM_BALLS, printDebug=print_debug,
                           print_score_update=not suppress_scorekeeping,
                           auto_score=auto_score,
                           rand_reset=rand_reset,
                           max_steps=max_steps)

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
            game.giveCommands([a.getAction(game.log()) for a in agents])

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
