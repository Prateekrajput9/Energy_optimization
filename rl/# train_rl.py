
import os
import gym
import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import DummyVecEnv
from energy_env import EnergyEnv

def train(output_dir='models', total_timesteps=200_000):
    os.makedirs(output_dir, exist_ok=True)
    env = DummyVecEnv([lambda: EnergyEnv(episode_len=96)])
    model = PPO('MlpPolicy', env, verbose=1, tensorboard_log="./tb_logs/",
                learning_rate=3e-4, n_steps=2048, batch_size=64, n_epochs=10)

    # checkpoint callback to save intermediate models
    checkpoint_callback = CheckpointCallback(save_freq=10000, save_path=output_dir,
                                             name_prefix='ppo_energy')

    model.learn(total_timesteps=total_timesteps, callback=checkpoint_callback)
    model.save(os.path.join(output_dir, 'ppo_energy_final'))
    print("Model training complete and saved.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--timesteps', type=int, default=200000, help='Total timesteps for training')
    parser.add_argument('--out', type=str, default='models', help='Output folder for models')
    args = parser.parse_args()

    train(output_dir=args.out, total_timesteps=args.timesteps)
