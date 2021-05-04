
import pyglet


key = pyglet.window.key

class main(pyglet.window.Window):
    def __init__ (self, track, agents, width=960, height=540):
        super(main, self).__init__(width, height)
        self.ref = [key.W, key.A, key.S, key.D]
        self.input = [0, 0, 0, 0]
        self.alive = 1
        self.trackBatch = pyglet.graphics.Batch()
        self.agentBatch = pyglet.graphics.Batch()
        self.agents = agents
        self.tracks = track
        self.tracks.render(self.trackBatch) #Only need to run once

    
    def give_input(self):
        '''
        Groups the pyglet input and gives like this. \\
        Thinking of implementing RL controls like this, common standard.
        Could be altered to accomodate slider steering.
        '''
        #print(self.input)
        return self.input

    def update_inp(self, symbol, val):
        '''
        Alters the inpus list to reflect key input
        val - 0, 1 (the number to overwrite with)
        called with 1 in on_key_press
        called with 0 in on_key_release
        '''
        if symbol == key.W:
            self.input[0] = val
        elif symbol == key.A:
            self.input[1] = val
        elif symbol == key.D:
            self.input[3] = val
        elif symbol == key.S:
            self.input[2] = val
        

    def on_close(self):
        self.alive = 0

    def on_key_release(self, symbol, modifiers):
        self.update_inp(symbol, 0)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE: # [ESC]
            self.alive = 0
            pyglet.clock.unschedule(self.update)
            self.close()
        self.update_inp(symbol, 1)
        #print(symbol)
    

    def render(self):
        self.clear()
        #print(self.agents)
        for agent in self.agents:
            #print("Draw?")
            agent.render(self.agentBatch)
        self.trackBatch.draw()
        self.agentBatch.draw()
    
    def on_draw(self):
        self.clear()
        self.trackBatch.draw()
        self.agentBatch.draw()

    def update(self, dt):
        #print("This next")
        self.render()
    
    def run(self, update_func, dt):
        pyglet.clock.schedule_interval(update_func, dt)
        pyglet.app.run()


