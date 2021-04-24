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
    def __init__(self) -> None:
        super().__init__()

        
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
        