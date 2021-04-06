import numpy as np

'''
World and track width are fixed, should not be changed


'''
trackWidth = 5

class Track:
    '''
    Track objects represent the entire world
    '''
    openArea = True #Is outside area traversable
    #Relative dimensions of the world, which would be later scaled for the display
    HEIGHT = 50 
    WIDTH = 50
    wireFrame = True

    def __init__(self, track_elems) -> None:
        '''
        Track would've already been creaetd and verified, this is only placeholder
        '''
        self.track_elements = track_elems
        #Run the Track Engine and create according data structure
    
    def render(batch):
        pass

    def checkCollision(thing): #Here thing is of datatype thing
        pass


class TrackElement:
    '''
    A General data type for a track element
    '''
    nextElem = None

    def __init__(self, prev, end, start = None) -> None:
        if start == None:
            self.startPoint = prev.endPoint #Does not work with the very first lineElem
        elif prev == None:
            self.startPoint = start
        else:
            raise Exception #Should be one or the other

        self.endPoint = end
        self.prevElem = prev
    

class LineElement(TrackElement):
    '''
    Represents one straight line in the track as an object
    '''
    def __init__(self, prev, end) -> None:
        super().__init__(prev, end)
        self.set_endDir()
        if Track.wireFrame:
            self.points = self.wireFrame()
        
    def set_endDir(self):
        '''
        Useful in the wireframe config & future stages
        The startPoint's directional configuration should've been done by the previous track element
        '''
        angle = self.startPoint.angle(self.endPoint)
        if self.startPoint.dirVec == None: #Treats cases of StartingStrip
            self.startPoint.dirVec = angle
        assert angle == self.startPoint.dirVec, 'Directions from a line eleme should essentially be the same'
        self.endPoint.dirVec = angle
    
    def wireFrame(self):
        perp_angle = self.startPoint.dirVec
        x_off = np.cos(perp_angle) * trackWidth
        y_off = np.sin(perp_angle) * trackWidth
        right = [self.startPoint.xPos + x_off, self.startPoint.yPos + y_off, self.endPoint.xPos + x_off, self.endPoint.yPos + y_off]
        left = [self.startPoint.xPos - x_off, self.startPoint.yPos - y_off, self.endPoint.xPos - x_off, self.endPoint.yPos - y_off]
        to_return = [[left], [right]]
        return to_return


    def render(batch, color):
        pass


class TurnElement(TrackElement):
    '''
    Represents a curve in the track as an object
    '''
    def __init__(self, prev, end) -> None:
        super().__init__(prev, end)
        #Where are point directions settled?
        self.set_endDir()
        self.points = self.wireFrame()


    def prepDraw():
        '''
        fill
        '''
    
    def wireFrame(self):
        '''
        This is always run as the points generated here are important and neede regardless
        '''
        #Find inner side, get the perp direction towards centre
        #Get a difference vector of start and end
        #90 - (vector angle - perp direction) gives the arc angle
        # difference vector magnitude / cos(vector angle - perp direction) gives radius
        #go in perp direction to find anchor
        
    
    def render(self, batch):
        pass


class Point:
    '''
    API used for reference points in track elements
    '''
    def __init__(self, xPos, yPos, dir = None) -> None:
        self.xPos = xPos
        self.yPos = yPos

        self.dirVec = dir #Directional vector of movement & following track creation
        pass

    def angle(self, other):
        '''
        Common format to return in Radians
        '''
        delt_y = other.yPos - self.yPos
        delt_x = other.xPos - self.xPos
        to_return = np.arctan(np.divide(delt_y, delt_x)) 
        return to_return
    
    def distance(self, other):
        '''
        Returns distance to another point
        '''
        delt_y = np.power(other.yPos - self.yPos, 2)
        delt_x = np.power(other.xPos - self.xPos, 2)
        to_return = np.sqrt(delt_x + delt_y)
        return to_return

class StartingStrip(LineElement):
    def __init__(self, start, end) -> None:
        super().__init__(None, end, start)
        if Track.wireFrame:
            self.wireFrame()
    
    def wireFrame(self):
        third = [self.points[0][0:2], self.points[1][0:2]] #Back wall
        self.points.append([third]) #bottom two points

        
        
        

class FinishLine(TrackElement):
    def __init__(self, prev, end) -> None:
        super().__init__(prev, end)

class Block:
    '''
    Square block of side 1
    reference from lower left point
    '''

    def __init__(self) -> None:
        pass


class TrackEngine:
    def __init__(self) -> None:
        pass