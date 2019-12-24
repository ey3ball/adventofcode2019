#!/usr/bin/env python3

from collections import Counter, defaultdict
import string
import sys

with open("day18_i.txt", "r") as f:
    map_ = [[c for c in l if c != '\n'] for l in f.readlines()]

class Area:
    def __init__(self, map_, xs=None, ys=None):
        self.map = map_

        self.width = len(map_[0])
        self.height = len(map_)
        if xs is None:
            self.xstart = 0
            self.xend = self.width
        else:
            self.xstart = xs[0]
            self.xend = xs[1]

        if ys is None:
            self.ystart = 0
            self.yend = self.height
        else:
            self.ystart = ys[0]
            self.yend = ys[1]

    def show(self, pos=None):
        sys.stderr.write("AREA MAP\n\n")
        for y in range(self.ystart, self.yend):
            for x in range(self.xstart, self.xend):
                obj = self.map[y][x]
                if pos is not None and pos[0] == x and pos[1] == y:
                    sys.stderr.write("=")
                else:
                    sys.stderr.write(obj)
            sys.stderr.write("\n")
        sys.stderr.write("\n")

    def foreach(self, find_func):
        for y in range(self.ystart, self.yend):
            for x in range(self.xstart, self.xend):
                find_func(x, y, self.map[y][x])

    def get(self, pos):
        return self.map[pos[1]][pos[0]]

    def set(self, pos, tile):
        self.map[pos[1]][pos[0]] = tile

    def is_key(self, pos):
        return self.get(pos) in string.ascii_lowercase

    def is_door(self, pos):
        return self.get(pos) in string.ascii_uppercase

    def in_area(self, pos):
        return (pos[0] >= self.xstart and pos[0] < self.xend
                and pos[1] >= self.ystart and pos[1] < self.yend)

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

def walkable(tile, keys, doors=string.ascii_uppercase):
    if tile == "#":
        return False
    elif tile in string.ascii_lowercase:
        return True
    elif tile.lower() in keys:
        return True
    elif tile in doors:
        return False
    elif tile == ".":
        return True
    elif tile == "@":
        return True
    else:
        return True
        #assert False

def add_key(tile, keys):
    if tile in string.ascii_lowercase:
        return frozenset(keys | {tile})
    else:
        return keys

#visited = defaultdict(list)
#
# This class registers interesting paths to all maze points
#class BestPaths:
#    def __init__(self):
#        self.visited = defaultdict(list)
#
#    def new_path(self, pos, length, keys):
#        useless = False
#        new_paths = []
#
#        # Find similar paths reaching this point
#        # In the process we remove any previous path that's not interesting
#        # anymore
#        for best_length, with_keys in self.visited[pos]:
#            if keys <= with_keys:
#                useless = True
#
#            if with_keys <= keys and best_length + 1 >= length:
#                continue
#            new_path.append((best_length, with_keys))
#
#        if not useless:
#            new_paths.append((length, keys))
#            self.visited[pos] = new_paths
#            return True
#        else:
#            return False

