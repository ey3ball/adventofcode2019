#!/usr/bin/python3

from collections import defaultdict

with open("day6.txt", "r") as f:
    datafile = f.readlines()

orbits = defaultdict(list)
parents = dict()

for orbit in datafile:
    [around, obj] = orbit.strip().split(")")
    orbits[around].append(obj)
    parents[obj] = around

def list_parents(node):
    plist = []
    while True:
        if node == "COM":
            break
        plist.append(parents[node])
        node = parents[node]
    return plist

print("list_parents")
san = list_parents("SAN")
you = list_parents("YOU")

common_parents = set(san) & set(you)

first_common = None
for parent in san:
    if parent in common_parents:
        first_common = parent
        break

print(first_common)

nodes = ["COM"]
depth = 1
total_depth = 0

depth_common = 0
depth_san = 0
depth_you = 0

while True:
    nodes = sum([orbits[obj] for obj in nodes], [])
    total_depth += len(nodes) * depth


    if first_common in nodes:
        depth_common = depth
    if "YOU" in nodes:
        depth_you = depth
    if "SAN" in nodes:
        depth_san = depth

    depth += 1

    if not len(nodes):
        break

print(total_depth)
print(depth_common)
print(depth_you)
print(depth_san)
