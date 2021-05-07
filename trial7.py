from custom_io import *

read = CarReader('cardir/first.txt')
for x in range(100):
    print(read.next())