from math import trunc
from env import *

start = Point(797, 204)
end = Point(707, 262)

elems = []
elems.append(StartingStrip(start, end))
elems.append(LineElement(elems[-1], Point(644, 302.6)))
elems.append(TurnElement(elems[-1], Point(425, 320)))

f = open('tracks/main.txt', 'w')
