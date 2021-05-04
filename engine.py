import pyglet
import numpy as np
from env import *
from car import *
import render

class Master_Handler:
    def __init__(self, filename, dt = 1/10) -> None:
        '''
        Reads and initializes the track
        '''
        self.track = Track(filename)
        self.agents = [] #will be in terms of lists - [agent, inp_func]
        self.agents_alive = []
        self.dt = dt
        self.window = None


    def add_agent(self, inp_func, pos, dims, agent_class = Thing, updatewin = False):
        '''
        Adds a new agent
        '''
        new_agent = agent_class(pos, dims, init_angle = self.track.startAngle())
        self.agents.append([new_agent, inp_func])
        self.agents_alive.append(True)
        if updatewin:
            self.window.agents = [elem[0] for elem in self.agents]

    def control_agents(self):
        '''
        Iterates through the agents list and calls on the controls and passes htem on to the agents
        '''
        for num in range(len(self.agents_alive)):
            if self.agents_alive[num]:
                pair = self.agents[num]
                # do the newstate, reward, done -- here
                pair[0].register_control(pair[1](), self.dt) 
                val = self.track.checkCollision(pair[0].funcs)
                print(val, self.agents[0][0].centre)
                self.agents_alive[num] = not val

    
    def master_update(self, dt):
        #print("Running")
        self.control_agents()
        if self.window != None: #Part for rendering
            self.window.update(dt)
    
    def window_setup(self):
        self.window = render.main(self.track, [elem[0] for elem in self.agents])
    
    def start_render(self):
        self.window.run(self.master_update, self.dt)

    def wipe(self):
        '''
        Resets the gamestate so numerous trials can occur in the same state and 
        new objs do not need to be created each instance
        '''
        self.agents = []
        self.agents_alive = []
        if self.window != None:
            self.window.close()
        self.window = None


x = Master_Handler('tracks/first.txt')
print("Done")
x.window_setup()
x.add_agent(x.window.give_input, [100, 100], [5, 3], updatewin = True)
#print(x.agents[0][0].funcs)
x.start_render()
print("Done")