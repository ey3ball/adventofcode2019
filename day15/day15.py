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

def show_map(ship_map, pos=None):
    sys.stderr.write("SHIP MAP\n\n")
    for x, line in enumerate(ship_map):
        for y, obj in enumerate(line):
            if pos is not None and pos[0] == x and pos[1] == y:
                sys.stderr.write("=")
            elif obj == 0:
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

GRID_SIZE = int(64)
center = np.array([GRID_SIZE // 2, GRID_SIZE // 2])
ship_map = np.zeros((GRID_SIZE + 1, GRID_SIZE + 1))

DIRECTIONS = {DIR_NORTH, DIR_SOUTH, DIR_EAST, DIR_WEST}

pos = center

class Droid:
    def __init__(self, program):
        self.droid = IntCodeInterpreter(program)
        self.droid_gen = self.droid.run_gen()

    def move(self, direction):
        self.droid.push_input(direction)

    def status(self):
        return next(self.droid_gen)


class DroidSimulator:
    def __init__(self, ship_map, pos):
        self.ship_map = ship_map.copy()
        self.pos = pos
        self.reply = 0

    def move(self, direction):
        test_pos = self.pos + movement(direction)
        if self.ship_map[test_pos[0]][test_pos[1]] == 1:
            self.reply = 0
        else:
            self.reply = 1
            self.pos = test_pos

    def status(self):
        return self.reply


droid = Droid(program)

def explore(droid, ship, pos):
    movement_stack = list(DIRECTIONS)
    len_from_start = 0
    max_len = 0
    oxygen_distance = 0
    oxygen_pos = None

    ship[pos[0], pos[1]] = 4
    while movement_stack != []:
        next_direction = movement_stack.pop()
        if next_direction < 0:
            rollback = True
            next_direction = -next_direction
        else:
            rollback = False

        next_move = movement(next_direction)
        next_pos = pos + next_move

        # Don't proceed if we've already explored that direction
        if (ship[next_pos[0]][next_pos[1]] != 0
                and ship[next_pos[0]][next_pos[1]] != 4
                and not rollback):
            continue

        droid.move(next_direction)
        droid_status = droid.status()

        if droid_status == STATUS_WALL:
            ship[next_pos[0]][next_pos[1]] = "1"
        elif (droid_status == STATUS_OK
                or droid_status == STATUS_OXYGEN):
            ship[next_pos[0]][next_pos[1]] = "2"
            back = opposite(next_direction)

            if rollback:
                len_from_start -= 1
            else:
                len_from_start += 1

                if len_from_start >= max_len:
                    max_len = len_from_start

            if droid_status == STATUS_OXYGEN:
                ship[next_pos[0]][next_pos[1]] = "3"
                oxygen_distance = len_from_start
                oxygen_pos = pos
                print("FOUND OXYGEN")
                #break

            if not rollback:
                movement_stack.append(-back)
                movement_stack += list(DIRECTIONS - {back})
            pos = next_pos

    return (oxygen_distance, oxygen_pos, max_len)


(ox_dst, ox_pos, _) = explore(droid, ship_map, pos)
print("Oxygen dst {} pos {}".format(ox_dst, ox_pos))
show_map(ship_map)

droid2 = DroidSimulator(ship_map, ox_pos)
ship_map2 = np.zeros((GRID_SIZE + 1, GRID_SIZE + 1))
(_, _, max_len) = explore(droid2, ship_map2, ox_pos)
print(max_len + 1)
