import haxballgym
from haxball_baselines.agents.baseline_ppo_agent import PPOBaselineAgent
from haxball_baselines.agents.baseline_DQN_agent import DQNBaselineAgent
from haxball_ai.model import ActorCriticAgent
from haxball_ai.envs import get_2p_env

# human agent with WASD key bindings
human_agent = haxballgym.HumanAgent(team="red")

# random motion agent
red_random = haxballgym.RandomAgent(10)

# agent which does nothing
idle_agent = haxballgym.IdleAgent()

"""
# PPO-trained agent
ppo_agent = PPOBaselineAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_baselines/models/PPO_example_single_player.zip',
    15,
    haxballgym.SinglePlayerEnvironment()
)

# DQN-trained agent
dqn_agent = DQNBaselineAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_baselines/models/DQN_example_single_player.zip',
    15,
    haxballgym.SinglePlayerEnvironment(use_discrete_actionspace=True),
    team="blue"
)
"""

# A3C agent
A3C_agent_red = ActorCriticAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_ai/saves/1140.5663781166077',
    15,
    get_2p_env(),
    team="red"
)
A3C_agent_blue = ActorCriticAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_ai/saves/1763.4958679676056',
    15,
    get_2p_env(),
    team="blue"
)


# play visual games
haxballgym.play_visual_games(red_agents=[A3C_agent_red], blue_agents=[A3C_agent_blue], print_debug=True)
