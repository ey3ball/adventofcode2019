from itertools import permutations
import sys

from intcode import run_intcode

intcode = sys.argv[1]
init_memmap = [int(i) for i in intcode.split(",")]

thrusters = []
for phase_sequence in permutations(range(5,10)):

    signal = 0
    amplifiers = []

    # Instantiate all amplifiers according to phase sequence
    for phase in phase_sequence:
        inputs = [phase]
        amplifier = run_intcode(init_memmap, inputs)
        amplifiers.append((inputs, amplifier))

    # Inject feedback looped signal
    running = True
    while running:
        for (ampin, amplifier) in amplifiers:
            try:
                ampin.append(signal)
                signal = next(amplifier)
            except StopIteration:
                running = False
                continue

    thrusters.append((signal, phase_sequence))

print(sorted(thrusters))
