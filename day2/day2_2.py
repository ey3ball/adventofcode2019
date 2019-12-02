#!/bin/bash

import sys

OPCODE_ADD = 1
OPCODE_MULT = 2
OPCODE_END = 99

intcode = sys.argv[1]
start_state = [int(i) for i in intcode.split(",")]

for x, y in [(x, y) for x in range(0,99) for y in range(0,99)]:
    state = list(start_state)
    state[1] = x
    state[2] = y
    for i in range(0, int(len(start_state) / 4)):
        index = i * 4
        opcode = state[index]
        arg1 = state[index + 1]
        arg2 = state[index + 2]
        out = state[index + 3]

        if opcode == OPCODE_ADD:
            state[out] = state[arg1] + state[arg2]
        elif opcode == OPCODE_MULT:
            state[out] = state[arg1] * state[arg2]
        elif opcode == OPCODE_END:
            break

    if state[0] == 19690720:
        break

print(x)
print(y)
