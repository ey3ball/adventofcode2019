#!/usr/bin/env python3

from collections import Counter
from math import gcd
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
    dy = asteroid[1] - base[1]

    if dx == 0:
        return (0, dy/abs(dy))
    elif dy == 0:
        return (dx/abs(dx), 0)

    factor = gcd(dx, dy)

    return (dx / factor, dy / factor)


#print(space_map)
#print(find_asteroids(space_map))

asteroids = find_asteroids(space_map)

reachable_from = Counter()
for base in asteroids:
    line_of_sights = Counter()
    for target in [(x,y) for x in range(0, WIDTH)
                      for y in range(0,HEIGHT)]:
        (x,y) = target
        if space_map[y][x] == 0:
            continue
        if target == base:
            continue

        line_of_sights[angle(base, target)] += 1

    #print(base)
    #print(line_of_sights)

    reachable_from[base] = len(line_of_sights)

print(reachable_from)
