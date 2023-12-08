from haxball_gym.pygame_player import play_visual_games


def play_arena_games(red_agents, blue_agents, games, step_len=1, max_steps=200, randStart=False):
    red_wins, blue_wins = play_visual_games(
        red_agents,
        blue_agents,
        print_debug=None,
        auto_score=True,
        rand_reset=randStart,
        max_steps=max_steps,
        max_games=games,
        save_dir=None,
        save_master_dir='',
        save_step_length=1,
        suppress_display=True,
        suppress_scorekeeping=True,
        step_length=step_len
    )
    print("Final score:")
    print("Red:" + str(red_wins))
    print("Blue:" + str(blue_wins))
    return red_wins, blue_wins
