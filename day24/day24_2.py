from collections import defaultdict

import string
import sys
import time
import copy

with open("day24_i.txt", "r") as f:
    map_ = [[c for c in l if c != '\n'] for l in f.readlines()]

# Small class use to keep track of map levels
# Each area can call upper/lower to locate tiles of surrounding levels
class AreaManager:
    def __init__(self, l0):
        area0 = Area(l0, self)
        self.maps = {area0: (None,None)}
        self.levels = {area0: 0}
        self.upper(area0)

    def default(self):
        return Area([["." for i in range(0,5)] for j in range(0,5)], self)

    def ajacent_levels(self, area):
        (down, up) = self.maps[area]
        if down == None:
            down = self.default()
            self.maps[area] = (down, up)
            self.maps[down] = (None, area)
            self.levels[down] = self.levels[area] + 1
        if up == None:
            up = self.default()
            self.maps[area] = (down, up)
            self.maps[up] = (area, None)
            self.levels[up] = self.levels[area] - 1
        return (down, up)

    def upper(self, area):
        (_, up) = self.ajacent_levels(area)
        return up

    def lower(self, area):
        (down, _) = self.ajacent_levels(area)
        return down

class Area:
    def __init__(self, map_, manager):
        self.map = map_
        self.width = len(map_[0])
        self.height = len(map_)
        self.manager = manager

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

    def rank(self):
        r = [0]
        def _rank(x, y, obj):
            if obj == "#":
                r[0] += 2 ** (x + y * self.width)

        self.foreach(_rank)
        return r[0]

    def in_area(self, pos):
        return (pos[0] >= 0 and pos[0] < self.width
                and pos[1] >= 0 and pos[1] < self.height)

    def vicinity(self, pos):
        if pos == (2,2):
            return []

        candidates = [
            (pos[0] + 1, pos[1]),
            (pos[0] - 1, pos[1]),
            (pos[0], pos[1] + 1),
            (pos[0], pos[1] - 1)
        ]


        # Compute plutonian = it's the list of values from adjacent nodes,
        # taking into account the recursive shape of the surrounding space
        plutonian = []
        for i, c in enumerate(candidates):
            upper = None
            # Hit center of grid we're looking one level down
            if c == (2,2):
                lower_grid = self.manager.lower(self)
                if i == 0:
                    lower = ([0],range(0,5))
                elif i == 1:
                    lower = ([4],range(0,5))
                elif i == 2:
                    lower = (range(0,5), [0])
                elif i == 3:
                    lower = (range(0,5), [4])
                for x in lower[0]:
                    for y in lower[1]:
                        #print((x,y))
                        plutonian.append(lower_grid.get((x,y)))
            # Outside of grid, we're looking at the upper level
            elif not self.in_area(c):
                upper_grid = self.manager.upper(self)
                if i == 0:
                    upper = (3,2)
                elif i == 1:
                    upper = (1,2)
                elif i == 2:
                    upper = (2,3)
                elif i == 3:
                    upper = (2,1)
                #print("upper", pos, upper)
                plutonian.append(upper_grid.get(upper))
            else:
                plutonian.append(self.get(c))
        #print(pos, len(plutonian), plutonian)
        return [1 for p in plutonian if p == "#"]

area = AreaManager(map_)

#for a in area.maps.keys():
#    print("Level {}".format(area.levels[a]))
#    a.show()

t = 0
ranks = set()
while True:
    if t == 200:
        break

    print(t)
    # Show maps for debug purposes
    #for a in area.maps.keys():
    #    if abs(area.levels[a]) <= t:
    #        print("Level {}".format(area.levels[a]))
    #        a.show()

    # Create a copy of existing areas
    new_maps = dict()
    for a in area.maps.keys():
        new_maps[a] = copy.deepcopy(a.map)

    # Life !
    for a in dict(area.maps).keys():
        new_map = new_maps[a]
        def life(x,y,obj):
            if obj == "#":
                neighs = a.vicinity((x,y))
                neighs_life = sum(neighs)
                if neighs_life == 1:
                    new_map[y][x] = "#"
                else:
                    new_map[y][x] = "."
            elif obj == ".":
                neighs = a.vicinity((x,y))
                neighs_life = sum(neighs)
                if neighs_life == 1 or neighs_life == 2:
                    new_map[y][x] = "#"
                else:
                    new_map[y][x] = "."
            else:
                assert False, "Unknown object"

        a.foreach(life)

    # Propagate updated maps
    for a in area.maps.keys():
        if a in new_maps:
            a.map = new_maps[a]
        else:
            pass

    t += 1

bugs = 0
for a in area.maps.keys():
    print("Level {}".format(area.levels[a]))
    for line in a.map:
        for obj in line:
            if obj == "#":
                bugs += 1
    #a.show()

print(bugs)
