from .envs import DiseaseTreatmentEnv
from gym.envs.registration import register

print("Initializing treat_rl package")
register(
    id='DiseaseTreatment-v0',
    entry_point='treat_rl:DiseaseTreatmentEnv',
)


