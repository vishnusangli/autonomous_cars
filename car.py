import pyglet as pt

import numpy as np

window = pt.window.Window()
batch = pt.graphics.Batch()



class car:
    lineWidth = 19
    def __init__(self, width, height, xloc, yloc):
        self.width = width
        self.height = height
        self.xloc = xloc
        self.yloc = yloc


    def construct (self): 
        shape = pt.shapes.Rectangle(self.xloc, self.yloc, width = self.width, height = self.height, color = (255, 255, 255), batch = batch)
        shape.opacity = 128
        return shape

    def line (self, angle, radius):
        vcfld = pt.shapes.Line(self.xloc, self.yloc, self.xloc + (radius*np.cos(90 - angle)), self.yloc + (radius*np.sin(90 - angle)), width= car.lineWidth, batch = batch)
        return vcfld



    

car1 = car(30, 20, 50, 50)
rectangle = car1.construct()
fl1 = car1.line(0, 30)
fl2 = car1.line(30, 30)
fl3 = car1.line(45, 30)
fl4 = car1.line(-30, 30)
fl5 = car1.line(-45, 30)

print(car1.yloc)



@window.event
def on_key_press(key, modifiers):
    global rectangle
    if (key == pt.window.key.UP):
        car1.yloc += 10
        rectangle = car1.construct()
    elif (key == pt.window.key.LEFT):
        car1.xloc -= 10
        rectangle = car1.construct()
    elif (key == pt.window.key.DOWN):
        car1.yloc -= 10
        rectangle = car1.construct()
    elif (key == pt.window.key.RIGHT):
        car1.xloc += 10
        rectangle = car1.construct()
    print(car1.xloc)
    
@window.event
def on_draw():
    window.clear()
    batch.draw()

pt.app.run()




    
        
