'''
This file handles file reading and writing
They include string writers and buffered readers
'''

from os import error
import numpy as np

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

class CarReader:
    inp_dict = ['w', 'a', 's', 'd']
    def __init__(self, carfile) -> None:
        #print("WHAT")
        self.carfile = carfile
        self.read_str = self.toRead()
        self.curr_counter = 0
        self.curr_act = [0, 0, 0, 0]
        self.currelem = 0
        self.done = False

    def isint(self, val):
        try: 
            vals = int(val)
        except ValueError:
            return False
        return True
    
    def toRead(self):
        f = open(self.carfile, 'r')
        
        line = f.readline()
        return line

    def givechar(self, elem):
        return self.read_str[elem]
        
    def next(self):
        #print("WHAT")
        if self.done:
            return self.curr_act
        #print(self.currelem, self.givechar(self.currelem))
        if self.curr_counter == 0:
            com_val = ""
            while not self.isint(self.givechar(self.currelem)):
                com_val += self.givechar(self.currelem)
                #print("Command", self.givechar(self.currelem))
                self.currelem += 1
            num_val = ""
            while self.isint(self.givechar(self.currelem)):
                num_val += self.givechar(self.currelem)
                #print("Counter", self.givechar(self.currelem))
                self.currelem += 1
            
            self.curr_act = self.convert_inp(com_val)
            try:
                self.curr_counter = int(num_val)
            except ValueError as e:
                print("Screwed Up")
                print(e)
        self.curr_counter -= 1

        if self.currelem == len(self.read_str):
            self.done = True
            self.curr_act = [0, 0, 0, 0]

        return self.curr_act
    
    def convert_inp(self, inp):
        new_inp = [0, 0, 0, 0]
        for char in inp:
            elem = self.inp_dict.index(char)
            new_inp[elem] = 1
        return new_inp


        


        
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

        f.write(str(w) + ", " + str(h) + '\n')
        
        for elem in self.elems:
            f.write(elem[0] + ", ")
            f.write(str(elem[1][0]) + ", " + str(elem[1][1]) + ", ")
            f.write(str(elem[2][0]) + ", " + str(elem[2][1]))
            f.write("\n")        
        f.close()

class CarWriter:
    conv = ['w', 's', 'wa', 'wd', 'sa', 'sd', 'a', 'd']
    def __init__(self) -> None:
        self.save_str = ""
        self.curr_ac = ""
        self.curr_t = 0


    def next_step(self, control):
        curr = self.conv[control]
        if curr != self.curr_ac:
            self.reg_curr()
            self.curr_ac = curr

        self.curr_t += 1
    
    def reg_curr(self):
        if self.curr_ac != "" and self.curr_t > 0:
            self.save_str += self.curr_ac + str(int(self.curr_t))
        self.curr_ac = ""
        self.curr_t = 0

    def write(self, suggest):
        f = open(suggest, 'w')
        f.write(self.save_str)
        f.close()
        
def write_stats(vals, suggest):
    f = open(suggest, 'w')
    for elem in range(len(vals[0])):
       for thing in vals:
           f.write(f"{thing[elem]} ")
       f.write("\n")
    f.close() 

def read_stats(suggest):
    f = open(suggest, 'r')
    main = []
    for line in f:
        line = line.strip().split()

        newline = [float(a) for a in line]
        main.append(newline)
    return np.matrix(main)