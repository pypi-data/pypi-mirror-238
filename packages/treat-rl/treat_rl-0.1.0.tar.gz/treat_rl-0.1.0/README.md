# DiseaseTreatmentRL

DiseaseTreatmentRL is a reinforcement learning environment built on OpenAI Gym, designed for simulating and optimizing disease treatment strategies. It provides a flexible framework to model different diseases, symptoms, and treatments, enabling the exploration of various medical interventions.

## Features
- Customizable disease, symptom, and treatment settings
- Support for multiple diseases and treatments
- Simulated symptom modulation in response to treatments
- Built-in reward system for treatment optimization
- Extensible for various clinical scenarios

## Installation

To get started, you'll need to install the required dependencies. You can install them using pip:

```bash
pip install gym numpy
```

## Usage

To use DiseaseTreatmentRL in your project, you can import and initialize the environment as follows:

```python
import gym
import disease_treatment_rl

env = gym.make('DiseaseTreatmentEnv-v0')
```

You can then interact with the environment using standard OpenAI Gym methods:

```python
observation = env.reset()
action = env.action_space.sample()
next_observation, reward, done, info = env.step(action)
```

## Customization

You can customize the environment by passing specific parameters during initialization:

```python
env = DiseaseTreatmentEnv(n_diseases=5, n_treatments=7, n_symptoms=10)
```

Refer to the class documentation for more information on each parameter.
