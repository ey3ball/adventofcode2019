import numpy as np
import copy
import math
from itertools import combinations

#m puzzle input
moons = [
    [np.array([-17, 9, -5]), np.array([0,0,0])],
    [np.array([-1, 7, 13]), np.array([0,0,0])],
    [np.array([-19, 12, 5]), np.array([0,0,0])],
    [np.array([-6, -6, -4]), np.array([0,0,0])]
]

# first example
#moons = [
#    [np.array([-1, 0, 2]), np.array([0,0,0])],
#    [np.array([2, -10, -7]), np.array([0,0,0])],
#    [np.array([4, -8, 8]), np.array([0,0,0])],
#    [np.array([3, 5, -1]), np.array([0,0,0])]
#]

# hard example
#moons = [
#    [np.array([-8, -10, 0]), np.array([0,0,0])],
#    [np.array([5, 5, 10]), np.array([0,0,0])],
#    [np.array([2, -7, 3]), np.array([0,0,0])],
#    [np.array([9, -8, -3]), np.array([0,0,0])]
#]

t = 0

def gravity(moon1, moon2):
    pull = ((moon1[0] < moon2[0]) * 1
            + (moon1[0] > moon2[0]) * -1)

    moon1[1] += pull
    moon2[1] -= pull


def move(moons):
    for moon1, moon2 in combinations(moons, 2):
        gravity(moon1, moon2)

    for moon in moons:
        moon[0] += moon[1]

def energy(moons):
    energy = 0
    for moon in moons:
        potential = sum(abs(moon[0]))
        kinetic = sum(abs(moon[1]))

        energy += (potential * kinetic)
    return energy

def ppcm(a,b):
	return a*b // math.gcd(a,b)

t = 0
init_moons = copy.deepcopy(moons)
period = [0, 0, 0]
while True:
    move(moons)
    t += 1

    if t == 1000:
        print("Energy: {}".format(energy(moons)))

    same_state = np.array([True, True, True])
    for i in range(0, len(moons)):
        same_state = np.logical_and(same_state, moons[i][0] == init_moons[i][0])
        same_state = np.logical_and(same_state, moons[i][1] == init_moons[i][1])

    # Find periods on each component
    for i in range(0,3):
        if same_state[i] == True and period[i] == 0:
            print("period of {}: {}".format(i, t))
            period[i] = t

    if all(period):
        break

print(ppcm(ppcm(period[0], period[1]), period[2]))
