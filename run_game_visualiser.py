import haxballgym
from haxball_baselines.agents.baseline_ppo_agent import PPOBaselineAgent
from haxball_baselines.agents.baseline_DQN_agent import DQNBaselineAgent

# human agent with WASD key bindings
human_agent = haxballgym.HumanAgent(team="red")

# random motion agent
red_random = haxballgym.RandomAgent(10)

# agent which does nothing
idle_agent = haxballgym.IdleAgent()

# PPO-trained agent
ppo_agent = PPOBaselineAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_baselines/models/PPO_trained_goal_scorer.zip',
    15,
    haxballgym.SinglePlayerEnvironment()
)

# DQN-trained agent
dqn_agent = DQNBaselineAgent(
    '/Users/stefanclarkework/Desktop/HaxballEnv/haxball_baselines/models/DQN_example2.zip',
    15,
    haxballgym.SinglePlayerEnvironment(use_discrete_actionspace=True)
)

# choose the agent to observe (change this one)
agent_to_watch = dqn_agent

# play visual games
haxballgym.play_visual_games(red_agents=[agent_to_watch], blue_agents=[], print_debug=True)
