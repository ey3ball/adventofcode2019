#!/usr/bin/env python3

from intcode import IntCodeInterpreter
import sys

with open("day19_1.txt", "r") as f:
    program = f.readline().strip()

SIZE = 100
scanner = [[" " for x in range(0,SIZE)] for y in range(0, SIZE)]

x_off = int(sys.argv[1])
y_off = int(sys.argv[2])

def show_map(scan):
    for y, line in enumerate(scan):
        for x, obj in enumerate(line):
            sys.stderr.write(obj)
        sys.stderr.write("\n")
    sys.stderr.write("\n")

count = 0
drone = IntCodeInterpreter(program)
drone_gen = drone.run_gen()
for y, line in enumerate(scanner):
    for x, _ in enumerate(line):
        drone.reset()
        drone.push_input(x+x_off)
        drone.push_input(y+y_off)

        status = next(drone_gen)

        if status == 0:
            scanner[y][x] = "."
        else:
            scanner[y][x] = "#"
            count += 1

show_map(scanner)
print(count)
