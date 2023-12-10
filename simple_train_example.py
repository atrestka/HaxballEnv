from stable_baselines3 import A2C
from haxballgym import SinglePlayerEnvironment


env = SinglePlayerEnvironment()
print(env.action_space)
model = A2C("MlpPolicy", env, verbose=2, policy_kwargs={'net_arch': [256, 256, 256]}, ent_coef=0.01, gamma=0.997)
model.learn(total_timesteps=10000, log_interval=10)
model.save("haxball_baselines/models/A2C_example")