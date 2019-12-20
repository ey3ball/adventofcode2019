#!/usr/bin/env python3

from collections import Counter
import string
import sys

with open("day20_0.txt", "r") as f:
    map_ = [l.replace("\n", "") for l in f.readlines()]

class Area:
    def __init__(self, map_):
        self.map = map_
        self.width = len(map_[0])
        self.height = len(map_)

    def show(self, pos=None):
        sys.stderr.write("AREA MAP\n\n")
        for x, line in enumerate(self.map):
            sys.stderr.write("{:2d}".format(x))
            for y, obj in enumerate(line):
                if pos is not None and pos[0] == x and pos[1] == y:
                    sys.stderr.write("=")
                else:
                    sys.stderr.write(obj)
            sys.stderr.write("\n")
        sys.stderr.write("\n")

    def foreach(self, find_func):
        for y, line in enumerate(self.map):
            for x, obj in enumerate(line):
                find_func(x, y, obj)

    def get(self, pos):
        return self.map[pos[1]][pos[0]]

    def is_portal(self, pos):
        return self.get(pos) in string.ascii_lowercase

    def is_wall(self, pos):
        return self.get(pos) in string.ascii_uppercase

    def vicinity(self, pos):
        candidates = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1)
        ]
        return [p for p in candidates 
                if p[0] >= 0
                and p[0] < self.width
                and p[1] >= 0
                and p[1] < self.height]

def find_obj(area, target):
    found = []
    def _find_obj(x, y, obj):
        if obj == target:
            found.append((x,y))
    area.foreach(_find_obj)
    return found

area = Area(map_)
area.show()

def find_portals(area):
    found = dict()
    def _find_portal(x, y, obj):
        if obj not in string.ascii_uppercase:
            return

        last_letter = obj

        nearby_objs = [area.get(nearby) for nearby in area.vicinity((x,y))]

        if Counter(nearby_objs)[" "] != 2:
            return
        if Counter(nearby_objs)["."] != 1:
            return
       
        first_letter = list(set(nearby_objs) - {" ", "."})[0]

        found[first_letter + last_letter] = (x,y)

    area.foreach(_find_portal)
    return found

print(find_portals(area))
