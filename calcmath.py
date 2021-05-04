import numpy as np

rad_deg = lambda x: x * (180./np.pi)
deg_rad = lambda x: x * (np.pi/180.)

class Point:
    '''
    API used for reference points in track elements
    Standard --- Angle Radian System
    '''
    def __init__(self, xPos, yPos, dir = None) -> None: 
        self.xPos = xPos
        self.yPos = yPos

        self.dirVec = dir #Directional vector of movement & following track creation


    def angle(self, other):
        '''
        Common format to return in Radians
        '''
        d = np.inf
        if other.xPos - self.xPos != 0:
            d = np.divide(other.yPos - self.yPos, other.xPos - self.xPos)
        angle = np.arctan(d) 
    
        if d == np.inf and self.yPos > other.yPos:
            angle = -np.pi/2 #90 degrees to 270 degrees
        elif (angle < 0 and self.yPos < other.yPos):
            angle += np.pi #Negative angles in quadrant 4 to quadrant 2

        elif angle > 0 and self.yPos > other.yPos:
            angle = - np.pi + angle #Positive angles in quadrant 1 to quadrant 3
        
        elif angle == 0 and self.xPos >= other.xPos:
            angle = np.pi
        
    
        return angle

    
    def distance(self, other):
        '''
        Returns distance to another point
        '''
        delt_y = np.power(other.yPos - self.yPos, 2)
        delt_x = np.power(other.xPos - self.xPos, 2)
        to_return = np.sqrt(delt_x + delt_y)
        return to_return
    
    def gradient(self, other):
        '''
        Returns gradient
        '''
        val = np.divide(self.yPos - other.yPos, self.xPos - other.xPos)
        return val
    


    def givePos(self):
        return [self.xPos, self.yPos]
    
    def __str__(self):
        return 'Point[{0:4.4f}, {1:4.4f}]|'.format(self.xPos, self.yPos) + str(self.dirVec)
    
    def __repr__(self):
        return 'Point[{0:4.4f}, {1:4.4f}]|'.format(self.xPos, self.yPos) + str(self.dirVec)

def loc_gradient(x1, y1, x2, y2):
    '''
    Returns gradient
    '''
    if x1 == x2:
        if y2 > y1:
            return  np.inf
        elif y2 < y1:
            return -np.inf
        else:
            return 0
    val = np.divide(y1 - y2, x1 - x2)
    return val

def rad_reduce(x):
    while x < 0:
        x = (2 * np.pi) + x
        
    while x > 2 * np.pi:
        x -= 2 * np.pi
    
    if x > np.pi:
        x -= 2 * np.pi
    return x

def rad_sincircle(x):
    '''
    Reducing angle to only [0, 2pi], not [-pi, pi]
    '''
    while x < 0:
        x += (2 * np.pi)
        
    while x > 2 * np.pi:
        x -= (2 * np.pi)
    return x


def frame_angle(lims, theta):
    theta = rad_reduce(theta)
    
    '''
    If a valid angle is give, only 1 while loop would be used
    If invalid angle is given, first loop runs until overshot, after which second doesn't, returning 
    an angle that is beyond range
    '''
    lims.sort()
    while theta > lims[1]:
        theta -= (2 * np.pi)

    while theta < lims[0]:
        theta += (2 * np.pi)
        
    if lims[0] <= theta <= lims[1]:
        return theta
    else:
        #print(lims, theta)
        #print([a == theta for a in lims])
        return None


def get_angle(start, end):
    d = np.divide(end[1] - start[1], end[0] - start[0])
    angle = np.arctan(d) 
    
    if (angle < 0 and start[1] < end[1]):
        angle += np.pi
        
    elif angle > 0 and start[1] > end[1]:
        angle = np.pi - angle
    
    return angle

def get_distance(start, end):
    distance = np.sqrt(np.power(start[1] - end[1], 2) + np.power(start[0] - end[0], 2))
    return distance
    
    
def turnCalc(start, end):
    '''
    return anchor, angle, and rotation angle
    Next stage -- radius changing with track width
    '''
    halfpi = np.pi/2
    deriv = rad_reduce(start.dirVec)
    
    
    angle = start.angle(end)
    angle = frame_angle([deriv - halfpi, deriv + halfpi], angle) 

    if angle == None:
        return
    #Now both angles are in radians
    standard = deriv - halfpi
    if deriv < angle:
        standard = deriv + halfpi
    distance = start.distance(end)
    theta = angle - standard
    radius = np.divide(distance, 2 * np.cos(theta))
    phi = np.pi - (2 * abs(rad_reduce(theta)))
    
    anchor = Point(start.xPos + (radius * np.cos(standard)), start.xPos + (radius * np.sin(standard)))
    rotate = min([anchor.angle(start), anchor.angle(end)])
    rotate = -rad_deg(rotate)
    #print(rotate)
    return anchor, radius, phi, rotate

