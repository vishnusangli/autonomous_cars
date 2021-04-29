'''
This file handles file reading and writing
They include string writers and buffered readers
'''

class BufferedReader:
    def __init__(self, filename) -> None:
        self.filename = filename
         

    def next(self):
        pass

    def has_next(self) -> bool:


        pass


class TrackReader(BufferedReader):
    '''
    This class reads the info that is stored in the track file 
    to initialize in the joint game-run file
    '''
    
    def __init__(self) -> None:
        super().__init__()

    def toread(self, suggest):
        typ, x, y = np.loadtxt(suggest, delimiter = ',', unpack = True)

        loc = np.zeros(len(x))
        
        for i in range(len(x)):
            loc[i] = [x[i], y[i]]

        return typ, loc

class CarReader(BufferedReader):
    def __init__(self, carfile) -> None:
        super().__init__()
        self.carlist = self.carread()
        self.carfile = carfile

    def carread(self):
        def isint(val):

            try:
                int(val)
                return True
            except ValueError:
                return False

        f = open('suggest.txt', 'r')

        line = f.readline()

        line = line.split(", ")

        final = []

        for i in line:
            if isint(i) == False:
                final.append(i)
            else:
                temp = final[-1]

                for j in range(int(i) - 1):
                    final.append(temp)

        return final


    

        
class TrackWriter:
    def __init__(self, elems) -> None:
        '''
        Writes the track schematics. No checking whether it works or not, it's just creation
        elems - list of start, end points from worldcreation
        (To be noted that many of the start points in elems are incorrect, they're needed for worldcreation but not here
        so all startpoints except first startingstrip one should be ignored)
        '''
        self.elems = elems
    
    def write(self, suggest):
        '''
        suggests the name. Returns false if there's a file with that name (so then it overwrites on a cache file?)
        '''
        f = open(suggest, 'w')

        f.write('\n')

        for i in self.elems:
            p = str(i)
            f.write(p)

        
        f.close()

        return None



        