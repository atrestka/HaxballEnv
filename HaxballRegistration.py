import gymnasium as gym
from gymnasium.envs.registration import register

try:
    from haxballgym import SinglePlayerEnvironment
except ImportError:
    print("haxballgym is not installed. Please install it to continue.")
else:
    # Function to create the environment instance without passing render_mode
    def create_single_player_env() -> gym.Env:
        return SinglePlayerEnvironment()

    # Register the environment without the unsupported render_mode argument
    register(
        id='SinglePlayerHaxball-v0',  # Unique identifier for the environment
        entry_point=create_single_player_env,  # Adjusted entry point
    )

# Example on how to create and use the environment
try:
    env = gym.make('SinglePlayerHaxball-v0')
    print("Environment created successfully. You can now use it!")
except gym.error.UnregisteredEnv:
    print("Environment is not registered. Ensure registration code is executed.")

