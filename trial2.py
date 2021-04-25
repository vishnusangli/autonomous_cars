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


line = None
line1 = shapes.Line(0, 270, 960, 270, batch=batch)
line2 = shapes.Line(480, 0, 480, 540, batch=batch)

its_angle = np.pi/4
its_rotation = 0
try_arc = shapes.Arc(480, 270, 100, segments=25, angle=its_angle, color=(255, 255, 255), batch=batch)
try_arc.rotation = its_rotation

def update_frame(dt):
    global try_arc
    global its_angle
    global its_rotation
    #its_angle += np.multiply(np.pi/16, dt)
    its_rotation -= np.multiply(20, dt)
    try_arc = shapes.Arc(480, 270, 100, segments=25, angle=its_angle, color=(255, 255, 255), batch=batch)
    try_arc.rotation = its_rotation
    batch.draw()
move = True

@window.event
def on_mouse_press(x, y, button, modifiers):
    global line
    global move
    if move:
        line = shapes.Line(480, 270, x, y, batch=batch)
        do_thing(480, 270, x, y, batch)
        do_thing2(480, 270, x, y, batch)
    move = not move

@window.event
def on_mouse_motion(x, y, dx, dy):
    global line
    global move
    if (move):
        line = shapes.Line(480, 270, x, y, batch=batch)
        do_thing(480, 270, x, y, batch)
        do_thing2(480, 270, x, y, batch)


#@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global line
    line = shapes.Line(480, 270, x, y, width=19, batch=batch)




@window.event
def on_draw():
    window.clear()
    batch.draw()

line5 = None
line6 = None
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
line8 = None
line9 = None

rad_deg = lambda x: x * (180./np.pi)
deg_rad = lambda x: x * (np.pi/180.)

def do_thing2(x1, y1, x2, y2, batch):
    global arc5
    global arc6
    global arc7
    global line8
    global line9

    start = Point(x1, y1, np.pi/2)
    end = Point(x2, y2)
    width = 10

    try_val = circCalc(start, end)
    if try_val != None:
        anchor, radius, phi, rotate = try_val
        #print(start, end, anchor, radius, phi, rotate)
        #print(rad_deg(rotate))
        #phi = 2 * np.pi
        #print(start, end, anchor, rotate)
        arc5 = shapes.Arc(anchor.xPos, anchor.yPos, radius, segments=25, angle=phi, color=(255, 255, 255), batch=batch)
        arc5.rotation = rotate

        arc6 = shapes.Arc(anchor.xPos, anchor.yPos, radius - width, segments=25, angle=phi, color=(255, 255, 255), batch=batch)
        arc6.rotation = rotate

        arc7 = shapes.Arc(anchor.xPos, anchor.yPos, radius + width, segments=25, angle=phi, color=(255, 255, 255), batch=batch)
        arc7.rotation = rotate

        line8 = shapes.Line(0, anchor.yPos, 960, anchor.yPos, batch=batch)
        line9 =  shapes.Line(anchor.xPos, 0, anchor.xPos, 540, batch=batch)
    
pyglet.clock.schedule_interval(update_frame, 1/60.0)
pyglet.app.run()