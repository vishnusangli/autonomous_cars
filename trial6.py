import pyglet
from pyglet import shapes
from pyglet.window import mouse
from pyglet.window import key
import numpy as np
from pyglet.gl import *


from calcmath import *
from car import *

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()
move = Thing([100, 100], [30, 20])
keys = []


def update_frame(dt):
    global move
    global batch
    global friction
    inp = create_input(keys)
    move.register_control(inp, dt)
    #move.update()
    move.render(batch)
    #batch.draw()

def give_conv(symbol):
    ref = [key.W, key.A, key.S, key.D]
    if symbol in ref:
        return symbol
    else:
        return None
    

def create_input(conts):
    '''
    Returning list is of [w, a, s, d] format
    '''
    to_return = [0, 0, 0, 0]
    if key.W in conts:
        to_return[0] = 1 
    if key.A in conts:
        to_return[1] = 1
    if key.S in conts:
        to_return[2] = 1
    if key.D in conts:
        to_return[3] = 1

    return to_return

@window.event
def on_key_press(symbol, modifiers):
    val = give_conv(symbol)
    if val and not val in keys:
        keys.append(val)

@window.event
def on_key_release(symbol, modifiers):
    val = give_conv(symbol)
    if val and val in keys:
        keys.remove(val)

@window.event
def on_draw():
    global batch
    window.clear()
    batch.draw()

#pyglet.clock.schedule(update_frame, 1./30)
pyglet.clock.schedule_interval(update_frame, 1/60.0)
pyglet.app.run()