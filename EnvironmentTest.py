# import gymnasium
# from gym.envs.registration import register

#TroubleShooting
################################

# env = SinglePlayerEnvironment()

# try: 
#     seed = 123
#     env.seed(seed)
#     print(f"Environment has 'seed' method. Seed set to {seed}.")
# except AttributeError:
#     print("Environment does not have 'seed' method.")


# try:
#     register(
#         id = 'SinglePlayerHaxball-v1',
#         entry_point = 'haxballgym:SinglePlayerEnvironment'
#     )
#     print('Environment Registered')
# except AttributeError:
#     print("Environment Will not register")


# try:
#     envOld = gym.make('SinglePlayerHaxball-v1')
#     print('Environment Made')
# except AttributeError:
#     print("Environment Will not made")

# try:
#     envNEw = gymnasium.make("GymV26Environment-v0", env_id = "SinglePlayerHaxball-v1")
#     print("Eureka!.. Maybe lol")
# except gymnasium.error.CustomSpaceError:
#     print("Environment coould not be Updated")

################################

#Test functionality of gymnasium on already proven environment

# testEnv = gymnasium.make("LunarLander-v2", render_mode="human")
# testObservation, testInfo = testEnv.reset()

# for i in range(1000):
#     testAction = testEnv.action_space.sample()
#     testObservation, testReward, testTerminated, testTruncated, testInfo = testEnv.step(testAction)

#     if testTerminated or testTruncated:
#         testObservation, testInfo = testEnv.reset()

# testEnv.close()

#works -- no figure lol

################################

#Investigate New Environment Space

# import gymnasium as gym
# from gymnasium.envs.registration import register
# from haxballgym import SinglePlayerEnvironment
# # from typing import Callable, Optional







# #Verify Registration



# #We fixed it!

# # #Initialize SinglePlayerHaxballEnvironment with new version of Gym

# env = gym.make("SinglePlayerHaxball")
# print(env.action_space)


# testObservation, testInfo = testEnv.reset()

# for i in range(1000):
#     testAction = testEnv.action_space.sample()
#     testObservation, testReward, testTerminated, testTruncated, testInfo = testEnv.step(testAction)

#     if testTerminated or testTruncated:
#         testObservation, testInfo = testEnv.reset()









#This part is Relevant
#########################
import gym
import gymnasium
from gym.envs.registration import register
from typing import Callable, Optional
#from gymnasium.envs.registration import register

#Register Environment
register(    
    id = 'SinglePlayerHaxball',
    entry_point = 'haxballgym:SinglePlayerEnvironment'
)

env = gymnasium.make("GymV26Environment-v0", env_id = 'SinglePlayerHaxball')
print(env.action_space)



#Problem with registry here:

gymnasium.envs.registration.register(
    id = 'SinglePlayerHaxball-v1',
    entry_point = 'haxballgym:SinglePlayerEnvironment'
    # entry_point = env

)

print(gymnasium.spec('SinglePlayerHaxball-v1'))

envTest = gymnasium.make("SinglePlayerHaxball-v1")
print(envTest.action_space)


#uncomment to show further problem
# Obs, info = env.reset()

# for i in range(1000):
#     action = env.action_space.sample()
#     obs, reward, terminated, truncated, info = env.step(action)

#     if terminated or truncated:
#         observation, info = env.reset()

# env.close()



#This was an old test
######################


















