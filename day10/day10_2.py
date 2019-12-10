#!/usr/bin/env python3

from collections import Counter, defaultdict
from math import gcd, sqrt
import sys

raw_map = sys.argv[1]

with open(raw_map, "r") as f:
    space_map = [[" # " if c == "#" else "   " for c in line.strip()]
                 for line in f.readlines()]
    WIDTH = len(space_map[0])
    HEIGHT = len(space_map)

def find_asteroids(space_map):
    asteroids = []
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if space_map[y][x] == " # ":
                asteroids.append((x, y))
    return asteroids

def angle(base, asteroid):
    dx = asteroid[0] - base[0]
    #dy = asteroid[1] - base[1]
    dy = base[1] - asteroid[1]

    if dx == 0:
        return (0, dy/abs(dy))
    elif dy == 0:
        return (dx/abs(dx), 0)

    factor = gcd(dx, dy)

    return (dx / factor, dy / factor)

def distance(base, asteroid):
    dx = asteroid[0] - base[0]
    dy = asteroid[1] - base[1]

    return dx * dx + dy * dy#norm((dx, dy))

def norm(vec):
    return sqrt(vec[0] * vec[0] + vec[1] * vec[1])

def reachable(base, space_map, closest=True):
    asteroids = find_asteroids(space_map)
    if closest:
        line_of_sights = dict()
    else:
        line_of_sights = defaultdict(list)

    for target in [(x,y) for x in range(0, WIDTH)
                      for y in range(0,HEIGHT)]:
        (x,y) = target
        if space_map[y][x] != " # ":
            continue
        if target == base:
            continue

        direction = angle(base, target)

        if closest:
            dst = distance(base, target)
            if direction not in line_of_sights:
                line_of_sights[direction] = (dst, target)
            elif line_of_sights[direction][0] > dst:
                line_of_sights[direction] = (dst, target)
        else:
            line_of_sights[direction].append(target)
    return line_of_sights

def same_direction(quadrant, direction):
    same = True
    if (quadrant[0] > 0 and direction[0] < 0
            or quadrant[0] < 0 and direction[0] > 0):
        same = False

    if (quadrant[1] > 0 and direction[1] < 0
            or quadrant[1] < 0 and direction[1] > 0):
        same = False

    return same

#print(base)
#print(line_of_sights)

# Check if part 1 still works
#asteroids = find_asteroids(space_map)
#reachable_from = Counter()
#for base in asteroids:
#    can_reach = reachable(base, space_map, closest=True)
#    reachable_from[base] = len(can_reach)

#print(space_map)
#print(find_asteroids(space_map))

destroyed = 0
while True:
    base = (25, 31)
    #base = (0, 0)
    #base = (2, 2)
    can_reach = reachable(base, space_map, closest=True)

    if can_reach == dict():
        break

    quadrants = [[1,1],[1,-1],[-1,-1],[-1,1]]
    base_u = [(0,1),(1,0),(-1,0),(0,-1)]
    reachable_in_quadrant = [Counter(), Counter(), Counter(), Counter()]
    for direction in can_reach.keys():
        #print(direction)
        for idx, quadrant in enumerate(quadrants):
            if same_direction(quadrant, direction):
                n = norm(direction)
                u = base_u[idx]
                scalar_product = u[0] * direction[0] / n + u[1] * direction[1] / n

                #reachable_in_quadrant[idx][direction] = can_reach[direction][1]
                reachable_in_quadrant[idx][can_reach[direction][1]] = scalar_product
                #[scalar_product] = can_reach[direction][1]
                break

    print([reachable_in_quadrant[i] for i in range(0,4)])
    #print(space_map)
    for i in range(0,4):
        for asteroids, _ in reachable_in_quadrant[i].most_common():
            destroyed += 1
            print(asteroids, destroyed)
            space_map[asteroids[1]][asteroids[0]] = "{:3}".format(str(destroyed))

            if destroyed == 200:
                print("Killed it !")
                print(asteroids)
                sys.exit(0)
    #print(space_map)

for y in range(0, HEIGHT):
    for x in range(0, WIDTH):
        sys.stdout.write(space_map[y][x])
    sys.stdout.write("\n")

#print(destroyed)
#print(reachable_from)
