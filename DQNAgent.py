#Adapted from Pythonprogramming.net

#from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import TensorBoard
from custom_io import CarWriter, write_stats
import numpy as np
#import keras.backend.tensorflow_backend as backend

#from keras.models import Sequential
#from keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
#from keras.callbacks import TensorBoard  #tf1 Tensorboard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import tensorflow as tf
from collections import deque
import time
import random
#from tensorflow.python.keras.layers.convolutional import Conv1D
from tqdm import tqdm
import os
from threading import Thread
import sys
import traceback


#from tensorflow.keras.backend import set_session
#from tensorflow.compat.v1.keras.callbacks import TensorBoard # tf1 Tensorboard 

set_session = tf.compat.v1.keras.backend.set_session

from engine import *

tf.compat.v1.disable_eager_execution()

#tf.compat.v1.reset_default_graph()

print("Checkpoint 1")
DISCOUNT = 0.99
REPLAY_MEMORY_SIZE = 50_000  # How many last steps to keep for model training
MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps in a memory to start training
MINIBATCH_SIZE = 64  # How many steps (samples) to use for training
UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)
MODEL_NAME = '1x9'
#MIN_REWARD = -200  # For model save
MEMORY_FRACTION = 0.20
PREDICTION_BATCH_SIZE = 1
TRAINING_BATCH_SIZE = MINIBATCH_SIZE // 4
TRIAL_NUM = "trial7"
# Environment settings
EPISODES = 300

# Exploration settings
epsilon = 1.0 # not a constant, going to be decayed
EPSILON_DECAY = 0.97
MIN_EPSILON = 0.001

#  Stats settings
AGGREGATE_STATS_EVERY = 20  # episodes
DISPLAY = False
#STATE_SHAPE = (9)

class ModifiedTensorBoard(TensorBoard):

    # Overriding init to set initial step and writer (we want one log file for all .fit() calls)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step = 1
        #self.writer = tf.summary.create_file_writer(self.log_dir) ##############################################
        self.writer = tf.compat.v1.summary.FileWriter(self.log_dir)
        #tf.summary.
    # Overriding this method to stop creating default log writer
    def set_model(self, model):
        pass

    # Overrided, saves logs with our step number
    # (otherwise every .fit() will start writing from 0th step)
    def on_epoch_end(self, epoch, logs=None):
        self.update_stats(**logs)

    # Overrided
    # We train for one batch only, no need to save anything at epoch end
    def on_batch_end(self, batch, logs=None):
        pass

    # Overrided, so won't close writer
    def on_train_end(self, _):
        pass

    # Custom method for saving own metrics
    # Creates writer, writes custom metrics and closes writer
    def update_stats(self, **stats):
        self._write_logs(stats, self.step)

    def _write_logs(self, logs, index):
        for name, value in logs.items():
            if name in ['batch', 'size']:
                continue
            summary = tf.compat.v1.Summary()
            summary_value = summary.value.add()
            summary_value.simple_value = value
            summary_value.tag = name
            self.writer.add_summary(summary, index)
        self.writer.flush()

