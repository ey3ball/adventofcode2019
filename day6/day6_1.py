#!/usr/bin/python3

from collections import defaultdict

with open("day6.txt", "r") as f:
    datafile = f.readlines()

orbits = defaultdict(list)

for orbit in datafile:
    [around, obj] = orbit.strip().split(")")
    orbits[around].append(obj)

nodes = ["COM"]
depth = 1
total_depth = 0

while True:
    nodes = sum([orbits[obj] for obj in nodes], [])
    total_depth += len(nodes) * depth

    depth += 1

    if not len(nodes):
        break

print(total_depth)
