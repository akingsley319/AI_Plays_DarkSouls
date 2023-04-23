import time
import gym
#import sys
#asys.modules["gym"] = gym

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv

from src.EldenRing.ai_plays.environment import CustomEnv
from src.EldenRing.ai_plays.config import MODEL_PLAYS_PATH, LOGS_PLAYS_PATH
from src.EldenRing.ai_plays.callback import TrainAndLoggingCallback

time.sleep(5)  # gives time to jump back into game

# path to model and log directories
models_dir = MODEL_PLAYS_PATH
logs_dir = LOGS_PLAYS_PATH

# Forms environment
env = CustomEnv()
env = DummyVecEnv([lambda: env])
env = VecFrameStack(env, 4, channels_order='last')

# Setup callback
callback = TrainAndLoggingCallback(check_freq=100, save_path=logs_dir)

# This brings in the model; look for stable baselines 3 models to potentially replace A2C
model = PPO("CnnPolicy", env, verbose=1, tensorboard_log=logs_dir)

# Train model and save it every (TIMESTEPS) steps
TIMESTEPS = 10000
#env.reset()
# reset_num_timesteps=False, tb_log_name="PPO",
model.learn(total_timesteps=TIMESTEPS, callback=callback)
model.save(f"{models_dir}/{TIMESTEPS}")

# This just runs it as a test (episode) number of times
#episodes = 10
#for ep in range(episodes):
#    obs = env.reset()
#    done = False
#    while not done:
#        env.render()
#        action, _states = model.predict(obs)
#        obs, reward, done, info = env.step(action)

# Done with the environment, so close it out
env.close()
