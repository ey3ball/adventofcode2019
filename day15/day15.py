#!/usr/bin/env python3

import numpy as np
import sys
from intcode import IntCodeInterpreter
import time

DIR_NORTH = 1
DIR_SOUTH = 2
DIR_WEST = 3
DIR_EAST = 4

STATUS_WALL = 0
STATUS_OK = 1
STATUS_OXYGEN = 2

def opposite(direction):
    return {
        DIR_NORTH: DIR_SOUTH,
        DIR_SOUTH: DIR_NORTH,
        DIR_WEST: DIR_EAST,
        DIR_EAST: DIR_WEST
    }[direction]

def movement(direction):
    return {
        DIR_NORTH: np.array([0, -1]),
        DIR_SOUTH: np.array([0, 1]),
        DIR_WEST: np.array([1, 0]),
        DIR_EAST: np.array([-1, 0])
    }[direction]

def show_map(ship_map):
    sys.stderr.write("SHIP MAP\n\n")
    for line in ship_map:
        for obj in line:
            if obj == 0:
                sys.stderr.write(" ")
            elif obj == 1:
                sys.stderr.write("*")
            elif obj == 2:
                sys.stderr.write(".")
            elif obj == 3:
                sys.stderr.write("X")
            elif obj == 4:
                sys.stderr.write("#")
        sys.stderr.write("\n")
    sys.stderr.write("\n\n")

with open("day15.txt", "r") as f:
    program = f.readline().strip()

droid = IntCodeInterpreter(program)
droid_gen = droid.run_gen()

GRID_SIZE = int(64)
center = np.array([GRID_SIZE // 2, GRID_SIZE // 2])
ship = np.zeros((GRID_SIZE + 1, GRID_SIZE + 1))

pos = center
directions = {DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST}
movement_stack = list(directions)
moves = 0
len_from_start = 0
ship[pos[0], pos[1]] = 4
while movement_stack != []:
    moves += 1
    print(movement_stack)
    next_direction = movement_stack.pop()
    if next_direction < 0:
        rollback = True
        next_direction = -next_direction
    else:
        rollback = False

    next_move = movement(next_direction)
    next_pos = pos + next_move

    print(pos)
    print(next_move)
    print(next_pos)

    droid.push_input(next_direction)

    droid_status = next(droid_gen)
    if droid_status == STATUS_WALL:
        ship[next_pos[0]][next_pos[1]] = "1"
    elif droid_status == STATUS_OK:
        ship[next_pos[0]][next_pos[1]] = "2"
        back = opposite(next_direction)

        if rollback:
            len_from_start -= 1
        else:
            len_from_start += 1

        if not rollback:
            movement_stack.append(-back)
            movement_stack += list(directions - {back})
        pos = next_pos
    elif droid_status == STATUS_OXYGEN:
        len_from_start += 1
        ship[next_pos[0]][next_pos[1]] = "3"
        pos = next_pos
        print("FOUND OXYGEN")
        break

    if moves % 100 == 0:
        show_map(ship)
        time.sleep(0.1)

show_map(ship)
print(len_from_start)
