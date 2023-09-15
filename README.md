An environment for training AI to play Haxball.

Made mostly by Seb Towers (Oxford University) with help from Philip Nielsen, Stefan Clarke (Princeton University) and Taavet Kalda (Max Planck Institute).

To get the game running:
1. Pull the repository
2. Run "pip install -r requirements.txt"

3. To play a 1v1 game run "python game_visualiser.py --red-human --blue-human --not-rand-reset". Controls are:
   1. red: movement : [w a s d], kick: c
   2. blue: movement [i j k l], kick: .
4. For an example of how to train a basic PPO model to play the game run "python ppo_runner.py". The model will be saved to the folder "models".  Choose the name in the file "ppo_runner.py"
5. You can then play against the mdoel by running "python game_visualiser.py --red-human --blue-model="PPO_test" --not-rand-reset" (PPO_test is whatever you named the model you trained)


For examples of how to set up neural networks to play the game see "network.py".
For an example of a training loop see "basic_trainers.ppo_fixed.py".
For templates for getting your own agents to play on the visual game see "agents".