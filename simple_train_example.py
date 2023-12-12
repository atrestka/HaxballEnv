from stable_baselines3 import PPO
from haxballgym import SinglePlayerEnvironment
from stable_baselines3.common.base_class import BaseAlgorithm
import numpy as np
import gymnasium as gym

env = SinglePlayerEnvironment(max_steps=50)
# env = gym.make("CartPole")

model = PPO("MlpPolicy", env, verbose=2, policy_kwargs={'net_arch': [256, 256, 256]}, gamma=0.8,
            ent_coef=0.4, learning_rate=0.003)


def evaluate(
    model: BaseAlgorithm,
    num_episodes: int = 100,
    deterministic: bool = True,
) -> float:
    """
    Evaluate an RL agent for `num_episodes`.

    :param model: the RL Agent
    :param env: the gym Environment
    :param num_episodes: number of episodes to evaluate it
    :param deterministic: Whether to use deterministic or stochastic actions
    :return: Mean reward for the last `num_episodes`
    """
    # This function will only work for a single environment
    vec_env = model.get_env()
    obs = vec_env.reset()
    all_episode_rewards = []
    for _ in range(num_episodes):
        episode_rewards = []
        done = False
        # Note: SB3 VecEnv resets automatically:
        # https://stable-baselines3.readthedocs.io/en/master/guide/vec_envs.html#vecenv-api-vs-gym-api
        # obs = vec_env.reset()
        while not done:
            # _states are only useful when using LSTM policies
            # `deterministic` is to use deterministic actions
            action, _states = model.predict(obs, deterministic=deterministic)
            # here, action, rewards and dones are arrays
            # because we are using vectorized env
            obs, reward, done, _info = vec_env.step(action)
            episode_rewards.append(reward)

        all_episode_rewards.append(sum(episode_rewards))

    mean_episode_reward = np.mean(all_episode_rewards)
    print(f"Mean reward: {mean_episode_reward:.2f} - Num episodes: {num_episodes}")

    return mean_episode_reward


print(evaluate(model, 100))

model.learn(total_timesteps=1000000, log_interval=2, progress_bar=True)
model.save("haxball_baselines/models/PPO_example3")

print(evaluate(model, 100))