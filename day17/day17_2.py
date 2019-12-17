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

def show_map(cameras, intersect=None, robot=None):
    for x, line in enumerate(cameras):
        for y, obj in enumerate(line):
            if intersect and (x,y) in intersect:
                sys.stderr.write("O")
            elif robot and [x,y] == robot[0]:
                sys.stderr.write(robot[1])
            else:
                sys.stderr.write(chr(obj))
        sys.stderr.write("\n")
    sys.stderr.write("\n\n")

def opposite(direction):
    return {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E"
    }[direction]

def moves(point):
    return {
        "E": [point[0], point[1] + 1],
        "W": [point[0], point[1] - 1],
        "S": [point[0] + 1, point[1]],
        "N": [point[0] - 1, point[1]]
    }

def turns(fromto):
    return {
        "NE": "R",
        "NW": "L",
        "ES": "R",
        "EN": "L",
        "SW": "R",
        "SE": "L",
        "WN": "R",
        "WS": "L"
    }[fromto]

def vicinity(point):
    return {d:p for (d, p) in moves(point).items()
            if p[0] >= 0 and p[0] < HEIGHT and p[1] >= 0 and p[1] < WIDTH}

def reachable_path(cameras, point):
    return {d:p for (d, p) in vicinity(point).items()
            if cameras[p[0]][p[1]] == ord("#")}

def find_intersections(cameras):
    intersect = set()
    for x, line in enumerate(cameras):
        for y, obj in enumerate(line):
            if cameras[x][y] == ord(VOID):
                continue

            nearby_points = vicinity((x,y))
            neighbours = sum([cameras[p[0]][p[1]] == ord("#") for p in nearby_points.values()])
            if neighbours > 2:
                intersect.add((x,y))
    return intersect

intersect = find_intersections(cameras)
show_map(cameras, intersect=intersect)

POS = { "^": "N", "v": "S", ">": "E", "<": "W" }

for x, line in enumerate(cameras):
    for y, obj in enumerate(line):
        if chr(obj) in POS.keys():
            print("found")
            init_pos = [x, y]
            init_dir = POS[chr(cameras[x][y])]

print(init_pos)
print(init_dir)

pos = init_pos
orientation = init_dir

print("start")
path = []
turn = ""
steps = 0
i = 0
while True:
    neighbours = reachable_path(cameras, pos)

    if orientation in neighbours:
        if (pos[0], pos[1]) not in intersect:
            cameras[pos[0]][pos[1]] = ord("!")
        pos = moves(pos)[orientation]
        steps += 1
        continue

    next_orientation = list(neighbours.keys() - opposite(orientation))[0]
    #print("{}{}".format(turn, int(steps)))
    if turn != "":
        path.append("{}{}".format(turn, int(steps)))
    next_turn = turns(orientation + next_orientation)
    print("Turn {} after {} steps".format(next_turn, steps))
    steps = 0
    orientation = next_orientation
    turn = next_turn
    i += 1

    if i == 33:
        break

print(path)

path.append("L6")

As = "L8,R12,R12,R10"
Bs = "R10,R12,R10"
Cs = "L10,R10,L6"
A = As.split(",")
B = Bs.split(",")
C = Cs.split(",")
compresseds = "A,B,A,B,C,C,B,A,B,C"
expanded = compresseds.replace("A", As).replace("B", Bs).replace("C", Cs)
compressed  = A + B + A + B + C + C + B + A + B + C
As = As.replace("L", "L,")
As = As.replace("R", "R,")
Bs = Bs.replace("L", "L,")
Bs = Bs.replace("R", "R,")
Cs = Cs.replace("L", "L,")
Cs = Cs.replace("R", "R,")


print(compressed)
print(path)

assert(compressed == path)
assert(expanded.split(",") == path)

show_map(cameras, robot=(pos, orientation))

print(droid.mem[0])
program = str(2) + program[1:]
droid = IntCodeInterpreter(program)
print(droid.mem[0])

input_str = compresseds + "\n" + As + "\n" + Bs + "\n" + Cs + "\n" + "n" + "\n"
print(input_str)
droid.reg["in"] = [ord(i) for i in input_str]
droid.run()
print(droid.reg["out"])
