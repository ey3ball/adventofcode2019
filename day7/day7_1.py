#!/usr/bin/env python3

from itertools import permutations
import sys

from intcode import run_intcode

intcode = sys.argv[1]
init_memmap = [int(i) for i in intcode.split(",")]

thrusters = []
for phase_sequence in permutations(range(0,5)):

    signal = 0
    for phase in phase_sequence:
        signal = next(run_intcode(init_memmap, [phase, signal]))

    thrusters.append((signal, phase_sequence))

print(sorted(thrusters))
