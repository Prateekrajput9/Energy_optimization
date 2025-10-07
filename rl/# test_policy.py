
import gym
import numpy as np
from stable_baselines3 import PPO
from energy_env import EnergyEnv

def evaluate(model_path='models/ppo_energy_final.zip', episodes=5):
    env = EnergyEnv(episode_len=96)
    model = PPO.load(model_path)
    for ep in range(episodes):
        obs = env.reset()
        done = False
        total_reward = 0.0
        total_grid = 0.0
        steps = 0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(int(action))
            total_reward += reward
            total_grid += info.get('grid_import', 0.0)
            steps += 1
        print(f"Episode {ep+1}: reward={total_reward:.2f}, grid_import_total={total_grid:.2f}")

if __name__ == '__main__':
    evaluate()
