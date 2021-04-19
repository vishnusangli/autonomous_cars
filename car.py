import numpy as np
from calcmath import *
from pyglet import shapes

class Thing: #Most basic controllable car, a rectangle without wheels
    speed_range = [-20, 50]
    acc = 5 #acceleration
    steer = np.pi/4 #angle per second
    def __init__(self, pos, dims, batch, init_angle = np.pi/2, init_speed = 0) -> None:
        self.pos = pos #Currently I've made some bullshit of interpreting this as anchor, it must be centre point
        self.angle = init_angle
        self.speed = init_speed
        self.dims = dims
        self.render_obj = []
        self.calc_render_args(batch)
        #self.prev_orientation = np.pi/2 #render orientation

    def register_control(self, controls, friction, dt):
        '''
        Input args - control list, time diff
        - controls - [1, 1, 1, 1] of the form [w, a, s, d] indicating which is pressed
        0 - not pressed
        1 - pressed
        -dt the time difference
        '''
        delt_speed = np.multiply(self.acc, dt) * (controls[0] - controls[2]) #no acc if both are pressed
        new_speed = self.speed + delt_speed 
        if self.speed_range[0] <= new_speed <= self.speed_range[1]:
            self.speed = new_speed
        if self.speed != 0 : #Can only steer when moving
            delt_steer = np.multiply(self.steer, dt) * (controls[1] - controls[3]) #no turn if both are pressed
            self.angle = rad_reduce(self.angle + delt_steer)

        self.move(dt)

    def apply_friction(self):
        pass
    def move(self, dt):
        '''
        Simplistic moving command that disregards previous momentum (How would our shit change if we begin to include it?)
        '''
        delt_x = np.multiply(self.speed * np.cos(self.angle), dt)
        delt_y = np.multiply(self.speed * np.sin(self.angle), dt)

        self.pos[0] += delt_x
        self.pos[1] += delt_y


    def render(self, batch):
        '''
        Will first render
        '''
        self.render_obj = shapes.Rectangle(self.pos[0], self.pos[1], height = self.dims[0], width = self.dims[1], color=(255, 255, 255), batch=batch)
        self.render_obj.rotation = - rad_deg(self.angle)
    
    def change(self):
        self.render_obj.anchor_x = self.pos[0]
        self.render_obj.anchor_y = self.pos[1]
        self.render_obj.rotation = -deg_rad(self.angle)
        #print(self.speed)

    def calc_render_args(self, batch):
        '''
        we have centre pos and angle, calculate four points
        '''
        cen_x = self.pos[0]
        cen_y = self.pos[1]

        cen_front = angledpoint_end(Point(cen_x, cen_y), self.angle, np.divide(self.dims[0], 2))
        cen_back = angledpoint_end(Point(cen_x, cen_y), np.pi + self.angle, np.divide(self.dims[0], 2))

        perp_angle = self.angle - np.pi/2
        
        diffx = np.divide(self.dims[1], 2) * np.cos(perp_angle)
        diffy = np.divide(self.dims[1], 2) * np.sin(perp_angle)
        lower = [cen_front.xPos + diffx, cen_front.yPos + diffy]
        lower += [cen_back.xPos + diffx, cen_back.yPos + diffy]

        upper = [cen_front.xPos - diffx, cen_front.yPos - diffy]
        upper += [cen_back.xPos - diffx, cen_back.yPos - diffy]
        #print(self.angle)
        first = []
        first.append(shapes.Line(*lower, color = (255, 255, 255), batch=batch))
        first.append(shapes.Line(*upper, color = (255, 255, 255), batch=batch))
        self.render_obj = first




class Car(Thing):
    def __init__(self) -> None:
        super().__init__()

class Wheel:
    def __init__(self) -> None:
        pass
