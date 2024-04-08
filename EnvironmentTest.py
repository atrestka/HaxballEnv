import gymnasium as gym
from gymnasium.envs.registration import register

# Attempt to import the SinglePlayerEnvironment class to ensure it exists
try:
    # This import is just to check if haxballgym is installed and SinglePlayerEnvironment is accessible
    from haxballgym import SinglePlayerEnvironment
    haxballgym_installed = True
except ImportError:
    print("haxballgym is not installed.")
    haxballgym_installed = False

if haxballgym_installed:
    print('Keep going brotha')
    # Register the environment using a string-based entry_point
    register(
        id='SinglePlayerHaxball-v0',  # Unique identifier for the environment
        entry_point='haxballgym:SinglePlayerEnvironment',  # Adjusted entry point
    )

    # Example on how to create and use the environment
    try:
        env = gym.make('SinglePlayerHaxball-v0')
        print("Environment created successfully. You can now use it!")
    except gym.error.UnregisteredEnv:
        print("Environment is not registered. Ensure registration code is executed.")

















