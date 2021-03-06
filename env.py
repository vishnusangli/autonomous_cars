import numpy as np


from calcmath import *
from pyglet import shapes

'''
World and track width are fixed, should not be changed
'''
trackWidth = 20

class Track: 
    '''
    Track objects represent the entire world
    '''
    openArea = True #Is outside area traversable
    #Relative dimensions of the world, which would be later scaled for the display
    
    wireFrame = True

    def __init__(self, track_elems, height, width, engine) -> None:
        '''
        Track would've already been creaetd and verified, this is only placeholder
        '''
        self.track_elements = track_elems
        self.HEIGHT = height
        self.WIDTH = width
        self.engine = engine
        #Run the Track Engine and create according data structure
    
    def render(batch):
        pass

    def checkCollision(self, points): #Here thing is of datatype thing
        '''
        Input args: 4 lists of each pair of corners for the car object: 
        Thereby applying linefuncs and doing the individual grid_search check for each line
        Returns whether collided or not, point of contact is irrelevant
        '''
        for pair in points:
            f = line_func(*pair)
            success, pot, _ = self.engine.grid_search(f, [pair[0], pair[2]])
            if success:
                return True

        return False

    def lineof_sight(self, centre, angles, max_sight = 20):
        '''
        Takes in a list of angles with respect to obj and returns a dictionary of endPoints
        Currently it returns the points themselves, should consider returning merely distance
        However, the distance lines cannot be shown then
        '''
        sight_dict = {}
        ref = centre.dirVec
        for a in angles:
            end = angledpoint_end(centre, (a - np.pi/2) + ref, max_sight)
            f = line_func(centre.xPos, centre.yPos, end.xPos, end.yPos)
            success, pot, _ = self.engine.grid_search(f, [centre.xPos, end.xPos])
            if success:
                sight_dict[a] = Point(pot, f(pot))
            else:
                sight_dict[a] = end
        return sight_dict


class TrackElement:
    '''
    A General data type for a track element
    '''
    nextElem = None

    def __init__(self, prev, end, startPoint = None) -> None:
        #Different treatment for the StartingStrip
        if startPoint == None:
            self.startPoint = prev.endPoint #Does not work with the very first lineElem
        elif prev == None:
            self.startPoint = startPoint #start is a Point, for the StartingStrip
        else:
            raise Exception #Should be one or the other
        self.endPoint = end
        self.prevElem = prev

        self.color = (255, 255, 255)
        self.friction = 1.0    
        self.render_objs = []

class LineElement(TrackElement):
    '''
    Represents one straight line in the track as an object
    '''
    def __init__(self, prev, end, start = None) -> None:
        super().__init__(prev, end, start)
        self.set_endDir()

        self.points = self.wireFrame()
        self.funcs = self.wallFunc()
        
    def set_endDir(self):
        '''
        Useful in the wireframe config & future stages
        The startPoint's directional configuration should've been done by the previous track element
        '''
        angle = self.startPoint.angle(self.endPoint)
        if self.startPoint.dirVec == None: #Treats cases of StartingStrip
            self.startPoint.dirVec = angle
        #assert angle == self.startPoint.dirVec, 'Directions from a line eleme should essentially be the same'
        self.endPoint.dirVec = angle
    
    def wireFrame(self):
        '''
        Returns a list of two lists - each [x1, y1, x2, y2]
        For each side of the track
        Start points for both lists will correlate with start Point of chosen startPoint
        (For simplicity when defining and drawing the StartingStrip and FinishLine)
        '''
        perp_angle = self.startPoint.dirVec - np.pi/2
        
        diffx = np.divide(trackWidth, 2) * np.cos(perp_angle)
        diffy = np.divide(trackWidth, 2) * np.sin(perp_angle)
        lower = [self.startPoint.xPos + diffx, self.startPoint.yPos + diffy]
        lower += [self.endPoint.xPos + diffx, self.endPoint.yPos + diffy]

        upper = [self.startPoint.xPos - diffx, self.startPoint.yPos - diffy]
        upper += [self.endPoint.xPos - diffx, self.endPoint.yPos - diffy]

        to_return = [lower, upper]
        return to_return
    
    def wallFunc(self):
        '''
        Returns a list of ranged functions that characterize the element
        '''
        to_return = [math_func(a, True) for a in self.points]
        return to_return

    def render(self, x_fac, y_fac, batch):
        '''
        Need to explore pyglet before writing this function
        Do I need to re-create the render_objs list and objects
        or is just one render enough
        TRACK WILL NOT MOVE!!! NO PERSPECTIVE SHIT DEDICATE MORE TIME TO DL AND ML
        '''
        x_fac = 1 #Screw this shit I'm out
        y_fac = 1
        self.render_objs = []
        for pair in self.points:
            first = [np.divide(pair[0], x_fac), np.divide(pair[1], y_fac)]
            sec = [np.divide(pair[2], x_fac), np.divide(pair[3], y_fac)]
            self.render_objs.append(shapes.Line(*first, *sec, color = self.color, batch = batch))
        