def circCalc(start, end):
    '''
    Attempt at recreating turnCalc through different methods to solve the issue
    '''
    start_dir = rad_reduce(start.dirVec)
    grad_angle = start.angle(end)
    grad_angle = frame_angle([start_dir - np.pi/2, start_dir + np.pi/2], grad_angle)
    if grad_angle == None:
        #print("Fail")
        return None
    #print("Valid")
    standard = start_dir + np.pi/2
    if start_dir > grad_angle:
        standard = start_dir - np.pi/2
    
    theta = abs(grad_angle - standard)
    radius = np.divide(start.distance(end), 2 * np.cos(theta))
    anchor = angledpoint_end(start, standard, radius)
    phi = rad_reduce(2 * (np.pi/2 - theta))
    angles = [anchor.angle(start), anchor.angle(end)]
    min_ang = angles[1]
    if is_clockwise(angles[0], angles[1], rad_reduce(start.dirVec)):
        min_ang = angles[0]
    rotate = - rad_deg(min_ang)

    return anchor, radius, phi, rotate

exists = lambda x: x >= -np.inf
def funcsolve(f, g, lims, e = 1e-4, step = 0.2, min_step = 0.001):
    diff = lambda x: np.power(f(x) - g(x), 2)
    deriv = lambda f, x: np.divide(f(x) - f(x - step), step) #Backward differentiation
    
    def is_converging(x):
        f_val = f(x)
        f_deriv = deriv(f, x)
        
        g_val = g(x)
        g_deriv = deriv(g, x)
        
        #If two lines can converge
        if f_val > g_val:
            return g_deriv > f_deriv
        elif f_val < g_val:
            return f_deriv > g_deriv
        else: #Solution found
            return True
    def could_converge(lim):
        '''
        Does the inequality check
        Needn't worry about equality in either case as would've been checked already
        '''
        start = f(lim[0]) < g(lim[0])
        end = f(lim[1]) < g(lim[1])
        return start ^ end
    
    x = lims[0]
    prevDiff = diff(x) if exists(f(x)) and exists(g(x)) else np.inf
    
    prev = True #Will increase runtime for faulty ones, but setting initial True will ignore certain cases
    prev_existx = x
    #Prioritizing correctness over efficiency
    while x <= lims[1]:
        '''
        Has converging switched from True to Negative
        '''
        if exists(f(x)) and exists(g(x)):

            if diff(x) <= e: #Base condition
                return x, True
            prev_existx = x
            curr = is_converging(x)
            if prev and not curr: #Was converging and is not now
                pot_lim = [x - step, x]
                if could_converge(pot_lim) and step >= min_step: #Could it have converged; include a lower limit on the step
                    return funcsolve(f, g, pot_lim, step = np.divide(step, 10)) #Recursive call with smaller range and step
            prev = curr
        x += step
    return prev_existx, False



def line_func(x1, y1, x2, y2):
    grad = Point.loc_gradient(x1, y1, x2, y2)

    def return_func(x):
        if x < x1 or x > x2:
            return np.NaN
        delt_y = x - x1
        delt_y = delt_y * grad
        return delt_y + y1
    return return_func

def circ_func(anchor, radius, startPhi, endPhi, upper = True):
    '''
    upper provides the distinction between upper semicircle and lower semicircle
    Cannot make a master_func easily since it affects usage with repeating x vals
    Need to look big picture to implement this
    '''
    startPhi = rad_reduce(startPhi)
    endPhi = rad_reduce(endPhi)
    if upper:
        assert startPhi >= 0 and endPhi >= 0, "Circle angles need to be of same semicircle type"
    else:
        assert startPhi <= 0 and endPhi <= 0, "Circle angles need to be of same semicircle type"
    def return_func(x):
        val = radius**2 - np.power(x - anchor.xPos, 2)
        if val < 0:
            return np.NaN
        
        val = np.sqrt(val)
        if not upper:
            val = - val

        y = val + anchor.yPos
        angle = anchor.angle(Point(x, y))
        if startPhi <= angle <= endPhi:
            return y
        else:
            return np.NaN

    return return_func


def angledpoint_end(start, angle, length):
    '''
    Given a point and angle, gives the corresponding endPoint
    '''
    angle = rad_reduce(angle)
    end = Point(start.xPos + (length * np.cos(angle)), start.yPos + (length * np.sin(angle)), angle)
    return end

def is_clockwise(startPhi, endPhi, startAng):
    '''
    Determines whether the arc's orientation was clockwise or anti-clockwise
    Current usage - helping set_endDir() for turn element
    '''
    startPhi = rad_reduce(startPhi)
    startAng = frame_angle([startPhi - np.pi, startPhi + np.pi], startAng)
    return startAng > startPhi


class math_func:
    def __init__(self, points, line_bool, args = True):
        '''
        A revised Function that class that can produce various aspects of the enclosed function when needed
        Catered towards three different types of functions:
        -Linear Functions with usable gradient
        -Vertical lines
        -Circular functions
        If line function: 
        points gives [x1, y1, x2, y2]
        if circ function:
        points gives [anchorPoint, radius, startPhi, endPhi]
        '''
        self.points = points
        self.line_bool = line_bool
        self.args = args
        if line_bool:
            if self.points[0] == self.points[2]:
                self.grad = np.inf
                self.lims = [self.points[0], self.points[0]]
                self.func = self.vert_func #Make the vertical function
            else:
                self.grad = loc_gradient(*self.points) #Make the regular function
                self.lims = [self.points[0], self.points[2]]
                self.lims.sort() #Could be the opposite way
                #print(self.lims)

                self.func = self.line_func
                
        else:
            self.anchor = points[0]
            self.angle_range = [rad_reduce(self.points[2]), rad_reduce(self.points[3])]
            if self.angle_range[0] == np.pi and not args:
                self.angle_range[0] = -np.pi
            #print(self.angle_range)
            self.angle_range.sort()
            

            if args:
                assert self.angle_range[0] >= 0, "Circle angles need to be of same semicircle type"
            else:
                assert self.angle_range[1] <= 0, "Circle angles need to be of same semicircle type"
            self.lims = self.det_circ_range()
            self.func = self.circ_func

    def find_overlap(self, other):
        '''
        Finds an overlap in the ranges of two functions
        Returns success boolean, [min_x, max_x]
        if failed, -- False, None
        '''
        other_lims = other.lims
        use_range = [max(self.lims[0], other_lims[0]), min(self.lims[1], other_lims[1])]
        if use_range[0] > use_range[1]:
            return False, None
        else:
            return True, use_range
            #print (use_range)

    def give_vertrange(self):
        '''
        simple functions aimed at giving the vertical range of a vertical function
        '''
        vals = [self.points[1], self.points[3]]
        vals.sort()
        return vals

    def det_circ_range(self):
        '''
        Determining the exact x range for the function
        At this point, we have hte max and min angle and the hemisphere-confirmed angles
        Idea for interpretation here -- all values will lie only between the max and min angle, nothing beyond
        since this angle range does not cross the semicircle border
        Given points element dictionary here
        0 - anchorPoint
        1 - radius
        2 - StartPhi
        3 - endPhi
        '''

        pot = [self.points[0].xPos + (self.points[1] * np.cos(a)) for a in self.angle_range]
        pot.sort()
        return pot

    
    def circ_func(self, x):
        '''
        The Circle function
        Given points element dictionary here
        0 - anchorPoint
        1 - radius
        2 - StartPhi
        3 - endPhi
        '''
        if x < self.lims[0] or x > self.lims[1]:
            return np.NaN
        
        val = self.points[1]**2 - np.power(x - self.points[0].xPos, 2)       
        if val < 0:
            return np.NaN 
        val = np.sqrt(val)
        if not self.args:
            val = - val
        y = val + self.anchor.yPos
        return y
        

    def line_func(self, x):
        '''
        The regular linear function
        Assumes points is comprised of startt and end points:
        [x1, y1, x2, y2]
        '''
        if x < self.lims[0] or x > self.lims[1]:
            return np.NaN
        delt_y = x - self.points[0]
        delt_y = delt_y * self.grad
        return delt_y + self.points[1]


    def vert_func(self, x, other_y):
        '''
        The vertical line function
        '''
        assert x == self.points[0]

        if self.points[1] <= other_y <= self.points[3]:
            return other_y
        else:
            return np.NaN
    '''
    Comparison functions below
    Needed to incorporate the np.NaN thing
    All functions used are singularly piecewise. If they start at a given point and end, they don't restart somewhere
    If f(x1) exists and f(x2) does not, the upper lim lies between both. Since we know the upper and lower lims, we don't need to ever run
    an np.NaN-returning function (when executed correctly)
    '''
    def deriv(self, x, step):
        '''
        Gives the function's derivative at a particular point
        '''
        if self.line_bool == True:
            return self.grad
        
        if not exists(self.func(x)) or not exists(self.func(x - step)):
            return np.NaN
        else:
            return np.divide(self.func(x) - self.func(x - step), step)

    def diff(self, x, other):
        '''
        Gives the difference between two functions
        '''
        vals = [self.func(x), other.func(x)]
        if any([not exists(a) for a in vals]):
            return np.NaN
        else:
            return abs(vals[0] - vals[1])
    
    def is_converging(self, x, other, step):
        '''
        Same is_converging function, but here with np.NaN support
        '''
        if not exists(self.func(x)) or not exists(self.func(x - step)) or not exists(other.func(x - step)) or not exists(other.func(x)): 
            return False
       
        if self.func(x) < other.func(x):
            return self.deriv(x, step) > other.deriv(x, step)
        elif self.func(x) > other.func(x):
            return self.deriv(x, step) < other.deriv(x, step)
        else: #Solution is found
            return True

    def did_converge(self, x, other, step):
        '''
        could_coverge, but with np.NaN support
        '''
        
        start = self.func(x - step) < other.func(x - step)
        end = self.func(x) < other.func(x)

        return start ^ end

    def single_interact(self, x, other):
        '''
        This function outlines the interaction between a vertical function andother func (could be vertical or not)
        edit: this now is an arbitrary single x interaction
        '''
        this_range = []
        other_range = []
        if self.line_bool and self.grad == np.inf:
            this_range = self.give_vertrange()
        else:
            this_range = [self.func(x), self.func(x)]
        
        if other.line_bool and other.grad == np.inf:
            other_range = other.give_vertrange()
        else:
            other_range = [other.func(x), other.func(x)]
        #print(this_range, other_range)
        pot_val = max([this_range[0], other_range[0]])
        if pot_val <= min([this_range[1], other_range[1]]):
            return True, [x, pot_val] #vertical lowest point of intersection
        else:
            return False, None #Does not spill onto the next bits
    def __str__(self):
        if self.line_bool:
            to_return = "line:" + str(self.points)
            return to_return
        else:
            to_return = "circ:" + str(self.args) + str(self.points)
    
    def __repr__(self):
        return self.__str__()
        
        
        
  
def systemsolve(f_obj, g_obj, e = 1e-4, step = 0.2, conten_divis = 30, count = 3, lims = None, fringe = False):
    '''
    This is the potential candidate for funcsolve's successor
    The plans for change are to expedite the range and elimination check
    count - flagpoint for the recursive check, when end when reachedd 0
    '''
    #print(count)
    if count == 3:
        success, lims = f_obj.find_overlap(g_obj)
        if not success:
            return False, None

    assert lims != None, "Recursive call lims arg is not handled properly"
    if lims[0] == lims[1]:
        return f_obj.single_interact(lims[0], g_obj)

    new_step = np.divide(lims[1] - lims[0], conten_divis)
    step = min(step, new_step) #Take the one that's more suited to the range 
    #0.2 does not fit small ranges, like 0.9

    x = lims[0]
    prev_con = True
    
    run = True
    while run:
        if x > lims[1]:
            break
            #x = lims[1]
            #run = False
            
        if f_obj.diff(x, g_obj) <= e:
            if not fringe:
                if abs(x - f_obj.lims[1]) <= e or abs(x - g_obj.lims[1]) or abs(x - f_obj.lims[0]) or abs(x - g_obj.lims[0])<= e:
                    #print("Another one", fringe)
                    return False, None
            #print("Found one", fringe)
            return True, [x, f_obj.func(x)]

        curr_con = f_obj.is_converging(x, g_obj, step)
        '''
        Do not need to confirm if both functions exist in the range
        '''
        if prev_con and not curr_con:
            if f_obj.did_converge(x, g_obj, step) and count > 0:
                success, val = systemsolve(f_obj, g_obj, step = np.divide(step,10), count = count -1, lims = [x - step, x], fringe = fringe)
                if success: 
                    return success, val
        prev_con = curr_con
        x += step
    #print("None", fringe)
    return False, None