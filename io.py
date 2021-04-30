'''
This file handles file reading and writing
They include string writers and buffered readers
'''

class BufferedReader:
    def __init__(self) -> None:
        pass

    def next(self):
        pass

    def has_next(self) -> bool:
        pass


class TrackReader(BufferedReader):
    def __init__(self) -> None:
        super().__init__()

class CarReader(BufferedReader):
    def __init__(self, carfile) -> None:
        super().__init__()
        self.carfile = carfile

        self.carloc = self.toRead()
    
    def toRead(self):
        
        def isint(val):
            try: 
                vals = int(val)
            except ValueError:
                return False
            return True

        f = open(self.carfile, 'r'):

        carloc = []
        
        line = f.readline()
        
        line1 = line.split(', ')
        
        for i in line1:
            if isint(i) == False:
                carloc.append(i)
            else:
                temp = carloc[-1]
                for j in range(int(i) - 1):
                    carloc.append(temp)
                    
        return carloc


        
class TrackWriter:
    def __init__(self, elems) -> None:
        '''
        Writes the track schematics. No checking whether it works or not, it's just creation
        elems - list of start, end points from worldcreation
        (To be noted that many of the start points in elems are incorrect, they're needed for worldcreation but not here
        so all startpoints except first startingstrip one should be ignored)
        '''
        self.elems = elems
    
    def write(self, suggest, w, h):
        '''
        suggests the name. Returns false if there's a file with that name (so then it overwrites on a cache file?)
        '''
        f = open(suggest, 'w')

        f.write(str(w), str(h) + '\n')
        
        for i in self.elems:
            f.write(str(i) + '\n')

        f.close()

        return None


        
        