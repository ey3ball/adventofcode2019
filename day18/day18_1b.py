#!/usr/bin/env python3

from collections import Counter, defaultdict
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

    def in_area(self, pos):
        return (pos[0] >= 0 and pos[0] < self.width
                and pos[1] >= 0 and pos[1] < self.height)

    def vicinity(self, pos):
        candidates = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1)
        ]
        return [p for p in candidates
                if self.in_area(p)]

def find_obj(area, target):
    found = []
    def _find_obj(x, y, obj):
        if obj == target:
            found.append((x,y))
    area.foreach(_find_obj)
    return found

def find_keys(area):
    found = set()
    def _find_obj(x, y, obj):
        if obj in string.ascii_lowercase:
            found.add(obj)
    area.foreach(_find_obj)
    return found

def walkable(tile, keys):
    if tile == "#":
        return False
    elif tile in string.ascii_lowercase:
        return True
    elif tile.lower() in keys:
        return True
    elif tile in string.ascii_uppercase:
        return False
    elif tile == ".":
        return True
    elif tile == "@":
        return True
    else:
        assert False

def add_key(tile, keys):
    if tile in string.ascii_lowercase:
        return frozenset(keys | {tile})
    else:
        return keys

area = Area(map_)
area.show()
start_pos = find_obj(area, "@")[0]
all_keys = find_keys(area)
visited = defaultdict(list)
distance = 0
cur_points = [(frozenset(), start_pos)]

max_keys = 0

print(start_pos)
print(all_keys)
import time
while True:
    distance += 1
    next_points = []
    for keys, pos in cur_points:
        next_points += [(add_key(area.get(p), keys), p)
                        for p in area.vicinity(pos)
                            #if ((keys, p) not in visited.keys()
                                if walkable(area.get(p), keys)]

    if next_points == []:
        print("out of solutions")
        break

    #print(next_points)

    actual_points = []
    for new_point in next_points:
        if new_point[0] == all_keys:
            print("Collected all keys {} / took {} steps".format(all_keys, distance))
            sys.exit(0)
        if len(new_point[0]) > max_keys:
            max_keys = len(new_point[0])
            print("Got {} keys".format(max_keys))
            print("Path heads {}".format(len(next_points)))

        useless = False
        new_keys = set()
        for keys in visited[new_point[1]]:
            if new_point[0] <= keys:
                useless = True

            if keys <= new_point[0]:
                continue
            new_keys |= {keys}

        if not useless:
            new_keys |= {new_point[0]}
            visited[new_point[1]] = new_keys
            actual_points.append(new_point)

    #print(visited)
    #print(actual_points)
    cur_points = actual_points

p = (7,1)
keys = frozenset()
print(walkable(area.get(p), keys))
print(add_key(area.get(p), keys))