# Agent class
class DQNAgent:
    def __init__(self):

        # Main model
        self.sess = tf.compat.v1.Session()
        set_session(self.sess)
        self.model = self.create_model()

        # Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        # An array with last n steps for training
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        # Custom tensorboard object
        self.tensorboard = ModifiedTensorBoard(log_dir="logs/{}-{}/{}".format(MODEL_NAME, TRIAL_NUM, int(time.time())))

        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0
        self.graph = tf.compat.v1.get_default_graph() ##############################################
        self.terminate = False
        self.last_logged_episode = 0
        self.training_initialized = False

    def create_model(self):
        
        model = Sequential()

        model.add(Dense(9, input_shape = (1, 9)))
        model.add(Flatten())
        model.add(Dense(8, activation = 'linear'))
        model.add(Dense(8))
        
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=["accuracy"])
        return model

    # Adds step's data to a memory replay array
    # (observation space, action, reward, new observation space, done)
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    # Trains main network every step during episode
    def train(self, terminal_state, step):

        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        current_states = np.array([transition[0] for transition in minibatch])
        #print(minibatch)
        #print(current_states)
        #print(current_states.shape)
        current_qs_list = []
        with self.graph.as_default():
            for index, transition in enumerate(minibatch):
                set_session(self.sess)
                try:
                    current_qs_list.append(self.model.predict([transition[0]], PREDICTION_BATCH_SIZE))
                except:
                    traceback.print_exc()
                    current_qs_list.append(np.random.uniform(size = (1, 8)))

            
        future_qs_list = []
        with self.graph.as_default():
            for index, transition in enumerate(minibatch):
                set_session(self.sess)
                try:
                    future_qs_list.append(self.model.predict([transition[3]], PREDICTION_BATCH_SIZE))
                except:
                    traceback.print_exc()
                    future_qs_list.append(np.random.uniform(size = (1, 8)))

        current_qs_list = np.array(current_qs_list)
        future_qs_list = np.array(future_qs_list)
        #print(current_qs_list, current_qs_list.shape)
        X = []
        y = []

        for index, (current_state, action, reward, new_state, done) in enumerate(minibatch):
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            current_qs = current_qs_list[index]
            current_qs[0][action] = new_q

            X.append(current_state)
            y.append(current_qs)

        log_this_step = False
        if self.tensorboard.step > self.last_logged_episode:
            log_this_step = True
            self.last_log_episode = self.tensorboard.step

        with self.graph.as_default():
            for num in range(len(X)):
                set_session(self.sess)
                try:
                    self.model.fit(np.array(X[num]), np.array(y[num]), batch_size=TRAINING_BATCH_SIZE, verbose=0, shuffle=False, callbacks=[self.tensorboard] if log_this_step else None)
                except:
                    traceback.print_exc()

        if log_this_step:
            self.target_update_counter += 1

        if self.target_update_counter > UPDATE_TARGET_EVERY:
            with self.graph.as_default():
                set_session(self.sess)
                self.target_model.set_weights(self.model.get_weights())
                self.target_update_counter = 0

    def get_qs(self, state):
        #set_session(self.sess)
        return self.model.predict(state)[0]

    def train_in_loop(self):
        print("LOAD")
        
        X = np.random.uniform(size=(1, 1, 9)).astype(np.float32)
        y = np.random.uniform(size=(1, 8)).astype(np.float32)


        with self.graph.as_default(): ##############################################
            set_session(self.sess)
            try:
                self.model.fit(X,y, verbose=False, batch_size=1)
            except Exception as e:
                print(e)
        self.training_initialized = True

        while True:
            if self.terminate:
                return
            try:
                self.train(None, None)
            except:
                traceback.print_exc()
            time.sleep(0.01)

