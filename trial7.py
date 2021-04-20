from env import *

start = Point(10, 10)
end = Point(10, 100)
first = StartingStrip(start, end)
grid = gridEngine(500, 500)
passed = grid.check_track(first)
if passed:
    grid.register_track(passed, first)


end = Point(10, 200)
second = LineElement(first, end)
end = Point(100, 250)
third = TurnElement(second, end)