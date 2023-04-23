import gym
from stable_baselines3 import PPO


# Model path
model_dir = ""
model_path = ""

# Load in model
model = PPO.load(model_path)

# Forms environment
env = None
env.reset()

# Run model for show
done = False
while done:
    obs = env.reset()
    done = False
    while not done:
        env.render()
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)