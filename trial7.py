from env import *
from car import *
import time

start = time.time()
track = Track('tracks/first.txt')
end = time.time()
print(f"Creation: {end - start}")
car = Thing([345.629, 198.95], [5, 3], -2.584)
print(track.checkCollision(car.funcs))
print(f"Collision Check: {time.time() - end}")