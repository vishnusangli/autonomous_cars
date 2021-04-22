from env import *

start = Point(889, 334)
end = Point(826, 342)

elems = []
elems.append(StartingStrip(start, end))
elems.append(TurnElement(elems[0], Point(661, 299)))