import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time
import jump_package as jp # This is your code file

class JustJumpEnv(gym.Env):
    def __init__(self):
        super(JustJumpEnv, self).__init__()
        # Define Action: 0 = Nothing, 1 = Jump
        self.action_space = spaces.Discrete(2)
        
        # Define Observation: 128x128 grayscale image (normalized)
        self.observation_space = spaces.Box(low=0, high=1, shape=(1, 128, 128), dtype=np.float32)
        
        self.window_name = "Just Jump"
        self.score_file = "assets/highscore.txt" # Ensure path is correct

    def reset(self, seed=None, options=None):
        """Resets the game to a starting state."""
        super().reset(seed=seed)
        # You might need to send a 'Restart' keypress here via win32api
        # jp.press_jump(self.window_name) 
        
        obs = jp.get_window_pixels(self.window_name)
        # Reshape for PyTorch: (Channels, Height, Width)
        obs = np.expand_dims(obs, axis=0).astype(np.float32)
        return obs, {}

    def step(self, action):
        """The main loop: Act -> Observe -> Reward"""
        # 1. Take Action
        if action == 1:
            jp.press_jump(self.window_name)
        
        # 2. Wait for the game to update (Your 0.1s gap)
        time.sleep(0.1)
        
        # 3. Get New Observation
        obs = jp.get_window_pixels(self.window_name)
        obs = np.expand_dims(obs, axis=0).astype(np.float32)
        
        # 4. Get Reward
        reward = jp.get_and_reset_reward(self.score_file)
        
        # 5. Check if Dead (Terminated)
        # If your game stays at 0 reward for too long, or a 'GameOver' pixel appears:
        done = False 
        
        return obs, reward, done, False, {}

# --- START TRAINING ---
from stable_baselines3 import DQN

# Create the environment
env = JustJumpEnv()

# Initialize the Deep Q-Network
# 'CnnPolicy' tells it to use a Convolutional Neural Network for the images
model = DQN(
    "CnnPolicy", 
    env, 
    verbose=1, 
    buffer_size=10000, 
    learning_rate=1e-4,
    policy_kwargs={'normalize_images': False} # Tell SB3 to trust your float32 data
)

print("Starting training in 3 seconds... Switch to the game window!")
time.sleep(3)

# Train for 50,000 steps
model.learn(total_timesteps=50000)

# Save the brain
model.save("jump_ai_model")