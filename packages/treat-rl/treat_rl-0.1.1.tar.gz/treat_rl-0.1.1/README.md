# Treat RL

Treat RL is a reinforcement learning environment designed to model the process of treating diseases with different treatments. This environment is implemented using the OpenAI Gym interface, making it compatible with various reinforcement learning algorithms.

## Installation

You can install using pip:

```bash
pip install treat-rl
```

## Usage

Here is a basic example to how to use the DiseaseTreatmentRL environment:

```python
import gym
import disease_treatment_env

env = gym.make('DiseaseTreatment-v0')
observation = env.reset()

for _ in range(1000):
    env.render()
    action = env.action_space.sample()  # Take a random action
    observation, reward, done, info = env.step(action)
    if done:
        observation = env.reset()
env.close()
```

This example demonstrates the creation of the environment, taking random actions, and rendering the current state of the environment. The environment will be reset once a terminal state is reached.
