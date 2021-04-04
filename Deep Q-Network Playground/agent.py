#import packages
import model
import memory
import numpy as np
import random
import tensorflow as tf
import os
from scipy.special import logsumexp

# Deep Q-learning Agent for cartpole

class Agent:

    def __init__(self, state_size, action_size):    
        self.state_size = state_size
        self.action_size = action_size
        # create memory pool
        self.mempool = memory.ExperienceReplay(capacity = 2000)
        
        # create neural network model, we call it policy net
        self.net = model.Model(state_size=state_size, action_size=action_size)
        ### Should compile the model here instead of within the Model class in model.py
        self.net.model.compile(optimizer = tf.keras.optimizers.Adam(0.001),
                           loss = ['mse'])
#         model_path = 'weights_cartpoledqn.h5'
#         if os.path.exists(model_path):
#             try:
#                 self.net._load_model()
#                 print("Past model found and loaded.")
#             except:
#                 pass
        
        # parameters for q-learning
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01       # the low bound of espison
        self.epsilon_decay = 0.995    # used for adjusting the epsion along with the time/steps
                
    def eps_greedy(self, state):

        rnd = random.random()
        if rnd < self.epsilon:
            return random.randint(0, self.action_size - 1)
        return self.get_greedy_action(state)
    
    def get_greedy_action(self, state):

        Q_values = self.net.model.predict(state)[0]
        greedy_action = np.argmax(Q_values)
        
        return greedy_action
    
    def eps_greedy_boltzmann(self, state):

        rnd = random.random()
        if rnd < self.epsilon:
            return self.boltzmann_action_with_temperature(state)
        return self.get_greedy_action(state)
    
    def boltzmann_action_with_temperature(self, state):

        Q_values = self.net.model.predict(state)[0] / self.epsilon
        log_probs = Q_values - logsumexp(Q_values)
        [action] = np.random.choice(self.action_size, size = 1, p = np.exp(log_probs))
        
        return action
    
    def get_training_data(self, batch_size):
        
        states, actions, rewards, dones, next_states = self.mempool.sample(batch_size)

        future_rewards = self.gamma * np.max(self.net.model.predict(next_states), axis = -1) # note preds are Nx2

        targets = [t if d else (t + f) for t, d, f in zip(rewards, dones, future_rewards)]
        target_preds = self.net.model.predict(states) # Nx2

        # print(target_preds.shape, len(actions), len(targets)) # (32,1,2), 32, 32
        for i, (t, a) in enumerate(zip(targets, actions)):
            target_preds[i][a] = t

        targets = target_preds
        targets = np.array(targets)
        
        return states, targets
            
    def train_policy_net(self, batch_size):

        states, targets = self.get_training_data(batch_size)

        self.net.model.fit(x = states, y = targets, verbose = 0)
            # Decay the value of epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay