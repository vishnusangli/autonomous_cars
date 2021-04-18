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
    
        if (angle < 0 and self.yPos < other.yPos):
            angle += np.pi #Negative angles in quadrant 4 to quadrant 2
        
        elif d == np.inf and self.yPos > other.yPos:
            angle = -np.pi/2 #90 degrees to 270 degrees

        elif angle > 0 and self.yPos > other.yPos:
            angle = - np.pi + angle #Positive angles in quadrant 1 to quadrant 3
        
        elif angle == 0 and self.xPos > other.xPos:
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
    
    def loc_gradient(x1, y1, x2, y2):
        '''
        Returns gradient
        '''
        val = np.divide(y1 - y2, x1 - x2)
        return val

    def givePos(self):
        return [self.xPos, self.yPos]
    
    def __str__(self):
        return 'Point[{0:4.4f}, {1:4.4f}]|'.format(self.xPos, self.yPos) + str(self.dirVec)
    
    def __repr__(self):
        return 'Point[{0:4.4f}, {1:4.4f}]|'.format(self.xPos, self.yPos) + str(self.dirVec)

def rad_reduce(x):
    if x < 0:
        x = (2 * np.pi) + x
        
    while x > 2 * np.pi:
        x -= 2 * np.pi
    
    if x > np.pi:
        x -= 2 * np.pi
    
    return x

def frame_angle(lims, theta):
    theta = rad_reduce(theta)
    
    '''
    If a valid angle is give, only 1 while loop would be used
    If invalid angle is given, first loop runs until overshot, after which second doesn't, returning 
    an angle that is beyond range
    '''
    while theta < lims[0]:
        theta += (2 * np.pi)
        
    while theta > lims[1]:
        theta -= (2 * np.pi)
    
    if lims[0] <= theta <= lims[1]:
        return theta
    else:
        #print(lims, theta)
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
                    return funcsolve(f, g, pot_lim, step = np.divide(step, 10))#Recursive call with smaller range and step
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
        assert startPhi >= 0 and endPhi >= 0, "Circle angles need to be of same semicircle type"
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

def is_clockwise(startPhi, endPhi):
    '''
    Determines whether the arc's orientation was clockwise or anti-clockwise
    Current usage - helping set_endDir() for turn element
    '''
    startPhi = rad_reduce(startPhi)
    endPhi = rad_reduce(endPhi)

    return endPhi > startPhi