class StartingStrip(LineElement):
    def __init__(self, start, end) -> None:
        super().__init__(None, end, start)

    
    def wireFrame(self):
        '''
        Adds the end wall to the points list
        '''
        prev_ones = super().wireFrame()

        third = prev_ones[0][0:2] #Back wall
        third += prev_ones[1][0:2]
        prev_ones.append(third) #bottom two points
        return prev_ones

    
        
        
        

class FinishLine(TrackElement):
    def __init__(self, prev, end) -> None:
        super().__init__(prev, end)
        self.points = self.wireFrame()
        self.funcs = self.wallFunc()
    
    def wireFrame(self):
        '''
        Uses the final two points of previous element
        Ne
        '''
        third = [self.prev.points[0][2:], self.prev.points[1][2:]] #Back wall
        self.lims = self.prev.lims #wasteful, but so what
        return third

    def wallFunc(self):
        return line_func(*self.points)

class TurnElement(TrackElement):
    '''
    Represents a curve in the track as an object
    '''
    def __init__(self, prev, end) -> None:
        super().__init__(prev, end)
        #Where are point directions settled?
        self.anchor = None
        self.points = self.wireFrame()
        #print(self.startPoint)
        #print(self.startPoint.dirVec)
        
        self.set_endDir()
        self.funcs = self.wallFunc()
        

    def set_endDir(self):
        startPhi = self.anchor.angle(self.startPoint)
        endPhi = self.anchor.angle(self.endPoint)

        if is_clockwise(startPhi, endPhi, self.startPoint.dirVec):
            self.endPoint.dirVec = rad_reduce(endPhi + np.pi/2)
        else:
            self.endPoint.dirVec = rad_reduce(endPhi - np.pi/2)
    
    def wireFrame(self):
        '''
        This is always run as the points generated here are important and neede regardless
        '''
        #Find inner side, get the perp direction towards centre
        #Get a difference vector of start and end
        #90 - (vector angle - perp direction) gives the arc angle
        # difference vector magnitude / cos(vector angle - perp direction) gives radius
        #go in perp direction to find anchor
        side = np.divide(trackWidth, 2)
        self.anchor, radius, phi, rotate = circCalc(self.startPoint, self.endPoint)
        to_return = [[self.anchor.xPos, self.anchor.yPos, radius + side, phi, rotate]]
        to_return.append([self.anchor.xPos, self.anchor.yPos, radius - side, phi, rotate])
        return to_return
        
    
    def render(self, x_fac, y_fac, batch):

        self.render_objs = []
        for pair in self.points:
            
            val = shapes.Arc(pair[0], pair[1], pair[2], segments = 30, angle = pair[3], color = self.color, batch = batch)
            val.rotation = pair[4]
            self.render_objs.append(val)
            

    def wallFunc(self):
        '''
        Need to consider the upper-lower semicircle breakup
        '''
        angles = [self.anchor.angle(self.startPoint), self.anchor.angle(self.endPoint)]
        min_a = min(angles)
        max_a = max(angles)
        if min_a < 0 and max_a == np.pi:
            max_a = min_a
            min_a = -np.pi #Treating that issue
        to_return = []
        if min_a < 0 and max_a > 0:
            for elem in self.points:
                
                to_return.append(math_func([self.anchor, elem[2], min_a, 0], False, False))
                to_return.append(math_func([self.anchor, elem[2], 0, max_a], False, True))
        else:
            for elem in self.points:
                to_return.append(math_func([self.anchor, elem[2], min_a, max_a], False, min_a > 0))
        return to_return


