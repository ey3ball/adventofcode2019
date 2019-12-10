#!/usr/bin/env python3

from collections import Counter, defaultdict
from math import gcd, sqrt
import sys

raw_map = sys.argv[1]

with open(raw_map, "r") as f:
    space_map = [[1 if c == "#" else 0 for c in line.strip()]
                 for line in f.readlines()]
    WIDTH = len(space_map[0])
    HEIGHT = len(space_map)

def find_asteroids(space_map):
    asteroids = []
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if space_map[y][x] == 1:
                asteroids.append((x, y))
    return asteroids

def angle(base, asteroid):
    dx = asteroid[0] - base[0]
    #dy = asteroid[1] - base[1]
    dy = asteroid[1] - base[1]

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
        if space_map[y][x] == 0:
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

while True:
    #base = (25, 31) 
    base = (0, 0) 
    can_reach = reachable(base, space_map, closest=True)

    quadrants = [[1,1],[1,-1],[-1,-1],[-1,1]]
    reachable_in_quadrant = [dict(), dict(), dict(), dict()]
    for direction in can_reach.keys():
        for idx, quadrant in enumerate(quadrants):
            if same_direction(quadrant, direction):
                n = norm(direction)
                scalar_product = quadrant[0] * direction[0] / n + quadrant[1] * direction[1] / n

                reachable_in_quadrant[idx][scalar_product] = can_reach[direction][1]
                break
    print(reachable_in_quadrant)
    break

#print(reachable_from)
