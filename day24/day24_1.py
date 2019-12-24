import string
import sys
import time
import copy 

with open("day24_i.txt", "r") as f:
    map_ = [[c for c in l if c != '\n'] for l in f.readlines()]

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

    def rank(self):
        r = [0]
        def _rank(x, y, obj):
            if obj == "#":
                r[0] += 2 ** (x + y * self.width)

        self.foreach(_rank)
        return r[0]

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

area = Area(map_)
area.show()

t = 0
ranks = set() 
while True:
    print(t)
    #area.show()
    new_map = copy.deepcopy(area.map)

    if t % 1000 == 0:
        print(t)

    def life(x,y,obj):
        if obj == "#":
            neighs = area.vicinity((x,y))
            neighs_life = sum([1 for n in neighs if area.get(n) == "#"])

            if neighs_life == 1:
                new_map[y][x] = "#"
            else:
                new_map[y][x] = "."
        elif obj == ".":
            neighs = area.vicinity((x,y))
            neighs_life = sum([1 for n in neighs if area.get(n) == "#"])

            if neighs_life == 1 or neighs_life == 2:
                new_map[y][x] = "#"
            else:
                new_map[y][x] = "."
        else:
            assert False, "Unknown object"

    area.foreach(life)

    area.map = new_map

    area.show()
    rating = area.rank()
    if rating in ranks:
        print("repeats !")
        print(t)
        print(rating)
        break
    else:
        ranks |= {rating}
    #print(ranks)
    #time.sleep(0.5)
    t += 1
