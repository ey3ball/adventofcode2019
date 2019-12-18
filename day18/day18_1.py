#!/usr/bin/env python3

import sys

with open("day18_1.txt", "r") as f:
    area = [l.strip() for l in f.readlines()]

WIDTH = len(area[0])
HEIGHT = len(area)

def show_area(area, pos=None):
    sys.stderr.write("AREA MAP\n\n")
    for x, line in enumerate(area):
        for y, obj in enumerate(line):
            if pos is not None and pos[0] == x and pos[1] == y:
                sys.stderr.write("=")
            else:
                sys.stderr.write(obj)
        sys.stderr.write("\n")
    sys.stderr.write("\n")

def foreach(area, find_func):
    for x, line in enumerate(area):
        for y, obj in enumerate(line):
            find_func(area, x, y, obj)

def find_obj(area, target):
    found = []
    def _find_obj(area, x, y, obj):
        if obj == target:
            found.append((x,y))
    foreach(area, _find_obj)
    return found

start_pos = find_obj(area, "@")[0]

print(start_pos)


show_area(area)
