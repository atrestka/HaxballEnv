import haxball_gym

default_red_bindings = ('w', 'd', 's', 'a', 'c')
default_blue_bindings = ('i', 'l', 'k', 'j', '.')

red_random = haxball_gym.RandomAgent(10)
blue_random = haxball_gym.RandomAgent(10)

haxball_gym.play_arena_games(red_agents=[red_random, red_random], blue_agents=[blue_random, blue_random, blue_random],
                             games=2, max_steps=1000)
