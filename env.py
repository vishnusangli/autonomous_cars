import numpy as np

import calcmath

'''
World and track width are fixed, should not be changed
'''
trackWidth = 50

class Track:
    '''
    Track objects represent the entire world
    '''
    openArea = True #Is outside area traversable
    #Relative dimensions of the world, which would be later scaled for the display
    
    wireFrame = True

    def __init__(self, track_elems, height, width) -> None:
        '''
        Track would've already been creaetd and verified, this is only placeholder
        '''
        self.track_elements = track_elems
        self.HEIGHT = height
        self.WIDTH = width
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
        #assert angle == self.startPoint.dirVec, 'Directions from a line eleme should essentially be the same'
        self.endPoint.dirVec = angle
    
    def wireFrame(self):
        '''
        Returns a list of two lists - each (startX, startX, endX, endY)
        For each side of the track
        Start points for both lists will correlate with start Point of chosen startPoint
        (For simplicity when defining and drawing the StartingStrip and FinishLine)
        '''
        perp_angle = self.startPoint.dirVec - np.pi/2

        x_off = np.cos(perp_angle) * trackWidth
        y_off = np.sin(perp_angle) * trackWidth
        right = [self.startPoint.xPos + x_off, self.startPoint.yPos + y_off, self.endPoint.xPos + x_off, self.endPoint.yPos + y_off]
        left = [self.startPoint.xPos - x_off, self.startPoint.yPos - y_off, self.endPoint.xPos - x_off, self.endPoint.yPos - y_off]
        to_return = [[left], [right]]
        return to_return


    def render(batch, color):
        pass

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
        if Track.wireFrame:
            self.wireFrame()
    
    def wireFrame(self):
        '''
        Uses the final two points of previous element
        Ne
        '''
        third = [self.points[0][0:2], self.points[1][0:2]] #Back wall
        self.points.append([third]) #bottom two points


class TurnElement(TrackElement):
    '''
    Represents a curve in the track as an object
    '''
    def __init__(self, prev, end) -> None:
        super().__init__(prev, end)
        #Where are point directions settled?
        self.set_endDir()
        self.points = self.wireFrame()
        if Track.wireFrame:
            self.wireFrame()
    
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


class TrackEngine:
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width

        self.worldGrid = self.writeGrid(width, height)

    def writeGrid(width, height):
        world_grid = [[[] for y in range(height)] for x in range(width)]
        return world_grid

    def fillGrid(self, anchor, track):
        '''
        Adds a track to a corresponding Block, will be called when 
        '''
        self.findBlock(anchor).append(track)


    def findBlock(self, anchor):
        '''
        Returns the Block TrackElement list
        '''
        assert anchor[0] < self.width, 'Invalid coordinates'
        assert anchor[1] < self.height, 'Invalid coordinates'
        x = int(anchor[0])
        y = int(anchor[1])

        return self.worldGrid[x][y]
    
    def findWall(self, start_anchor, angle):
        '''
        Searching the closest LineElement (point on the wall) from a point and angle
        returns the point in that line and the corresponding Track Element
        '''
        pass

    def shapeCollide(self, start, angle, shape):
        pass