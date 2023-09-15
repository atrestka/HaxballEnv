import basic_trainers.ppo_fixed as ppo
import torch
import gym_haxball.solofixedgym as solo
from network import SebPolicy

if __name__ == "__main__":
    mod1 = SebPolicy()
    mod2 = SebPolicy()
    mod1.to("cpu")
    mod2.to("cpu")
    trainer = ppo.PPOTrainer(mod1, solo.env_constructor(mod2), 10, parallelise=True)
    trainer.train(100)
    torch.save(mod1, "models/PPO_test.model")