class MazeBot:
    def __init__(self, area, start_pos):
        self.area = area

        self.all_keys = find_keys(self.area)
        self.all_doors = set([c.upper() for c in list(self.all_keys)])
        self.visited = defaultdict(list)
        self.distance = 0
        self.cur_points = [(frozenset(), 0, start_pos)]
        self.max_keys = 0
        self.done = False
        self.static_points = set()

    def state(self):
        if self.done:
            return [(self.all_keys, self.distance)]
        else:
            return [(keys, dst) for (keys, dst, _) in list(self.static_points) if dst != 0]

    def inject(self, state):
        if self.done:
            return 0

        for keys, dst, pos in list(self.static_points):
            for (ext_keys, ext_dst) in state:
                self.cur_points.append((keys | ext_keys, dst + ext_dst, pos)) 

    def filter_useless(self, points):
        actual_points = []
        for new_point in points:
            if new_point[0] >= self.all_keys:
                self.distance = new_point[1]
                sys.stderr.write("Collected all keys {} / took {} steps\n"
                        .format(self.all_keys, new_point[1]))
                self.done = True
                return 1
            if len(new_point[0]) > self.max_keys:
                self.max_keys = len(new_point[0])
                #sys.stderr.write("Got {} keys {}\n".format(self.max_keys, new_point[0]))
                sys.stderr.write("Including {}\n".format(self.all_keys & new_point[0]))
                print("Path heads {}".format(len(points)))

            useless = False
            new_keys = set()
            for keys in self.visited[new_point[2]]:
                if new_point[0] <= keys:
                    useless = True

                if keys <= new_point[0]:
                    continue
                new_keys |= {keys}

            if not useless:
                new_keys |= {new_point[0]}
                self.visited[new_point[2]] = new_keys
                actual_points.append(new_point)
        return actual_points

    def progress(self):
        if self.done:
            return 1

        next_points = []
        for keys, dst, pos in self.cur_points:
            next_points += [(add_key(self.area.get(p), keys), dst + 1, p)
                            for p in self.area.vicinity(pos)
                                #if ((keys, p) not in visited.keys()
                                    if walkable(self.area.get(p), keys,
                                        doors=self.all_doors)]

        nearby_doors = set()
        # Keep points of interest available. When we see a wall, just wait
        # there in case another bot unlocks it for us
        for keys, dst, pos in self.cur_points:
            doors = [self.area.get(p)
                     for p in self.area.vicinity(pos)
                     if self.area.is_door(p)]
            if doors != []:
                nearby_doors |= set(doors)
                self.static_points |= {(frozenset(self.all_keys & keys), dst, pos)}

        actual_points = self.filter_useless(next_points)
        if actual_points == []:
            print("out of options, nearby doors: {}".format(nearby_doors))
            return -1

        self.cur_points = actual_points

        return 0


area = Area(map_)
start_pos = find_obj(area, "@")[0]

area.show()

# Fix center of maze for p2
for pos in area.vicinity(start_pos):
    area.set(pos, "#")
area.set(start_pos, "#")
sub_areas = []
for i, j in [(a, b) for a in [1, -1] for b in [1, -1]]:
    area.set((start_pos[0] + i, start_pos[1] + j), "@")

    if i == -1:
        xs = (0, start_pos[0] + 1)
    else:
        xs = (start_pos[0], area.width)
    if j == -1:
        ys = (0, start_pos[1] + 1)
    else:
        ys = (start_pos[1], area.height)

    sub_area = Area(area.map, xs, ys)

    sub_areas.append(((start_pos[0] + i, start_pos[1] + j), sub_area))
    sub_area.show()

#start_pos = find_obj(area, "@")
#area.show()
print(start_pos)

# Instantiate vault bots
bots = [MazeBot(area, pos) for pos, area in sub_areas]

for bot in bots:
    sys.stderr.write("Keys {}\n".format(bot.all_keys))

for i, bot in enumerate(bots):
    print("Advance bot {}".format(i))
    while bot.progress() == 0:
        pass

for it in range(0,10):
    for i, bot in enumerate(bots):
        inject_state = [to_inject
                        for other_bot in bots
                        for to_inject in other_bot.state()
                            if other_bot != bot]

        print("Advance bot {}".format(i))
        print("Inject other bots state {}".format(len(inject_state)))
        #print(inject_state)

        bot.inject(inject_state)
        while bot.progress() == 0:
            pass

        print("Bot {} state {}".format(i, len(bot.state())))

        all_done = True 
        for bot in bots:
            if not bot.done:
                all_done = False

        if all_done:
            print("Collected all keys accross bots")
            sys.exit(0)

        #print(bot.state())

#bot = MazeBot(area, start_pos)
#while bot.progress() == 0:
#    pass
