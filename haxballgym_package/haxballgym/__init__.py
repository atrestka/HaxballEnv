from haxballgym.config import config
from haxballgym.environments.env import HaxballGymEnvironment
from haxballgym.environments.single_player_env import SinglePlayerEnvironment
from haxballgym.environments.loaded_opponent_env import LoadedOpponentEnv
from haxballgym.agents.humanagent import HumanAgent
from haxballgym.agents.idleagent import IdleAgent
from haxballgym.agents.randomagent import RandomAgent
from haxballgym.agents.templatenumpyagent import TemplateAgent
from haxballgym.pygame_player import play_visual_games
from haxballgym.arena import play_arena_games
from gym.envs.registration import register

register(
    id='HaxballSinglePlayer-v0',
    entry_point='haxballgym.environments.single_player_env:SinglePlayerEnvironment',
    max_episode_steps=300,
)
