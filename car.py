import numpy as np
from calcmath import *
from pyglet import shapes

class Thing: #Most basic controllable car, a rectangle without wheels
    speed_range = [-80, 80]
    steer_range = [-np.pi/3, np.pi/3]
    minspd = 60
    slprng = np.multiply(50/180, np.pi) 
    acc = 30 #acceleration
    turn_acc = np.pi/4
    friction = 5
    turn_rate = np.pi/4 #angle per second
    def __init__(self, pos, dims, init_angle = np.pi/2, init_speed = 0) -> None:
        '''
        Initializes the steering car
        Args - 
        pos - [x, y] starting position of car
        dims - [height, width] dimensions of car
        init_angle - starting angle w.r.t xy coords
        init_speed - the initial scalar speed
        Movement is broken down into current orientation, scalar speed and steering angle
        Need to make pos a point with angle part of it
        Currently it has only steering only changes angle, implementing proper steering
        '''
        #Render variables

        self.centre = Point(*pos, init_angle)
        self.dims = dims
        self.try_render = None
        self.anchor_add = np.arctan(np.divide(*dims)) + np.pi/2
        self.funcs = self.create_funcs()
        self.speed = init_speed
        self.steer = 0
        self.val = 0


            
        #self.prev_orientation = np.pi/2 #render orientation

    def register_control(self, controls, dt):
        '''
        Input args - control list, time diff
        - controls - [1, 1, 1, 1] of the form [w, a, s, d] indicating which is pressed
        0 - not pressed
        1 - pressed
        -dt the time difference
        '''
        self.speed_change(controls, dt)
        if self.speed != 0 : #Can only steer when moving
            self.steering_turn(controls, dt)
        self.apply_friction(dt)
        self.move(controls, dt)
    
    def speed_change(self, controls, dt):
        '''
        Changes the speed of the car object
        Separate function to introduce complexities like difference deleration for braking when needed
        '''
        delt_speed = np.multiply(self.acc, dt) * (controls[0] - controls[2]) #no acc if both are pressed
        new_speed = self.speed + delt_speed 
        if self.speed_range[0] <= new_speed <= self.speed_range[1]:
            self.speed = new_speed

    def regular_turn(self, controls, dt):
        '''
        Simulates simplistic and regular turning 
        Holding steering keys only turns the object's orientation
        Constant angular rate of change
        '''
        self.delt_turn = np.multiply(self.turn_rate, dt) * (controls[1] - controls[3]) #no turn if both are pressed
        self.centre.dirVec = rad_reduce(self.centre.dirVec + self.delt_turn)
        

    def steering_turn(self, controls, dt):
        '''
        Simulates a form of steering turn
        Holding steering keys changes rate of angular change
        '''
        self.delt_steer = np.multiply(self.turn_acc, dt) * (controls[1] - controls[3]) #no change if both are pressed
        self.val = self.steer + self.delt_steer
        if self.steer_range[0] <= self.val <= self.steer_range[1]:
            self.steer = self.val
        
        delt_turn = np.multiply(self.steer, dt)
        self.centre.dirVec = rad_reduce(self.centre.dirVec + delt_turn)



    def apply_friction(self, dt):
        val = max(abs(self.speed) - np.multiply(self.friction, dt), 0)
        if val > 0:
            mult = (abs(self.speed) / self.speed)
            val = val * mult
        self.speed = val


    def move(self, controls, dt):
        '''
        Simplistic moving command that disregards previous momentum (How would our shit change if we begin to include it?)
        '''


        newAng = self.centre.dirVec

        if self.is_drift():
            
            if controls[1] == 1:
                newAng -= np.pi/2
            elif controls[3] == 1:
                newAng += np.pi/2
            self.speed -= 0.5
        delt_x = np.multiply(self.speed * np.cos(newAng), dt)
        delt_y = np.multiply(self.speed * np.sin(newAng), dt)


        
        self.centre.xPos += delt_x
        self.centre.yPos += delt_y
        #print(self.centre)
        self.funcs = self.create_funcs()
    

    def render(self, batch):
        '''
        we have centre pos and angle, calculate four points
        '''
        use_angle = self.centre.dirVec + self.anchor_add
        anchor = angledpoint_end(self.centre, use_angle, np.sqrt(self.dims[0]**2 + self.dims[1]**2)/2)
        use_angle = rad_deg(self.centre.dirVec - np.pi/2)
        self.try_render = shapes.Rectangle(anchor.xPos, anchor.yPos, height = self.dims[0], width = self.dims[1], color = (255, 255, 255), batch = batch)
        self.try_render.rotation = - use_angle

    def init_render(self, batch):
        '''
        Initializes the render object
        '''
        self.render(batch)
    
    def update(self):
        '''
        Does not re-initialize the render object but only shifts its position and orientation
        '''
        use_angle = self.centre.dirVec + self.anchor_add
        anchor = angledpoint_end(self.centre, use_angle, np.sqrt(self.dims[0]**2 + self.dims[1]**2)/2)
        use_angle = rad_deg(self.centre.dirVec - np.pi/2)
        self.try_render.anchor_position = anchor.givePos()
        self.try_render.rotation = - use_angle
        
    def create_funcs(self):
        '''
        Initializes 4 line function objects for the car
        '''
        cen_front = angledpoint_end(self.centre, self.centre.dirVec, np.divide(self.dims[0], 2))
        cen_back = angledpoint_end(self.centre, np.pi + self.centre.dirVec, np.divide(self.dims[0], 2))

        perp_angle = self.centre.dirVec - np.pi/2

        diffx = np.divide(self.dims[1], 2) * np.cos(perp_angle)
        diffy = np.divide(self.dims[1], 2) * np.sin(perp_angle)
        lower = [cen_front.xPos + diffx, cen_front.yPos + diffy]
        lower += [cen_back.xPos + diffx, cen_back.yPos + diffy]

        upper = [cen_front.xPos - diffx, cen_front.yPos - diffy]
        upper += [cen_back.xPos - diffx, cen_back.yPos - diffy]
        #Define the function classes with these points
        #Should be lower, upper [lower[0], upper[0]], [lower[1], upper[1]]

        to_return = [math_func(lower, True), math_func(upper, True), 
        math_func(lower[0:2] + upper[0:2], True), math_func(lower[2:4] + upper[2:4], True)]
        return to_return
   
    
    def hud(self, loc):
        '''
        Creates a small hud for steering wheel and info
        kind of a fun thing, but wast of time
        '''
        pass
    def is_drift(self):

        if abs(self.speed) >= self.minspd:
            if abs(self.val) >=  self.slprng:
                return True

        else:
            return False

    

        


class Car(Thing):
    def __init__(self) -> None:
        super().__init__()

class Wheel:
    def __init__(self) -> None:
        pass