if __name__ == '__main__':
    print("Starting Training")
    DT = 1./20
    # For stats
    ep_rewards = [-200]

    # For more repetitive results
    random.seed(1)
    np.random.seed(1)
    #tf.set_random_seed(1)

    # Memory fraction, used mostly when trai8ning multiple agents
    #gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=MEMORY_FRACTION)
    #tf.config.gpu.set_per_process_memory_fraction(0.4)
    #tf.config.gpu.set_per_process_memory_growth(True)

    # Create models folder
    

    # Create agent and environment
    
    agent = DQNAgent()
    env = Master_Handler(filename = 'tracks/second.txt', dt = DT)


    tf.compat.v1.global_variables_initializer()
    # Start training thread and wait for training to be initialized
    trainer_thread = Thread(target=agent.train_in_loop, daemon=True)
    trainer_thread.start()
    while not agent.training_initialized:
        #print("WAIT")
        time.sleep(0.01)
    print("SUCCESS STARTING")
    # Initialize predictions - forst prediction takes longer as of initialization that has to be done
    # It's better to do a first prediction then before we start iterating over episode steps
    agent.get_qs(np.ones((1, 1, 9)))

    writer = CarWriter()
    write = True
    write_reward_max = -200
    write_dist_max = 0
    stats = [[], [], []] #epsilon, reward, distance
    # Iterate over episodes
    for episode in tqdm(range(1, EPISODES + 1), ascii=True, unit='episodes'):
        #if episode == EPISODES:
            #write = True

        #print(f"Episode: {episode}")
        try:

            #env.collision_hist = []

            # Update tensorboard step every episode
            agent.tensorboard.step = episode

            # Restarting episode - reset episode reward and step number
            episode_reward = 0
            step = 1

            # Reset environment and get initial state
            current_state, reward, done = env.reset()

            # Reset flag and start iterating until episode ends
            done = False
            episode_start = time.time()

            # Play for given number of seconds only
            while True:

                # This part stays mostly the same, the change is to query a model for Q values
                if np.random.random() > epsilon:
                    # Get action from Q table
                    action = np.argmax(agent.get_qs(current_state))
                else:
                    # Get random action
                    action = np.random.randint(0, 8)
                    # This takes no time, so we add a delay matching 60 FPS (prediction above takes longer)
                    #time.sleep(DT)
                try:
                    new_state, reward, done, dist = env.step(action)
                    #print(new_state, reward, done)
                    if not new_state.shape == (1, 1, 9):
                        print("State array got reshaped")
                    #sys.exit(1)
                except Exception as e:
                    print("First Point Error: ", e)
                    #sys.exit(1)
                    break
                if write:
                    writer.next_step(action)

                # Transform new continous state to new discrete state and count reward
                episode_reward += reward

                # Every step we update replay memory
                agent.update_replay_memory((current_state.tolist(), action, reward, new_state.tolist(), done))

                current_state = new_state
                step += 1

                if done:
                    break
                #print("Checkpoint")
            # End of episode - destroy agents
            env.wipe()

            # Append episode reward to a list and log stats (every given number of episodes)
            ep_rewards.append(episode_reward)
            if not episode % AGGREGATE_STATS_EVERY or episode == 1:
                average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:])/len(ep_rewards[-AGGREGATE_STATS_EVERY:])
                min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
                max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
                agent.tensorboard.update_stats(reward_avg=average_reward, reward_min=min_reward, reward_max=max_reward, epsilon=epsilon)

                # Save model, but only when min reward is greater or equal a set value
                #if min_reward >= MIN_REWARD:
                    #agent.model.save(f'models/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')

            # Decay epsilon
            if epsilon > MIN_EPSILON:
                epsilon *= EPSILON_DECAY
                epsilon = max(MIN_EPSILON, epsilon)

            if episode_reward > max_reward:
                writer.write(f'cardir/{MODEL_NAME}-{TRIAL_NUM}/{episode}-{int(episode_reward)}-{int(dist)}.txt')
                writer = CarWriter()
                max_reward = episode_reward
                print(f"New Max Reward: {max_reward}")
            if dist >  write_dist_max:
                write_dist_max = dist
                print(f"New Max Distance: {dist}")
                if episode_reward != max_reward:
                    writer.write(f'cardir/{MODEL_NAME}-{TRIAL_NUM}/{episode}-{int(episode_reward)}-{int(dist)}.txt')
            stats[0].append(epsilon)
            stats[1].append(episode_reward)
            stats[2].append(dist)
        except Exception as e:
            print("Second Point Error", e)
            break

    write_stats(stats, f'stats/{MODEL_NAME}-{TRIAL_NUM}-{episode}-{int(episode_reward)}-{int(dist)}.txt')
        #riter = CarWriter



    # Set termination flag for training thread and wait for it to finish
    agent.terminate = True
    trainer_thread.join()
    agent.model.save(f'models/{MODEL_NAME}__{TRIAL_NUM}.model')
