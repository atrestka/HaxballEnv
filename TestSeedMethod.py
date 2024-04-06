from haxballgym import SinglePlayerEnvironment

env = SinglePlayerEnvironment(max_steps=50, seed=500)

env.reset(46000)
print(env.getState())

env.reset(46000)
print(env.getState())






