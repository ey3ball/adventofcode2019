#!/usr/bin/env python3

from intcode import IntCodeInterpreter
import sys
import math

SCAFFOLD = "#"
VOID = "."
INTERSECT = "O"

with open("day17.txt", "r") as f:
    program = f.readline().strip()

droid = IntCodeInterpreter(program)
droid_gen = droid.run_gen()

cameras = []
line = []
for output in droid_gen:
    if output == 10:
        if line != []:
            cameras.append(line)
            line = []
    else:
        line.append(output)
    sys.stderr.write(chr(output))

HEIGHT = len(cameras)
WIDTH = len(cameras[0])
print(HEIGHT)

def show_map(cameras, intersect=None):
    for x, line in enumerate(cameras):
        for y, obj in enumerate(line):
            if intersect and (x,y) in intersect:
                sys.stderr.write("O")
            else:
                sys.stderr.write(chr(obj))
        sys.stderr.write("\n")
    sys.stderr.write("\n\n")

def vicinity(point):
    points = [[point[0] + 1, point[1]],
                [point[0] - 1, point[1]],
                [point[0], point[1] + 1],
                [point[0], point[1] - 1]]

    return [p for p in points
            if p[0] >= 0 and p[0] < HEIGHT and p[1] >= 0 and p[1] < WIDTH]

def find_intersections(cameras):
    intersect = set() 
    for x, line in enumerate(cameras):
        for y, obj in enumerate(line):
            if cameras[x][y] == ord(VOID):
                continue

            nearby_points = vicinity((x,y))
            neighbours = sum([cameras[p[0]][p[1]] == ord("#") for p in nearby_points])
            if neighbours > 2:
                intersect.add((x,y)) 
    return intersect 

intersect = find_intersections(cameras)
show_map(cameras, intersect=intersect)
print(find_intersections(cameras))
print(len(cameras))
print(WIDTH)
print(HEIGHT)

print(intersect)
print(sum([p[0] * p[1] for p in intersect]))
