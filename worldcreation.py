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
import sys
from custom_io import *

key = pyglet.window.key
#world_dims = [1000, 1000] #width, height

window = pyglet.window.Window(960, 540)
grid = gridEngine(960, 540)
pot_grids = []

batch = pyglet.graphics.Batch()

save_elems = [] #A list of all coordinates and 
render_elems = [] #List of all previous track elems so they stay rendered

curr_elem = 'start' #Others -- 'turn', 'line'
first = True
currelem_save = [] #pair of coordinates
currelem_obj = [] #The current track elem render objs
x_fac = np.divide(500, 960)
y_fac = np.divide(500, 540)
err_list = []

engine = gridEngine(960, 540)
batch = pyglet.graphics.Batch()

print('starting now')
@window.event
def on_draw():
    global batch
    window.clear()
    batch.draw()

@window.event
def on_key_press( symbol, modifiers):
    # Do something when a key is pressed?
    # Pause the audio for instance?
    # use `if symbol == key.SPACE: ...`

    # This is just an example of how you could load the audio.
    # You could also do a standard input() call and enter a string
    # on the command line.
    #print(symbol)
    global curr_elem
    global first

    if symbol == key.Q:
        #Leave
        print(save_elems) #Save into file
    if first:
        return
    elif symbol == key.LEFT:
        curr_elem = 'turn'
    elif symbol == key.RIGHT:
        curr_elem = 'line'
    on_draw()

@window.event
def on_mouse_motion(x, y, dx, dy):
    #print(x, y)
    #print("wtf")
    global first
    global curr_elem
    if first:
        return
    if curr_elem == 'start':
        draw_startingStrip(x, y)
    elif curr_elem == 'turn':
        draw_turnElem(x, y)
    elif curr_elem == 'line':
        draw_lineElem(x, y)   
    on_draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    '''
    Save the current valid track elem and move on to the next
    '''
    #print(x, y)
    global curr_elem
    global first
    global currelem_save
    global currelem_obj
    global grid
    global pot_grids

    if not first:
        currelem_save.insert(0, curr_elem)
        currelem_save.append(currelem_obj.endPoint.givePos()) #Treats cases of current invalid position and line_elem projection
        save_elems.append(currelem_save)
        render_elems.append(currelem_obj)
        grid.register_track(pot_grids, currelem_obj)
        pot_grids = []
        if curr_elem == 'start':
            curr_elem = 'line'
    else:
        print("First point")
        first = False
    currelem_save = [[x, y]]
    currelem_obj = []
    on_draw()
    
    '''
    if self.curr_elem == 'start':
        pass #Register elem into the gridEngine
    elif self.curr_elem == 'turn':
        pass
    elif self.curr_elem == 'line':
        pass
    ''' #Nothing else needs to be done, right?
    
def draw_startingStrip( x, y, length = 20):
    '''
    The startingStrip is being given a fixed length to allow space for car objs
    Will enforce the length limit next
    '''
    #print("draw_startingStrip")
    global currelem_obj
    global batch
    global currelem_save
    global pot_grids
    global grid
    #print("here?")

    currelem_obj = StartingStrip(Point(*currelem_save[0]), Point(x, y))
    success, grids = grid.check_track(currelem_obj)
    if success: 
        pot_grids = grids
        currelem_obj.render(1, 1, batch)


def draw_turnElem( x, y, min_rad = 10):
    global currelem_obj
    global batch

    global err_list

    global grid
    global pot_grids

    stuff = circCalc(render_elems[-1].endPoint, Point(x, y))
    if stuff != None and stuff[1] >= 2 * trackWidth:
        #print(stuff)
        err_list = [render_elems[-1].endPoint, [x, y]]
        val = TurnElement(render_elems[-1], Point(x, y))
        success, grids = grid.check_track(val)
        success, grids = True, []
        #print(success, x, y)
        if success:
            pot_grids = grids
            currelem_obj = val
            currelem_obj.render(1, 1, batch)

    
def draw_lineElem( x, y, min_length = 1):
    '''
    Takes only the given x value and outputs the projected line elem, since
    it already has an angle. Hence, y val is irrelevant here
    '''
    global currelem_obj
    global batch

    global grid
    global pot_grids

    start = render_elems[-1].endPoint
    delt_y = (x - start.xPos) * np.tan(start.dirVec)
    y = start.yPos + delt_y

    val = LineElement(render_elems[-1], Point(x, y))
    success, grids = grid.check_track(val)
    success, grids = True, []
    #print(success, x, y)
    if success:
        pot_grids = grids
        currelem_obj = val
        currelem_obj.render(1, 1, batch)

    

try:
    pyglet.app.run()
finally:
    print("Whatever happened, look at this shit")
    print(save_elems)
    print(render_elems)
    print(currelem_save)
    x = input("Write?")
    if x == "y":
        w = TrackWriter(save_elems)
        w.write('tracks/second.txt', 960, 540)
    print("Final error list: ", err_list)