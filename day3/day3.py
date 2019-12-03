#!/usr/bin/python3

from collections import Counter

def compute_trace(path):
    pos = (0, 0)
    reached = set()
    steps = dict()
    history = []
    step_count = 1

    for step in path:
        direction = step[0]
        distance = int(step[1:])

        if direction == "R":
            move = (1, 0)
        elif direction == "L":
            move = (-1, 0)
        elif direction == "U":
            move = (0, 1)
        elif direction == "D":
            move = (0, -1)

        for i in range(distance):
            pos = (pos[0] + move[0], pos[1] + move[1])
            history.append(pos)
            reached.update([pos])

            if pos not in steps:
                steps[pos] = step_count

            step_count += 1


    return (reached, steps)

def distance(points):
    return [abs(p[0]) + abs(p[1]) for p in points]

testwire1 = "R8,U5,L5,D3".split(",")
testwire2 = "U7,R6,D4,L4".split(",")

(reached1, steps1) = compute_trace(testwire1)
(reached2, steps2) = compute_trace(testwire2)

assert(min(distance(reached1 & reached2)) == 6)
assert(min([steps1[point] + steps2[point] for point in reached1 & reached2]) == 30)


testwireb1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(",")
testwireb2 = "U62,R66,U55,R34,D71,R55,D58,R83".split(",")

(reached1, steps1) = compute_trace(testwireb1)
(reached2, steps2) = compute_trace(testwireb2)

assert(min(distance(reached1 & reached2)) == 159)
assert(min([steps1[point] + steps2[point] for point in reached1 & reached2]) == 610)

testwirec1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(",")
testwirec2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(",")

(reached1, steps1) = compute_trace(testwirec1)
(reached2, steps2) = compute_trace(testwirec2)

assert(min(distance(reached1 & reached2)) == 135)
assert(min([steps1[point] + steps2[point] for point in reached1 & reached2]) == 410)

with open("path.txt") as f:
    wire1 = f.readline().split(",")
    wire2 = f.readline().split(",")

(reached1, steps1) = compute_trace(wire1)
(reached2, steps2) = compute_trace(wire2)

distances = distance(reached1 & reached2)
distances.sort()
print(distances)

print(min([steps1[point] + steps2[point] for point in reached1 & reached2]))
