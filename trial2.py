import pyglet
from pyglet import shapes
from pyglet.window import mouse
import math
import numpy as np
from pyglet.gl import *

import importlib
from calcmath import *

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()



line = shapes.Line(100, 100, 100, 200, batch=batch)
arc = shapes.Arc(100, 400, 34, segments=25, angle=np.pi, color=(255, 255, 0), batch=batch)
rect = shapes.Rectangle(500, 500, height = 70, width = 30, color=(255, 255, 0), batch=batch)
rect.rotation = - 45
arc2 = shapes.Arc(100, 0, 100, segments=200, angle=np.pi/2, color=(255, 255, 0), batch=batch)
arc2.rotation = -90
line2 = shapes.Line(100, 100, 200, 100, batch=batch)

frame = 0
def update_frame(x, y):
    global frame

    if frame == None or frame == 20:
        frame = 0
    else:
        frame += 1
    batch.draw()
move = True

@window.event
def on_mouse_press(x, y, button, modifiers):
    global line
    global move
    if move:
        line = shapes.Line(100, 100, x, y, batch=batch)
        do_thing(100, 100, x, y, batch)
        do_thing2(100, 100, x, y, batch)
    move = not move

@window.event
def on_mouse_motion(x, y, dx, dy):
    global line
    global move
    if (move):
        line = shapes.Line(100, 100, x, y, batch=batch)
        do_thing(100, 100, x, y, batch)
        do_thing2(100, 100, x, y, batch)


#@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global line
    line = shapes.Line(100, 100, x, y, width=19, batch=batch)




@window.event
def on_draw():
    window.clear()
    batch.draw()

line7 = None
def do_thing(x1, y1, x2, y2, batch):
    global line5
    global line6
    global line7
    start = Point(x1, y1)
    end = Point(x2, y2)
    halfpi = np.pi/2
    width = 10
    #print(start.angle(end))
    perp = start.angle(end) - halfpi
    
    diff = Point(width * np.cos(perp), width * np.sin(perp))
    #print(perp)
    lower = Point(start.xPos + diff.xPos, start.yPos + diff.yPos)
    upper = Point(start.xPos - diff.xPos, start.yPos - diff.yPos)
    line7 = shapes.Line(lower.xPos, lower.yPos, upper.xPos, upper.yPos, batch=batch)

    upper_pair = Point(end.xPos - diff.xPos, end.yPos - diff.yPos)
    lower_pair = Point(end.xPos + diff.xPos, end.yPos + diff.yPos)

    line5 = shapes.Line(lower.xPos, lower.yPos, lower_pair.xPos, lower_pair.yPos, batch=batch)
    line6 = shapes.Line(upper.xPos, upper.yPos, upper_pair.xPos, upper_pair.yPos, batch=batch)

arc5 = None
arc6 = None
arc7 = None

rad_deg = lambda x: x * (180./np.pi)
deg_rad = lambda x: x * (np.pi/180.)

def do_thing2(x1, y1, x2, y2, batch):
    global arc5
    global arc6
    global arc7

    start = Point(x1, y1, np.pi/2)
    end = Point(x2, y2)
    halfpi = np.pi/2
    width = 10

    try_val = turnCalc(start, end)
    if try_val != None:
        anchor, radius, phi, rotate = try_val
        #print(start, end, anchor, radius, phi, rotate)
        #print(rad_deg(rotate))
        arc5 = shapes.Arc(anchor.xPos, anchor.yPos, radius, segments=25, angle=phi, color=(255, 255, 255), batch=batch)
        arc5.rotation = rotate

        arc6 = shapes.Arc(anchor.xPos, anchor.yPos, radius - width, segments=25, angle=phi, color=(255, 255, 255), batch=batch)
        arc6.rotation = rotate

        arc7 = shapes.Arc(anchor.xPos, anchor.yPos, radius + width, segments=25, angle=phi, color=(255, 255, 255), batch=batch)
        arc7.rotation = rotate
    
pyglet.clock.schedule(update_frame, 1/10.0)
pyglet.app.run()