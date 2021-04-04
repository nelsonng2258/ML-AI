import gym
import agent
import numpy as np
import tensorflow
import tensorflow as tf
from tqdm import tqdm
import matplotlib.pyplot as plt

    
############  start the episodes, fill the memory pool and train	
def train():

    # initialize gym environment
    env = gym.make('CartPole-v0')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    
    # Create agent
    cartpole_agent = agent.Agent(state_size, action_size)
    
    # Parameters
    batch_size = 64  # size of the batch sampled from memory pool, for updating the weights
    maxscore = 0     # for saving the weights with highest score 
    EPISODES = 202   # play the game 200 times
    scores = []

    # Iterate the game
    for e in tqdm(range(EPISODES)):

        # reset state in the beginning of each game
        state = env.reset()
        state = np.reshape(state, [1, 4])
        done = False
        
        if e%10 == 1 and e != 1:
            np.savetxt('./agent_scores/agent_scores_train.csv', np.array(scores),delimiter = ', ')
            plt.figure(figsize = (10,6))
            plt.plot(scores)
            plt.xlabel("Episode")
            plt.ylabel("Score")
            plt.savefig(f'./agent_scores/episode_{e-1}_train_scores', dpi = 300)

            plt.figure(figsize = (10,6))
            plt.hist(scores)
            plt.xlabel("Score")
            plt.ylabel("Frequency")
            plt.savefig(f'./agent_scores/episode_{e-1}_histo_train_scores', dpi = 300)
            plt.close('all')

        # t : steps, the maximal score is 200, terminate the episode if done
        for t in range(200):
            
            # Decide action: boltzmann action
            action = cartpole_agent.eps_greedy(state)
            # take action, get the next state and reward              
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 4])

            # append the transition(previous state, action, reward, state, done) in the memory pool 
            cartpole_agent.mempool.append((state, action, reward, done, next_state))

            # make next_state the new current state
            state = next_state
            
            # time to turn to the next episode
            # but before the next episode, to print out info of current episode and save the weights of the best model			
            if done:
                # print the score and break out of the loop
                print("episode: {}/{}, score: {}".format(e, EPISODES, t))
                scores.append(t)
                
                if maxscore < t:
                    maxscore = t
                    cartpole_agent.net._save_model()
                break
            
            # start train only if samples in memory pool are sufficient for learning 
            if len(cartpole_agent.mempool) > batch_size:
                cartpole_agent.train_policy_net(batch_size)  
                  
    env.close()
    
def play():
    
    EPISODES = 202   # play the game 200 times
    scores = []

    # initialize gym environment
    env = gym.make('CartPole-v0')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    # Create agent
    cartpole_agent = agent.Agent(state_size, action_size)

      # Load weights for the model
    cartpole_agent.net._load_model()

    for e in tqdm(range(EPISODES)):
        
        if e%10 == 1 and e != 1:
            np.savetxt('./agent_scores/agent_scores_play.csv', np.array(scores),delimiter = ', ')
            plt.figure(figsize = (10,6))
            plt.plot(scores)
            plt.xlabel("Episode")
            plt.ylabel("Score")
            plt.savefig(f'./agent_scores/episode_{e-1}_play_scores', dpi = 300)

            plt.figure(figsize = (10,6))
            plt.hist(scores)
            plt.xlabel("Score")
            plt.ylabel("Frequency")
            plt.savefig(f'./agent_scores/episode_{e-1}_histo_play_scores', dpi = 300)
            plt.close('all')
        
        observe = env.reset()
        state = np.reshape(observe, [1, 4])
        done = False
        score = 0

        while(not done):
            action = cartpole_agent.get_greedy_action(state)
            observe, reward, done, _ = env.step(action)
            state = np.reshape(observe, [1, 4])
            # env.render()
            score+=1
            
        scores.append(score)

    env.close()
    
def play_once():
    
    EPISODES = int(input("How many episodes?: "))
    # EPISODES = 1   # play the game 200 times
    scores = []

    # initialize gym environment
    env = gym.make('CartPole-v0')
    env._max_episode_steps = 999
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    # Create agent
    cartpole_agent = agent.Agent(state_size, action_size)

      # Load weights for the model
    cartpole_agent.net._load_model()

    for e in tqdm(range(EPISODES)):
        
        observe = env.reset()
        state = np.reshape(observe, [1, 4])
        done = False
        score = 0

        while(not done):
            action = cartpole_agent.get_greedy_action(state)
            observe, reward, done, _ = env.step(action)
            state = np.reshape(observe, [1, 4])
            env.render()
            score+=1
        print(f"Score for episode {e} is: {score}.")
            
        scores.append(score)

    env.close()