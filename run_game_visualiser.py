import argparse
import haxballgym
from haxball_baselines.agents.baseline_a2c_agent import A2CBaselineAgent
from haxball_baselines.agents.baseline_ppo_agent import PPOBaselineAgent



# Example command line code:
#   python game_visualiser.py --red-model="trained_fixed_v1" --blue-model="arun_v4" --suppress-display

def parse_from_cmd():
    parser = argparse.ArgumentParser(description='Visualise different matchups between agents')
    parser.add_argument(
        '--seed', type=int, default=-1, help='random seed (default: -1)')
    parser.add_argument(
        '--red-human',
        action="store_true",
        help='Does the red team have a human player?')
    parser.add_argument(
        '--blue-human',
        action="store_true",
        help='Does the blue team have a human player?')
    parser.add_argument(
        '--load-dir',
        default='models/',
        help='directory to load the agents from (default models/)')
    parser.add_argument(
        '--red-model',
        default=None,
        help='Specify the model of the red team if there is any')
    parser.add_argument(
        '--blue-model',
        default=None,
        help='Specify the model of the blue team if there is any')
    parser.add_argument(
        '--red-normalised',
        action="store_true",
        help='Specify whether the model of the red team takes normalised input or not')
    parser.add_argument(
        '--blue-normalised',
        action="store_true",
        help='Specify whether the model of the blue team takes normalised input or not')
    parser.add_argument(
        '--print-debug',
        action="store_true",
        help='Specify whether debug info should be printed or not')
    parser.add_argument(
        '--not-auto-score',
        dest="auto_score",
        action="store_false",
        help='Specify whether the game should autoscore goals')
    parser.add_argument(
        '--not-rand-reset',
        dest="rand_reset",
        action="store_false",
        help='Specify whether gamesim places entities randomly when reseting')
    parser.add_argument(
        '--suppress-scorekeeping',
        action="store_true",
        help='Specify whether gamesim should print scores to terminal')
    parser.add_argument(
        '--suppress-display',
        action="store_true",
        help='Specify whether the display of the game should be suppressed or not')
    parser.add_argument(
        '--max-steps',
        type=int,
        default=-1,
        help='Specify the maximum number of steps in gamesim per game')
    parser.add_argument(
        '--step-length',
        type=int,
        default=1,
        help='Specify the number of steps per action received from the models')
    parser.add_argument(
        '--save-master-dir',
        type=str,
        default="recorded_games",
        help='Specify the subdirectory where all the recorded games folders are gonna be saved in')
    parser.add_argument(
        '--save-dir',
        type=str,
        default="None",
        help='Specify the name of the directory where the current sessions is gonna be saved in')
    parser.add_argument(
        '--save-step-length',
        type=int,
        default=-1,
        help='Specify the saving step length. Defaults to step length')
    parser.add_argument(
        '--max-games',
        type=int,
        default=2147483648,
        help='Specify the number of games to be played. Defaults to infinity')

    args = parser.parse_args()
    return args


default_red_bindings = ('w', 'd', 's', 'a', 'c')
default_blue_bindings = ('i', 'l', 'k', 'j', '.')

red_agent = haxballgym.HumanAgent(default_red_bindings)
red_random = haxballgym.RandomAgent(10)
blue_agent = haxballgym.HumanAgent(default_blue_bindings)
blue_random = haxballgym.RandomAgent(10)
idle_agent = haxballgym.IdleAgent()
bot_agent = A2CBaselineAgent('/Users/stefanclarkework/Desktop/HaxballEnv/haxball_baselines/models/A2C_example.zip',
                             15,
                             haxballgym.SinglePlayerEnvironment())
ppo_agent = PPOBaselineAgent('/Users/stefanclarkework/Desktop/HaxballEnv/haxball_baselines/models/PPO_example3.zip',
                             15,
                             haxballgym.SinglePlayerEnvironment())

haxballgym.play_visual_games(red_agents=[ppo_agent], blue_agents=[], print_debug=True)
