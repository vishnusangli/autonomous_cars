import pyglet
from pyglet import shapes
from pyglet.window import mouse
from pyglet.window import key
import math
import numpy as np
from pyglet.gl import *

window = pyglet.window.Window(960, 540)
keys = key.KeyStateHandler()
window.push_handlers(keys)
batch = pyglet.graphics.Batch()


thing = shapes.Rectangle(100, 100, 30, 40, batch = batch)
angle = np.pi/2
speed = 0



frame = 0
a = 255
def update(dt):
    global a
    a -= 10
    thing.color = (a, a, a)
    a = 255 if a == 0 else a
    if keys[key.A]:
        a = 0


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        thing.y += 2
    elif symbol == key.A:
        thing.x -= 2
    elif symbol == key.S:
        thing.y -= 2
    elif symbol == key.D:
        thing.x += 2


@window.event
def on_text(motion):
    if motion == key.MOTION_UP:
        thing.y += 2
    elif motion == key.A:
        thing.x -= 2
    elif motion == key.S:
        thing.y -= 2
    elif motion == key.D:
        thing.x += 2

@window.event
def on_draw():
    window.clear()
    batch.draw()
    
    
pyglet.clock.schedule_interval(update, 0.1)
pyglet.app.run()

