#!/usr/bin/env python3

from intcode import IntCodeInterpreter
import sys

with open("day19_1.txt", "r") as f:
    program = f.readline().strip()

SIZE = 100

def show_map(scan):
    for x, line in enumerate(scan):
        for y, obj in enumerate(line):
            sys.stderr.write(obj)
        sys.stderr.write("\n")
    sys.stderr.write("\n")

def check_pos(x,y):
    drone = IntCodeInterpreter(program)
    drone_gen = drone.run_gen()
    drone.push_input(x)
    drone.push_input(y)
    return next(drone_gen)

def find_area(origin, size):
    Y = origin[1] + size

    count = 0
    found_attracted = False
    for x in range(origin[0], origin[0] + 2*size):
        status = check_pos(x, Y)
        if status == 1:
            if not found_attracted:
                X = x
            found_attracted = True
            count += 1
        elif found_attracted:
            break
    return (X, Y), count 

import time
pos = (0, 0)
# Coarse area selection
# Find a beam section that's large enough
while True:
    next_pos, cnt = find_area(pos, SIZE)

    print(next_pos, cnt)
    pos = next_pos

    if cnt >= 100:
        break

# Find closest matching area 
while True:
    x = pos[0]
    y = pos[1]
    # Find right edge of beam
    while check_pos(x, y) == 1:
        x += 1
    x -= 1

    # Check if opposite corner is in beam
    if check_pos(x - SIZE + 1, y + SIZE - 1) == 1:
        # got it
        pos = (x - SIZE + 1, y)
        break
    else:
        # opposite corner not in beam, try next line
        pos = (x, y + 1)


print("found ! {}", pos)
