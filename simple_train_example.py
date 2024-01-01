from stable_baselines3 import PPO
from haxballgym import SinglePlayerEnvironment
from haxball_baselines.evaluation import evaluate


# set up single player environment
env = SinglePlayerEnvironment(max_steps=50)

print(env.observation_space)

# define the models
model = PPO("MlpPolicy", env, verbose=2, policy_kwargs={'net_arch': [256, 256, 256]}, gamma=0.4, learning_rate=0.003,
            ent_coef=1.)

# test initialization
print('initial test result:')
print(evaluate(model, 100))

# train the model with stable_baselines3
model.learn(total_timesteps=100000, log_interval=2, progress_bar=True)

# save the model
model.save("haxball_baselines/models/PPO_example5")

# test trained model
print('final test result:')
print(evaluate(model, 100))
