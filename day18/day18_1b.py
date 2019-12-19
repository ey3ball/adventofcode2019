#!/usr/bin/env python3

from collections import Counter
import string
import sys

with open("day18_i.txt", "r") as f:
    map_ = [l.strip() for l in f.readlines()]

class Area:
    def __init__(self, map_):
        self.map = map_
        self.width = len(map_[0])
        self.height = len(map_)

    def show(self, pos=None):
        sys.stderr.write("AREA MAP\n\n")
        for x, line in enumerate(self.map):
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

    def is_key(self, pos):
        return self.get(pos) in string.ascii_lowercase

    def is_wall(self, pos):
        return self.get(pos) in string.ascii_uppercase

    def can_walk(self, tile):
        if tile == "#":
            return False
        elif tile in string.ascii_lowercase:
            return True
        elif tile in string.ascii_uppercase:
            return False
        elif tile == ".":
            return True
        elif tile == "@":
            return True
        else:
            print(tile)
            assert False

    def vicinity(self, pos):
        if self.is_key(pos):
            return []

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
                and p[1] < self.height
                and self.can_walk(self.get(p))]

def find_obj(area, target):
    found = []
    def _find_obj(x, y, obj):
        if obj == target:
            found.append((x,y))
    area.foreach(_find_obj)
    return found

area = Area(map_)
area.show()
start_pos = find_obj(area, "@")[0]
visited = Counter({start_pos: 0})
distance = 0
cur_points = [start_pos]

print(start_pos)
while True:
    distance += 1
    next_points = []
    for pos in cur_points:
        next_points += [p for p in area.vicinity(pos) if p not in visited.keys()]

    if next_points == []:
        break

    for new_point in next_points:
        visited[new_point] = distance

    cur_points = next_points

for x in range(area.width):
    for y in range(area.height):
        if (x,y) in visited:
            if area.get((x,y)) in string.ascii_lowercase:
                sys.stderr.write(area.get((x,y)))
            else:
                sys.stderr.write(".")
        else:
            sys.stderr.write(" ")
    sys.stderr.write("\n")
sys.stderr.write("\n")
