import pyglet
from pyglet import shapes
import math
import numpy as np
from pyglet.gl import *

window = pyglet.window.Window(960, 540)
batch = pyglet.graphics.Batch()

circle = shapes.Circle(700, 150, 100, color=(50, 225, 30), batch=batch)
square = shapes.Rectangle(200, 200, 200, 200, color=(55, 55, 255), batch=batch)
rectangle = shapes.Rectangle(250, 300, 400, 200, color=(255, 22, 20), batch=batch)
rectangle.opacity = 128
rectangle.rotation = 90
line = shapes.Line(100, 100, 100, 200, width=19, batch=batch)
line2 = shapes.Line(150, 150, 444, 111, width=4, color=(200, 20, 20), batch=batch)
arc = shapes.Arc(100, 400, 34, segments=25, angle=np.pi, color=(255, 255, 0), batch=batch)
arc1 = shapes.Arc(150, 400, 34, segments=25, angle=np.pi * 0.5, color=(255, 255, 0), batch=batch)
arc2 = shapes.Arc(200, 400, 34, segments=25, angle=np.pi * 0.2, color=(255, 255, 0), batch=batch)
arc.rotation = 50
circle1 = shapes.Circle(900, 150, 100, color=(50, 225, 30), batch=batch)
def PointsInCircum(r, n=25, pi=3.14):
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]
pts = np.array(PointsInCircum(20))

frame = 0
def update_frame(x, y):
    global frame
    if frame == None or frame == pts.shape[0]-1:
        frame = 0
    else:
        frame += 1

@window.event
def on_draw():
    window.clear()
    batch.draw()
    glBegin(GL_LINES)
    glVertex3f(100,100,0)
    glVertex3f(pts[frame][1]+100,pts[frame][0]+100,0)
    glEnd()

pyglet.clock.schedule(update_frame, 1/10.0)
pyglet.app.run()