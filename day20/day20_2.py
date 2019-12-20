#!/usr/bin/env python3

from collections import Counter
import string
import sys

with open("day20_2.txt", "r") as f:
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

    def in_area(self, pos):
        return (pos[0] >= 0 and pos[0] < self.width
                and pos[1] >= 0 and pos[1] < self.height)

    def is_edge(self, pos):
        return (pos[0] <= 1 or pos[0] >= self.width - 2
                or pos[1] <= 1 or pos[1] >= self.height - 2)

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

area = Area(map_)
area.show()
print(area.width)
print(area.height)

def find_portals(area):
    outer = dict()
    inner = dict()
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

        if area.is_edge((x,y)):
            outer[(x,y)] = gate_name(first_letter + last_letter)
        else:
            inner[(x,y)] = gate_name(first_letter + last_letter)

    area.foreach(_find_portal)
    return (outer, inner)

def exit_portal(area, name, portals):
    [exit_pos] = [k for k,v in portals.items() if v == name]

    nearby_pos = [nearby for nearby in area.vicinity(exit_pos)]

    for pos in nearby_pos:
        if area.get(pos) == ".":
            return pos

def gate_name(letters):
    if letters[0] > letters[1]:
        return letters[1] + letters[0]
    else:
        return letters

(outer_portals, inner_portals) = find_portals(area)
gates = {v for k,v in {**outer_portals, **inner_portals}.items()}
print(outer_portals)
print(inner_portals)
print(gates)


[start_pos] = [k for k,v in outer_portals.items() if v == "AA"]
print("start")
print(start_pos)

cur_points = [(0, start_pos)]
visited = Counter({cur_points[0]: 0})
distance = 0

while True:
    distance += 1
    next_points = []
    for level, pos in cur_points:
        next_points += [(level, p) for p in area.vicinity(pos)
                        if (level, p) not in visited.keys()
                            and area.get(p) != "#"
                            and area.get(p) != " "]

    if next_points == []:
        break

    actual_points = []
    for level, new_point in next_points:
        if new_point in outer_portals.keys():
            if outer_portals[new_point] == "ZZ":
                if level == 0:
                    print("Found ZZ")
                    print(distance - 2)
                    sys.exit(0)
                else:
                    continue
            if level == 0 or outer_portals[new_point] == "AA":
                continue
            new_point = (level - 1, exit_portal(area, outer_portals[new_point], inner_portals))
        elif new_point in inner_portals.keys():
            new_point = (level + 1, exit_portal(area, inner_portals[new_point], outer_portals))
        else:
            new_point = (level, new_point)

        if new_point in visited:
            continue

        visited[new_point] = distance
        actual_points.append(new_point)

    #print("possible points {}".format(actual_points))

    cur_points = actual_points


print(area.vicinity((9,6)))
print(area.get((9,7)))
print((9,7) in visited.keys())
print((9,7) in portals.keys())
print(exit_portal(area, (9,7), portals))
