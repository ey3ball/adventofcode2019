#!/usr/bin/env python3

from collections import Counter, defaultdict
import string
import sys

with open("day18_i.txt", "r") as f:
    map_ = [[c for c in l if c != '\n'] for l in f.readlines()]

class Area:
    def __init__(self, map_):
        self.map = map_
        self.width = len(map_[0])
        self.height = len(map_)

    def show(self, pos=None):
        sys.stderr.write("AREA MAP\n\n")
        for y, line in enumerate(self.map):
            for x, obj in enumerate(line):
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

    def set(self, pos, tile):
        self.map[pos[1]][pos[0]] = tile

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

class MazeBot:
    def __init__(self, area, start_pos):
        self.area = area

        self.all_keys = find_keys(self.area)
        self.visited = defaultdict(list)
        self.distance = 0
        self.cur_points = [(frozenset(), start_pos)]
        self.max_keys = 0

    def progress(self):
        self.distance += 1
        next_points = []
        for keys, pos in self.cur_points:
            next_points += [(add_key(self.area.get(p), keys), p)
                            for p in self.area.vicinity(pos)
                                #if ((keys, p) not in visited.keys()
                                    if walkable(self.area.get(p), keys)]

        if next_points == []:
            print("out of options")
            return -1

        #print(next_points)

        actual_points = []
        for new_point in next_points:
            if new_point[0] == self.all_keys:
                print("Collected all keys {} / took {} steps"
                        .format(self.all_keys, self.distance))
                return 1
            if len(new_point[0]) > self.max_keys:
                self.max_keys = len(new_point[0])
                print("Got {} keys".format(self.max_keys))
                print("Path heads {}".format(len(next_points)))

            useless = False
            new_keys = set()
            for keys in self.visited[new_point[1]]:
                if new_point[0] <= keys:
                    useless = True

                if keys <= new_point[0]:
                    continue
                new_keys |= {keys}

            if not useless:
                new_keys |= {new_point[0]}
                self.visited[new_point[1]] = new_keys
                actual_points.append(new_point)

        self.cur_points = actual_points
        return 0




area = Area(map_)
start_pos = find_obj(area, "@")[0]

# Fix center of maze for p2
#for pos in area.vicinity(start_pos):
#    area.set(pos, "#")
#area.set(start_pos, "#")
#for i, j in [(a, b) for a in [1, -1] for b in [1, -1]]:
#    area.set((start_pos[0] + i, start_pos[1] + j), "@")

area.show()

bot = MazeBot(area, start_pos)
while bot.progress() == 0:
    pass
