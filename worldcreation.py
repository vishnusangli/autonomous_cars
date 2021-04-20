

'''
This is the warm up assignment to the racetrack rendering
Should be completely standalone, including the render loop
'''

'''
Track input should be done as a track buffered object
The saved track should be of the same form of input as one gets when interactively creating it
'''
import numpy as np
import pyglet
from pyglet.window import key
from pyglet.gl import *

from env import *

key = pyglet.window.key


class main(pyglet.window.Window):
    def __init__ (self, height, width):
        super(main, self).__init__(500, 500, fullscreen = False)

        self.save_elems = [] #A list of all coordinates and 
        self.render_elems = [] #List of all previous track elems so they stay rendered

        self.curr_elem = 'start' #Others -- 'turn', 'line'
        self.first = True
        self.currelem_save = [] #pair of coordinates
        self.currelem_obj = [] #The current track elem render objs
        self.x_fac = np.divide(500, width)
        self.y_fac = np.divide(500, height)

        self.engine = gridEngine(height, width)
        self.batch = pyglet.graphics.Batch()
        self.alive = 1

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_close(self):
        self.alive = 0

    def on_key_press(self, symbol, modifiers):
        # Do something when a key is pressed?
        # Pause the audio for instance?
        # use `if symbol == key.SPACE: ...`

        # This is just an example of how you could load the audio.
        # You could also do a standard input() call and enter a string
        # on the command line.
        if symbol == key.Q:
            #Leave
            print(self.save_elems) #Save into file
            self.alive = 0
        if self.first:
            return
        elif symbol == key.LEFT:
            self.curr_elem = 'turn'
        elif symbol == key.RIGHT:
            self.curr_elem = 'line'

    def on_mouse_motion(self, x, y, dx, dy):
        if self.first:
            return

        if self.curr_elem == 'start':
            self.draw_startingStrip(x, y)
        elif self.curr_elem == 'turn':
            self.draw_turnElem(x, y)
        elif self.curr_elem == 'line':
            self.draw_lineElem(x, y)   
        print("Drew?")
        
        
    def on_mouse_press(self, x, y, button, modifiers):
        '''
        Save the current valid track elem and move on to the next
        '''
        if not self.first:
            self.currelem_save.insert(0, self.curr_elem)
            self.save_elems.append(self.currelem_save)
            self.render_elems.append(self.currelem_obj)
        else:
            self.first = False
        self.currelem_save = [x, y]
        self.currelem_obj = []


        '''
        if self.curr_elem == 'start':
            pass #Register elem into the gridEngine
        elif self.curr_elem == 'turn':
            pass
        elif self.curr_elem == 'line':
            pass
        ''' #Nothing else needs to be done, right?
        

    def draw_startingStrip(self, x, y, length = 20):
        '''
        The startingStrip is being given a fixed length to allow space for car objs
        Will enforce the length limit next
        '''
        print("draw_startingStrip")
        self.currelem_obj = StartingStrip(Point(*self.currelem_save), Point(x, y))
        self.currelem_obj.render(1, 1, self.batch)

    def draw_turnElem(self, x, y, min_rad = 10):
        self.currelem_obj = TurnElement(self.render_elems[-1], Point(x, y))
        self.currelem_obj.render(1, 1, self.batch)

    def draw_lineElem(self, x, y, min_length = 1):
        '''
        Takes only the given x value and outputs the projected line elem, since
        it already has an angle. Hence, y val is irrelevant here
        '''
        self.currelem_obj = LineElement(self.render_elems[-1], Point(x, y))
        self.currelem_obj.render(1, 1, self.batch)

    def render(self):
        self.clear()
        self.flip()

    def run(self):
        while self.alive == 1:


            # -----------> This is key <----------
            # This is what replaces pyglet.app.run()
            # but is required for the GUI to not freeze
            #
            event = self.dispatch_events()
        

x = main(500, 500)
x.run()
