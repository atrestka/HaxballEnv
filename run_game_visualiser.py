import haxballgym
from haxball_baselines.agents.baseline_ppo_agent import PPOBaselineAgent
from haxball_baselines.agents.baseline_DQN_agent import DQNBaselineAgent
from haxball_ai.model import ActorCriticAgent
from haxball_ai.envs import get_2p_env


# human agent with WASD key bindings
human_agent = haxballgym.HumanAgent(team="red")

# human agent with WASD key bindings
human_agent_2 = haxballgym.HumanAgent(team="blue")

# random motion agent
red_random = haxballgym.RandomAgent(10)

# agent which does nothing
#idle_agent = haxballgym.IdleAgent()


# # PPO-trained agent
# ppo_agent = PPOBaselineAgent(
#     '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_baselines/models/PPO_example_single_player.zip',
#     15,
#     haxballgym.SinglePlayerEnvironment()
# )

"""
# play visual games
haxballgym.play_visual_games_pennymatching(red_agents=[human_agent], blue_agents=[red_random], print_debug=True)




# A3C agent
A3C_agent_red = ActorCriticAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_ai/saves/2863.8579771518707',
    15,
    get_2p_env(),
    team=0
)
A3C_agent_blue = ActorCriticAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_ai/saves/2863.8579771518707',
    15,
    get_2p_env(),
    team=1
)

"""

# DQN-trained agent
# dqn_agent = DQNBaselineAgent(
#     '/Users/alextrestka/Desktop/HaxballEnv/haxball_baselines/models/DQN_SinglePlayerHaxball-v0.zip',
#     15,
#     haxballgym.SinglePlayerEnvironment(use_discrete_actionspace=True),
#     team=0
# )

# haxballgym.play_visual_games_4team([human_agent], [red_random], [red_random], [red_random])

# haxballgym.play_visual_games_pennymatching([human_agent], [red_random])

#remember to always change config
# play visual games
haxballgym.play_visual_games_2team([human_agent_2], [human_agent], print_debug=True)