class gridEngine:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.grid = self.make_grid()
        
    def make_grid(self) -> list:
        main = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append([])
            main.append(row)
        return main
    
    def access(self, x, y) -> list:
        assert x < self.width, "Invalid grid width"
        assert y < self.height, "invalid grid height"
        #x, y are not integers, it's shitting over everything
        print(x, y)
        to_return = self.grid[x][y]
        return to_return
    
    def add_to(self, x, y, elem):
        loc = self.access(x, y)
        if not elem in loc:
            loc.append(elem)


    def grid_search(self, func_obj):
        '''
        The grid search, but altered to incorporate a list-based mainfunc
        '''
        
        lims = func_obj.lims
        if func_obj.line_bool and func_obj.grad == np.inf:
            y_range = func_obj.give_vertrange()
            x = int(lims[0])
            y = int(y_range[0])
            grids = []
            while y < y_range[1]:
                potential = self.check_box(func_obj, x, int(y))
                grids.append([x, y])
                if potential[0] < np.inf:
                    return True, potential, grids
                y += 1
            return False, [], grids
        #Check if vertical function
        y = func_obj.func(lims[0])
        x = int(lims[0])
        #step = min(0.2, np.divide(lims[1] - lims[0], num)) #Don't make abs, if erroneous lims step still works

        prev = [x, int(y)]
        grids = [prev]
        potential = self.check_box(func_obj, int(x), int(y))
        if potential[0] < np.inf:
            return True, potential, grids
        
        x += 1
        run = True

        while run:
            if x > lims[1]:
                x = lims[1]
                run = False
            y = func_obj.func(x)
            if exists(y):
                x = round(x)
                red_y = int(y)
                val = self.check_box(func_obj, x, red_y)
                pots = {val[0]:val}
                grids.append([x, red_y])
                loop_x = round(x - 1)
                if red_y > prev[1]: #If they're not adjacent
                    for y_use in range(prev[1], red_y, 1):
                        val = self.check_box(func_obj, loop_x, y_use)
                        pots[val[0]] = val
                        grids.append([loop_x, red_y])
                else:
                    for y_use in range(prev[1], red_y, -1):
                        val = self.check_box(func_obj, loop_x, y_use)
                        pots[val[0]] = val
                        grids.append([loop_x, red_y])
                
                    grids.append([loop_x, red_y])
                prev = [x, red_y]
                cont_der = min(pots.keys()) #contender
                if cont_der < np.inf:
                    return True, pots[cont_der], grids
            x += 1
        return False, [], grids

            

    def check_box(self, mainfunc, x, y):
        elems = self.access(x, y)
        obstructs = {}
        for e in elems:
            success, val = self.find_obstruct(mainfunc, e.funcs)
            if success:
                obstructs[val[0]] = val
        if obstructs:
            return obstructs[min(obstructs.keys())]
        else:
            return [np.inf, np.inf]


    def find_obstruct(self, mainfunc, funcs):
        '''
        Takes in an elemFunc
        
        Returns -- boolean, endPoint
        boolean - if obstruction was found
        enPoint - the obstruction (if found), else None
        endPoint will be the max line of sight if no obstruction is found

        with ranged elemfuncs, range is implicit, needs some way of calculation
        TrackElems could have min_x, max_x (line elems already have as elem.points, 
        [anchor_x - rad, anchor_x + rad] for turn elems)
        Questions: 
        - will minx, maxx be reqd or can be ooptional args?
        - should use trackelem as arg or funcs?

        With minx, maxx as inputed args, trackelem needn't be an arg

        list of mainfuncs, lims - input args
        Search through grid-method
        if overlapping grid found: do the mainfuncs-funcs obstruction check
        Keep empty obstructions list outside, append those found.
        At the end of the given grid box search, check if obstruction found and follow same exit procedure
        '''
        obstructions = {}
        for f in funcs:
            success, loc = systemsolve(mainfunc, f)
            #x_val, success = funcsolve(mainfunc, f, lims)
            if success:
                obstructions[loc[0]] = loc
        if any(obstructions):
            xval = min(obstructions.keys())
            yval = obstructions[xval][1]
            assert exists(yval), "Invalid intersection result from funcsolve"
            return True, obstructions[xval]
        else:
            #Potential error, does mainfunc(lims[1]) exist? Must ensure
            #Max pos here is only needed in line of sight, can just implement anglepoint_end() in the function that calls this one
            return False, None

    def register_track(self, grids, elem):
        for a in grids:
            self.add_to(*a, elem)

    def check_track(self, elem):
        '''
        Takes the walls of the track elem and returns whether it's successful
        True - can save, no obstructions
        False - didn't save, obstructions
        '''
        grids_passed = []
        for f in elem.funcs:
            success, inters, grids = self.grid_search(f)
            if success:
                return False, []
            grids_passed += grids
        return True, grids_passed


'''
Inspired to write an elemFunc class, that stores some function and it's limits


Track: interpret each track elem, register in grid engine
track funcs 
-is_collide() - find_obstruct on all 4 sides of car
-lineof_sight() - find_obstruct in each line, return dict with angle as key
'''
        