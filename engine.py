from custom_io import CarReader
import pyglet
import numpy as np
from env import *
from car import *
import render

class Master_Handler:
    def __init__(self, filename = 'tracks/first.txt', dt = 1/20) -> None:
        '''
        Reads and initializes the track
        '''
        
        self.track = Track(filename)
        self.agents = [] #will be in terms of lists - [agent, inp_func]
        self.agents_alive = []
        self.dt = dt
        self.window = None
        self.time = 10
        self.trials_left = np.divide(self.time, dt) #60 seconds
        self.first = None


    def add_agent(self, inp_func, dims, agent_class = Thing):
        '''
        Adds a new agent
        '''

        a, b= self.track.startAngle()

        new_agent = agent_class(b.givePos(), dims, init_angle = a)
        self.agents.append([new_agent, inp_func])
        self.agents_alive.append(True)


    def control_agents(self):
        '''
        Iterates through the agents list and calls on the controls and passes htem on to the agents
        '''
        if self.trials_left <= 0:
            self.agents_alive = [False]
        for num in range(len(self.agents_alive)):
            if self.agents_alive[num]:
                pair = self.agents[num]
                # do the newstate, reward, done -- here
                con = pair[1]()
                #print(con, self.trials_left)
                pair[0].register_control(con, self.dt)
                #state, reward, done = self.track.give_stuff(pair[0], self.dt)
                #print(state)
                #print(reward, pair[0].dist_travelled)
                #print(state)
                #print(val, self.agents[0][0].centre)
                #self.agents_alive[num] = not done
                
    def master_update(self, dt):

        #print("Running")
        self.trials_left -= 1
        self.control_agents()
        if self.window != None: #Part for rendering
            self.window.update(dt)


        
    
    def window_setup(self):
        self.window = render.main(self.track, [elem[0] for elem in self.agents])
    
    def start_render(self):
        self.window.agents = [elem[0] for elem in self.agents]
        self.window.run(self.master_update, self.dt)

    def wipe(self):
        '''
        Resets the gamestate so numerous trials can occur in the same state and 
        new objs do not need to be created each instance
        '''
        self.agents = []
        self.agents_alive = []
        self.trials_left = np.divide(self.time, self.dt) #60 seconds
        if self.window != None:
            self.window.close()
        self.window = None

    '''
    Single car - DQNAgent training functions
    '''
    def reset(self):
        self.wipe()
        self.add_agent(None, [8, 5])
        self.first = self.agents[0][0]
        self.agents_alive = [True]
        return self.track.give_stuff(self.first, self.dt)
    
    def step(self, control):
        #print(self.trials_left)
        if not self.agents_alive[0]:
            state, reward, done = self.track.give_stuff(self.first, self.dt)
            return state, reward, True
        self.trials_left -= 1
        self.first.register_control(self.track.convert_DQNaction(control), self.dt)
        state, reward, done = self.track.give_stuff(self.first, self.dt)
        self.agents_alive[0] = not done
        done = True if self.trials_left == 0 else done
        if done:
            print(f"Finished with {self.trials_left} frames left, last reward: {reward}, distance: {self.first.dist_travelled}")
        return state, reward, done, self.first.dist_travelled


# x = Master_Handler('tracks/first.txt')
# print("Done")
# x.window_setup()
# x.add_agent(x.window.give_input, [8, 5], updatewin = True)
# #print(x.agents[0][0].funcs)
# x.start_render()
# print("Done")
# x.wipe()

def display_main(track = 'tracks/first.txt', cons = ["key"]):
    main = Master_Handler(track)
    main.window_setup()
    for elem in cons:
        try:
            if elem == "key":
                main.add_agent(main.window.give_input, [8, 5])
            else:
                read = CarReader(elem)
                main.add_agent(read.next, [8, 5])
            print(f"Successfully added Agent: {elem}")
        except Exception as e:
            print(f"Failed to add Agent: {elem}")
    main.start_render()
    main.wipe()



