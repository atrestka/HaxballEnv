from stable_baselines3 import DQN
from haxballgym import SinglePlayerEnvironment
from haxball_baselines.evaluation import evaluate


# set up single player environment
env = SinglePlayerEnvironment(max_steps=50, use_discrete_actionspace=True)

# define the model
model = DQN("MlpPolicy", env, verbose=2, policy_kwargs={'net_arch': [256, 256, 256]}, gamma=0.8, learning_rate=0.003)

# test initialization
print('initial test result:')
print(evaluate(model, 100))

# train the model with stable_baselines3
model.learn(total_timesteps=10000000, log_interval=2, progress_bar=True)

# save the model
model.save("haxball_baselines/models/DQN_example3")

# test trained model
print('final test result:')
print(evaluate(model, 100))