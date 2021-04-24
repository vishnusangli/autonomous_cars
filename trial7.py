from math import trunc
from env import *

start = Point(797, 204)
end = Point(707, 262)
print('start')
grid  = gridEngine(960, 540)
print('start')

elems = []
elems.append(StartingStrip(start, end))
success, grids = grid.check_track(elems[-1])
if success:
    grid.register_track(grids, elems[-1])
elems.append(LineElement(elems[-1], Point(644, 302.6)))
success, grids = grid.check_track(elems[-1])
if success:
    grid.register_track(grids, elems[-1])
elems.append(TurnElement(elems[-1], Point(425, 320)))
success, grids = grid.check_track(elems[-1])
if success:
    grid.register_track(grids, elems[-1])

#f = open('tracks/main.txt', 'w')
