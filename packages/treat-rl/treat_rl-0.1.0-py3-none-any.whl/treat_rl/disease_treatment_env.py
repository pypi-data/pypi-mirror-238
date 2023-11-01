import gym
from gym import spaces
import numpy as np
import random

class DiseaseTreatmentEnv(gym.Env):
    """Environment to model disease treatment using RL."""

    def __init__(self, 
                 n_diseases=3, 
                 n_treatments=5, 
                 n_symptoms=7, 
                 treatment_cost_range=(1, 5), 
                 symptom_modulation_range=(-0.5, 0.5),
                 remission_reward=100,
                 seed=1,
                 max_visits=32):
        super(DiseaseTreatmentEnv, self).__init__()

        # Create a non-defaut numpy rng
        rng = np.random.RandomState(seed)

        # Configurable parameters
        self.treatment_cost_range = treatment_cost_range
        self.symptom_modulation_range = symptom_modulation_range
        self.remission_reward = remission_reward
        self.max_visits=max_visits

        # Step tracking
        self.visit_number = 0

        # Action and observation spaces
        self.action_space = spaces.Discrete(n_treatments)
        self.observation_space = spaces.Box(low=0, high=1,
                 shape=(n_symptoms + n_treatments,), dtype=np.float32)

        self.n_diseases = n_diseases
        self.n_treatments = n_treatments
        self.n_symptoms = n_symptoms

        self.connection_probability = 1 / (2 * n_diseases)
        
        self.generate_diseases(rng)
        self.disease_list = list(self.diseases.keys())
        self.treatments = self.generate_treatments(rng)

        self.current_disease = None
        self.current_symptoms = np.zeros(n_symptoms)
        self.reset()
        
        self.generate_transition_matrix(rng)

    def generate_transition_matrix(self, rng):
        # Initializing a matrix filled with 1s on the diagonal (self transitions)
        self.transition_matrix = np.eye(self.n_diseases)

        for i in range(self.n_diseases):
            total_borrowed_probability = 0  # The total probability that's redistributed to other states
            for j in range(self.n_diseases):
                if i != j and rng.rand() < self.connection_probability:  # Avoid maxing out self-loop and check for connection
                    transition_prob = rng.uniform(0.01, 0.2)  # Transition probability between 1% to 20%
                    self.transition_matrix[i][j] = transition_prob
                    total_borrowed_probability += transition_prob
            # Subtract the borrowed probabilities from the self-transition
            self.transition_matrix[i][i] -= total_borrowed_probability

    def generate_diseases(self, rng):
        self.diseases = {}  # Initialize the dictionary
        for i in range(self.n_diseases):
            num_symptoms_for_disease = rng.randint(1, max(2, self.n_symptoms // 2))
            symptoms_for_disease = rng.choice(self.n_symptoms, size=num_symptoms_for_disease, replace=False)

            num_effective_treatments = rng.randint(1, max(2, self.n_treatments // 2))
            effective_treatments = rng.choice(self.n_treatments, size=num_effective_treatments, replace=False)
            
           
            means = rng.uniform(0.3, 0.7, size=num_symptoms_for_disease)  # Choosing values to make sure most symptoms stay within [0,1]
            std_devs = rng.uniform(0.05, 0.15, size=num_symptoms_for_disease)  # Small values to prevent wild swings in symptom values
            symptom_distributions = list(zip(means, std_devs))
 
            treatment_to_remission_probs = rng.uniform(0.1, 0.8, size=num_effective_treatments)
            
            # Calculate base reward based on the number of symptoms (negative value)
            base_reward = -num_symptoms_for_disease

            self.diseases[f"Disease_{i}"] = {
                'symptoms': symptoms_for_disease,
                'treatments': effective_treatments,
                'symptom_distributions': symptom_distributions,
                'remission_probs': dict(zip(effective_treatments, treatment_to_remission_probs)),
                'base_reward': base_reward  # Assign base reward for the disease
            }

    def _combine(self, observation, action):
        """Combine the observation and action into a single vector
        action vector is one-hot encoded"""
        action_one_hot = np.zeros(self.n_treatments, dtype=np.float32)
        action_one_hot[int(action)] = 1.0
        return np.concatenate([observation, action_one_hot])

    def step(self, action):
        prev_disease = self.current_disease
        old_symptoms = self.current_symptoms.copy()
        self.visit_number += 1

        # Get the chosen treatment
        treatment = self.treatments[f"Treatment_{action}"]
        
        # Apply the treatment's base cost
        reward = -treatment['base_cost']

        # Check remission based on current disease and treatment
        remission_prob = self.diseases[self.current_disease]['remission_probs'].get(action, 0)

        # If remission occurs, update state and reward
        if np.random.rand() < remission_prob:
            self.current_disease = "Remission"
            #print("[DEBUG] Remission achieved!")
            reward += self.remission_reward
            self.current_symptoms = np.zeros(self.n_symptoms)  # Reset symptoms for remission
            return self._combine(self.current_symptoms, action), reward, True, {"treatment": action, "disease_pre_treatment": self.current_disease}

        # If remission doesn't occur, proceed with disease transition logic
        treatment_modifiers = treatment["transition_modifiers"]
        modified_transitions = self.transition_matrix[self.current_disease_index] * treatment_modifiers

        # More debugging print statements

        modified_transitions /= modified_transitions.sum()
        new_disease_index = np.random.choice(self.n_diseases, p=modified_transitions)
        self.current_disease = f"Disease_{new_disease_index}"
        self.current_disease_index = new_disease_index
        #print(f"[DEBUG] Previous disease: {prev_disease}, Applied treatment: {action}, New disease: {self.current_disease}")


        # Deduct the base reward for the current disease from the total reward
        reward += self.diseases[self.current_disease]['base_reward']

        # Fluctuate symptoms based on disease distributions and then adjust them based on treatment effects
        self.current_symptoms = self.sample_symptoms()
        for symptom, change in treatment['affected_symptoms'].items():
            self.current_symptoms[symptom] += change
        self.current_symptoms = np.clip(self.current_symptoms, 0, 1)

        # Visits cutoff
        terminated = self.visit_number == self.max_visits
            

        #if np.any(np.isnan(self.current_symptoms)) or np.any(self.current_symptoms < 0) or np.any(self.current_symptoms > 1):
            #print("[DEBUG] Invalid symptom values detected!", self.current_symptoms, "Old symptoms:", old_symptoms, "Applied treatment:", action)

        #print(f"[DEBUG] Obs: {self.current_symptoms}, Reward: {reward}, Treatment: {action}, Disease: {self.current_disease}")
        return self._combine(self.current_symptoms, action), reward, terminated, {"treatment": action, "disease_pre_treatment": self.current_disease}

    def sample_symptoms(self):
        symptom_values = np.zeros(self.n_symptoms)
        
        if self.current_disease == "Remission":
            return symptom_values  # No symptoms
        
        symptoms_for_disease = self.diseases[self.current_disease]['symptoms']
        symptom_distributions = self.diseases[self.current_disease]['symptom_distributions']
        
        for symptom, (mean, std_dev) in zip(symptoms_for_disease, symptom_distributions):
            sampled_value = np.random.normal(mean, std_dev)
            symptom_values[symptom] = sampled_value
        symptom_values = np.clip(symptom_values, 0, 1)

        return symptom_values
    
    def generate_treatments(self, rng):
        treatments = {}
        for i in range(self.n_treatments):
            # Each treatment can have a cost between the configurable range
            base_cost = rng.uniform(*self.treatment_cost_range)  
            
            affected_symptoms_count = rng.randint(1, max(2, self.n_symptoms // 2))
            affected_symptoms = rng.choice(self.n_symptoms, size=affected_symptoms_count, replace=False)
            
            # Change in symptom severity due to treatment is generated within the configurable range
            symptom_changes = {symptom: rng.uniform(*self.symptom_modulation_range) for symptom in affected_symptoms}
            
            treatments[f"Treatment_{i}"] = {
                'base_cost': base_cost,
                'affected_symptoms': symptom_changes
            }

            # Generate treatment-specific transition modifiers for each disease transition
            transition_modifiers = rng.uniform(0.5, 1.5, size=self.n_diseases)
            treatments[f"Treatment_{i}"]["transition_modifiers"] = transition_modifiers
        return treatments

    def reset(self, *, seed=None, options=None):
        self.current_disease = random.choice(list(self.diseases.keys()))
        self.current_disease_index = self.disease_list.index(self.current_disease)
        self.current_symptoms = self.sample_symptoms()  # Initialize symptoms based on the current disease
        self.visit_number=0
        #print(f"[DEBUG] Resetting environment. Starting disease: {self.current_disease}, Initial symptoms: {self.current_symptoms}")
        return self._combine(self.current_symptoms, -1)
        

    def render(self, mode='human'):
        # Simple visualization for now
        print(f"Current Disease: {self.current_disease}")
        print(f"Current Symptoms: {self.current_symptoms}")
        print("\n")
